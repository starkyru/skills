---
name: clone-skill
description: >-
  Clones a skill into this repo and security-audits it before integration.
  Source can be an existing skill in skills/ (duplicate under a new name), a
  local directory, or a git URL. Can also run the audit standalone. Use when
  the user says "/clone-skill", "clone skill <x>", "import/copy a skill from
  <path or repo>", or "audit skill <x>".
argument-hint: "<source> [new-name]"
---

# Clone Skill

Clone a skill into `skills/`, run a mandatory static security audit before it touches the repo, validate, and register it in the README.

## Arguments

`<source> [new-name]`

- `source` — one of: an existing skill name in `skills/`, a local path to a directory containing `SKILL.md`, or a git URL (append `#<subdir>` when the skill lives in a subdirectory of the repo).
- `new-name` — kebab-case target directory name. Required when duplicating an in-repo skill; defaults to the source directory name otherwise.

**Audit-only mode:** if the user asked only to audit (no cloning implied), run steps 3–4 against the skill in place and report the verdict. Skip staging and integration.

## Steps

1. **Resolve the source.**
   - `skills/<source>/SKILL.md` exists → in-repo duplicate. Require `new-name`, and it must differ from `source`.
   - Local path with `SKILL.md` → external local skill.
   - Git URL → `git clone --depth 1 <url> "$(mktemp -d)"`, then locate the directory containing `SKILL.md` (use the `#<subdir>` fragment if given; if multiple candidates, list them and ask which).
   - No `SKILL.md` found → stop and report what was found instead.
2. **Stage.** Copy the skill directory to a temp staging dir (`mktemp -d`). Never copy into `skills/` before the audit passes. If `skills/<new-name>` already exists, stop and ask.
3. **Security audit — mandatory, static only.** Read `references/security-audit.md` and follow it exactly. Read every file in the staged copy completely. Never execute anything from the skill during the audit.
4. **Act on the verdict.**
   - `FAIL` → delete the staging copy, do not integrate, present all findings with evidence.
   - `PASS WITH WARNINGS` → present findings, ask the user whether to proceed.
   - `PASS` → continue.
5. **Integrate.** Move the staged copy to `skills/<new-name>`. Then:
   - Set frontmatter `name` to `<new-name>`.
   - For in-repo duplicates: rewrite `description` — two skills with identical trigger phrases collide at retrieval time, so the clone must state its own distinct triggers (ask the user for the clone's purpose if unclear).
   - `chmod +x` any files under `scripts/`; verify scripts use paths relative to the skill directory.
   - Reject or flag symlinks that point outside the skill directory.
6. **Validate.** Run `python3 scripts/validate.py` from the repo root — must exit 0.
7. **Register.** Add a row for the skill to the README "Skills" table, keeping it alphabetical.
8. **Report.** Source, destination, audit verdict with findings summary, validation result. Note that changes are uncommitted.

## Edge cases

- Source frontmatter has keys outside this repo's known set → keep them, but include the validator warning in the report.
- Binary or minified files in the source → the audit covers this (unauditable content fails).
- Git clone requires auth or fails → report the exact error; do not retry with credentials.
- Temp dirs (clone + staging) → remove them once done, including on failure.
