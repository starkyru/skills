#!/usr/bin/env python3
"""Validate skills in this repo.

Checks every skills/*/SKILL.md for:
  - parseable YAML frontmatter with required keys: name, description
  - name: kebab-case, <= 64 chars, equals the directory name
  - description: non-empty, <= 1024 chars
  - non-empty body
Warnings (non-fatal): unknown frontmatter keys, SKILL.md over 500 lines.

Exit code 0 = all skills valid, 1 = errors found.
Stdlib-only fallback parser is used when PyYAML is not installed; it handles
flat `key: value` pairs and `>-`/`|` block scalars, which covers this repo's
frontmatter rules.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024
MAX_BODY_LINES = 500
KNOWN_KEYS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "argument-hint",
    "disable-model-invocation",
    "user-invocable",
    "model",
}


def parse_frontmatter_naive(text: str) -> dict:
    """Flat key: value parser with basic block-scalar support."""
    data: dict = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value in (">", ">-", "|", "|-"):
            block: list[str] = []
            while i < len(lines) and (
                lines[i].startswith((" ", "\t")) or not lines[i].strip()
            ):
                block.append(lines[i].strip())
                i += 1
            joiner = "\n" if value.startswith("|") else " "
            data[key] = joiner.join(b for b in block if b)
        else:
            data[key] = value.strip("'\"")
    return data


def parse_frontmatter(text: str) -> dict:
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(text)
        if not isinstance(loaded, dict):
            raise ValueError("frontmatter is not a mapping")
        return loaded
    except ImportError:
        return parse_frontmatter_naive(text)


def split_document(content: str):
    """Return (frontmatter_text, body_text) or (None, None) if malformed."""
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", content, re.DOTALL)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def validate_skill(skill_dir: Path, errors: list, warnings: list) -> None:
    rel = skill_dir.relative_to(REPO_ROOT)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"{rel}: missing SKILL.md")
        return

    content = skill_md.read_text(encoding="utf-8")
    fm_text, body = split_document(content)
    if fm_text is None:
        errors.append(f"{rel}/SKILL.md: missing or malformed frontmatter block")
        return

    try:
        fm = parse_frontmatter(fm_text)
    except Exception as exc:
        errors.append(f"{rel}/SKILL.md: frontmatter does not parse: {exc}")
        return

    name = fm.get("name")
    if not name:
        errors.append(f"{rel}/SKILL.md: frontmatter missing 'name'")
    else:
        name = str(name)
        if not NAME_RE.match(name):
            errors.append(f"{rel}/SKILL.md: name '{name}' is not kebab-case")
        if len(name) > MAX_NAME_LEN:
            errors.append(
                f"{rel}/SKILL.md: name is {len(name)} chars (max {MAX_NAME_LEN})"
            )
        if name != skill_dir.name:
            errors.append(
                f"{rel}/SKILL.md: name '{name}' != directory '{skill_dir.name}'"
            )

    desc = fm.get("description")
    if not desc or not str(desc).strip():
        errors.append(f"{rel}/SKILL.md: frontmatter missing 'description'")
    elif len(str(desc)) > MAX_DESC_LEN:
        errors.append(
            f"{rel}/SKILL.md: description is {len(str(desc))} chars"
            f" (max {MAX_DESC_LEN})"
        )

    unknown = set(fm) - KNOWN_KEYS
    if unknown:
        warnings.append(
            f"{rel}/SKILL.md: unknown frontmatter keys: {', '.join(sorted(unknown))}"
        )

    if not body.strip():
        errors.append(f"{rel}/SKILL.md: body is empty")

    total_lines = content.count("\n") + 1
    if total_lines > MAX_BODY_LINES:
        warnings.append(
            f"{rel}/SKILL.md: {total_lines} lines (recommended max {MAX_BODY_LINES};"
            " move detail to references/)"
        )


def main() -> int:
    errors: list = []
    warnings: list = []

    if not SKILLS_DIR.is_dir():
        print(f"error: {SKILLS_DIR} does not exist", file=sys.stderr)
        return 1

    skill_dirs = sorted(
        d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")
    )
    for skill_dir in skill_dirs:
        validate_skill(skill_dir, errors, warnings)

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")

    print(
        f"\n{len(skill_dirs)} skill(s) checked,"
        f" {len(errors)} error(s), {len(warnings)} warning(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
