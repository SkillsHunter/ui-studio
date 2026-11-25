#!/usr/bin/env python3
"""Build and validate the UI Studio release files from the ui-studio/ folder.

Usage:
    python tools/build.py            # validate, then write dist/
    python tools/build.py --check    # validate only

Outputs (all reproducible: same source in, byte-identical zip out):
    dist/ui-studio.zip               the full skill (SKILL.md, references/, scripts/)
    dist/ui-studio-single-file.zip   one SKILL.md with the references inlined as appendices
    dist/SHA256SUMS                  checksums for both zips

ui-studio/ is the only source of truth. The single-file build is generated from it,
so the two can never drift apart.
"""
import argparse
import hashlib
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "ui-studio"
DIST = ROOT / "dist"

# Fixed timestamp so the same source always produces the same zip bytes.
ZIP_DATE = (2026, 1, 1, 0, 0, 0)
EXCLUDE_NAMES = {"__pycache__", ".DS_Store", "Thumbs.db"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}

# Appendix letter and short cross-reference label for each reference file, in order.
APPENDICES = [
    ("actions.md", "Making the main action work"),
    ("avoid.md", "What looks machine-made"),
    ("floor.md", "Quality floor"),
    ("type-and-colour.md", "Type and colour"),
    ("page-anatomy.md", "Page anatomy"),
    ("handoff.md", "Handing over"),
]

MAX_DESCRIPTION = 1024


class BuildError(Exception):
    pass


def read_text(path):
    """Read a text file with normalised LF line endings."""
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n")


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise BuildError("SKILL.md has no YAML frontmatter block.")
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    return fields


def source_files():
    files = []
    for p in sorted(SKILL_DIR.rglob("*")):
        rel = p.relative_to(SKILL_DIR)
        if any(part in EXCLUDE_NAMES for part in rel.parts) or p.suffix in EXCLUDE_SUFFIXES:
            continue
        if p.is_file():
            files.append(p)
    return files


def validate():
    """Return a list of problems with the skill source. Empty means valid."""
    problems = []
    skill_md = SKILL_DIR / "SKILL.md"
    if not skill_md.is_file():
        return ["ui-studio/SKILL.md is missing."]
    text = read_text(skill_md)
    try:
        fm = parse_frontmatter(text)
    except BuildError as e:
        return [str(e)]
    if fm.get("name") != SKILL_DIR.name:
        problems.append(f"Frontmatter name {fm.get('name')!r} does not match folder {SKILL_DIR.name!r}.")
    desc = fm.get("description", "")
    if not desc:
        problems.append("Frontmatter description is empty.")
    elif len(desc) > MAX_DESCRIPTION:
        problems.append(f"Description is {len(desc)} characters; the limit is {MAX_DESCRIPTION}.")

    for ref in sorted(set(re.findall(r"`((?:references|scripts)/[\w.-]+)`", text))):
        if not (SKILL_DIR / ref).is_file():
            problems.append(f"SKILL.md mentions {ref}, which does not exist.")
    listed = {name for name, _ in APPENDICES}
    actual = {p.name for p in (SKILL_DIR / "references").glob("*.md")}
    for missing in sorted(actual - listed):
        problems.append(f"references/{missing} is not in tools/build.py APPENDICES, so the single-file build would drop it.")
    for gone in sorted(listed - actual):
        problems.append(f"APPENDICES lists references/{gone}, which does not exist.")

    for p in source_files():
        raw = p.read_bytes()
        if b"\r\n" in raw:
            problems.append(f"{p.relative_to(ROOT).as_posix()} has CRLF line endings (run: git add --renormalize .).")
        if p.suffix in {".md", ".py"}:
            try:
                raw.decode("utf-8")
            except UnicodeDecodeError:
                problems.append(f"{p.relative_to(ROOT).as_posix()} is not valid UTF-8.")
    return problems


def _zip_entry(name, is_dir=False, executable=False):
    info = zipfile.ZipInfo(name, date_time=ZIP_DATE)
    info.create_system = 3  # Unix, so the permission bits below are honoured
    if is_dir:
        info.external_attr = (0o40755 << 16) | 0x10
    else:
        info.external_attr = (0o100755 if executable else 0o100644) << 16
        info.compress_type = zipfile.ZIP_DEFLATED
    return info


def write_zip(path, entries):
    """entries: list of (archive_name, bytes or None for a directory)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as z:
        for name, data in entries:
            if data is None:
                z.writestr(_zip_entry(name, is_dir=True), b"")
            else:
                z.writestr(_zip_entry(name), data, compresslevel=9)


def full_entries():
    names = {}
    for p in source_files():
        rel = p.relative_to(SKILL_DIR)
        for i in range(len(rel.parts) - 1):
            names["ui-studio/" + "/".join(rel.parts[: i + 1]) + "/"] = None
        names["ui-studio/" + rel.as_posix()] = read_text(p).encode("utf-8")
    names["ui-studio/"] = None
    return sorted(names.items())


def single_file_skill():
    """SKILL.md with every reference inlined as a lettered appendix."""
    text = read_text(SKILL_DIR / "SKILL.md").rstrip("\n")
    label = {}
    for i, (name, short) in enumerate(APPENDICES):
        label[name] = f"Appendix {chr(ord('A') + i)} ({short})"

    def ref(m):
        return label[m.group(1)]

    checker = "**Run the checker** if you can run code:"
    if checker not in text:
        raise BuildError(f"Single-file build expects the phrase {checker!r} in SKILL.md; update tools/build.py.")
    text = text.replace(checker, "**Run the checker** if `scripts/check.py` is available and you can run code:")
    text = re.sub(r"`references/([\w.-]+\.md)`", ref, text)

    parts = [text]
    for i, (name, _) in enumerate(APPENDICES):
        body = read_text(SKILL_DIR / "references" / name).strip("\n")
        title, _, rest = body.partition("\n")
        if not title.startswith("# "):
            raise BuildError(f"references/{name} must start with a '# ' title.")
        rest = re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", rest, flags=re.M)
        rest = re.sub(r"`([\w.-]+\.md)`", lambda m: label.get(m.group(1), m.group(0)), rest)
        parts.append(f"## Appendix {chr(ord('A') + i)}. {title[2:].strip()}\n{rest}")
    out = "\n\n---\n\n".join(parts[:1]) + "\n\n---\n\n" + "\n\n".join(parts[1:]) + "\n"
    leftover = re.findall(r"references/[\w.-]+\.md", out)
    if leftover:
        raise BuildError(f"Single-file build still mentions {sorted(set(leftover))}.")
    return out


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    full = DIST / "ui-studio.zip"
    single = DIST / "ui-studio-single-file.zip"
    write_zip(full, full_entries())
    write_zip(single, [("ui-studio/", None), ("ui-studio/SKILL.md", single_file_skill().encode("utf-8"))])
    sums = "".join(f"{sha256(p)}  {p.name}\n" for p in (full, single))
    (DIST / "SHA256SUMS").write_text(sums, encoding="utf-8", newline="\n")
    return [full, single, DIST / "SHA256SUMS"]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="validate only; write nothing")
    args = parser.parse_args(argv)
    problems = validate()
    if problems:
        print("Skill source has problems:", file=sys.stderr)
        for p in problems:
            print(" - " + p, file=sys.stderr)
        return 1
    if args.check:
        single_file_skill()  # proves the single-file build still generates
        print("Skill source is valid.")
        return 0
    try:
        outputs = build()
    except BuildError as e:
        print(f"Build failed: {e}", file=sys.stderr)
        return 1
    for p in outputs:
        print(p.relative_to(ROOT).as_posix())
    print((DIST / "SHA256SUMS").read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
