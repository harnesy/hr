#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pavel Buchnev (harnsy)
"""Detect a project's toolchain and run its own format, lint and test commands.

  run_checks.py <project-dir>                 show what was found and what would run
  run_checks.py <project-dir> --run           run the commands, report exit codes
  run_checks.py <project-dir> --run --only test
  run_checks.py <project-dir> --json          machine-readable plan

Looks at files in the project root: package.json (and angular.json), pubspec.yaml,
Package.swift, *.xcodeproj / *.xcworkspace, build.gradle(.kts) / gradlew, Gemfile,
Rakefile, CMakeLists.txt, Makefile.

It never installs, updates or downloads anything and makes no network calls itself.
If dependencies look missing (no node_modules, bundle not installed, Dart packages not
resolved, Gradle distribution not cached, CMake build directory not configured), it
stops and says what is missing; installing is the person's decision.
The commands it runs are the project's own scripts and tools: read them before --run.

Exit codes: 0 all commands passed (or plan shown), 1 a command failed,
2 cannot run (nothing detected, missing dependencies, missing tools, bad arguments).
Standard library only.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CATEGORIES = ("format", "lint", "test")


class Plan:
    def __init__(self):
        self.toolchains = []   # (name, evidence)
        self.commands = []     # dicts: category, toolchain, argv, note
        self.blockers = []     # strings: why nothing can run
        self.notes = []        # strings: hints that do not block
        self.will_run = False  # set when --run is given

    def add(self, category, toolchain, argv, note=""):
        self.commands.append({"category": category, "toolchain": toolchain,
                              "argv": list(argv), "note": note})


def read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def have(tool):
    return shutil.which(tool) is not None


# --- JavaScript / TypeScript (incl. Angular, React Native) -----------------

FORMAT_SCRIPTS = ("format:check", "fmt:check", "check-format", "check:format",
                  "prettier:check", "lint:format", "format-check")
LINT_SCRIPTS = ("lint", "lint:check", "eslint", "typecheck", "type-check", "tsc")
TEST_SCRIPTS = ("test", "test:unit", "test:ci", "unit")


def detect_node(root, plan):
    pkg_file = root / "package.json"
    if not pkg_file.is_file():
        return
    try:
        pkg = json.loads(read_text(pkg_file) or "{}")
    except ValueError as exc:
        plan.blockers.append(f"package.json is not valid JSON: {exc}")
        return
    scripts = pkg.get("scripts") or {}
    deps = {**(pkg.get("dependencies") or {}), **(pkg.get("devDependencies") or {})}
    if (root / "pnpm-lock.yaml").is_file():
        pm = "pnpm"
    elif (root / "yarn.lock").is_file():
        pm = "yarn"
    elif (root / "bun.lockb").is_file() or (root / "bun.lock").is_file():
        pm = "bun"
    else:
        pm = "npm"
    flavour = "node"
    evidence = ["package.json"]
    if (root / "angular.json").is_file() or "@angular/core" in deps:
        flavour = "angular"
        evidence.append("angular.json" if (root / "angular.json").is_file() else "@angular/core")
        version = deps.get("@angular/core")
        if version:
            plan.notes.append(f"Angular version in package.json: {version} (check it before advice)")
    elif "react-native" in deps:
        flavour = "react-native"
        evidence.append("react-native dependency")
    plan.toolchains.append((f"{flavour} ({pm})", ", ".join(evidence)))
    if not (root / "node_modules").is_dir():
        plan.blockers.append(f"node_modules is missing: dependencies are not installed "
                             f"(the person runs `{pm} install` if they agree)")
    if not have(pm):
        plan.blockers.append(f"`{pm}` is not on PATH")

    def run_script(name):
        if pm == "npm":
            return ["npm", "run", "--silent", name] if name != "test" else ["npm", "test"]
        return [pm, "run", name] if pm != "yarn" else ["yarn", name]

    found = {c: None for c in CATEGORIES}
    for c, names in (("format", FORMAT_SCRIPTS), ("lint", LINT_SCRIPTS), ("test", TEST_SCRIPTS)):
        for name in names:
            if name in scripts:
                found[c] = name
                break
    for c in CATEGORIES:
        name = found[c]
        if not name:
            plan.notes.append(f"{flavour}: no {c} script in package.json")
            continue
        argv = run_script(name)
        note = f"script \"{name}\": {scripts[name]}"
        if c == "test" and flavour == "angular" and re.match(r"\s*ng\s+test\b", scripts[name]) \
                and "--watch" not in scripts[name]:
            argv += (["--"] if pm in ("npm", "pnpm", "bun") else []) + ["--watch=false"]
            note += " (single run)"
        plan.add(c, flavour, argv, note)


# --- Flutter / Dart --------------------------------------------------------

def detect_dart(root, plan):
    pub = root / "pubspec.yaml"
    if not pub.is_file():
        return
    text = read_text(pub)
    flutter = re.search(r"^\s*flutter\s*:", text, re.M) is not None
    name = "flutter" if flutter else "dart"
    plan.toolchains.append((name, "pubspec.yaml"))
    tool = "flutter" if flutter else "dart"
    if not have(tool):
        plan.blockers.append(f"`{tool}` is not on PATH")
    if not (root / ".dart_tool" / "package_config.json").is_file():
        plan.blockers.append(f"Dart packages are not resolved (.dart_tool/package_config.json "
                             f"missing; the person runs `{tool} pub get` if they agree)")
    plan.add("format", name, ["dart", "format", "--output=none", "--set-exit-if-changed", "."])
    plan.add("lint", name, [tool, "analyze"],
             "rules from analysis_options.yaml" if (root / "analysis_options.yaml").is_file() else "")
    if (root / "test").is_dir():
        plan.add("test", name, [tool, "test"])
    else:
        plan.notes.append(f"{name}: no test/ directory")


# --- Swift / Xcode ---------------------------------------------------------

def detect_swift(root, plan):
    package = root / "Package.swift"
    projects = sorted(p.name for p in root.glob("*.xcworkspace")) + \
        sorted(p.name for p in root.glob("*.xcodeproj"))
    if package.is_file():
        plan.toolchains.append(("swift package", "Package.swift"))
        if not have("swift"):
            plan.blockers.append("`swift` is not on PATH")
        resolved = root / "Package.resolved"
        if resolved.is_file() and '"pins"' in read_text(resolved) \
                and not (root / ".build" / "checkouts").is_dir():
            plan.blockers.append("Swift package dependencies are not fetched (.build/checkouts "
                                 "missing); `swift test` would download them. The person "
                                 "runs `swift package resolve` if they agree")
        if (root / ".swift-format").is_file():
            plan.add("format", "swift", ["swift", "format", "lint", "--recursive", "."])
        if (root / ".swiftlint.yml").is_file():
            if have("swiftlint"):
                plan.add("lint", "swift", ["swiftlint", "lint", "--strict"])
            else:
                plan.notes.append("swift: .swiftlint.yml found but swiftlint is not on PATH")
        plan.add("test", "swift", ["swift", "test"])
    if projects:
        plan.toolchains.append(("xcode", ", ".join(projects)))
        if (root / "Podfile").is_file() and not (root / "Pods").is_dir():
            plan.notes.append("xcode: Podfile found but Pods/ is missing (pods not installed)")
        plan.notes.append("xcode: tests need a scheme and a simulator destination; list them "
                          "with `xcodebuild -list` and run e.g. `xcodebuild test -scheme <scheme> "
                          "-destination 'platform=iOS Simulator,name=<device>'` (not run by this script)")
        if not package.is_file() and (root / ".swiftlint.yml").is_file() and have("swiftlint"):
            plan.add("lint", "xcode", ["swiftlint", "lint", "--strict"])


# --- Gradle (Android, Kotlin, Java) ----------------------------------------

def gradle_dist_cached(root):
    props = root / "gradle" / "wrapper" / "gradle-wrapper.properties"
    text = read_text(props)
    m = re.search(r"distributionUrl\s*=\s*(\S+)", text)
    if not m:
        return None
    name = m.group(1).replace("\\:", ":").rsplit("/", 1)[-1]
    if name.endswith(".zip"):
        name = name[:-4]
    home = Path(os.environ.get("GRADLE_USER_HOME", Path.home() / ".gradle"))
    return (home / "wrapper" / "dists" / name).is_dir()


def detect_gradle(root, plan):
    builds = [p for p in ("build.gradle", "build.gradle.kts", "settings.gradle",
                          "settings.gradle.kts") if (root / p).is_file()]
    if not builds:
        return
    text = "".join(read_text(p) for p in list(root.glob("*.gradle*")) + list(root.glob("*/build.gradle*")))
    android = "com.android" in text or "android {" in text or (root / "app" / "src" / "main" / "AndroidManifest.xml").is_file()
    name = "gradle (android)" if android else "gradle"
    plan.toolchains.append((name, ", ".join(builds)))
    wrapper = root / ("gradlew.bat" if os.name == "nt" else "gradlew")
    if wrapper.is_file():
        gradle = [str(wrapper)]
        cached = gradle_dist_cached(root)
        if cached is False:
            plan.blockers.append("the Gradle distribution named in gradle-wrapper.properties is not "
                                 "in the local Gradle cache; the wrapper would download it")
    elif have("gradle"):
        gradle = ["gradle"]
        plan.notes.append("gradle: no wrapper script; using gradle from PATH (version may differ)")
    else:
        plan.blockers.append("no gradlew wrapper and no gradle on PATH")
        gradle = ["gradle"]
    base = gradle + ["--offline", "--console=plain"]
    if "spotless" in text:
        plan.add("format", name, base + ["spotlessCheck"])
    elif "ktlint" in text:
        plan.add("format", name, base + ["ktlintCheck"])
    if android:
        plan.add("lint", name, base + ["lint"], "Android Lint")
    if "detekt" in text:
        plan.add("lint", name, base + ["detekt"])
    plan.add("test", name, base + ["test"], "local unit tests; instrumented tests "
             "(connectedAndroidTest) need a device or emulator and are not run" if android else "")


# --- Ruby / Rails ----------------------------------------------------------

def detect_ruby(root, plan):
    gemfile = root / "Gemfile"
    if not gemfile.is_file():
        return
    text = read_text(gemfile)
    rails = (root / "bin" / "rails").is_file() or re.search(r"""gem\s+["']rails["']""", text)
    name = "rails" if rails else "ruby"
    plan.toolchains.append((name, "Gemfile" + (", bin/rails" if rails else "")))
    if not have("bundle"):
        plan.blockers.append("`bundle` is not on PATH")
    elif not plan.will_run:
        plan.notes.append(f"{name}: `bundle check` runs only with --run (it reads the Gemfile)")
    else:
        try:
            r = subprocess.run(["bundle", "check"], cwd=root, capture_output=True,
                               text=True, timeout=120)
            if r.returncode != 0:
                plan.blockers.append("`bundle check` says the bundle is not installed "
                                     "(the person runs `bundle install` if they agree)")
        except (OSError, subprocess.TimeoutExpired) as exc:
            plan.blockers.append(f"`bundle check` could not run: {exc}")

    def gem(n):
        return re.search(r"""gem\s+["']%s["']""" % re.escape(n), text) is not None

    if gem("standard"):
        plan.add("lint", name, ["bundle", "exec", "standardrb"])
    elif gem("rubocop") or (root / ".rubocop.yml").is_file():
        plan.add("lint", name, ["bundle", "exec", "rubocop"], "also checks layout (format)")
    if (root / "spec").is_dir() and (gem("rspec-rails") or gem("rspec")):
        plan.add("test", name, ["bundle", "exec", "rspec"])
    elif rails and (root / "test").is_dir():
        plan.add("test", name, ["bin/rails", "test"])
    elif (root / "Rakefile").is_file():
        plan.add("test", name, ["bundle", "exec", "rake", "test"])
    else:
        plan.notes.append(f"{name}: no spec/, test/ or Rakefile found")


# --- C / C++ (CMake, Make) -------------------------------------------------

def cmake_build_dirs(root):
    dirs = []
    for d in sorted(root.iterdir()):
        if d.is_dir() and (d / "CMakeCache.txt").is_file():
            dirs.append(d)
    return dirs


def tracked_sources(root):
    exts = (".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx")
    try:
        r = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, timeout=60)
        files = [f for f in r.stdout.splitlines() if f.endswith(exts)] if r.returncode == 0 else []
    except (OSError, subprocess.TimeoutExpired):
        files = []
    return files


def detect_c(root, plan):
    cmake = (root / "CMakeLists.txt").is_file()
    make = (root / "Makefile").is_file() or (root / "GNUmakefile").is_file()
    if not cmake and not make:
        return
    if cmake:
        plan.toolchains.append(("cmake", "CMakeLists.txt"))
        dirs = cmake_build_dirs(root)
        if not dirs:
            plan.blockers.append("no configured CMake build directory (no */CMakeCache.txt). "
                                 "Configure and build first with the project's documented "
                                 "options, e.g. `cmake -S . -B build` then `cmake --build build`; "
                                 "configuring may download dependencies, so this script does not do it")
        else:
            b = dirs[0]
            if len(dirs) > 1:
                plan.notes.append("cmake: several build directories: " +
                                  ", ".join(d.name for d in dirs) + f"; using {b.name}")
            for tool in ("cmake", "ctest"):
                if not have(tool):
                    plan.blockers.append(f"`{tool}` is not on PATH")
            plan.add("test", "cmake", ["cmake", "--build", str(b)], "build before testing")
            plan.add("test", "cmake", ["ctest", "--test-dir", str(b), "--output-on-failure"])
            if (root / ".clang-tidy").is_file():
                if (b / "compile_commands.json").is_file() and have("clang-tidy"):
                    srcs = [f for f in tracked_sources(root) if f.endswith((".c", ".cc", ".cpp", ".cxx"))]
                    if srcs:
                        plan.add("lint", "cmake", ["clang-tidy", "-p", str(b), "--quiet"] + srcs,
                                 f"{len(srcs)} tracked source files")
                else:
                    plan.notes.append("cmake: .clang-tidy found, but clang-tidy or "
                                      "compile_commands.json is missing")
    if make and not cmake:
        text = read_text(root / "Makefile") + read_text(root / "GNUmakefile")
        targets = set(re.findall(r"^([A-Za-z0-9_.-]+)\s*:(?!=)", text, re.M))
        plan.toolchains.append(("make", "Makefile"))
        if not have("make"):
            plan.blockers.append("`make` is not on PATH")
        for c, names in (("format", ("format-check", "fmt-check", "check-format")),
                         ("lint", ("lint",)), ("test", ("test", "check"))):
            for n in names:
                if n in targets:
                    plan.add(c, "make", ["make", n])
                    break
            else:
                plan.notes.append(f"make: no {c} target")
    if (root / ".clang-format").is_file():
        if have("clang-format"):
            srcs = tracked_sources(root)
            if srcs:
                plan.add("format", "c/c++", ["clang-format", "--dry-run", "--Werror"] + srcs,
                         f"{len(srcs)} tracked files")
        else:
            plan.notes.append("c/c++: .clang-format found but clang-format is not on PATH")


DETECTORS = (detect_node, detect_dart, detect_swift, detect_gradle, detect_ruby, detect_c)

NESTED_MARKERS = ("package.json", "pubspec.yaml", "Package.swift", "build.gradle",
                  "build.gradle.kts", "Gemfile", "CMakeLists.txt", "Podfile")


def nested_projects(root):
    found = []
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in ("node_modules", "build", "Pods", "vendor"):
            continue
        marks = [m for m in NESTED_MARKERS if (d / m).is_file()]
        if marks or list(d.glob("*.xcodeproj")):
            found.append(f"{d.name}/ ({', '.join(marks) or 'xcodeproj'})")
    return found


def build_plan(root, only, will_run=False):
    plan = Plan()
    plan.will_run = will_run
    for detect in DETECTORS:
        detect(root, plan)
    if only:
        plan.commands = [c for c in plan.commands if c["category"] == only]
    nested = nested_projects(root)
    if nested:
        plan.notes.append("subprojects (not checked; run this script on each): " + "; ".join(nested))
    return plan


def show(plan, root):
    print(f"Project: {root}")
    if not plan.toolchains:
        print("No known toolchain found in the project root.")
    for name, evidence in plan.toolchains:
        print(f"Toolchain: {name}  [{evidence}]")
    for c in CATEGORIES:
        cmds = [x for x in plan.commands if x["category"] == c]
        for x in cmds:
            line = " ".join(x["argv"])
            if len(line) > 160:
                line = line[:157] + "..."
            print(f"  {c:<6} {line}" + (f"   # {x['note']}" if x["note"] else ""))
    for n in plan.notes:
        print(f"Note: {n}")
    for b in plan.blockers:
        print(f"BLOCKED: {b}")


def run(plan, root, timeout):
    results = []
    env = dict(os.environ, CI="true")
    broken_builds = set()
    for x in plan.commands:
        if x["category"] == "test" and x["toolchain"] in broken_builds:
            results.append((x, None))
            continue
        print(f"\n=== {x['category']}: {' '.join(x['argv'])[:200]}", flush=True)
        try:
            code = subprocess.run(x["argv"], cwd=root, env=env, timeout=timeout).returncode
        except FileNotFoundError:
            code = 127
            print(f"command not found: {x['argv'][0]}")
        except subprocess.TimeoutExpired:
            code = 124
            print(f"timed out after {timeout} s")
        print(f"=== exit {code}", flush=True)
        results.append((x, code))
        if x["note"] == "build before testing" and code != 0:
            print("build failed; the tests of this build are skipped")
            broken_builds.add(x["toolchain"])
    print("\nSummary:")
    failed = 0
    for x, code in results:
        status = "skipped" if code is None else ("ok" if code == 0 else f"FAILED ({code})")
        if code not in (0, None):
            failed += 1
        print(f"  {x['category']:<6} {status:<12} {' '.join(x['argv'])[:120]}")
    print(f"{len(results)} commands, {failed} failed")
    return 1 if failed else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Detect a project's toolchain and run its own checks.")
    ap.add_argument("project", help="project directory")
    ap.add_argument("--run", action="store_true", help="run the commands (default: only show them)")
    ap.add_argument("--only", choices=CATEGORIES, help="limit to one category")
    ap.add_argument("--timeout", type=int, default=1800, help="seconds per command (default 1800)")
    ap.add_argument("--json", action="store_true", help="print the plan as JSON")
    args = ap.parse_args(argv)
    root = Path(args.project).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    plan = build_plan(root, args.only, args.run)
    if args.json:
        print(json.dumps({"project": str(root), "toolchains": plan.toolchains,
                          "commands": plan.commands, "notes": plan.notes,
                          "blockers": plan.blockers}, indent=2))
    else:
        show(plan, root)
    if not plan.toolchains or not plan.commands:
        if not args.json:
            print("Nothing to run.")
        return 2
    if not args.run:
        return 2 if plan.blockers else 0
    if plan.blockers:
        print("\nNot running: fix the BLOCKED items above first (installing is the person's decision).")
        return 2
    return run(plan, root, args.timeout)


if __name__ == "__main__":
    sys.exit(main())
