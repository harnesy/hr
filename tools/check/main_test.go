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
	write("publishers/acme.json", `{"name": "Acme", "description": "Test publisher.", "github": ["acme"]}`)
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
		{"listing subtitle and license_note", map[string]string{"listing.json": `{"subtitle":"A character in the spirit of Ada Lovelace.","license_note":"No rights in the names are granted."}`}, one, ""},
		{"listing subtitle on two lines", map[string]string{"listing.json": `{"subtitle":"one\ntwo"}`}, one, "subtitle: one line, printable characters only"},
		{"listing license_note too long", map[string]string{"listing.json": `{"license_note":"` + strings.Repeat("x", 401) + `"}`}, one, "license_note: one line, 1..400 bytes"},
		{"listing unknown key", map[string]string{"listing.json": `{"subline":"x"}`}, one, `unknown field "subline"`},
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
	checkPullRequest(&p, pr, base, "acme")
	if len(p.list) > 0 {
		t.Fatalf("a .git file is not a change, got:\n%s", strings.Join(p.list, "\n"))
	}
}
