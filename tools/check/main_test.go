package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

const testSkillDoc = "---\nname: video-record\ndescription: Record a screen video when the person asks for one.\n---\n\n# Steps\n\nRun `node scripts/take.mjs`.\n"

// testEmployee writes a catalog with one employee version: its skills folder from files (paths under the version
// folder; "" content removes a default) and bundle.json "skills" from refs.
func testEmployee(t *testing.T, files map[string]string, refs []any) []string {
	t.Helper()
	dir := t.TempDir()
	write := func(rel, content string) {
		f := filepath.Join(dir, filepath.FromSlash(rel))
		if err := os.MkdirAll(filepath.Dir(f), 0o755); err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(f, []byte(content), 0o644); err != nil {
			t.Fatal(err)
		}
	}
	write("publishers/acme.json", `{"name": "Acme", "description": "Test publisher.", "github": ["acme"], "github_ids": [42]}`)
	bundle := map[string]any{
		"schema":  "harnsy.employee/v1",
		"persona": map[string]any{"name": "Vera"},
		"role":    map[string]any{"name": "Recorder", "prompt": "You are an AI agent."},
		"license": "CC-BY-4.0",
	}
	if refs != nil {
		bundle["skills"] = refs
	}
	bj, _ := json.Marshal(bundle)
	v := "employees/acme/recorder/1.0.0/"
	write(v+"bundle.json", string(bj))
	all := map[string]string{
		"skills/video-record/SKILL.md":         testSkillDoc,
		"skills/video-record/LICENSE":          "MIT License\n\nCopyright (c) 2026 Acme\n",
		"skills/video-record/scripts/take.mjs": "console.log('take')\n",
	}
	for k, c := range files {
		all[k] = c
	}
	for k, c := range all {
		if c != "" {
			write(v+k, c)
		}
	}
	var p problems
	checkTree(&p, dir)
	return p.list
}

func ref(name string) map[string]string {
	return map[string]string{"name": name, "description": "Records the screen."}
}

func TestSkills(t *testing.T) {
	one := []any{ref("video-record")}
	six := map[string]string{}
	sixRefs := []any{ref("video-record")}
	for _, n := range []string{"a", "b", "c", "d", "e"} {
		six["skills/"+n+"/SKILL.md"] = "---\nname: " + n + "\ndescription: Does " + n + ".\n---\n"
		sixRefs = append(sixRefs, ref(n))
	}
	doc := func(front string) map[string]string {
		return map[string]string{"skills/video-record/SKILL.md": "---\n" + front + "---\nBody.\n"}
	}
	cases := []struct {
		name  string
		files map[string]string
		refs  []any
		want  string // "" = passes
	}{
		{"valid", nil, one, ""},
		{"valid with an older string label", nil, []any{"recording", ref("video-record")}, ""},
		{"valid frontmatter keys", doc("name: video-record\ndescription: \"Records.\"\nlicense: MIT\nversion: 1.0.0\nwhen_to_use: Asked.\nargument-hint: <file>\n"), one, ""},
		{"bad name", map[string]string{"skills/Video_Record/SKILL.md": "---\nname: Video_Record\ndescription: x\n---\n"}, one,
			`skill name "Video_Record" — use lowercase latin letters, digits and -, at most 40`},
		{"six skills", six, sixRefs, "6 skills, at most 5"},
		{"extra file at skill root", map[string]string{"skills/video-record/hooks.json": "{}"}, one, "skills/video-record/hooks.json: not a skill file"},
		{"mcp file", map[string]string{"skills/video-record/.mcp.json": "{}"}, one, "skills/video-record/.mcp.json: not a skill file"},
		{"hooks folder", map[string]string{"skills/video-record/hooks/run.sh": "echo"}, one, "skills/video-record/hooks: not a skill file"},
		{"nested scripts dir", map[string]string{"skills/video-record/scripts/lib/x.js": "x"}, one, "scripts/lib: a folder under scripts/ — keep scripts flat"},
		{"device name", map[string]string{"skills/video-record/scripts/NUL.txt": "x"}, one, `script name "NUL.txt" is a device name on Windows`},
		{"device name lowercase", map[string]string{"skills/video-record/scripts/com1.js": "x"}, one, `script name "com1.js" is a device name on Windows`},
		{"case duplicate", map[string]string{"skills/video-record/scripts/Take.mjs": "x"}, one, "in another letter case"},
		{"hidden file", map[string]string{"skills/video-record/scripts/.env": "A=1"}, one, `script name ".env": a hidden file`},
		{"trailing dot", map[string]string{"skills/video-record/scripts/take.": "x"}, one, `script name "take." ends in a dot`},
		{"NUL byte", map[string]string{"skills/video-record/scripts/bin.js": "a\x00b"}, one, "scripts/bin.js: not UTF-8 text"},
		{"no SKILL.md", map[string]string{"skills/video-record/SKILL.md": ""}, one, "skills/video-record: no SKILL.md"},
		{"SKILL.md too large", map[string]string{"skills/video-record/SKILL.md": testSkillDoc + strings.Repeat("a", 64<<10)}, one, "at most 65536"},
		{"no frontmatter", map[string]string{"skills/video-record/SKILL.md": "# Steps\n"}, one, "SKILL.md: no frontmatter"},
		{"allowed-tools", doc("name: video-record\ndescription: x\nallowed-tools: Bash\n"), one,
			`frontmatter key "allowed-tools" is not taken (allowed-tools would grant tools without a prompt`},
		{"hooks key", doc("name: video-record\ndescription: x\nhooks:\n  PreToolUse: x\n"), one, `frontmatter key "hooks" is not taken`},
		{"name mismatch", doc("name: other\ndescription: x\n"), one, `frontmatter name "other" is not the folder's name — write name: video-record`},
		{"description too long", doc("name: video-record\ndescription: " + strings.Repeat("d", 1025) + "\n"), one, "frontmatter description: say when to use the skill, 1..1024 bytes"},
		{"description missing", doc("name: video-record\n"), one, "frontmatter description"},
		{"inline bang backtick", map[string]string{"skills/video-record/SKILL.md": testSkillDoc + "Now !`date`\n"}, one, "SKILL.md: runs inline shell"},
		{"fence bang", map[string]string{"skills/video-record/SKILL.md": testSkillDoc + "```!\ndate\n```\n"}, one, "SKILL.md: runs inline shell"},
		{"tilde fence bang in LICENSE", map[string]string{"skills/video-record/LICENSE": "MIT License\n~~~!\ndate\n~~~\n"}, one, "LICENSE: runs inline shell"},
		{"scripts without LICENSE", map[string]string{"skills/video-record/LICENSE": ""}, one, "scripts need skills/video-record/LICENSE"},
		{"skills[] missing a folder", nil, nil, `skills: folder skills/video-record/ is not named`},
		{"skills[] only a string", nil, []any{"video-record"}, `skills: folder skills/video-record/ is not named`},
		{"skills[] names a missing folder", nil, []any{ref("video-record"), ref("other")}, `skills: "other" has no folder skills/other/`},
		{"listing floor below the skills floor", map[string]string{"listing.json": `{"harnsy":">=0.9.9"}`}, one, `harnsy ">=0.9.9": a bundle with skills needs >=0.10.0`},
		{"listing floor at the skills floor", map[string]string{"listing.json": `{"harnsy":">=0.10.0"}`}, one, ""},
	}
	for _, c := range cases {
		t.Run(c.name, func(t *testing.T) {
			got := testEmployee(t, c.files, c.refs)
			if c.want == "" {
				if len(got) > 0 {
					t.Fatalf("want ok, got:\n%s", strings.Join(got, "\n"))
				}
				return
			}
			for _, l := range got {
				if strings.Contains(l, c.want) {
					return
				}
			}
			t.Fatalf("want a problem with %q, got:\n%s", c.want, strings.Join(got, "\n"))
		})
	}
}

func TestSkillsTotalSize(t *testing.T) {
	files := map[string]string{}
	big := strings.Repeat("x", 250<<10)
	for _, n := range []string{"a", "b", "c", "d", "e", "f", "g", "h", "i"} {
		files["skills/video-record/scripts/"+n+".js"] = big
	}
	got := strings.Join(testEmployee(t, files, []any{ref("video-record")}), "\n")
	if !strings.Contains(got, "bytes in all skills, at most 2097152") {
		t.Fatalf("want the 2 MB limit, got:\n%s", got)
	}
}

func TestSkillsTooManyFiles(t *testing.T) {
	files := map[string]string{}
	for i := 0; i < 20; i++ {
		files["skills/video-record/scripts/s"+string(rune('a'+i))+".js"] = "x"
	}
	got := strings.Join(testEmployee(t, files, []any{ref("video-record")}), "\n")
	if !strings.Contains(got, "23 files, at most 20 per skill") {
		t.Fatalf("want the 20 files limit, got:\n%s", got)
	}
}

func TestPullRequestSkipsGitFile(t *testing.T) {
	pr, base := t.TempDir(), t.TempDir()
	os.WriteFile(filepath.Join(pr, ".git"), []byte("gitdir: /elsewhere\n"), 0o644)
	var p problems
	checkPullRequest(&p, pr, base, account{"acme", 42})
	if len(p.list) > 0 {
		t.Fatalf("a .git file is not a change, got:\n%s", strings.Join(p.list, "\n"))
	}
}

func writeFiles(t *testing.T, dir string, files map[string]string) {
	t.Helper()
	for rel, content := range files {
		f := filepath.Join(dir, filepath.FromSlash(rel))
		if err := os.MkdirAll(filepath.Dir(f), 0o755); err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(f, []byte(content), 0o644); err != nil {
			t.Fatal(err)
		}
	}
}

func joined(p problems) string { return strings.Join(p.list, "\n") }

// The text of a community employee is CC-BY-4.0 or CC0-1.0; harnsy's own is CC-BY-4.0 (TERMS.md 3.1).
func TestTextLicence(t *testing.T) {
	for _, c := range []struct {
		pub, lic string
		ok       bool
	}{
		{"acme", "CC-BY-4.0", true}, {"acme", "CC0-1.0", true}, {"acme", "CC BY 4.0", true},
		{"acme", "CC-BY-NC-4.0", false}, {"acme", "CC-BY-SA-4.0", false}, {"acme", "GPL-3.0-only", false},
		{"acme", "LicenseRef-Mine", false}, {"harnsy", "CC-BY-4.0", true}, {"harnsy", "CC0-1.0", false},
	} {
		dir := t.TempDir()
		bj, _ := json.Marshal(map[string]any{"schema": "harnsy.employee/v1", "persona": map[string]any{"name": "Vera"},
			"role": map[string]any{"name": "Recorder", "prompt": "You are an AI agent."}, "license": c.lic})
		writeFiles(t, dir, map[string]string{
			"publishers/" + c.pub + ".json":                 `{"name": "P", "description": "", "github": ["acme"], "github_ids": [42]}`,
			"employees/" + c.pub + "/rec/1.0.0/bundle.json": string(bj),
		})
		var p problems
		checkTree(&p, dir)
		if got := strings.Contains(joined(p), "license"); got == c.ok {
			t.Errorf("%s %q: ok=%v, got:\n%s", c.pub, c.lic, c.ok, joined(p))
		}
	}
}

// A publisher is bound to the account id: a login taken over after a rename does not send under it.
func TestPublisherAccountID(t *testing.T) {
	base, pr := t.TempDir(), t.TempDir()
	pub := `{"name": "Acme", "description": "", "github": ["acme"], "github_ids": [42]}`
	writeFiles(t, base, map[string]string{"publishers/acme.json": pub})
	writeFiles(t, pr, map[string]string{"publishers/acme.json": pub, "employees/acme/rec/1.0.0/listing.json": "{}"})
	for _, c := range []struct {
		a  account
		ok bool
	}{{account{"acme", 42}, true}, {account{"acme", 7}, false}, {account{"other", 42}, true}} {
		var p problems
		checkPullRequest(&p, pr, base, c.a)
		if got := !strings.Contains(joined(p), "belongs to"); got != c.ok {
			t.Errorf("%+v: ok=%v, got:\n%s", c.a, c.ok, joined(p))
		}
	}
	// A new publisher names its login and id.
	pr2 := t.TempDir()
	writeFiles(t, pr2, map[string]string{"publishers/new.json": `{"name": "New", "description": "", "github": ["neo"]}`})
	var p problems
	checkPullRequest(&p, pr2, t.TempDir(), account{"neo", 9})
	if !strings.Contains(joined(p), `your id 9 in "github_ids"`) {
		t.Errorf("a new publisher without github_ids passed:\n%s", joined(p))
	}
}

// A block is a date, without a reason (TERMS.md 6.4).
func TestBannedIsADate(t *testing.T) {
	for v, ok := range map[string]bool{"2026-10-08": true, "spam": false, "2026-10-08 copied prompts": false} {
		dir := t.TempDir()
		writeFiles(t, dir, map[string]string{"publishers/acme.json": `{"name": "Acme", "description": "", "github": ["acme"], "github_ids": [42], "banned": "` + v + `"}`})
		var p problems
		checkTree(&p, dir)
		if got := !strings.Contains(joined(p), "banned"); got != ok {
			t.Errorf("banned %q: ok=%v, got:\n%s", v, ok, joined(p))
		}
	}
}

// The description keeps the template's boxes ticked and names the base's terms version.
func TestBody(t *testing.T) {
	base := t.TempDir()
	writeFiles(t, base, map[string]string{"TERMS.md": "# Terms\n\nVersion `2026-10-08.1` · effective 8 October 2026\n"})
	ticked := "## Confirmations\n\nTerms: [contributor terms, version 2026-10-08.1](../blob/main/TERMS.md).\n\n" + strings.Repeat("- [x] yes\n", 6)
	for name, c := range map[string]struct {
		body, want string
	}{
		"ok":           {ticked, ""},
		"crlf":         {strings.ReplaceAll(ticked, "\n", "\r\n"), ""},
		"old version":  {strings.Replace(ticked, "2026-10-08.1", "2026-09-01.1", 1), "terms version"},
		"one unticked": {ticked + "- [ ] no\n", "not ticked"},
		"no template":  {"Here is my employee.", "terms version"},
		"few boxes":    {strings.Replace(ticked, strings.Repeat("- [x] yes\n", 6), "- [x] yes\n", 1), "fewer than"},
	} {
		f := filepath.Join(t.TempDir(), "body.md")
		os.WriteFile(f, []byte(c.body), 0o644)
		var p problems
		checkBody(&p, base, f)
		if got := joined(p); (c.want == "") != (got == "") || !strings.Contains(got, c.want) {
			t.Errorf("%s: want %q, got:\n%s", name, c.want, got)
		}
	}
	// No TERMS.md on the base yet: nothing to check.
	var p problems
	checkBody(&p, t.TempDir(), filepath.Join(base, "missing"))
	if len(p.list) > 0 {
		t.Errorf("no TERMS.md on the base, got:\n%s", joined(p))
	}
}

// SPDX expressions as harnsy reads them (#1674).
func TestSPDXExpr(t *testing.T) {
	for in, want := range map[string]string{
		"CC-BY-4.0 AND MIT":                             "CC-BY-4.0 AND MIT",
		"GPL-2.0-or-later WITH Classpath-exception-2.0": "GPL-2.0-or-later WITH Classpath-exception-2.0",
		"( mit or Apache-2.0 )  and CC-BY-4.0":          "(mit OR Apache-2.0) AND CC-BY-4.0",
		"cc by 4.0":                                     "CC-BY-4.0",
		"MIT MIT":                                       "",
		"MIT AND":                                       "",
		"(MIT":                                          "",
		"CC BY 4.0 AND MIT":                             "",
		"MIT)":                                          "",
		"((((MIT))))":                                   "((((MIT))))",
		"(((((MIT)))))":                                 "",
		strings.Repeat("MIT AND ", 10) + "MIT":          "",
	} {
		got, err := spdx("license", in)
		if (err != nil) != (want == "") || got != want {
			t.Errorf("%q: got %q %v, want %q", in, got, err, want)
		}
	}
}

// The bundle's licence: text CC-BY-4.0 / CC0-1.0, an expression may add the scripts' licences.
func TestBundleLicenceExpr(t *testing.T) {
	for _, c := range []struct {
		pub, lic string
		ok       bool
	}{
		{"acme", "CC-BY-4.0 AND MIT", true}, {"acme", "cc-by-4.0 and mit", true}, {"acme", "(CC0-1.0 AND Apache-2.0)", true}, {"acme", "MIT", false},
		{"acme", "CC-BY-4.0 AND GPL-3.0-only", false}, {"acme", "CC-BY-4.0 WITH Classpath-exception-2.0", false},
		{"harnsy", "CC-BY-4.0 AND MIT", true}, {"harnsy", "CC0-1.0 AND MIT", false},
	} {
		var p problems
		checkBundleLicence(&p, "bundle.json", c.pub, c.lic)
		if (len(p.list) == 0) != c.ok {
			t.Errorf("%s %q: ok=%v, got:\n%s", c.pub, c.lic, c.ok, joined(p))
		}
	}
}
