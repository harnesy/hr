// Package main checks a catalog employee the way the hr.harnsy.dev signer does (rules copied from the signer, harnesy/site
// deploy/hr/bundle.go). It only reads files: nothing from a pull request is ever run.
package main

import (
	"bytes"
	"encoding/binary"
	"encoding/json"
	"errors"
	"fmt"
	"image"
	_ "image/jpeg"
	_ "image/png"
	"regexp"
	"strings"
	"unicode"
	"unicode/utf8"
)

const (
	maxBundleJSON = 256 << 10 // bundle.json
	maxTexts      = 64 << 10  // mandate + deliverable + prompt + persona.character
	maxComps      = 32
	maxAvatar     = 5 << 20
	maxCardLine   = 400 // listing.json subtitle and license_note, bytes, one line each (the feed signer takes the same)
)

var (
	partRE   = regexp.MustCompile(`^[a-z0-9][a-z0-9-]{0,63}$`)
	semverRE = regexp.MustCompile(`^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$`)
	avatarRE = regexp.MustCompile(`^avatar\.(png|jpe?g|webp)$`)
)

const (
	casebookFile = "docs/persona-casebook.md"
	maxCasebook  = 64 << 10
	minAvatarPx  = 512
	maxFiles     = 16
	floorHarnsy  = ">=0.10.0" // the catalog's floor (contract @271fca89; hiring ships in 0.10.0): a lower harnsy refuses the bundle
	skillsFloor  = "0.10.0"   // a bundle with skills needs harnsy >= this (signer's skills.go): an older one would hire it without them
)

var (
	harnsyRE    = regexp.MustCompile(`^>=(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$`)
	industryRE  = regexp.MustCompile(`^[a-z][a-z0-9-]{0,39}$`)
	departments = map[string]bool{"engineering": true, "product": true, "design": true, "marketing": true, "sales": true,
		"support": true, "operations": true, "finance": true, "legal": true, "management": true, "content": true, "data": true, "hr": true}
	sourceKinds = map[string]bool{"team-rule": true, "item": true, "doc": true, "book": true, "talk": true, "other": true}
)

type bundleDoc struct {
	Schema  string `json:"schema"`
	Persona struct {
		Name       string `json:"name"`
		Character  string `json:"character"`
		Avatar     string `json:"avatar"`
		Principles []struct {
			Text    string   `json:"text"`
			Sources []string `json:"sources"`
		} `json:"principles"`
		Voice struct {
			Rules   []string `json:"rules"`
			Samples []struct {
				Text   string `json:"text"`
				Source string `json:"source"`
			} `json:"samples"`
		} `json:"voice"`
		Sources []struct {
			ID    string `json:"id"`
			Title string `json:"title"`
			Kind  string `json:"kind"`
			URL   string `json:"url"`
		} `json:"sources"`
	} `json:"persona"`
	Role struct {
		Name        string   `json:"name"`
		Department  string   `json:"department"`
		Mandate     string   `json:"mandate"`
		Deliverable string   `json:"deliverable"`
		Prompt      string   `json:"prompt"`
		Tagline     string   `json:"tagline"`
		Industries  []string `json:"industries"`
		Keywords    []string `json:"keywords"`
		ReportsTo   string   `json:"reports_to"`
	} `json:"role"`
	Requires struct {
		Tools []struct {
			Name string `json:"name"`
			Min  string `json:"min"`
		} `json:"tools"`
		Keys []string `json:"keys"`
		Max  []string `json:"max"`
	} `json:"requires"`
	Competencies []struct {
		Key  string `json:"key"`
		Name string `json:"name"`
	} `json:"competencies"`
	License     string          `json:"license"`     // the text's licence (#1605): SPDX, a few spellings normalised
	Attribution json.RawMessage `json:"attribution"` // public credit (#1605), read strictly by credit()
}

// Attribution is one public credit of a bundle (product #1605): shown on the card before a hire and in the profile after it.
type Attribution struct {
	Name     string `json:"name"`
	URL      string `json:"url"`
	License  string `json:"license"`
	Modified bool   `json:"modified"`
}

var (
	licenseRE = regexp.MustCompile(`^[A-Za-z0-9][A-Za-z0-9.+-]{0,63}$`) // an SPDX id or LicenseRef-…
	// The spellings harnsy takes beside SPDX (any case), stored as SPDX.
	licenseSpellings = map[string]string{"cc by 4.0": "CC-BY-4.0", "cc by-sa 4.0": "CC-BY-SA-4.0", "cc0 1.0": "CC0-1.0", "cc by 3.0": "CC-BY-3.0"}
)

const (
	maxAttribution = 20
	maxAttrName    = 120 // characters
	maxAttrURL     = 300
)

// spdx is a licence as harnsy stores it: "" stays "" (older bundles), a known spelling (spaces trimmed and collapsed)
// becomes its SPDX id.
func spdx(field, v string) (string, error) {
	v = strings.TrimSpace(v)
	if v == "" {
		return "", nil
	}
	if id, ok := licenseSpellings[strings.ToLower(strings.Join(strings.Fields(v), " "))]; ok {
		return id, nil
	}
	if !licenseRE.MatchString(v) {
		return "", fmt.Errorf("%s %q: an SPDX id (CC-BY-4.0) or LicenseRef-…", field, v)
	}
	return v, nil
}

// credit reads the bundle's licence and attribution by harnsy's hire rules (#1605): the licence normalised, every entry
// exactly name, url, license, modified (an unknown key is refused so a typo does not drop a credit).
func credit(b *bundleDoc) (string, []Attribution, error) {
	lic, err := spdx("license", b.License)
	if err != nil {
		return "", nil, err
	}
	raw := bytes.TrimSpace(b.Attribution)
	if len(raw) == 0 || bytes.Equal(raw, []byte("null")) {
		return lic, nil, nil
	}
	var entries []json.RawMessage
	if err := json.Unmarshal(raw, &entries); err != nil {
		return "", nil, errors.New("attribution: a list")
	}
	if len(entries) > maxAttribution {
		return "", nil, fmt.Errorf("attribution: at most %d entries", maxAttribution)
	}
	var out []Attribution
	for i, e := range entries {
		f := fmt.Sprintf("attribution[%d]", i)
		var keys map[string]json.RawMessage
		if err := json.Unmarshal(e, &keys); err != nil {
			return "", nil, fmt.Errorf("%s: an object", f)
		}
		for k := range keys {
			if k != "name" && k != "url" && k != "license" && k != "modified" {
				return "", nil, fmt.Errorf("%s: unknown key %q (name, url, license, modified)", f, k)
			}
		}
		if len(keys) != 4 {
			return "", nil, fmt.Errorf("%s: name, url, license and modified, all four", f)
		}
		var a Attribution
		dec := json.NewDecoder(bytes.NewReader(e))
		dec.DisallowUnknownFields()
		if err := dec.Decode(&a); err != nil {
			return "", nil, fmt.Errorf("%s: %v", f, err)
		}
		a.Name, a.URL = strings.TrimSpace(a.Name), strings.TrimSpace(a.URL) // harnsy trims both before its checks
		if n := utf8.RuneCountInString(a.Name); n == 0 || n > maxAttrName {
			return "", nil, fmt.Errorf("%s.name: one line, 1..%d characters", f, maxAttrName)
		}
		if err := oneLine(f+".name", a.Name, 4*maxAttrName); err != nil {
			return "", nil, err
		}
		if len(a.URL) > maxAttrURL || !strings.HasPrefix(a.URL, "https://") || len(a.URL) == len("https://") ||
			strings.ContainsAny(a.URL, " \t\"<>") {
			return "", nil, fmt.Errorf("%s.url: https://…, at most %d characters", f, maxAttrURL)
		}
		if err := oneLine(f+".url", a.URL, maxAttrURL); err != nil {
			return "", nil, err
		}
		if strings.TrimSpace(a.License) == "" {
			return "", nil, fmt.Errorf("%s.license: required", f)
		}
		if a.License, err = spdx(f+".license", a.License); err != nil {
			return "", nil, err
		}
		out = append(out, a)
	}
	return lic, out, nil
}

func oneLine(field, v string, max int) error {
	if v == "" || len(v) > max || !utf8.ValidString(v) {
		return fmt.Errorf("%s: one line, 1..%d bytes", field, max)
	}
	for _, r := range v {
		if !unicode.IsPrint(r) {
			return fmt.Errorf("%s: one line, printable characters only", field)
		}
	}
	return nil
}

// checkBundle refuses what harnsy would refuse, so no published bundle fails on a node.
func checkBundle(b *bundleDoc) error {
	if _, _, err := credit(b); err != nil {
		return err
	}
	if b.Schema != "harnsy.employee/v1" || b.Persona.Name == "" || b.Role.Name == "" {
		return errors.New("want schema harnsy.employee/v1, persona.name and role.name")
	}
	if n := len(b.Role.Mandate) + len(b.Role.Deliverable) + len(b.Role.Prompt) + len(b.Persona.Character); n > maxTexts {
		return fmt.Errorf("mandate+deliverable+prompt+character %d bytes, at most %d", n, maxTexts)
	}
	if d := b.Role.Department; d != "" && !departments[d] {
		return fmt.Errorf("role.department %q is not in the catalog's list", d)
	}
	if t := b.Role.Tagline; t != "" {
		if err := oneLine("role.tagline", t, 160); err != nil {
			return err
		}
	}
	if len(b.Role.Industries) > 10 {
		return errors.New("role.industries: at most 10")
	}
	for _, i := range b.Role.Industries {
		if !industryRE.MatchString(i) {
			return fmt.Errorf("role.industries: %q, want a lowercase word", i)
		}
	}
	if len(b.Role.Keywords) > 20 {
		return errors.New("role.keywords: at most 20")
	}
	for _, k := range b.Role.Keywords {
		if err := oneLine("role.keywords", k, 60); err != nil {
			return err
		}
	}
	if len(b.Requires.Tools) > 20 || len(b.Requires.Keys) > 20 {
		return errors.New("requires: at most 20 tools and 20 keys")
	}
	if len(b.Competencies) > maxComps {
		return fmt.Errorf("%d competencies, at most %d", len(b.Competencies), maxComps)
	}
	for _, c := range b.Competencies {
		if !partRE.MatchString(c.Key) {
			return fmt.Errorf("competency key %q", c.Key)
		}
	}
	// The persona's layers: bounded, one line each, every source id named is listed.
	p := &b.Persona
	if len(p.Principles) > 12 || len(p.Voice.Rules) > 10 || len(p.Voice.Samples) > 10 || len(p.Sources) > 40 {
		return errors.New("persona: at most 12 principles, 10 voice rules, 10 samples, 40 sources")
	}
	ids := map[string]bool{}
	for _, s := range p.Sources {
		if err := errors.Join(oneLine("persona.sources.id", s.ID, 40), oneLine("persona.sources.title", s.Title, 300)); err != nil {
			return err
		}
		if !sourceKinds[s.Kind] {
			return fmt.Errorf("persona.sources %s: kind %q", s.ID, s.Kind)
		}
		ids[s.ID] = true
	}
	for _, x := range p.Principles {
		if err := oneLine("persona.principles.text", x.Text, 600); err != nil {
			return err
		}
		for _, id := range x.Sources {
			if !ids[id] {
				return fmt.Errorf("persona.principles: source %q is not listed", id)
			}
		}
	}
	for _, r := range p.Voice.Rules {
		if err := oneLine("persona.voice.rules", r, 600); err != nil {
			return err
		}
	}
	for _, x := range p.Voice.Samples {
		if err := oneLine("persona.voice.samples.text", x.Text, 600); err != nil {
			return err
		}
		if x.Source != "" && !ids[x.Source] {
			return fmt.Errorf("persona.voice.samples: source %q is not listed", x.Source)
		}
	}
	return nil
}

// imageSize reads a PNG, JPEG or WebP picture's size without decoding it.
func imageSize(b []byte) (w, h int, err error) {
	if len(b) >= 30 && string(b[:4]) == "RIFF" && string(b[8:12]) == "WEBP" {
		switch string(b[12:16]) {
		case "VP8X":
			return 1 + (int(b[24]) | int(b[25])<<8 | int(b[26])<<16), 1 + (int(b[27]) | int(b[28])<<8 | int(b[29])<<16), nil
		case "VP8 ":
			return int(binary.LittleEndian.Uint16(b[26:]) & 0x3fff), int(binary.LittleEndian.Uint16(b[28:]) & 0x3fff), nil
		case "VP8L":
			v := binary.LittleEndian.Uint32(b[21:])
			return int(v&0x3fff) + 1, int(v>>14&0x3fff) + 1, nil
		}
		return 0, 0, errors.New("webp: unknown chunk")
	}
	c, _, err := image.DecodeConfig(bytes.NewReader(b))
	return c.Width, c.Height, err
}
