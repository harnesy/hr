#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Check the shape of commit messages: counts and flags, not a verdict.

  commit_msg_check.py MESSAGE_FILE [MESSAGE_FILE ...] [--changed-lines N] [options]
  commit_msg_check.py --log LOG_FILE|- [options]

Input, one of:
  - one or more files, each holding one commit message (lines starting with «#» are
    ignored, as in a message being edited); --changed-lines gives the size of the change;
  - --log: records separated by a NUL byte, each starting with the commit id on its own
    line, then the message; a line such as « 3 files changed, 40 insertions(+), 2
    deletions(-)» after a record is read as that commit's size. This is what
      git log -z --format='%H%n%B' --shortstat <range>
    prints. Use «-» to read from standard input.

Checks per message (each threshold is a default you can change):
  no-summary         the first line is empty
  summary-long       summary longer than --soft (50): a warning
  summary-too-long   summary longer than --hard (72)
  summary-full-stop  the summary ends with a full stop
  not-imperative     likely not an instruction: the first word (after an optional
                     «type(scope):» prefix) ends in -ed, -ing or a plain -s; a heuristic,
                     reported as «likely»
  no-blank-line      the second line is not empty
  no-body            no body although the change has more than --body-after (20) lines
  no-reason          a body without a word that gives a reason (because, so that,
                     otherwise, to avoid …) and without an issue or link reference; a heuristic
  line-long          body lines wider than --wrap (72); links, indented and quoted lines skipped
  trailer-shape      a line in the closing footer block that is not «Token: value» or
                     «Token #value», or a token with a space instead of «-»
  breaking-undeclared  the message says something is incompatible, no longer works, or that a
                     public option, function or field was removed or renamed,
                     but neither the summary has «!» before the colon nor a footer
                     declares the breaking change; a heuristic
  prefix             with --prefix only: the summary does not start with «type(scope): »
                     or «type: » (types from --types if given)

Output: one line per message with its id (or file name) and its flags, then a count per
flag. Exit code 0 (1 with --strict when any flag other than summary-long is raised; 2 on
bad input). No network, standard library only.
"""
import argparse
import re
import sys

REASON = re.compile(
    r"\b(because|since|so that|so the|so it|otherwise|to avoid|to prevent|to allow|to let|to keep|to fix|"
    r"in order to|which caused|caused by|this means|without this|instead of|the reason|why|fixes|closes|refs)\b"
    r"|#\d+|\b[A-Z][A-Z0-9]+-\d+\b|https?://", re.I)
BREAKING_WORDS = re.compile(r"\b(incompatible|no longer|drops? support|breaks|breaking|(removed?|removes|renamed?|renames) (the )?(public|api|option|flag|endpoint|parameter|argument|field|command|setting|function|method)s?)\b", re.I)
TRAILER = re.compile(r"^([A-Za-z][A-Za-z0-9-]*|BREAKING CHANGE)(: | #)\S")
TRAILER_LOOSE = re.compile(r"^[A-Za-z][A-Za-z0-9 -]{0,40}(: | #)\S")
PREFIX = re.compile(r"^([a-z][a-z0-9-]*)(\([^()\s][^()]*\))?(!)?: \S")
SHORTSTAT = re.compile(r"^\s*\d+ files? changed(, (\d+) insertions?\(\+\))?(, (\d+) deletions?\(-\))?\s*$")
ID = re.compile(r"^[0-9a-f]{7,64}$")
# first words that end in -s but are usually instructions or nouns, not a third-person verb
S_OK = {"process", "address", "access", "pass", "bypass", "focus", "redis", "status", "alias", "canvas", "atlas", "gis", "dns", "css",
        "https", "ios", "macos", "news", "this", "its", "always", "has", "is", "was", "does", "less", "unless", "across"}
# first words ending in -ed or -ing that are instructions or common nouns
ED_OK = {"embed", "feed", "need", "seed", "shed", "speed", "proceed", "succeed", "exceed", "bed", "red", "shred", "bleed", "breed"}
ING_OK = {"bring", "ring", "sing", "string", "spring", "swing", "ping", "king", "thing", "wing", "sting", "cling", "fling", "logging",
          "routing", "tracing", "caching", "billing", "pricing", "packaging", "testing", "linting", "tooling", "styling", "naming",
          "wording", "spacing", "padding", "rounding", "scaling", "loading", "onboarding", "parsing", "formatting", "tracking"}


def parse_args(argv):
    p = argparse.ArgumentParser(description="Check the shape of commit messages: counts and flags, not a verdict.")
    p.add_argument("files", nargs="*", help="message files, one message each")
    p.add_argument("--log", help="NUL-separated log (id line, message, optional size line); «-» for standard input")
    p.add_argument("--changed-lines", type=int, default=None, help="size of the change for a message file (lines added + removed)")
    p.add_argument("--soft", type=int, default=50, help="summary length that raises a warning (default 50)")
    p.add_argument("--hard", type=int, default=72, help="summary length that raises a flag (default 72)")
    p.add_argument("--wrap", type=int, default=72, help="widest body line (default 72)")
    p.add_argument("--body-after", type=int, default=20, help="changes larger than this many lines need a body (default 20)")
    p.add_argument("--prefix", action="store_true", help="the project uses a «type(scope): » prefix; check it")
    p.add_argument("--types", default="", help="comma-separated allowed prefix types, e.g. feat,fix,docs (only with --prefix)")
    p.add_argument("--strict", action="store_true", help="exit 1 when any flag other than summary-long is raised")
    return p.parse_args(argv)


def read_text(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def records_from_log(text):
    """Split «git log -z --format='%H%n%B' --shortstat» style output into (id, message, size or None)."""
    out = []
    for chunk in text.split("\0"):
        lines = chunk.split("\n")
        # a size line at the start of a chunk belongs to the previous record
        while lines and (not lines[0].strip() or SHORTSTAT.match(lines[0])):
            m = SHORTSTAT.match(lines[0])
            if m and out:
                ins, dels = int(m.group(2) or 0), int(m.group(4) or 0)
                cid, msg, _ = out[-1]
                out[-1] = (cid, msg, ins + dels)
            lines.pop(0)
        if not lines:
            continue
        cid = lines[0].strip()
        if not ID.match(cid):
            raise ValueError(f"record does not start with a commit id: {cid[:40]!r}")
        out.append((cid[:12], "\n".join(lines[1:]), None))
    return out


def clean(message, comments=False):
    """Lines of a message without trailing space and trailing empty lines; with comments=True, «#» lines are dropped."""
    lines = [l.rstrip() for l in message.replace("\r\n", "\n").split("\n") if not (comments and l.startswith("#"))]
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def first_word(summary, use_prefix):
    s = summary
    m = PREFIX.match(s)
    if m:
        s = s[m.end() - 1:]
    elif use_prefix is False:
        m2 = re.match(r"^[A-Za-z0-9_./-]+: ", s)  # an area label such as «docs: » or «api/client: »
        if m2:
            s = s[m2.end():]
    w = re.match(r"\s*([A-Za-z][A-Za-z'-]*)", s)
    return w.group(1) if w else ""


def likely_not_imperative(word):
    w = word.lower()
    if not w:
        return False
    if w.endswith("ed") and w not in ED_OK and len(w) > 3:
        return True
    if w.endswith("ing") and w not in ING_OK and len(w) > 4:
        return True
    if w.endswith("s") and not w.endswith(("ss", "us", "is")) and w not in S_OK and len(w) > 3:
        return True
    return False


def footer_block(body_lines):
    """The last paragraph of the body, if it looks like a footer block (its first line has a token shape)."""
    paras, cur = [], []
    for l in body_lines:
        if l.strip():
            cur.append(l)
        elif cur:
            paras.append(cur)
            cur = []
    if cur:
        paras.append(cur)
    if not paras:
        return [], body_lines
    last = paras[-1]
    if TRAILER_LOOSE.match(last[0]) and not last[0].startswith(("http://", "https://")):
        # the footer lines are not prose; everything before them is the body text
        n = len(body_lines)
        idx = max(i for i in range(n) if body_lines[i] == last[0])
        return last, body_lines[:idx]
    return [], body_lines


def check(message, size, a, types, comments=False):
    flags = []
    lines = clean(message, comments)
    if not lines or not lines[0].strip():
        return [("no-summary", "the first line is empty")]
    summary = lines[0].strip()
    n = len(summary)
    if n > a.hard:
        flags.append(("summary-too-long", f"{n} > {a.hard} characters"))
    elif n > a.soft:
        flags.append(("summary-long", f"{n} > {a.soft} characters (warning)"))
    if summary.endswith(".") and not summary.endswith("..."):
        flags.append(("summary-full-stop", "remove the full stop at the end of the summary"))
    word = first_word(summary, a.prefix if a.prefix else False)
    if likely_not_imperative(word):
        flags.append(("not-imperative", f"«{word}» is likely not an instruction; write it as one, e.g. «Add …», «Fix …»"))
    if a.prefix:
        m = PREFIX.match(summary)
        if not m:
            flags.append(("prefix", "summary does not start with «type(scope): » or «type: »"))
        elif types and m.group(1) not in types:
            flags.append(("prefix", f"type «{m.group(1)}» is not one of {', '.join(sorted(types))}"))
    rest = lines[1:]
    if rest and rest[0].strip():
        flags.append(("no-blank-line", "leave the second line empty"))
    body_all = [l for l in rest]
    while body_all and not body_all[0].strip():
        body_all.pop(0)
    footer, body = footer_block(body_all)
    text = "\n".join(body).strip()
    if not text:
        if size is not None and size > a.body_after:
            flags.append(("no-body", f"no body for a change of {size} lines (more than {a.body_after}); say why the change is needed"))
    elif not REASON.search(text + "\n" + "\n".join(footer)):
        flags.append(("no-reason", "the body says what changed but no reason was found (heuristic): add why"))
    for i, l in enumerate(body, start=3):
        if len(l) > a.wrap and not re.search(r"https?://\S{20,}", l) and not l.startswith(("    ", "\t", ">")):
            flags.append(("line-long", f"body line {i - 2}: {len(l)} > {a.wrap} characters"))
    for l in footer:
        if l.startswith((" ", "\t")):
            continue  # a continuation of the previous footer value
        if not TRAILER.match(l):
            if TRAILER_LOOSE.match(l):
                flags.append(("trailer-shape", f"«{l[:40]}»: use «-» instead of spaces in the token"))
            else:
                flags.append(("trailer-shape", f"«{l[:40]}» is not «Token: value» or «Token #value»"))
    declared = bool(re.match(r"^[a-z][a-z0-9-]*(\([^()]*\))?!: ", summary)) or any(
        re.match(r"^BREAKING[ -]CHANGE: ", l) for l in footer)
    if not declared and BREAKING_WORDS.search(summary + "\n" + text):
        flags.append(("breaking-undeclared", "the message mentions a removal, rename or incompatibility; if existing users are "
                                             "affected, declare it (a «!» before the colon or a breaking-change footer)"))
    return flags


def main(argv):
    a = parse_args(argv)
    types = {t.strip() for t in a.types.split(",") if t.strip()}
    comments = False
    try:
        if a.log:
            recs = records_from_log(read_text(a.log))
        elif a.files:
            recs = [(f, read_text(f), a.changed_lines) for f in a.files]
            comments = True
        else:
            print("give message files or --log (see --help)", file=sys.stderr)
            return 2
    except (OSError, ValueError) as e:
        print(f"cannot read input: {e}", file=sys.stderr)
        return 2
    if not recs:
        print("no messages found", file=sys.stderr)
        return 2
    print(f"# Commit message check: {len(recs)} message(s). Counts and flags, not a verdict.")
    print(f"# Limits: summary warning > {a.soft}, flag > {a.hard}; body lines > {a.wrap}; body needed above {a.body_after} changed lines; "
          f"prefix check {'on' if a.prefix else 'off'}.")
    counts, strict_hit = {}, False
    for cid, msg, size in recs:
        fl = check(msg, size, a, types, comments)
        summary = (clean(msg, comments) or [""])[0][:60]
        size_s = f" [{size} lines]" if size is not None else ""
        if not fl:
            print(f"{cid}{size_s}: ok | {summary}")
        else:
            print(f"{cid}{size_s}: {' '.join(sorted({f for f, _ in fl}))} | {summary}")
            for f, why in fl:
                print(f"    {f}: {why}")
        for f, _ in fl:
            counts[f] = counts.get(f, 0) + 1
            if f != "summary-long":
                strict_hit = True
    print("\n# Count per flag")
    if not counts:
        print("none")
    for f in sorted(counts):
        print(f"{f}: {counts[f]}")
    return 1 if (a.strict and strict_hit) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
