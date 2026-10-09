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
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
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
		case strings.HasPrefix(in, "skills/"): // its layout: checkSkills
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
	skills := checkSkills(p, dir, v)
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
	checkSkillRefs(p, bf, bj, skills)
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
			Subtitle      string   `json:"subtitle"`     // a line under the name on the card (legends: the «in the spirit of» sentence)
			LicenseNote   string   `json:"license_note"` // a line beside the licence (legends: no rights in names or likenesses)
		}
		dec := json.NewDecoder(bytes.NewReader(lb))
		dec.DisallowUnknownFields()
		if err := dec.Decode(&l); err != nil {
			p.add(filepath.Join(rel, "listing.json"), "%v", err)
		} else if (l.Harnsy != "" && !harnsyRE.MatchString(l.Harnsy)) || (l.CVURL != "" && !strings.HasPrefix(l.CVURL, "https://hr.harnsy.dev/")) {
			p.add(filepath.Join(rel, "listing.json"), "harnsy wants >=MAJOR.MINOR.PATCH; cv_url only on https://hr.harnsy.dev/")
		} else if len(skills) > 0 && l.Harnsy != "" && harnsyBelow(l.Harnsy, skillsFloor) {
			p.add(filepath.Join(rel, "listing.json"), "harnsy %q: a bundle with skills needs >=%s", l.Harnsy, skillsFloor)
		}
		for _, f := range []struct{ name, v string }{{"subtitle", l.Subtitle}, {"license_note", l.LicenseNote}} {
			if f.v != "" {
				if err := oneLine(f.name, f.v, maxCardLine); err != nil {
					p.add(filepath.Join(rel, "listing.json"), "%v", err)
				}
			}
		}
	}
}

// harnsyBelow: ">=A.B.C" is below the version floor (both MAJOR.MINOR.PATCH, already matched by harnsyRE).
func harnsyBelow(expr, floor string) bool {
	a, b := strings.Split(strings.TrimPrefix(expr, ">="), "."), strings.Split(floor, ".")
	for i := range 3 {
		x, _ := strconv.Atoi(a[i])
		y, _ := strconv.Atoi(b[i])
		if x != y {
			return x < y
		}
	}
	return false
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
			if d.Name() == ".git" { // a checkout's .git: a folder, or a file in a git worktree
				if d.IsDir() {
					return filepath.SkipDir
				}
				return nil
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

// Skills (harnsy docs/bundle-v1.md «Skills»; rules as harnsy's skills.go reads a bundle): skills/<name>/ holds SKILL.md,
// an optional LICENSE and flat scripts/<file>; bundle.json "skills" names every folder.
const (
	skillsMax      = 5
	skillMaxFiles  = 20
	skillDocMax    = 64 << 10 // SKILL.md, LICENSE
	skillScriptMax = 256 << 10
	skillsTotalMax = 2 << 20
	skillDescMax   = 1024
)

var (
	skillNameRe   = regexp.MustCompile(`^[a-z0-9-]{1,40}$`)
	skillScriptRe = regexp.MustCompile(`^[A-Za-z0-9._-]{1,64}$`)
	frontKeyRe    = regexp.MustCompile(`^([A-Za-z0-9_-]+):`)
	// skillFrontKeys: the SKILL.md frontmatter keys harnsy takes; allowed-tools would grant tools without a prompt, hooks
	// would run commands.
	skillFrontKeys = map[string]bool{"name": true, "description": true, "license": true, "version": true, "when_to_use": true, "argument-hint": true}
	// windowsReserved: device names Windows opens instead of a file, with any extension.
	windowsReserved = map[string]bool{"CON": true, "PRN": true, "AUX": true, "NUL": true,
		"COM1": true, "COM2": true, "COM3": true, "COM4": true, "COM5": true, "COM6": true, "COM7": true, "COM8": true, "COM9": true,
		"LPT1": true, "LPT2": true, "LPT3": true, "LPT4": true, "LPT5": true, "LPT6": true, "LPT7": true, "LPT8": true, "LPT9": true}
	// inlineShellRe: what Claude Code runs as a skill loads, without a tool call: `!` right before a backtick, or a fence
	// opening with ``` or ~~~ and then `!`.
	inlineShellRe = regexp.MustCompile("!\\s*`|(?m)^[ \\t>]*(```|~~~)[^\\n]*!")
)

// checkSkills checks the layout of <version>/skills/ and returns the skill folders it holds. File contents (UTF-8, no
// NUL, no secrets) and symlinks are checked by the walk in checkVersion.
func checkSkills(p *problems, dir, v string) map[string]bool {
	found := map[string]bool{}
	root := filepath.Join(v, "skills")
	entries, err := os.ReadDir(root)
	if err != nil {
		if st, e := os.Lstat(root); e == nil && !st.IsDir() {
			p.add(relTo(dir, root), "a file — skills/ is a folder of skills/<name>/")
		}
		return found
	}
	total := 0
	for _, e := range entries {
		at := relTo(dir, filepath.Join(root, e.Name()))
		switch {
		case e.Type()&fs.ModeSymlink != 0:
			continue // reported by the walk
		case !e.IsDir():
			p.add(at, "a file directly in skills/ — a skill is a folder skills/<name>/ with SKILL.md")
			continue
		case !skillNameRe.MatchString(e.Name()):
			p.add(at, "skill name %q — use lowercase latin letters, digits and -, at most 40", e.Name())
			continue
		}
		found[e.Name()] = true
		total += checkSkill(p, dir, filepath.Join(root, e.Name()), e.Name())
	}
	if len(found) > skillsMax {
		p.add(relTo(dir, root), "%d skills, at most %d — keep the ones the role needs most", len(found), skillsMax)
	}
	if total > skillsTotalMax {
		p.add(relTo(dir, root), "%d bytes in all skills, at most %d — make the scripts smaller", total, skillsTotalMax)
	}
	return found
}

// checkSkill checks one skills/<name>/ folder and returns its bytes.
func checkSkill(p *problems, dir, sd, name string) int {
	at := relTo(dir, sd)
	files, size := 0, 0
	var doc, lic []byte
	hasDoc, hasLic, hasScripts := false, false, false
	read := func(f string, max int) []byte {
		b, err := os.ReadFile(f)
		if err != nil {
			return nil
		}
		files++
		size += len(b)
		if len(b) > max {
			p.add(relTo(dir, f), "%d bytes, at most %d", len(b), max)
		}
		return b
	}
	entries, _ := os.ReadDir(sd)
	for _, e := range entries {
		f := filepath.Join(sd, e.Name())
		switch {
		case e.Type()&fs.ModeSymlink != 0:
			continue // reported by the walk
		case e.Name() == "SKILL.md" && e.Type().IsRegular():
			doc, hasDoc = read(f, skillDocMax), true
		case e.Name() == "LICENSE" && e.Type().IsRegular():
			lic, hasLic = read(f, skillDocMax), true
		case e.Name() == "scripts" && e.IsDir():
			folded := map[string]string{}
			scripts, _ := os.ReadDir(f)
			for _, s := range scripts {
				sf := filepath.Join(f, s.Name())
				switch {
				case s.Type()&fs.ModeSymlink != 0:
					continue
				case s.IsDir():
					p.add(relTo(dir, sf), "a folder under scripts/ — keep scripts flat: skills/%s/scripts/<file>", name)
					continue
				}
				if err := skillScriptName(s.Name()); err != nil {
					p.add(relTo(dir, sf), "%v — rename it", err)
				}
				if other, dup := folded[strings.ToLower(s.Name())]; dup {
					p.add(relTo(dir, sf), "%q has the name of %q in another letter case — rename one", s.Name(), other)
				}
				folded[strings.ToLower(s.Name())] = s.Name()
				read(sf, skillScriptMax)
				hasScripts = true
			}
		default:
			p.add(relTo(dir, f), "not a skill file — a skill holds SKILL.md, LICENSE and scripts/<file> only (no hooks, commands, agents, MCP servers or plugin files)")
		}
	}
	if files > skillMaxFiles {
		p.add(at, "%d files, at most %d per skill", files, skillMaxFiles)
	}
	if !hasDoc {
		p.add(at, "no SKILL.md — add it with a frontmatter (name, description) and the steps")
	} else if utf8.Valid(doc) {
		if err := checkSkillDoc(name, doc); err != nil {
			p.add(relTo(dir, filepath.Join(sd, "SKILL.md")), "%v", err)
		}
	}
	for f, b := range map[string][]byte{"SKILL.md": doc, "LICENSE": lic} {
		if inlineShellRe.Match(b) {
			p.add(relTo(dir, filepath.Join(sd, f)), "runs inline shell (`!` before a backtick, or a ```! fence) — put commands in scripts/ for the agent's Bash tool")
		}
	}
	if hasScripts {
		ok := false
		for _, l := range scriptLic {
			ok = ok || (hasLic && bytes.Contains(lic, []byte(l)))
		}
		if !ok {
			p.add(at, "scripts need skills/%s/LICENSE with the MIT, Apache-2.0 or CC0 text", name)
		}
	}
	return size
}

// skillScriptName checks a file name under scripts/: a portable name no file system reads as another.
func skillScriptName(name string) error {
	switch {
	case !skillScriptRe.MatchString(name):
		return fmt.Errorf("script name %q: latin letters, digits, '.', '_' and '-', at most 64", name)
	case strings.HasPrefix(name, "."):
		return fmt.Errorf("script name %q: a hidden file", name)
	case strings.HasSuffix(name, "."):
		return fmt.Errorf("script name %q ends in a dot", name)
	}
	stem, _, _ := strings.Cut(name, ".")
	if windowsReserved[strings.ToUpper(stem)] {
		return fmt.Errorf("script name %q is a device name on Windows", name)
	}
	return nil
}

// skillFrontmatter reads SKILL.md's frontmatter: its top-level keys and their one-line values. Only `key: value` lines,
// comments and indented continuations are read; anything else refuses it, so no key hides from the check.
func skillFrontmatter(doc string) (map[string]string, error) {
	doc = strings.ReplaceAll(doc, "\r\n", "\n")
	rest, ok := strings.CutPrefix(doc, "---\n")
	if !ok {
		return nil, fmt.Errorf("no frontmatter — start with a --- line, then name: and description:, then ---")
	}
	head, _, ok := strings.Cut(rest, "\n---")
	if !ok {
		return nil, fmt.Errorf("the frontmatter has no closing --- — end it with a --- line")
	}
	out := map[string]string{}
	for _, line := range strings.Split(head, "\n") {
		switch {
		case strings.TrimSpace(line) == "", strings.HasPrefix(line, "#"):
			continue
		case strings.HasPrefix(line, " "), strings.HasPrefix(line, "\t"):
			continue // a continuation of the key above
		}
		m := frontKeyRe.FindStringSubmatch(line)
		if m == nil {
			return nil, fmt.Errorf("frontmatter line %q — write one `key: value` per line", line)
		}
		if _, dup := out[m[1]]; dup {
			return nil, fmt.Errorf("frontmatter has %s twice — keep one", m[1])
		}
		out[m[1]] = strings.Trim(strings.TrimSpace(line[len(m[0]):]), `"'`)
	}
	return out, nil
}

// checkSkillDoc checks SKILL.md's frontmatter: the skill's own name, when to use it, nothing beyond the agent's own
// permissions.
func checkSkillDoc(name string, raw []byte) error {
	front, err := skillFrontmatter(string(raw))
	if err != nil {
		return err
	}
	keys := make([]string, 0, len(front))
	for k := range front {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	for _, k := range keys {
		if !skillFrontKeys[k] {
			return fmt.Errorf("frontmatter key %q is not taken (allowed-tools would grant tools without a prompt, hooks would run commands) — "+
				"keep name, description, license, version, when_to_use, argument-hint", k)
		}
	}
	if front["name"] != name {
		return fmt.Errorf("frontmatter name %q is not the folder's name — write name: %s", front["name"], name)
	}
	if d := front["description"]; d == "" || len(d) > skillDescMax {
		return fmt.Errorf("frontmatter description: say when to use the skill, 1..%d bytes", skillDescMax)
	}
	return nil
}

// checkSkillRefs: bundle.json "skills" names exactly the skill folders, as {name, description} objects (a plain string
// is an older label and carries nothing).
func checkSkillRefs(p *problems, bf string, bj []byte, folders map[string]bool) {
	var doc struct {
		Skills json.RawMessage `json:"skills"`
	}
	json.Unmarshal(bj, &doc)
	named := map[string]bool{}
	if raw := bytes.TrimSpace(doc.Skills); len(raw) > 0 && !bytes.Equal(raw, []byte("null")) {
		var items []json.RawMessage
		if err := json.Unmarshal(raw, &items); err != nil {
			p.add(bf, "skills: not a list — write \"skills\": [{\"name\": \"<skill>\", \"description\": \"…\"}]")
			return
		}
		for _, it := range items {
			var label string
			if json.Unmarshal(it, &label) == nil {
				continue
			}
			var s struct {
				Name        string `json:"name"`
				Description string `json:"description"`
			}
			if err := json.Unmarshal(it, &s); err != nil {
				p.add(bf, "skills: %s is not {name, description} — write one object per skill", it)
				continue
			}
			switch {
			case !skillNameRe.MatchString(s.Name):
				p.add(bf, "skills: name %q — use lowercase latin letters, digits and -, at most 40", s.Name)
			case named[s.Name]:
				p.add(bf, "skills: %q is listed twice — keep one", s.Name)
			case !folders[s.Name]:
				p.add(bf, "skills: %q has no folder skills/%s/ — add it or remove the entry", s.Name, s.Name)
			}
			named[s.Name] = true
		}
		if len(named) > skillsMax {
			p.add(bf, "skills: %d, at most %d", len(named), skillsMax)
		}
	}
	missing := []string{}
	for f := range folders {
		if !named[f] {
			missing = append(missing, f)
		}
	}
	sort.Strings(missing)
	for _, f := range missing {
		p.add(bf, "skills: folder skills/%s/ is not named — add {\"name\": %q, \"description\": \"…\"} to \"skills\"", f, f)
	}
}

func relTo(dir, f string) string {
	r, _ := filepath.Rel(dir, f)
	return r
}
