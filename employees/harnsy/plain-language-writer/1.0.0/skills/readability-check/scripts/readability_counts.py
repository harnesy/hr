#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Count the usual suspects in an English text: counts, not a verdict.

  readability_counts.py rewrite.md [--max-sentence 25] [--max-par-sentences 5] [--max-par-words 150]

Reads a plain-text or Markdown file. Paragraphs are separated by blank lines; each list
item counts as its own paragraph; headings and code blocks are skipped. Reports:

  - sentences longer than --max-sentence words (default 25);
  - paragraphs with more than --max-par-sentences sentences (default 5) or more than
    --max-par-words words (default 150; over 250 is marked as well);
  - likely passives: a form of «to be», maybe one adverb, then a past participle
    (a word ending in -ed or -en, or a common irregular one); some are false alarms;
  - hidden verbs: nouns ending in -tion, -sion, -ment or -ance, and «make/give/take
    (a/an/the) <such noun>»; many are fine, each is a suspect only;
  - negative contractions (don't, can't, won't …);
  - long words (three syllables or more, by a rough count) and their share of all words.

Every flag is a place to look at, not a fault. The script never says that a text is
plain, clear or meets any standard, and it computes no grade or named formula score.
Standard library only; no network.
"""
import argparse
import re
import sys

BE = r"(?:am|is|are|was|were|be|been|being|'s|'re)"
IRREGULAR = ("born built bought brought caught chosen done drawn driven eaten fallen felt found forgotten given gone "
             "grown held hidden hit hung kept known laid led left lent lost made meant met paid put read run said seen "
             "sent set shown shut sold sought spent split spoken spread stolen struck sung taken taught told thought "
             "thrown understood upheld withdrawn won worn written").split()
PARTICIPLE = r"(?:\w+ed|\w+en|" + "|".join(IRREGULAR) + r")"
PASSIVE = re.compile(r"\b" + BE + r"\s+(?:\w+ly\s+)?(" + PARTICIPLE + r")\b", re.I)
NOT_PARTICIPLE = {"need", "seed", "feed", "speed", "bleed", "breed", "indeed", "even", "often", "open", "ten", "seven",
                  "eleven", "listen", "kitchen", "garden", "children", "women", "men", "token", "citizen", "dozen",
                  "heaven", "golden", "sudden", "chicken", "oxygen", "eleven", "happen", "when", "then", "than"}
HIDDEN = re.compile(r"\b\w{3,}(?:tion|sion|ment|ance)s?\b", re.I)
LIGHT_VERB = re.compile(r"\b(?:make|makes|made|making|give|gives|gave|given|giving|take|takes|took|taken|taking|"
                        r"carry out|carries out|carried out|conduct|conducts|conducted)\s+(?:a|an|the)?\s*"
                        r"(\w+(?:tion|sion|ment|ance))\b", re.I)
NEG = re.compile(r"\b(?:\w+n't|can't|won't|shan't)\b", re.I)
ABBREV = re.compile(r"\b(?:e\.g|i\.e|etc|vs|mr|mrs|ms|dr|no|fig|approx|art|para|sec)\.", re.I)
WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")


def syllables(w):
    w = w.lower().strip("'’-")
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:es|ed)$", "", w) if not re.search(r"(?:ted|ded)$", w) else w
    w = re.sub(r"e$", "", w)
    groups = re.findall(r"[aeiouy]+", w)
    return max(1, len(groups))


def paragraphs(text):
    out, buf, in_code = [], [], False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not s:
            if buf:
                out.append(" ".join(buf))
                buf = []
            continue
        if s.startswith("#") or set(s) <= set("-=|: "):
            if buf:
                out.append(" ".join(buf))
                buf = []
            continue
        if re.match(r"^(?:[-*+]|\d+[.)])\s+", s):
            if buf:
                out.append(" ".join(buf))
                buf = []
            s = re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", s)
        buf.append(s)
    if buf:
        out.append(" ".join(buf))
    return out


def sentences(par):
    masked = ABBREV.sub(lambda m: m.group(0).replace(".", "\u0000"), par)
    parts = re.split(r"(?<=[.!?])[\"'»”)]?\s+(?=[\"'«“(]?[A-Z0-9])", masked)
    return [p.replace("\u0000", ".").strip() for p in parts if p.strip()]


def short(s, n=90):
    return s if len(s) <= n else s[: n - 1] + "…"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--max-sentence", type=int, default=25)
    ap.add_argument("--max-par-sentences", type=int, default=5)
    ap.add_argument("--max-par-words", type=int, default=150)
    a = ap.parse_args()
    try:
        text = open(a.file, encoding="utf-8").read()
    except OSError as e:
        sys.exit(f"readability_counts: {e}")

    pars = paragraphs(text)
    long_s, long_p, passives, hidden, neg = [], [], [], [], []
    n_sent = n_words = n_long = 0
    for pi, p in enumerate(pars, 1):
        ss = sentences(p)
        pw = len(WORD.findall(p))
        if len(ss) > a.max_par_sentences or pw > a.max_par_words:
            long_p.append((pi, len(ss), pw))
        for si, s in enumerate(ss, 1):
            words = WORD.findall(s)
            n_sent += 1
            n_words += len(words)
            n_long += sum(1 for w in words if syllables(w) >= 3)
            where = f"{pi}.{si}"
            if len(words) > a.max_sentence:
                long_s.append((where, len(words), s))
            for m in PASSIVE.finditer(s):
                if m.group(1).lower() not in NOT_PARTICIPLE:
                    passives.append((where, m.group(0), s))
            seen = set()
            for m in LIGHT_VERB.finditer(s):
                hidden.append((where, m.group(0), s))
                seen.add(m.group(1).lower())
            for m in HIDDEN.finditer(s):
                if m.group(0).lower() not in seen:
                    hidden.append((where, m.group(0), s))
            for m in NEG.finditer(s.replace("’", "'")):
                neg.append((where, m.group(0), s))

    print(f"# Readability counts: {a.file}")
    print()
    print("Counts, not a verdict. Each flag is a place to look at; read it and decide. People, not counts, show whether a text is understood.")
    print()
    print("| measure | count |")
    print("|---|---|")
    print(f"| paragraphs | {len(pars)} |")
    print(f"| sentences | {n_sent} |")
    print(f"| words | {n_words} |")
    print(f"| average words per sentence | {n_words / n_sent:.1f} |" if n_sent else "| average words per sentence | - |")
    print(f"| sentences over {a.max_sentence} words | {len(long_s)} |")
    print(f"| paragraphs over {a.max_par_sentences} sentences or {a.max_par_words} words | {len(long_p)} |")
    print(f"| likely passives | {len(passives)} |")
    print(f"| hidden-verb suspects | {len(hidden)} |")
    print(f"| negative contractions | {len(neg)} |")
    print(f"| long words (3+ syllables, rough) | {n_long} ({(100 * n_long / n_words) if n_words else 0:.0f}% of words) |")
    print()
    print("Places are paragraph.sentence, counting paragraphs and list items from the top; headings and code are skipped.")

    def section(title, rows, fmt):
        print()
        print(f"## {title} ({len(rows)})")
        print()
        if not rows:
            print("None found.")
        for r in rows:
            print(fmt(r))

    section(f"Sentences over {a.max_sentence} words", long_s, lambda r: f"- {r[0]}: {r[1]} words — {short(r[2])}")
    section("Long paragraphs", long_p,
            lambda r: f"- paragraph {r[0]}: {r[1]} sentences, {r[2]} words" + (" (over 250 words)" if r[2] > 250 else ""))
    section("Likely passives (name the actor where it matters; keep it where the actor is unknown or unimportant)", passives,
            lambda r: f"- {r[0]}: «{r[1]}» — {short(r[2])}")
    section("Hidden-verb suspects (could a verb say it shorter?)", hidden, lambda r: f"- {r[0]}: «{r[1]}» — {short(r[2])}")
    section("Negative contractions (spell them out where a misread would matter)", neg, lambda r: f"- {r[0]}: «{r[1]}»")


if __name__ == "__main__":
    main()
