#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Randomised property check of a Python function against a slow reference.

  prop_check.py --target algo.py:dedupe --reference ref.py:dedupe_ref --gen list[int]
  prop_check.py --target algo.py:sort_items --property props.py:is_sorted_permutation --gen list[int]

Each run makes one input with the generator, calls the target on a copy and
  - with --reference: compares the result with the reference's result (==);
  - with --property: calls property(input, result), which must return True.
Both may be given. Every run also checks that the target did not change its input.

Generators: int, list[int], str, list[str]. The first runs are edge values (0, 1, -1,
the bounds, empty and one-item lists, duplicates, sorted and reversed lists); the rest
are random from --seed (default: a fresh seed, always printed so the run can be replayed).
--pre file.py:func skips inputs for which func returns False; skipped inputs do not count
toward --runs, and the run stops if more than 10 times --runs are skipped.

On a failure the input is shrunk (items removed, values moved toward 0, characters
removed) to a small counter-example, printed with the seed. --pins file.json replays
saved counter-examples first; --save adds the new one to that file.

The target, reference and property files are imported and run as Python code: use only
code you have read. Standard library only; no network. Exit 0: all runs passed; 1: a
counter-example was found; 2: bad arguments.
"""
import argparse
import copy
import importlib.util
import json
import os
import random
import sys


def load(spec):
    path, _, name = spec.rpartition(":")
    if not path or not name:
        sys.exit(f"prop_check: want file.py:function, got «{spec}»")
    s = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(path))[0], path)
    if s is None:
        sys.exit(f"prop_check: cannot load {path}")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    if not hasattr(m, name):
        sys.exit(f"prop_check: {path} has no function {name}")
    return getattr(m, name)


class Gen:
    def __init__(self, kind, lo, hi, max_len, rng):
        if kind not in ("int", "list[int]", "str", "list[str]"):
            sys.exit(f"prop_check: generator «{kind}»: use int, list[int], str or list[str]")
        self.kind, self.lo, self.hi, self.max_len, self.rng = kind, lo, hi, max_len, rng

    def one_int(self):
        return self.rng.randint(self.lo, self.hi)

    def one_str(self):
        return "".join(self.rng.choice("ab cAé") for _ in range(self.rng.randint(0, 6)))

    def edges(self):
        ints = sorted({0, 1, -1, self.lo, self.hi} & set(range(self.lo, self.hi + 1)))
        if self.kind == "int":
            return [[i] for i in ints]
        if self.kind == "str":
            return [[s] for s in ["", "a", "aa", " ", "é", "A a"]]
        item = ints if self.kind == "list[int]" else ["", "a", "b", "a"]
        out = [[], [item[0]], [item[-1], item[-1]], sorted(item), sorted(item, reverse=True), item + item]
        return [[x] for x in out]

    def random(self):
        if self.kind == "int":
            return [self.one_int()]
        if self.kind == "str":
            return [self.one_str()]
        n = self.rng.randint(0, self.max_len)
        f = self.one_int if self.kind == "list[int]" else self.one_str
        xs = [f() for _ in range(n)]
        if n > 1 and self.rng.random() < 0.3:  # bias toward duplicates
            xs[self.rng.randrange(n)] = xs[self.rng.randrange(n)]
        return [xs]


def shrink_candidates(x):
    if isinstance(x, list):
        for i in range(len(x)):
            yield x[:i] + x[i + 1:]
        for i, v in enumerate(x):
            for w in shrink_candidates(v):
                yield x[:i] + [w] + x[i + 1:]
    elif isinstance(x, int):
        if x != 0:
            yield 0
            yield x // 2 if x > 0 else -((-x) // 2)
            yield x - 1 if x > 0 else x + 1
    elif isinstance(x, str):
        for i in range(len(x)):
            yield x[:i] + x[i + 1:]


def check(args, target, reference, prop):
    """Return None when the input passes, else a short reason."""
    before = copy.deepcopy(args)
    try:
        work = copy.deepcopy(args)
        got = target(*work)
    except Exception as e:  # a crash is a failure too
        return f"target raised {type(e).__name__}: {e}"
    if work != before:
        return "target changed its input"
    if reference is not None:
        try:
            want = reference(*copy.deepcopy(args))
        except Exception as e:
            return f"reference raised {type(e).__name__}: {e} (fix the reference first)"
        if got != want:
            return f"target returned {got!r}, reference returned {want!r}"
    if prop is not None:
        try:
            ok = prop(copy.deepcopy(args[0]) if len(args) == 1 else copy.deepcopy(args), got)
        except Exception as e:
            return f"property raised {type(e).__name__}: {e}"
        if ok is not True:
            return f"property returned {ok!r} for result {got!r}"
    return None


def shrink_args(args):
    """Smaller versions of one argument at a time; the argument list itself keeps its length."""
    for i, v in enumerate(args):
        for w in shrink_candidates(v):
            yield args[:i] + [w] + args[i + 1:]


def shrink(args, why, ok_fn, pre):
    steps = 0
    changed = True
    while changed and steps < 2000:
        changed = False
        for cand in shrink_args(args):
            steps += 1
            if pre and not pre(*copy.deepcopy(cand)):
                continue
            r = ok_fn(cand)
            if r is not None:
                args, why, changed = cand, r, True
                break
    return args, why, steps


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", required=True, help="file.py:function under test")
    ap.add_argument("--reference", help="file.py:function, a slow, obviously correct version")
    ap.add_argument("--property", help="file.py:function(input, result) -> True when the property holds")
    ap.add_argument("--pre", help="file.py:function(input) -> True for valid inputs (precondition)")
    ap.add_argument("--gen", default="list[int]", help="int, list[int], str or list[str] (default list[int])")
    ap.add_argument("--runs", type=int, default=100, help="random runs after the edge values (default 100)")
    ap.add_argument("--seed", type=int, help="seed for a repeatable run (default: a fresh one, printed)")
    ap.add_argument("--min", type=int, default=-10)
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--max-len", type=int, default=12)
    ap.add_argument("--pins", help="JSON file with saved counter-examples, replayed first")
    ap.add_argument("--save", action="store_true", help="add a new counter-example to --pins")
    a = ap.parse_args()
    if not a.reference and not a.property:
        ap.error("give --reference, --property or both")
    if a.min > a.max or a.runs < 1:
        ap.error("--min must not exceed --max, and --runs must be at least 1")

    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1, 10**6)
    rng = random.Random(seed)
    target = load(a.target)
    reference = load(a.reference) if a.reference else None
    prop = load(a.property) if a.property else None
    pre = load(a.pre) if a.pre else None
    gen = Gen(a.gen, a.min, a.max, a.max_len, rng)
    ok_fn = lambda args: check(args, target, reference, prop)

    pins = []
    if a.pins and os.path.exists(a.pins):
        with open(a.pins, encoding="utf-8") as f:
            pins = json.load(f)
    print(f"# Property check: {a.target}")
    print(f"seed {seed} · generator {a.gen} · runs {a.runs} · pinned examples {len(pins)}"
          + (f" · reference {a.reference}" if a.reference else "") + (f" · property {a.property}" if a.property else ""))

    def report(kind, args, why):
        small, why2, steps = shrink(args, why, ok_fn, pre)
        print()
        print(f"FAIL ({kind}): {why}")
        print(f"  input:   {json.dumps(args[0] if len(args) == 1 else args, ensure_ascii=False)}")
        print(f"  shrunk:  {json.dumps(small[0] if len(small) == 1 else small, ensure_ascii=False)}  ({steps} shrink steps)")
        print(f"  reason:  {why2}")
        print(f"  replay:  --seed {seed}")
        if a.save and a.pins:
            item = small[0] if len(small) == 1 else small
            if item not in pins:
                pins.append(item)
                with open(a.pins, "w", encoding="utf-8") as f:
                    json.dump(pins, f, ensure_ascii=False, indent=1)
                print(f"  pinned:  added to {a.pins}; make it an example test too")
        sys.exit(1)

    for p in pins:
        args = [p]
        why = ok_fn(args)
        if why:
            report("pinned example", args, why)
    passed, skipped = 0, 0
    for args in gen.edges():
        if pre and not pre(*copy.deepcopy(args)):
            skipped += 1
            continue
        why = ok_fn(args)
        if why:
            report("edge value", args, why)
        passed += 1
    edge = passed
    random_passed = 0
    while random_passed < a.runs:
        args = gen.random()
        if pre and not pre(*copy.deepcopy(args)):
            skipped += 1
            if skipped > 10 * a.runs:
                print(f"\nSTOPPED: {skipped} inputs rejected by the precondition; widen the generator or loosen --pre.")
                sys.exit(1)
            continue
        why = ok_fn(args)
        if why:
            report(f"random run {random_passed + 1}", args, why)
        random_passed += 1
    print()
    print(f"PASS: {len(pins)} pinned, {edge} edge and {random_passed} random inputs; {skipped} rejected by the precondition. "
          "Passing runs are evidence, not proof.")


if __name__ == "__main__":
    main()
