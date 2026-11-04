package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"unicode/utf8"
)

// changes/<publisher>/<name>.json and categories/<id>.json: site-side files beside employees/ (the signer reads them with the
// bundle: hr.harnsy.dev shows them on the CV page and in the department lists). Same rules as the signer's changes.go and
// categories.go.
const (
	maxChanges         = 5   // lines per version
	maxChangeChars     = 160 // characters per line
	maxCategoryName    = 40
	maxCategorySummary = 200
)

var categoryIDRE = regexp.MustCompile(`^[a-z0-9][a-z0-9-]{0,39}$`)

// employeeIDs: «publisher/name» → its version folders.
func employeeIDs(dir string) map[string]map[string]bool {
	out := map[string]map[string]bool{}
	vers, _ := filepath.Glob(filepath.Join(dir, "employees", "*", "*", "*"))
	for _, v := range vers {
		if st, err := os.Stat(v); err != nil || !st.IsDir() {
			continue
		}
		parts := strings.Split(filepath.ToSlash(strings.TrimPrefix(v, filepath.Join(dir, "employees")+string(filepath.Separator))), "/")
		id := parts[0] + "/" + parts[1]
		if out[id] == nil {
			out[id] = map[string]bool{}
		}
		out[id][parts[2]] = true
	}
	return out
}

func checkChanges(p *problems, dir string) {
	files, _ := filepath.Glob(filepath.Join(dir, "changes", "*", "*.json"))
	if len(files) == 0 {
		return
	}
	have := employeeIDs(dir)
	sort.Strings(files)
	for _, f := range files {
		fr := relTo(dir, f)
		id := filepath.Base(filepath.Dir(f)) + "/" + strings.TrimSuffix(filepath.Base(f), ".json")
		if have[id] == nil {
			p.add(fr, "no employee %s in employees/", id)
			continue
		}
		raw, err := os.ReadFile(f)
		if err != nil || len(raw) > maxBundleJSON {
			p.add(fr, "unreadable or over %d bytes", maxBundleJSON)
			continue
		}
		var byVersion map[string][]string
		if err := json.Unmarshal(raw, &byVersion); err != nil {
			p.add(fr, "want {\"<version>\": [\"line\", …]}: %v", err)
			continue
		}
		for v, lines := range byVersion {
			if !have[id][v] {
				p.add(fr, "%s has no version folder %s", id, v)
			}
			if len(lines) == 0 || len(lines) > maxChanges {
				p.add(fr, "%s: 1..%d lines (leave the version out when there is nothing to say)", v, maxChanges)
			}
			for i, c := range lines {
				if n := utf8.RuneCountInString(c); n == 0 || n > maxChangeChars {
					p.add(fr, "%s line %d: one line, 1..%d characters", v, i+1, maxChangeChars)
				} else if err := oneLine("line", c, 4*maxChangeChars); err != nil {
					p.add(fr, "%s line %d: %v", v, i+1, err)
				}
				if itemRefRE.MatchString(c) {
					p.add(fr, "%s line %d: internal reference — retell it without item numbers", v, i+1)
				}
			}
		}
	}
}

func checkCategories(p *problems, dir string) {
	files, _ := filepath.Glob(filepath.Join(dir, "categories", "*.json"))
	if len(files) == 0 {
		return
	}
	have := employeeIDs(dir)
	sort.Strings(files)
	for _, f := range files {
		fr := relTo(dir, f)
		if !categoryIDRE.MatchString(strings.TrimSuffix(filepath.Base(f), ".json")) {
			p.add(fr, "the file name is the category id: lowercase letters, digits and dashes")
			continue
		}
		raw, err := os.ReadFile(f)
		if err != nil || len(raw) > maxBundleJSON {
			p.add(fr, "unreadable or over %d bytes", maxBundleJSON)
			continue
		}
		var c struct {
			Name    string   `json:"name"`
			NameRU  string   `json:"name_ru"`
			Summary string   `json:"summary"`
			Members []string `json:"members"`
		}
		dec := json.NewDecoder(strings.NewReader(string(raw)))
		dec.DisallowUnknownFields()
		if err := dec.Decode(&c); err != nil {
			p.add(fr, "want {\"name\", \"name_ru\"?, \"summary\", \"members\"}: %v", err)
			continue
		}
		for _, x := range []struct {
			what, v string
			max     int
			need    bool
		}{{"name", c.Name, maxCategoryName, true}, {"name_ru", c.NameRU, maxCategoryName, false}, {"summary", c.Summary, maxCategorySummary, true}} {
			if n := utf8.RuneCountInString(x.v); (x.need && n == 0) || n > x.max {
				p.add(fr, "%s: 1..%d characters (name_ru may be left out)", x.what, x.max)
			} else if x.v != "" {
				if err := oneLine(x.what, x.v, 4*x.max); err != nil {
					p.add(fr, "%v", err)
				}
			}
		}
		seen := map[string]bool{}
		for _, m := range c.Members {
			if have[m] == nil {
				p.add(fr, "member %s is not an employee of employees/", m)
			}
			if seen[m] {
				p.add(fr, "member %s listed twice", m)
			}
			seen[m] = true
		}
	}
}
