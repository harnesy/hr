#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Structure scan: rank the files, functions, folders and components of a repository by size.
Python 3.11+, standard library only, offline, read-only. It ranks; people decide.

usage:
  structure_scan.py [PATH] [--md FILE] [--json FILE] [--compare BASELINE.json] [--fail-on-worse]
                    [--exclude GLOB]... [--include-data] [--include-tests]
                    [--dupes [N]] [--top N] [threshold flags]

  PATH            repository root to scan (default: current directory)
  --md FILE       write the Markdown report to FILE instead of stdout
  --json FILE     write a baseline: every metric, one row per file and per function
  --compare FILE  print the delta against an earlier baseline; rows that got worse are marked
                  (take the baseline and the new scan with the same flags). Worse also means:
                  a function, component or file already over its hard limit that grew, and a
                  new file over --new-file-hard (it needs the OK)
  --fail-on-worse exit 1 when --compare finds a worse metric (default: always exit 0)
  --exclude GLOB  leave out files whose path from PATH, file name, or any parent folder
                  matches GLOB (repeatable; for example --exclude 'web/src/i18n/*'
                  --exclude '*.pb.go'); the count shows in the Skipped line
  --include-data  also scan the data folders that are skipped by default (below)
  --include-tests count test files like source files (for code whose product is the tests)
  --dupes [N]     also list the top N repeated 10-line blocks across files (default N: 20)
  --top N         rows per table (default 25)

Thresholds (defaults in brackets): --file-limit [300] --file-hard [800] --func-limit [50]
--func-hard [100] --nesting [3] --folder-limit [20] --component-limit [200]
--component-hard [600] --methods [40] --new-file-hard [500]

What it measures. Lines are non-blank lines. Tests, stories, generated, minified, vendored and .d.ts
files are excluded from the limits (tests are listed separately). Folders that usually hold data
rather than code (locales, i18n, lang, translations, fixtures, testdata) are skipped by default;
the Skipped line says how many source-language files each one held, so nothing is hidden.
A string folder (locales, i18n, lang, translations) that holds a function is code, not data
(a Go package `lang`): it is scanned, and the Skipped line names it. fixtures and testdata
hold test inputs, which are often code on purpose: they stay skipped.
  files       lines per source file; files over the limit and over the hard limit; p50/p90/p99
  folders     non-test source files per folder; folders at or over the folder limit
  functions   length and maximum nesting per function:
              Go: `func` at column 0 to `}` at column 0;
              Python/Ruby: `def` to the next statement at the same or lower indent;
              brace languages (JS/TS, Java, Kotlin, C#, PHP, Rust, C/C++, Swift, Dart):
              signature to the matching brace, strings and comments stripped first
  types       methods per type (Go: by receiver across the package; others: inside class bodies)
  components  .vue/.svelte/.tsx/.jsx size (Vue/Svelte: template + script, <style> excluded),
              boolean props where cheaply visible
  names       near-duplicate file names in different folders: same stem after common
              abbreviations (Btn = Button), or edit distance <= 2 (<= 1 for names under 10 letters)

What it misses. A copy shorter than the 10-line window (a three-line handler pasted into many
components) is not found by --dupes; search for it by hand.
"""
import sys

if sys.version_info < (3, 11):  # checked before the patterns below, which need 3.11
    sys.exit("structure_scan.py needs Python 3.11 or newer (found %d.%d)" % sys.version_info[:2])

import argparse  # noqa: E402
import fnmatch  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
from collections import Counter, defaultdict  # noqa: E402

DISCLAIMER = ("Not claimed: correctness, true complexity, true duplicates (name and block matches "
              "are hints only), coupling or design quality. Heuristic, about ±10%. It ranks; people decide.")

LANGS = {
    ".go": "go", ".py": "python", ".rb": "ruby", ".js": "js", ".jsx": "js", ".mjs": "js",
    ".cjs": "js", ".ts": "ts", ".tsx": "ts", ".mts": "ts", ".cts": "ts", ".java": "java",
    ".kt": "kotlin", ".kts": "kotlin", ".cs": "csharp", ".php": "php", ".rs": "rust",
    ".c": "c", ".h": "c", ".cc": "c", ".cpp": "c", ".cxx": "c", ".hpp": "c", ".hh": "c",
    ".swift": "swift", ".dart": "dart", ".vue": "vue", ".svelte": "svelte",
}
UI_EXT = {".vue", ".svelte", ".tsx", ".jsx"}
SKIP_DIRS = {"vendor", "node_modules", "dist", "build", "target", "venv",
             "__pycache__", "site-packages", "bower_components", "coverage", "third_party",
             "third-party", "Pods", "DerivedData"}
DATA_DIRS = {"locales", "i18n", "lang", "translations", "fixtures", "testdata"}
STRING_DIRS = {"locales", "i18n", "lang", "translations"}  # skipped only when they hold no function
LOCKFILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "go.sum", "Cargo.lock",
             "poetry.lock", "composer.lock", "Gemfile.lock", "Pipfile.lock", "bun.lockb"}
TEST_DIRS = {"test", "tests", "__tests__", "spec", "specs", "e2e", "__mocks__", "cypress"}
TEST_FILE = re.compile(
    r"(_test\.(go|py|rb|dart)$|^test_.*\.py$|^conftest\.py$|_spec\.rb$"
    r"|\.(test|spec|cy|stories|story)\.[^.]+$|(Tests?|Spec)\.(java|kt|cs|swift|scala)$)")
GENERATED = re.compile(r"^\s*(?://|#|/?\*|<!--|--)[ \t]*(?:(?i:code generated|@generated|"
                       r"auto-?generated|this file (?:is|was) (?:automatically )?generated)|"
                       r".*DO NOT EDIT)", re.M)

# --- stripping strings and comments (newlines kept, so line numbers stay valid) ---------------
_DQ = r'"(?:\\.|[^"\\\n])*"'
_SQ = r"'(?:\\.|[^'\\\n])*'"
_CHAR = r"'(?:\\[^'\n]{1,10}|[^'\\\n])'"
_BLOCK, _LINE = r"/\*[\s\S]*?\*/", r"//[^\n]*"
STRIP = {
    "c_like": re.compile("|".join([_BLOCK, _LINE, r'"""[\s\S]*?"""', r'@"(?:""|[^"])*"', _DQ,
                                   _CHAR, r"`[^`]*`"])),
    "js": re.compile("|".join([_BLOCK, _LINE, _DQ, _SQ, r"`(?:\\.|[^`\\])*`"])),
    "php": re.compile("|".join([_BLOCK, _LINE, r"#(?!\[)[^\n]*", _DQ, _SQ])),
    "dart": re.compile("|".join([_BLOCK, _LINE, r'"""[\s\S]*?"""', r"'''[\s\S]*?'''", _DQ,
                                 _SQ])),
    "python": re.compile(r"[rRbBuUfF]{0,2}(?:\"\"\"[\s\S]*?\"\"\"|'''[\s\S]*?''')|#[^\n]*|"
                         + _DQ + "|" + _SQ),
    "ruby": re.compile(r"^=begin[\s\S]*?^=end|#[^\n]*|" + _DQ + "|" + _SQ, re.M),
}
STRIP_FAMILY = {"js": "js", "ts": "js", "vue": "js", "svelte": "js", "php": "php",
                "dart": "dart", "python": "python", "ruby": "ruby"}


def _blank(m):
    text = m.group(0)
    n = text.count("\n")
    if text[:1] in "/#=":  # comment: drop it, keep its line breaks
        return "\n" * n
    return '""' + "\n" * n


def strip_code(text, lang):
    return STRIP[STRIP_FAMILY.get(lang, "c_like")].sub(_blank, text)


# --- brace languages ---------------------------------------------------------------------------
CONTROL = {"if", "for", "while", "switch", "catch", "with", "foreach", "using", "lock", "fixed",
           "elseif", "match", "synchronized", "when", "do", "return", "sizeof", "typeof", "new",
           "else", "try", "guard", "unless", "until", "loop", "select", "defer", "go", "super",
           "this", "base", "await", "throw", "yield", "case", "delete", "function", "func",
           "fn", "fun", "assert"}
BLOCK_START = re.compile(r"^\s*(?:\}\s*)?(if|else|for|while|switch|match|select|guard|loop|case|"
                         r"unless|until|unsafe|go|defer|catch|try|do|finally|when|func|fn|fun)\b")
BLOCK_END_WORD = re.compile(r"\b(else|try|do|finally|loop|unsafe|async|defer|static|get|set|"
                            r"init|deinit|catch)\s*$")
TYPE_RE = re.compile(r"(?:^|[\s(])(?:class|interface|struct|enum|trait|object|record|protocol|"
                     r"extension|union)\s+([A-Za-z_]\w*)")
IMPL_RE = re.compile(r"(?:^|\s)impl\b(?:\s*<[^{]*?>)?\s+(?:[\w:<>, &']+?\s+for\s+)?([A-Za-z_]\w*)")
KEYWORD_FN = {
    "rust": re.compile(r"\bfn\s+(\w+)"),
    "kotlin": re.compile(r"\bfun\s+(?:<[^>]*>\s*)?(?:[\w.<>?]+\.)?(\w+)\s*\("),
    "swift": re.compile(r"\bfunc\s+(\w+)|\b(init|deinit)\b\s*[(?{]"),
    "php": re.compile(r"\bfunction\s+&?(\w+)\s*\("),
    "js": re.compile(r"\bfunction\s*\*?\s*(\w+)\s*(?:<[^>]*>)?\s*\("),
}
GENERIC_LANGS = {"js", "ts", "vue", "svelte", "java", "csharp", "c", "dart"}
_SUFFIX = (r"(?>\s*+(?>(?::|->)[^(){};=]*+(?:\([^(){}]*+\)[^(){};=]*+)*+|throws\s[\w.,\s]++|"
           r"where\s[^{};]++|const|noexcept|override|final|async\*?|sync\*?|&))*+\s*+$")
GENERIC_RE = re.compile(r"(~?[A-Za-z_]\w*)\s*+(?:<[^(){};]*+>)?\s*+\((?:[^()]++|\([^()]*+"
                        r"(?:\([^()]*+\)[^()]*+)*+\))*+\)" + _SUFFIX)
ARROW_RE = re.compile(r"([A-Za-z_$][\w$]*)\s*(?::[^=;{}]*?)?\s*[=:]\s*(?:[\w$.]+\s*\(\s*)*"
                      r"(?:async\s+)?(?:<[^>]*>\s*)?(?:\((?:[^()]++|\([^()]*+\))*+\)|[A-Za-z_$][\w$]*)\s*"
                      r"(?::\s*[^=;{}]*?)?\s*=>\s*$")
BAD_BEFORE = set(".=(,!&|?:+-/%<[{")


def is_block(header, lang):
    """Does this `{` open a code block (counts for nesting) rather than a literal?"""
    h = header.rstrip()
    if not h:
        return True
    if h[-1] == ")" or h.endswith("=>") or h.endswith("->"):
        return True
    if h[-1] in "=([,:?&|!<>":
        return False
    last = h[h.rfind("\n") + 1:]
    if BLOCK_START.match(last) or BLOCK_END_WORD.search(h):
        return True
    return lang in ("kotlin", "swift") and re.search(r"\.\w+\s*$", h) is not None


def classify(header, lang, in_func):
    """Return ('type'|'func'|None, name, offset of the name in header)."""
    if lang != "go":
        m = TYPE_RE.search(header) or (IMPL_RE.search(header) if lang == "rust" else None)
        if m and not (lang in ("js", "ts", "vue", "svelte") and header.rstrip().endswith("=>")):
            return "type", m.group(1), m.start(1)
    kw = KEYWORD_FN.get("js" if lang in ("ts", "vue", "svelte") else lang)
    if kw:
        found = None
        for found in kw.finditer(header):
            pass
        if found:
            g = 1 if found.group(1) else 2
            return "func", found.group(g), found.start(g)
    h = header.rstrip()
    if lang in ("js", "ts", "vue", "svelte") and h.endswith("=>"):
        m = ARROW_RE.search(h)
        return ("func", m.group(1), m.start(1)) if m else (None, "", 0)
    if lang in GENERIC_LANGS and not in_func and ")" in h:
        m = GENERIC_RE.search(h)
        if m and m.group(1) not in CONTROL:
            before = h[:m.start(1)].rstrip()
            words = before.split()
            if before.endswith("::"):
                return "func", before[:-2].split()[-1].split("*")[-1] + "::" + m.group(1), m.start(1)
            if not before or (
                    before[-1] not in BAD_BEFORE and words[-1] not in CONTROL):
                return "func", m.group(1), m.start(1)
    return None, "", 0


TOKENS = re.compile(r"[{}();]")


def brace_scan(s, lang, nlines):
    """One pass over stripped text. Returns functions [(name, start, end, type, block depth)]
    and the deepest block opened on each line (for nesting)."""
    stack, funcs = [], []
    line_maxb = [0] * (nlines + 1)
    prev, paren, line, pos = -1, 0, 0, 0
    for m in TOKENS.finditer(s):
        p = m.start()
        line += s.count("\n", pos, p)
        pos = p
        c = s[p]
        if c == "(":
            paren += 1
        elif c == ")":
            paren = max(0, paren - 1)
        elif c == ";":
            if paren == 0:
                prev = p
        elif c == "{":
            hstart = max(prev + 1, p - 400)
            header = s[hstart:p]
            parent = stack[-1] if stack else None
            in_func = bool(parent and (parent["in_func"] or parent["kind"] == "func"))
            kind, name, off = (None, "", 0) if lang == "go" else classify(header, lang, in_func)
            block = kind == "func" or is_block(header, lang)
            bd = (parent["bd"] if parent else 0) + (1 if block else 0)
            start = line - s.count("\n", hstart + off, p)
            stack.append({"kind": kind, "name": name, "start": start, "bd": bd,
                          "in_func": in_func, "prev": prev, "paren": paren,
                          "parent": parent["name"] if parent and parent["kind"] == "type" else None})
            line_maxb[line] = max(line_maxb[line], bd)
            prev, paren = p, 0
        else:  # "}"
            if not stack:
                prev = p
                continue
            e = stack.pop()
            paren = e["paren"]
            prev = e["prev"] if paren > 0 else p
            if e["kind"] == "func":
                funcs.append((e["name"], e["start"], line, e["parent"], e["bd"]))
    return funcs, line_maxb


GO_FUNC = re.compile(r"^func\s*(?:\(\s*(?:\w+\s+)?\*?\s*(\w+)[^)]*\)\s*)?(\w+)")


def go_functions(slines):
    """Go: `func` at column 0 to `}` at column 0."""
    out, i, n = [], 0, len(slines)
    while i < n:
        m = GO_FUNC.match(slines[i])
        if not m:
            i += 1
            continue
        j = i
        if not (slines[i].count("{") and slines[i].count("{") == slines[i].count("}")):
            j = i + 1
            while j < n and not slines[j].startswith("}") and not GO_FUNC.match(slines[j]):
                j += 1
            if j >= n or not slines[j].startswith("}"):
                i += 1  # declaration without body
                continue
        out.append((m.group(2), i, j, m.group(1), 1))
        i = j + 1
    return out


# --- indent languages --------------------------------------------------------------------------
PY_BLOCK = re.compile(r"(?:async\s+)?(if|elif|else|for|while|try|except|finally|with|match|case)"
                      r"\b")
DEF_RE = {"python": re.compile(r"(?:async\s+)?def\s+(\w+)"),
          "ruby": re.compile(r"def\s+(?:self\.)?([\w?!=\[\]<>+\-*/%]+)")}
CLASS_RE = re.compile(r"(?:class|module)\s+([A-Za-z_]\w*(?:::\w+)*)")


def indent_scan(slines, lang):
    """Python/Ruby: def to the next statement at the same or lower indent (Ruby: that `end`)."""
    sig, depth = [], 0  # significant lines: start a statement outside any open bracket
    for i, s in enumerate(slines):
        t = s.strip()
        if t and depth == 0:
            sig.append((i, len(s) - len(s.lstrip()), t))
        depth = max(0, depth + sum(s.count(c) for c in "([{") - sum(s.count(c) for c in ")]}"))
    funcs, stack, methods = [], [], Counter()
    for k, (i, ind, t) in enumerate(sig):
        while stack and stack[-1][2] >= ind:
            stack.pop()
        cm = CLASS_RE.match(t)
        dm = DEF_RE[lang].match(t)
        if cm:
            stack.append(("class", cm.group(1), ind))
        elif dm:
            owner = stack[-1][1] if stack and stack[-1][0] == "class" else None
            if owner:
                methods[owner] += 1
            end, body, nest, unit = i, [], 0, None
            for (j, jind, jt) in sig[k + 1:]:
                if jind <= ind:
                    if lang == "ruby" and jind == ind and jt == "end":
                        end = j
                    break
                body.append((jind, jt))
                end = j
            else:
                end = len(slines) - 1
            if body:
                base = body[0][0]
                unit = max(1, base - ind)
                for jind, jt in body:
                    lvl = (jind - base) // unit
                    if lang == "ruby":
                        nest = max(nest, lvl)
                    elif PY_BLOCK.match(jt):
                        nest = max(nest, lvl + 1)
            funcs.append((dm.group(1), i, end, owner, nest))
            stack.append(("def", dm.group(1), ind))
    return funcs, methods


# --- per file ----------------------------------------------------------------------------------
BOOL_PROP = re.compile(r"\b\w+\??\s*:\s*(?:boolean|Boolean)\b")
STYLE_RE = re.compile(r"<style\b[\s\S]*?</style>", re.I)
SCRIPT_RE = re.compile(r"(<script\b[^>]*>)([\s\S]*?)</script>", re.I)


def keep_only(text, spans):
    """Blank everything outside spans, keeping line breaks."""
    out, last = [], 0
    for a, b in spans:
        out.append("\n" * text.count("\n", last, a))
        out.append(text[a:b])
        last = b
    out.append("\n" * text.count("\n", last))
    return "".join(out)


def analyse(text, lang, ext, dirname):
    raw = text.split("\n")
    sized = text
    if lang in ("vue", "svelte"):
        sized = STYLE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
        text = keep_only(text, [m.span(2) for m in SCRIPT_RE.finditer(text)])
    nb = [0]  # prefix sums of non-blank lines
    for ln in raw:
        nb.append(nb[-1] + (1 if ln.strip() else 0))
    lines = sum(1 for ln in sized.split("\n") if ln.strip())
    s = strip_code(text, lang)
    slines = s.split("\n")
    methods = Counter()
    if lang in ("python", "ruby"):
        funcs, owners = indent_scan(slines, lang)
        line_maxb = None
        methods.update({(dirname, k): v for k, v in owners.items()})
    else:
        funcs, line_maxb = brace_scan(s, lang, len(slines))
        if lang == "go":
            funcs = go_functions(slines)
    rows = []
    for name, a, b, owner, bd in funcs:
        if line_maxb is not None:
            nest = max(line_maxb[a:b + 1] or [bd]) - bd
        else:
            nest = bd
        if lang not in ("python", "ruby") and owner:
            methods[(dirname, owner)] += 1
        rows.append({"name": f"{owner}.{name}" if owner else name, "line": a + 1,
                     "lines": nb[b + 1] - nb[a], "nesting": max(0, nest)})
    if lang == "c":  # out-of-class C++ definitions: Type::method
        for m in re.finditer(r"\b([A-Za-z_]\w*)::(~?\w+)\s*\([^;{}]*\)[^;{}]*\{", s):
            if m.group(1) != m.group(2):
                methods[(dirname, m.group(1))] += 1
    comp = bools = None
    if ext in UI_EXT:
        comp = lines
        bools = len(BOOL_PROP.findall(s))
    return lines, rows, methods, comp, bools


def classify_file(rel, name):
    parts = rel.split("/")[:-1]
    if TEST_FILE.search(name) or any(p in TEST_DIRS for p in parts):
        return True
    return False


def _keep_dir(dp, d):
    return (not d.startswith(".") and d not in SKIP_DIRS
            and not os.path.exists(os.path.join(dp, d, "pyvenv.cfg")))


def count_sources(top):
    """Source-language files under a skipped data folder (for the Skipped line)."""
    n = 0
    for dp, dns, fns in os.walk(top):
        dns[:] = [d for d in dns if _keep_dir(dp, d)]
        n += sum(1 for fn in fns if os.path.splitext(fn)[1].lower() in LANGS and fn not in LOCKFILES)
    return n


def has_functions(top):
    """True when a source file under a string folder defines a function (then it is code)."""
    for dp, dns, fns in os.walk(top):
        dns[:] = [d for d in dns if _keep_dir(dp, d)]
        for fn in fns:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in LANGS or fn in LOCKFILES:
                continue
            try:
                with open(os.path.join(dp, fn), encoding="utf-8", errors="replace") as f:
                    if analyse(f.read(), LANGS[ext], ext, ".")[1]:
                        return True
            except OSError:
                continue
    return False


def excluded(rel, globs):
    """Does a --exclude glob match the path, the file name, or a parent folder (path or name)?"""
    if not globs:
        return False
    parts = rel.split("/")
    cands = [rel, parts[-1]]
    for i in range(1, len(parts)):
        cands += ["/".join(parts[:i]), parts[i - 1]]
    return any(fnmatch.fnmatchcase(c, g.rstrip("/")) for g in globs for c in cands)


def walk(root, data_dirs, data_skipped, data_code):
    for dp, dns, fns in os.walk(root):
        keep = []
        for d in sorted(dns):
            if not _keep_dir(dp, d):
                continue
            if d in data_dirs:
                top = os.path.join(dp, d)
                if d in STRING_DIRS and has_functions(top):
                    data_code[d] += 1
                else:
                    n = count_sources(top)
                    if n:
                        data_skipped[d] += n
                    continue
            keep.append(d)
        dns[:] = keep
        for fn in sorted(fns):
            yield dp, fn


def scan(root, excludes=(), include_data=False, include_tests=False):
    files, funcs, skipped = [], [], Counter()
    methods, data_skipped, data_code = Counter(), Counter(), Counter()
    for dp, fn in walk(root, set() if include_data else DATA_DIRS, data_skipped, data_code):
        ext = os.path.splitext(fn)[1].lower()
        lang = LANGS.get(ext)
        if fn in LOCKFILES or not lang:
            continue
        path = os.path.join(dp, fn)
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if excluded(rel, excludes):
            skipped["excluded by --exclude"] += 1
            continue
        if ".min." in fn:
            skipped["minified"] += 1
            continue
        if fn.endswith(".d.ts"):
            skipped["type declarations"] += 1
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            skipped["unreadable"] += 1
            continue
        if any(len(ln) > 1000 for ln in text.split("\n", 400)[:400]) or (
                len(text) > 2000 and len(text) / (text.count("\n") + 1) > 200):
            skipped["minified"] += 1
            continue
        if GENERATED.search(text[:3000]):
            skipped["generated"] += 1
            continue
        dirname = os.path.dirname(rel) or "."
        test = classify_file(rel, fn) and not include_tests
        lines, rows, meth, comp, bools = analyse(text, lang, ext, dirname)
        files.append({"path": rel, "lang": lang, "lines": lines, "test": test,
                      "component_lines": comp, "bool_props": bools})
        if not test:
            methods.update(meth)
            for r in rows:
                r["file"] = rel
                funcs.append(r)
    if data_skipped:
        skipped["in data folders"] = sum(data_skipped.values())
    return files, funcs, methods, skipped, data_skipped, data_code


# --- names and repeated blocks -----------------------------------------------------------------
ABBR = {"btn": "button", "dlg": "dialog", "msg": "message", "img": "image", "pic": "picture",
        "cfg": "config", "ctx": "context", "mgr": "manager", "svc": "service", "nav": "navigation",
        "ctrl": "controller", "repo": "repository", "util": "utils", "info": "information"}
NAME_STOP = {"index", "main", "mod", "lib", "init", "app", "page", "layout", "default", "error",
             "loading", "types", "utils", "helpers", "constants", "config", "routes", "server",
             "client", "store", "api", "service", "model", "models", "view", "views", "style",
             "styles", "setup", "plugin", "module", "component", "doc", "docs", "root"}


FAMILY = {"js": "web", "ts": "web", "vue": "web", "svelte": "web", "java": "jvm", "kotlin": "jvm"}


TOOL_CONFIG = re.compile(r"\.config\.\w+$|^vite-env|rc\.\w+$")  # vite.config.ts, .eslintrc.js


def name_words(stem):
    return [ABBR.get(w.lower(), w.lower())
            for w in re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+", stem)]


def edit_distance(a, b, cap=2):
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        if min(cur) > cap:
            return cap + 1
        prev = cur
    return prev[-1]


def _deletes(w, n=2):
    out, level = {w}, {w}
    for _ in range(n):
        level = {x[:i] + x[i + 1:] for x in level for i in range(len(x))}
        out |= level
    return out


def near_duplicates(files):
    """Pairs of files in different folders, same language family, both UI or both not: same
    normalised stem (CopyBtn = CopyButton), or edit distance <= 2 (<= 1 under 10 letters)."""
    by_key = defaultdict(list)
    for f in files:
        if f["test"]:
            continue
        fn = f["path"].rsplit("/", 1)[-1]
        if TOOL_CONFIG.search(fn):
            continue
        words = name_words(fn.rsplit(".", 1)[0])  # keep inner parts: user.controller != user.guard
        key = "".join(words)
        ui = os.path.splitext(fn)[1] in UI_EXT
        if len(key) < 4 or key in NAME_STOP or (len(words) < 2 and not ui):
            continue
        by_key[(FAMILY.get(f["lang"], f["lang"]), ui, key)].append(f["path"])
    pairs = []
    for key, paths in by_key.items():
        other = [p for p in paths if os.path.dirname(p) != os.path.dirname(paths[0])]
        if other:
            pairs.append({"a": paths[0], "b": other[0], "count": len(paths), "why": "same name"})
    index = defaultdict(set)
    for k in by_key:
        if len(k[2]) >= 6:
            for d in _deletes(k[2]):
                index[(k[0], k[1], d)].add(k)
    seen = set()
    for group in index.values():
        if len(group) < 2:
            continue
        for a in group:
            for b in group:
                if a >= b or (a, b) in seen:
                    continue
                seen.add((a, b))
                x, y = a[2], b[2]
                if x + "s" == y or y + "s" == x or re.sub(r"\d", "", x) == re.sub(r"\d", "", y):
                    continue  # plural or numbered series
                if edit_distance(x, y) <= (2 if min(len(x), len(y)) >= 10 else 1):
                    pa, pb = sorted((by_key[a][0], by_key[b][0]))
                    if os.path.dirname(pa) != os.path.dirname(pb):
                        pairs.append({"a": pa, "b": pb, "count": 2,
                                      "why": f"edit distance {edit_distance(x, y)}"})
    pairs.sort(key=lambda r: (-r["count"], r["a"]))
    return pairs


def families(files):
    fam = defaultdict(set)
    for f in files:
        fn = f["path"].rsplit("/", 1)[-1]
        if f["test"] or os.path.splitext(fn)[1] not in UI_EXT:
            continue
        words = re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+", fn.split(".")[0])
        if len(words) >= 2:
            fam[ABBR.get(words[-1].lower(), words[-1].lower())].add(f["path"])
    return sorted(((k, len(v)) for k, v in fam.items() if len(v) >= 3), key=lambda x: -x[1])


TRIVIAL = re.compile(r"^(import|from|#include|using|package|require|use|export \{|[})\]];?,?$)")


def repeated_blocks(root, files, top):
    """Repeated windows of 10 non-blank lines (whitespace normalised) across files."""
    seen = defaultdict(list)
    for f in files:
        if f["test"]:
            continue
        with open(os.path.join(root, f["path"]), encoding="utf-8", errors="replace") as fh:
            src = [(i + 1, " ".join(ln.split())) for i, ln in enumerate(fh) if ln.strip()]
        for k in range(len(src) - 9):
            win = [t for _, t in src[k:k + 10]]
            if sum(1 for t in win if len(t) >= 8 and not TRIVIAL.match(t)) < 6:
                continue
            seen[hash(tuple(win))].append((f["path"], src[k][0]))
    hits = sorted((v for v in seen.values() if len({p for p, _ in v}) > 1), key=lambda v: -len(v))
    covered, out = defaultdict(list), []
    for locs in hits:
        p0, l0 = locs[0]
        if any(a <= l0 <= a + 12 for a in covered[p0]):
            continue
        for p, ln in locs:
            covered[p].append(ln)
        out.append({"count": len(locs), "at": [f"{p}:{ln}" for p, ln in locs[:4]]})
        if len(out) >= top:
            break
    return out


# --- report ------------------------------------------------------------------------------------
def pct(values, q):
    if not values:
        return 0
    v = sorted(values)
    return v[max(0, math.ceil(q * len(v) / 100) - 1)]


def share(n, total):
    return f"{n} ({100 * n / total:.1f}%)" if total else "0"


def build(root, args):
    files, funcs, methods, skipped, data_skipped, data_code = scan(
        root, args.exclude or (), args.include_data, args.include_tests)
    src = [f for f in files if not f["test"]]
    folders = Counter(os.path.dirname(f["path"]) or "." for f in src)
    comps = [f for f in src if f["component_lines"] is not None]
    t = vars(args)
    flen = [f["lines"] for f in src]
    fnl = [r["lines"] for r in funcs]
    clen = [c["component_lines"] for c in comps]
    mcount = list(methods.values())
    summary = {
        "source_files": len(src), "test_files": len(files) - len(src),
        "skipped": dict(skipped), "skipped_data_folders": dict(data_skipped),
        "data_folders_as_code": dict(data_code),
        "excludes": list(args.exclude or []), "tests_counted": bool(args.include_tests),
        "languages": dict(Counter(f["lang"] for f in src)),
        "file_p50": pct(flen, 50), "file_p90": pct(flen, 90), "file_p99": pct(flen, 99),
        "files_over_limit": sum(x > t["file_limit"] for x in flen),
        "files_over_hard": sum(x > t["file_hard"] for x in flen),
        "functions": len(funcs), "func_p50": pct(fnl, 50), "func_p90": pct(fnl, 90),
        "func_p99": pct(fnl, 99), "funcs_over_limit": sum(x > t["func_limit"] for x in fnl),
        "funcs_over_hard": sum(x > t["func_hard"] for x in fnl),
        "funcs_over_nesting": sum(r["nesting"] > t["nesting"] for r in funcs),
        "folders_at_limit": sum(n >= t["folder_limit"] for n in folders.values()),
        "types": len(mcount), "methods_p50": pct(mcount, 50), "methods_p90": pct(mcount, 90),
        "methods_p99": pct(mcount, 99), "types_over_methods": sum(n > t["methods"] for n in mcount),
        "components": len(comps), "component_p50": pct(clen, 50),
        "component_p90": pct(clen, 90), "component_p99": pct(clen, 99),
        "components_over_limit": sum(x > t["component_limit"] for x in clen),
        "components_over_hard": sum(x > t["component_hard"] for x in clen),
    }
    near = near_duplicates(files)
    summary["near_duplicate_names"] = len(near)
    data = {"version": 1, "root": os.path.basename(os.path.abspath(root)),
            "thresholds": {k: t[k] for k in ("file_limit", "file_hard", "func_limit", "func_hard",
                                             "nesting", "folder_limit", "component_limit",
                                             "component_hard", "methods", "new_file_hard")},
            "summary": summary, "files": files, "functions": funcs,
            "folders": dict(folders),
            "types": [{"dir": d, "type": n, "methods": c} for (d, n), c in methods.most_common()],
            "near_duplicates": near, "families": families(files)}
    if args.dupes is not None:
        data["repeated_blocks"] = repeated_blocks(root, files, args.dupes)
    return data


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return out


def render(d, top):
    s, t = d["summary"], d["thresholds"]
    n, nf, nc = s["source_files"], s["functions"], s["components"]
    skips = []
    for k, v in s["skipped"].items():
        if k == "in data folders":
            per = ", ".join(f"{name}/ {c}" for name, c in sorted(s["skipped_data_folders"].items()))
            k += f" ({per}; --include-data to scan them)"
        skips.append(f"{v} {k}")
    if s.get("data_folders_as_code"):
        per = ", ".join(f"{name}/ {c}" for name, c in sorted(s["data_folders_as_code"].items()))
        skips.append(f"not skipped, scanned as code because they hold functions: {per}")
    tests = ("Tests and stories (not counted)" if not s.get("tests_counted")
             else "Tests counted as source (--include-tests); other tests")
    out = [f"# Structure scan: {d['root']}", "", f"> {DISCLAIMER}", "",
           f"Source files: {n} ({', '.join(f'{k} {v}' for k, v in sorted(s['languages'].items(), key=lambda x: -x[1]))}). "
           f"{tests}: {s['test_files']}.", "",
           "Skipped: " + ("; ".join(skips) or "none") + ".", ""]
    if s.get("excludes"):
        out += ["Excluded globs: " + ", ".join(f"`{g}`" for g in s["excludes"]) + ".", ""]
    out += ["## Summary", ""]
    out += table(["Metric", "Value"], [
        ["Lines per file p50 / p90 / p99", f"{s['file_p50']} / {s['file_p90']} / {s['file_p99']}"],
        [f"Files > {t['file_limit']} lines", share(s["files_over_limit"], n)],
        [f"Files > {t['file_hard']} lines (HARD)", share(s["files_over_hard"], n)],
        [f"Folders with >= {t['folder_limit']} source files", s["folders_at_limit"]],
        ["Function length p50 / p90 / p99", f"{s['func_p50']} / {s['func_p90']} / {s['func_p99']}"],
        [f"Functions > {t['func_limit']} lines", share(s["funcs_over_limit"], nf)],
        [f"Functions > {t['func_hard']} lines (HARD)", share(s["funcs_over_hard"], nf)],
        [f"Functions nested deeper than {t['nesting']}", share(s["funcs_over_nesting"], nf)],
        ["Methods per type p50 / p90 / p99", f"{s['methods_p50']} / {s['methods_p90']} / {s['methods_p99']}"],
        [f"Types with > {t['methods']} methods", share(s["types_over_methods"], s["types"])],
        ["UI component size p50 / p90 / p99", f"{s['component_p50']} / {s['component_p90']} / {s['component_p99']}"],
        [f"Components > {t['component_limit']} lines", share(s["components_over_limit"], nc)],
        [f"Components > {t['component_hard']} lines (HARD)", share(s["components_over_hard"], nc)],
        ["Near-duplicate file names", s["near_duplicate_names"]]])
    src = sorted((f for f in d["files"] if not f["test"]), key=lambda f: -f["lines"])
    big = [f for f in src if f["lines"] > t["file_limit"]]
    out += ["", f"## Files over {t['file_limit']} lines (top {min(top, len(big))} of {len(big)})", ""]
    out += table(["Lines", "File", ""], [[f["lines"], f["path"], "HARD" if f["lines"] > t["file_hard"] else ""]
                                         for f in big[:top]])
    fold = sorted(((c, p) for p, c in d["folders"].items() if c >= t["folder_limit"]), reverse=True)
    out += ["", f"## Folders with >= {t['folder_limit']} source files ({len(fold)})", ""]
    out += table(["Files", "Folder"], fold[:top])
    fns = sorted(d["functions"], key=lambda r: -r["lines"])
    out += ["", f"## Longest functions (over {t['func_limit']}: {s['funcs_over_limit']}, over {t['func_hard']}: {s['funcs_over_hard']})", ""]
    out += table(["Lines", "Nesting", "Function", "Where"],
                 [[r["lines"], r["nesting"], r["name"], f"{r['file']}:{r['line']}"] for r in fns[:top]])
    deep = sorted((r for r in fns if r["nesting"] > t["nesting"]), key=lambda r: (-r["nesting"], -r["lines"]))
    out += ["", f"## Deepest nesting (> {t['nesting']}: {len(deep)})", ""]
    out += table(["Nesting", "Lines", "Function", "Where"],
                 [[r["nesting"], r["lines"], r["name"], f"{r['file']}:{r['line']}"] for r in deep[:top]])
    out += ["", f"## Types with the most methods (> {t['methods']} flagged)", ""]
    out += table(["Methods", "Type", "Folder", ""], [[r["methods"], r["type"], r["dir"], "over" if r["methods"] > t["methods"] else ""]
                                                     for r in d["types"][:top]])
    comps = sorted((f for f in src if f["component_lines"] is not None), key=lambda f: -f["component_lines"])
    if comps:
        out += ["", f"## UI components (> {t['component_limit']}: {s['components_over_limit']}, > {t['component_hard']} HARD: {s['components_over_hard']})", ""]
        out += table(["Lines", "Boolean props (approx.)", "Component"], [[c["component_lines"], c["bool_props"], c["path"]] for c in comps[:top]])
    out += ["", f"## Near-duplicate file names ({len(d['near_duplicates'])}; hints only)", ""]
    out += table(["Files", "Example", "Other", "Why"], [[r["count"], r["a"], r["b"], r["why"]] for r in d["near_duplicates"][:top]])
    if d["families"]:
        out += ["", "## UI name families (last word of the component name, >= 3 files)", ""]
        out += table(["Word", "Files"], d["families"][:15])
    if "repeated_blocks" in d:
        out += ["", "## Repeated 10-line blocks (hints only)", ""]
        out += table(["Copies", "Where"], [[r["count"], ", ".join(r["at"])] for r in d["repeated_blocks"]])
    tests = sorted((f for f in d["files"] if f["test"]), key=lambda f: -f["lines"])
    if tests:
        out += ["", f"## Tests (reported separately, not limited): {len(tests)} files, p90 {pct([f['lines'] for f in tests], 90)} lines", ""]
        out += table(["Lines", "File"], [[f["lines"], f["path"]] for f in tests[:5]])
    return "\n".join(out) + "\n"


def compare(base, d):
    """Delta against a baseline. Returns (markdown, worse?)."""
    t = d["thresholds"]
    bf = {f["path"]: f for f in base["files"] if not f["test"]}
    rows, details, worse = [], [], False

    def mark(label, b, n, bad):
        nonlocal worse
        worse |= bad
        rows.append([label, b, n, "**worse**" if bad else ("better" if n < b else "same")])

    bs, ns = base["summary"], d["summary"]
    for key, label in [("files_over_limit", f"Files > {t['file_limit']}"),
                       ("files_over_hard", f"Files > {t['file_hard']}"),
                       ("folders_at_limit", f"Folders >= {t['folder_limit']}"),
                       ("funcs_over_limit", f"Functions > {t['func_limit']}"),
                       ("funcs_over_hard", f"Functions > {t['func_hard']}"),
                       ("funcs_over_nesting", f"Functions nested > {t['nesting']}"),
                       ("types_over_methods", f"Types > {t['methods']} methods"),
                       ("components_over_limit", f"Components > {t['component_limit']}"),
                       ("components_over_hard", f"Components > {t['component_hard']}")]:
        mark(label, bs.get(key, 0), ns.get(key, 0), ns.get(key, 0) > bs.get(key, 0))
    for f in d["files"]:
        if f["test"]:
            continue
        old = bf.get(f["path"])
        if f["lines"] > t["file_limit"] and (old is None or old["lines"] <= t["file_limit"]):
            details.append(("**worse**", f"{'new file' if old is None else 'grew past limit'}: {f['path']} "
                            f"{old['lines'] if old else 0} -> {f['lines']}"))
        elif old and old["lines"] > t["file_hard"] and f["lines"] > old["lines"]:
            details.append(("**worse**", f"over {t['file_hard']} and grew: {f['path']} {old['lines']} -> {f['lines']}"))
        elif old and old["lines"] > t["file_limit"] and f["lines"] > old["lines"]:
            details.append(("note", f"over {t['file_limit']} and grew: {f['path']} {old['lines']} -> {f['lines']}"))
        if old is None and f["lines"] > t.get("new_file_hard", 500):
            details.append(("**worse**", f"new file over {t.get('new_file_hard', 500)}, needs the OK: "
                            f"{f['path']} ({f['lines']})"))
        c, oc = f["component_lines"], old and old["component_lines"]
        if c is not None and c > t["component_hard"]:
            if oc is None or oc <= t["component_hard"]:
                details.append(("**worse**", f"component over {t['component_hard']}: {f['path']} ({c})"))
            elif c > oc:
                details.append(("**worse**", f"component over {t['component_hard']} and grew: {f['path']} {oc} -> {c}"))
        folder = os.path.dirname(f["path"]) or "."
        if old is None and d["folders"].get(folder, 0) >= t["folder_limit"]:
            details.append(("**worse**", f"new file in a folder with {d['folders'][folder]} files: {f['path']}"))
    seen = Counter()
    bfun = {}  # (file, name, occurrence) -> lines, for functions already over the hard limit
    for r in base["functions"]:
        k = (r["file"], r["name"])
        seen[k] += 1
        if r["lines"] > t["func_hard"]:
            bfun[(k, seen[k])] = r["lines"]
    seen.clear()
    for r in d["functions"]:
        k = (r["file"], r["name"])
        seen[k] += 1
        old = bfun.get((k, seen[k]))
        if r["lines"] > t["func_hard"] and old is None:
            details.append(("**worse**", f"function over {t['func_hard']}: {r['name']} {r['file']}:{r['line']} ({r['lines']})"))
        elif old is not None and r["lines"] > old:
            details.append(("**worse**", f"function over {t['func_hard']} and grew: {r['name']} "
                            f"{r['file']}:{r['line']} {old} -> {r['lines']}"))
    bnear = {(r["a"], r["b"]) for r in base.get("near_duplicates", [])}
    new_near = [r for r in d["near_duplicates"] if (r["a"], r["b"]) not in bnear]
    mark("Near-duplicate names", len(bnear), len(d["near_duplicates"]), bool(new_near))
    details += [("**worse**", f"new near-duplicate name: {r['a']} ~ {r['b']}") for r in new_near]
    worse |= any(k == "**worse**" for k, _ in details)
    out = ["", "## Compared with the baseline", ""]
    flags = ("excludes", "tests_counted", "skipped_data_folders")
    if any(bs.get(k) != ns.get(k) for k in flags[:2]) or set(bs.get(flags[2], {})) != set(ns.get(flags[2], {})) \
            or base.get("thresholds") != t:
        out += ["Note: the baseline was taken with other flags, thresholds or data folders; "
                "rerun both with the same flags before reading the delta.", ""]
    out += table(["Check", "Baseline", "Now", "Status"], rows)
    if details:
        out += [""] + [f"- {k}: {v}" for k, v in details]
    out.append("\nResult: " + ("worse on at least one metric." if worse else "no metric got worse."))
    return "\n".join(out) + "\n", worse


def main(argv=None):
    ap =argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
                                 usage=argparse.SUPPRESS)
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--md")
    ap.add_argument("--json")
    ap.add_argument("--compare")
    ap.add_argument("--fail-on-worse", action="store_true")
    ap.add_argument("--dupes", type=int, nargs="?", const=20)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--exclude", action="append", metavar="GLOB")
    ap.add_argument("--include-data", action="store_true")
    ap.add_argument("--include-tests", action="store_true")
    for flag, val in [("file-limit", 300), ("file-hard", 800), ("func-limit", 50), ("func-hard", 100),
                      ("nesting", 3), ("folder-limit", 20), ("component-limit", 200),
                      ("component-hard", 600), ("methods", 40), ("new-file-hard", 500)]:
        ap.add_argument("--" + flag, type=int, default=val)
    args = ap.parse_args(argv)
    if not os.path.isdir(args.path):
        ap.error(f"not a directory: {args.path}")
    data = build(args.path, args)
    md, worse = render(data, args.top), False
    if args.compare:
        with open(args.compare, encoding="utf-8") as f:
            delta, worse = compare(json.load(f), data)
        md += delta
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1)
    if args.md:
        with open(args.md, "w", encoding="utf-8") as f:
            f.write(md)
    else:
        sys.stdout.write(md)
    return 1 if (worse and args.fail_on_worse) else 0


if __name__ == "__main__":
    sys.exit(main())
