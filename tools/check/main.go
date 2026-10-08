// check reads the catalog and says what the hr.harnsy.dev signer would refuse. It never runs anything it reads.
//
//	check [--dir <catalog checkout>]                               every employee version and publisher
//	check --dir <pr checkout> --base <base checkout> --author <login>  plus the pull-request rules
//
// Each problem is one line «path: what is wrong — how to fix»; in GitHub Actions also an ::error annotation. Exit 1 on any.
package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io/fs"
	"os"
	"path"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"unicode"
	"unicode/utf8"
)

const (
	maxFile      = 256 << 10 // any text file in an employee folder
	maxVersion   = 8 << 20   // one version folder in all
	maxPubName   = 80
	maxPubDesc   = 300
	maxPublisher = 4 << 10
)

var (
	// Root paths of hr.harnsy.dev: a publisher page lives at /<id>, so these ids are taken.
	reserved = map[string]bool{"teams": true, "notices": true, "not-found": true, "v1": true, "packs": true, "profiles": true,
		"_nuxt": true, "api": true, "404": true, "200": true, "robots": true, "favicon": true, "sitemap": true}
	githubRE = regexp.MustCompile(`^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$`)
	secretRE = regexp.MustCompile(`AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{40,}|` +
		`sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|xox[abprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}`)
	httpRE    = regexp.MustCompile(`http://[^\s"'<>)\]]+`)
	itemRefRE = regexp.MustCompile(`\b[Ii]tems? #[0-9]+`)
	scriptLic = []string{"MIT License", "Apache License", "CC0"}
)

type problems struct{ list []string }

func (p *problems) add(file, format string, a ...any) {
	msg := fmt.Sprintf(format, a...)
	p.list = append(p.list, file+": "+msg)
	if os.Getenv("GITHUB_ACTIONS") == "true" {
		fmt.Printf("::error file=%s::%s\n", file, strings.ReplaceAll(msg, "\n", " "))
	}
}

func main() {
	dir := flag.String("dir", ".", "the catalog checkout to check")
	base := flag.String("base", "", "the base branch checkout: turns on the pull-request rules")
	author := flag.String("author", "", "the pull request's GitHub login (with --base)")
	flag.Parse()
	var p problems
	versions := checkTree(&p, *dir)
	if *base != "" {
		checkPullRequest(&p, *dir, *base, *author)
	}
	for _, l := range p.list {
		fmt.Println(l)
	}
	if len(p.list) > 0 {
		fmt.Printf("%d problem(s)\n", len(p.list))
		os.Exit(1)
	}
	fmt.Printf("ok: %d employee version(s)\n", versions)
}

// checkTree checks every publisher file and every employee version under dir.
func checkTree(p *problems, dir string) int {
	pubs, _ := filepath.Glob(filepath.Join(dir, "publishers", "*.json"))
	for _, f := range pubs {
		checkPublisher(p, dir, f)
	}
	n := 0
	vers, _ := filepath.Glob(filepath.Join(dir, "employees", "*", "*", "*"))
	sort.Strings(vers)
	for _, v := range vers {
		if st, err := os.Stat(v); err == nil && st.IsDir() {
			checkVersion(p, dir, v)
			n++
		}
	}
	if b, err := os.ReadFile(filepath.Join(dir, "revoked.json")); err == nil {
		var r []string
		if err := json.Unmarshal(b, &r); err != nil {
			p.add("revoked.json", "not a JSON list of strings — write [\"<publisher>/<name>@<version>\", …]")
		}
		for _, x := range r {
			id, ver, ok := strings.Cut(x, "@")
			pub, name, ok2 := strings.Cut(id, "/")
			if !ok || !ok2 || !partRE.MatchString(pub) || !partRE.MatchString(name) || !semverRE.MatchString(ver) {
				p.add("revoked.json", "%q — want <publisher>/<name>@<MAJOR.MINOR.PATCH>", x)
			}
		}
	}
	return n
}

type publisher struct {
	Name        string   `json:"name"`
	Description string   `json:"description"`
	GitHub      []string `json:"github"`
	Banned      string   `json:"banned,omitempty"`
}

func readPublisher(file string) (publisher, error) {
	var pb publisher
	b, err := os.ReadFile(file)
	if err != nil {
		return pb, err
	}
	dec := json.NewDecoder(bytes.NewReader(b))
	dec.DisallowUnknownFields()
	return pb, dec.Decode(&pb)
}

func checkPublisher(p *problems, dir, file string) {
	rel, _ := filepath.Rel(dir, file)
	id := strings.TrimSuffix(filepath.Base(file), ".json")
	if !partRE.MatchString(id) || reserved[id] {
		p.add(rel, "publisher id %q is not allowed — use lowercase letters, digits and dashes, not a site path", id)
	}
	if st, err := os.Stat(file); err == nil && st.Size() > maxPublisher {
		p.add(rel, "larger than %d bytes", maxPublisher)
		return
	}
	pb, err := readPublisher(file)
	if err != nil {
		p.add(rel, "%v — want {\"name\", \"description\", \"github\": [\"<login>\"]}", err)
		return
	}
	if err := oneLine("name", pb.Name, maxPubName*4); err != nil || utf8.RuneCountInString(pb.Name) > maxPubName {
		p.add(rel, "name: one line, 1..%d characters", maxPubName)
	}
	if utf8.RuneCountInString(pb.Description) > maxPubDesc || strings.ContainsAny(pb.Description, "\n\r") {
		p.add(rel, "description: one paragraph, at most %d characters", maxPubDesc)
	}
	if len(pb.GitHub) == 0 {
		p.add(rel, "github: list the GitHub login(s) allowed to send this publisher's employees")
	}
	for _, g := range pb.GitHub {
		if !githubRE.MatchString(g) {
			p.add(rel, "github: %q is not a GitHub login", g)
		}
	}
	latin(p, rel, pb.Name+" "+pb.Description)
}

// checkVersion checks one employees/<publisher>/<name>/<version>/ folder.
func checkVersion(p *problems, dir, v string) {
	rel, _ := filepath.Rel(dir, v)
	parts := strings.Split(filepath.ToSlash(rel), "/")
	pub, name, ver := parts[1], parts[2], parts[3]
	if !partRE.MatchString(pub) || !partRE.MatchString(name) || !semverRE.MatchString(ver) {
		p.add(rel, "want employees/<publisher>/<name>/<MAJOR.MINOR.PATCH> in lowercase letters, digits and dashes")
		return
	}
	if _, err := os.Stat(filepath.Join(dir, "publishers", pub+".json")); err != nil {
		p.add(rel, "no publishers/%s.json — add it with your name, description and GitHub login", pub)
	}
	// Files: what the signer packs, plus skills; text only except the avatar.
	var total int64
	skillScripts := map[string]bool{}
	filepath.WalkDir(v, func(f string, d fs.DirEntry, err error) error {
		if err != nil || d.IsDir() {
			return err
		}
		fr, _ := filepath.Rel(dir, f)
		in := filepath.ToSlash(strings.TrimPrefix(f, v+string(filepath.Separator)))
		info, _ := d.Info()
		total += info.Size()
		if d.Type()&fs.ModeSymlink != 0 {
			p.add(fr, "a symbolic link — commit the file itself")
			return nil
		}
		switch {
		case in == "bundle.json", in == "listing.json", in == casebookFile, avatarRE.MatchString(in):
		case strings.HasPrefix(in, "skills/") && strings.Count(in, "/") >= 2:
			skill := strings.Split(in, "/")[1]
			if !strings.HasSuffix(in, ".md") && path.Base(in) != "LICENSE" {
				skillScripts[skill] = true
			}
		default:
			p.add(fr, "not a catalog file — an employee folder holds bundle.json, listing.json, avatar.png|jpg|webp, %s and skills/<skill>/…", casebookFile)
			return nil
		}
		if avatarRE.MatchString(in) {
			return nil // checked with persona.avatar below
		}
		b, err := os.ReadFile(f)
		if err != nil {
			return err
		}
		if len(b) > maxFile {
			p.add(fr, "%d bytes, at most %d", len(b), maxFile)
		}
		if !utf8.Valid(b) || bytes.IndexByte(b, 0) >= 0 {
			p.add(fr, "not UTF-8 text — no binaries in a catalog; scripts are source code only")
			return nil
		}
		s := string(b)
		if secretRE.MatchString(s) {
			p.add(fr, "looks like a key or token — remove it; never put secrets in an employee")
		}
		if m := httpRE.FindString(s); m != "" {
			p.add(fr, "plain http link %s — use https://", m)
		}
		if m := itemRefRE.FindString(s); m != "" {
			p.add(fr, "internal reference %q — retell it without item numbers", m)
		}
		return nil
	})
	if total > maxVersion {
		p.add(rel, "%d bytes in all, at most %d", total, maxVersion)
	}
	for skill := range skillScripts {
		lic, err := os.ReadFile(filepath.Join(v, "skills", skill, "LICENSE"))
		ok := err == nil
		if ok {
			ok = false
			for _, l := range scriptLic {
				ok = ok || bytes.Contains(lic, []byte(l))
			}
		}
		if !ok {
			p.add(filepath.Join(rel, "skills", skill), "scripts need skills/%s/LICENSE with the MIT, Apache-2.0 or CC0 text", skill)
		}
	}
	// bundle.json by the signer's rules.
	bf := filepath.Join(rel, "bundle.json")
	bj, err := os.ReadFile(filepath.Join(v, "bundle.json"))
	if err != nil {
		p.add(bf, "missing")
		return
	}
	if len(bj) > maxBundleJSON {
		p.add(bf, "%d bytes, at most %d", len(bj), maxBundleJSON)
		return
	}
	var b bundleDoc
	if err := json.Unmarshal(bj, &b); err != nil {
		p.add(bf, "not valid JSON: %v", err)
		return
	}
	if err := checkBundle(&b); err != nil {
		p.add(bf, "%v", err)
	}
	if b.License == "" {
		p.add(bf, "license: state the text's licence, e.g. \"CC-BY-4.0\"")
	}
	latin(p, bf, string(bj))
	if a := b.Persona.Avatar; a != "" {
		ab, err := os.ReadFile(filepath.Join(v, a))
		switch {
		case !avatarRE.MatchString(a):
			p.add(bf, "persona.avatar %q — want avatar.png, avatar.jpg or avatar.webp", a)
		case err != nil:
			p.add(bf, "persona.avatar names %s, but the file is missing", a)
		case len(ab) > maxAvatar:
			p.add(filepath.Join(rel, a), "larger than %d bytes", maxAvatar)
		default:
			if w, h, err := imageSize(ab); err != nil || w < minAvatarPx || h < minAvatarPx {
				p.add(filepath.Join(rel, a), "want a picture of at least %d×%d (got %dx%d)", minAvatarPx, minAvatarPx, w, h)
			}
		}
	}
	if lb, err := os.ReadFile(filepath.Join(v, "listing.json")); err == nil {
		var l struct {
			Title         string   `json:"title"`
			Summary       string   `json:"summary"`
			Tags          []string `json:"tags"`
			Harnsy        string   `json:"harnsy"`
			PublisherName string   `json:"publisher_name"`
			CVURL         string   `json:"cv_url"`
		}
		dec := json.NewDecoder(bytes.NewReader(lb))
		dec.DisallowUnknownFields()
		if err := dec.Decode(&l); err != nil {
			p.add(filepath.Join(rel, "listing.json"), "%v", err)
		} else if (l.Harnsy != "" && !harnsyRE.MatchString(l.Harnsy)) || (l.CVURL != "" && !strings.HasPrefix(l.CVURL, "https://hr.harnsy.dev/")) {
			p.add(filepath.Join(rel, "listing.json"), "harnsy wants >=MAJOR.MINOR.PATCH; cv_url only on https://hr.harnsy.dev/")
		}
	}
}

// latin refuses letters of other scripts: catalog texts are English.
func latin(p *problems, file, s string) {
	for _, r := range s {
		if unicode.IsLetter(r) && !unicode.Is(unicode.Latin, r) {
			p.add(file, "letter %q: catalog texts are English (Latin letters only)", r)
			return
		}
	}
}

// checkPullRequest: one publisher, at most one new employee version, published versions untouched, the publisher's own
// GitHub login.
func checkPullRequest(p *problems, dir, base, author string) {
	changed := map[string]bool{}
	for _, root := range []string{dir, base} {
		filepath.WalkDir(root, func(f string, d fs.DirEntry, err error) error {
			if err != nil {
				return nil
			}
			if d.IsDir() && d.Name() == ".git" {
				return filepath.SkipDir
			}
			if d.IsDir() {
				return nil
			}
			rel, _ := filepath.Rel(root, f)
			rel = filepath.ToSlash(rel)
			a, errA := os.ReadFile(filepath.Join(dir, rel))
			b, errB := os.ReadFile(filepath.Join(base, rel))
			if (errA == nil) != (errB == nil) || !bytes.Equal(a, b) {
				changed[rel] = true
			}
			return nil
		})
	}
	pubs, versions := map[string]bool{}, map[string]bool{}
	for f := range changed {
		parts := strings.Split(f, "/")
		switch {
		case parts[0] == "employees" && len(parts) >= 5:
			pubs[parts[1]] = true
			v := strings.Join(parts[:4], "/")
			versions[v] = true
			if st, err := os.Stat(filepath.Join(base, filepath.FromSlash(v))); err == nil && st.IsDir() {
				p.add(f, "%s is published and never changes — send a new version folder instead", v)
			}
		case parts[0] == "publishers" && len(parts) == 2:
			pubs[strings.TrimSuffix(parts[1], ".json")] = true
		case f == "revoked.json":
			checkRevokedChange(p, dir, base, author)
		default:
			p.add(f, "outside employees/ and publishers/ — only maintainers change this; a contribution touches its own folders")
		}
	}
	if len(pubs) > 1 {
		p.add("pull request", "touches %d publishers — one pull request, one publisher", len(pubs))
	}
	if len(versions) > 1 {
		p.add("pull request", "adds %d employee versions — one pull request, one employee", len(versions))
	}
	for pub := range pubs {
		owner := filepath.Join(base, "publishers", pub+".json")
		if pb, err := readPublisher(owner); err == nil {
			if pb.Banned != "" {
				p.add("publishers/"+pub+".json", "this publisher is blocked: %s", pb.Banned)
			} else if !contains(pb.GitHub, author) {
				p.add("publishers/"+pub+".json", "publisher %q belongs to %s — send under your own publisher id", pub, strings.Join(pb.GitHub, ", "))
			}
		} else if pb, err := readPublisher(filepath.Join(dir, "publishers", pub+".json")); err != nil || !contains(pb.GitHub, author) {
			p.add("publishers/"+pub+".json", "a new publisher: add publishers/%s.json with your GitHub login %q in \"github\"", pub, author)
		}
	}
}

// checkRevokedChange: entries are only added, and only for the author's own publishers.
func checkRevokedChange(p *problems, dir, base, author string) {
	read := func(root string) map[string]bool {
		var r []string
		b, _ := os.ReadFile(filepath.Join(root, "revoked.json"))
		json.Unmarshal(b, &r)
		m := map[string]bool{}
		for _, x := range r {
			m[x] = true
		}
		return m
	}
	before, after := read(base), read(dir)
	for x := range before {
		if !after[x] {
			p.add("revoked.json", "%s was removed — a revocation is never undone by a pull request", x)
		}
	}
	for x := range after {
		if before[x] {
			continue
		}
		pub, _, _ := strings.Cut(x, "/")
		if pb, err := readPublisher(filepath.Join(base, "publishers", pub+".json")); err != nil || !contains(pb.GitHub, author) {
			p.add("revoked.json", "%s: only its publisher withdraws a version", x)
		}
	}
}

func contains(xs []string, s string) bool {
	for _, x := range xs {
		if strings.EqualFold(x, s) && s != "" {
			return true
		}
	}
	return false
}
