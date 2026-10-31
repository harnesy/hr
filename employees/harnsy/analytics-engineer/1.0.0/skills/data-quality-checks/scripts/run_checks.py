#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Run read-only data checks from a .sql file against a SQLite database.

Each check starts with a header line `-- check: <name>` and is one SELECT or WITH
query that returns the rows breaking a rule. Zero rows = pass.

  run_checks.py --db snapshot.sqlite checks.sql [--json] [--limit 5]

Exit codes: 0 all passed, 1 some failed, 2 error (bad file, refused check, database error).
The database is opened read-only; any check that is not a single SELECT/WITH query is refused.
Standard library only; no network. SQLite only: for other databases export a snapshot,
or run the same queries with a read-only user through your own client.
"""
import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

FORBIDDEN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|DETACH|PRAGMA|REPLACE|VACUUM|REINDEX|ANALYZE|BEGIN|COMMIT|ROLLBACK|SAVEPOINT|RELEASE)\b",
    re.I,
)


def strip_sql(text):
    """Remove comments and string literals, for the safety check only."""
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    text = re.sub(r"--[^\n]*", " ", text)
    text = re.sub(r"'(?:[^']|'')*'", "''", text)
    text = re.sub(r'"(?:[^"]|"")*"', '""', text)
    return text


def parse_checks(text):
    checks, name, buf = [], None, []
    for line in text.splitlines():
        m = re.match(r"\s*--\s*check:\s*(.+?)\s*$", line)
        if m:
            if name is not None:
                checks.append((name, "\n".join(buf).strip()))
            name, buf = m.group(1), []
        elif name is not None:
            buf.append(line)
    if name is not None:
        checks.append((name, "\n".join(buf).strip()))
    return checks


def refuse_reason(sql):
    bare = strip_sql(sql).strip()
    if bare.endswith(";"):
        bare = bare[:-1].rstrip()
    if not bare:
        return "empty check"
    if ";" in bare:
        return "more than one statement"
    if not re.match(r"(SELECT|WITH)\b", bare, re.I):
        return "not a SELECT or WITH query"
    m = FORBIDDEN.search(bare)
    if m:
        return f"forbidden keyword {m.group(1).upper()}"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", required=True, help="SQLite database file (opened read-only)")
    ap.add_argument("checks", help=".sql file with `-- check: <name>` sections")
    ap.add_argument("--json", action="store_true", help="print results as JSON")
    ap.add_argument("--limit", type=int, default=5, help="failing rows to show per check (default 5)")
    a = ap.parse_args()

    try:
        checks = parse_checks(Path(a.checks).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if not checks:
        print("error: no `-- check: <name>` sections found", file=sys.stderr)
        return 2
    for name, sql in checks:
        why = refuse_reason(sql)
        if why:
            print(f"error: check «{name}» refused: {why}", file=sys.stderr)
            return 2

    db = Path(a.db)
    if not db.is_file():
        print(f"error: no database file {db}", file=sys.stderr)
        return 2
    try:
        con = sqlite3.connect(f"{db.resolve().as_uri()}?mode=ro", uri=True)
        con.execute("PRAGMA query_only = ON")
    except sqlite3.Error as e:
        print(f"error: cannot open {db} read-only: {e}", file=sys.stderr)
        return 2

    results, failed = [], 0
    for name, sql in checks:
        try:
            cur = con.execute(sql.rstrip().rstrip(";"))
            cols = [d[0] for d in cur.description or []]
            rows = cur.fetchall()
        except sqlite3.Error as e:
            print(f"error: check «{name}»: {e}", file=sys.stderr)
            return 2
        ok = not rows
        failed += not ok
        results.append({"check": name, "status": "PASS" if ok else "FAIL", "failing_rows": len(rows),
                         "columns": cols, "examples": [list(r) for r in rows[: a.limit]]})
    con.close()

    if a.json:
        print(json.dumps({"database": str(db), "checks": results, "failed": failed}, indent=2, default=str))
    else:
        for r in results:
            print(f"{r['status']}  {r['check']}  ({r['failing_rows']} failing rows)")
            if r["examples"]:
                print("      " + " | ".join(r["columns"]))
                for row in r["examples"]:
                    print("      " + " | ".join(str(v) for v in row))
        print(f"{len(results) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
