# Skill authoring guide

How to write skills for this repo. The short version lives in [CLAUDE.md](../CLAUDE.md); this is the reasoning and detail.

## How agents consume skills

An agent sees only each skill's `name` and `description` at session start. The full `SKILL.md` body is read **only after** the agent decides the skill is relevant — and bundled `references/`, `scripts/`, `assets/` are loaded later still, on demand. This progressive disclosure drives every rule below: metadata is for retrieval, the body is for execution, bundled files are for depth.

## The description is the API

The description decides whether your skill ever gets used. A skill with a vague description is invisible.

**Include:**
- What the skill does (one clause).
- When to use it — the actual phrases, file types, tools, or situations that should trigger it.

**Bad:** `Helps with database work.`

**Good:** `Generates and reviews Postgres migrations. Use when the user asks to add/alter tables, writes SQL DDL, or edits files under migrations/.`

Write in third person ("Generates…", not "I generate…" / "You can…"). Max 1024 chars — but don't pad; density beats length.

## Naming

- Kebab-case, must equal the directory name: `skills/pdf-forms/SKILL.md` → `name: pdf-forms`.
- Prefer verb-ish or domain names that read naturally in a trigger list: `commit-style`, `api-benchmarks`, `pdf-forms`.
- Max 64 chars.

## Body structure

Write for an agent executing a task, not a human skimming docs:

- Imperative steps in execution order.
- Exact commands with real flags, not prose descriptions of commands.
- Expected outputs after each step, so the agent can self-verify.
- Edge cases and failure modes — what to do when a step fails.

Keep it under 500 lines. If a section grows past a screen, move it to `references/` and leave a one-line pointer with the condition for reading it ("read `references/api.md` when adding new endpoints").

## Bundled files

| Directory | Purpose | Loaded |
|-----------|---------|--------|
| `references/` | Documentation, schemas, examples the agent reads | On demand, when the body points to them |
| `scripts/` | Executable helpers the agent runs | Executed, not read — deterministic beats generated code |
| `assets/` | Templates, boilerplate, files copied into output | Used in output, rarely read |

Rules:
- Scripts must be executable (`chmod +x`) and work with relative paths from the skill directory.
- Prefer a script over instructing the agent to write code: scripts are deterministic, testable, and cheaper.
- No secrets, no machine-specific absolute paths — skills get copied to other machines.

## Anti-patterns

- **Duplicating agent defaults.** Don't write "read the file, then edit it carefully" — agents do that anyway. A skill earns its place by encoding what the agent *doesn't* already know.
- **One giant skill.** Split unrelated capabilities; each gets its own trigger surface.
- **Frontmatter feature-creep.** `name` + `description` cover almost everything. Add `allowed-tools` only to *restrict* a skill.
- **README instead of runbook.** Background/context sections that never change behavior are dead weight in the context window.

## Checklist before committing

1. `python3 scripts/validate.py` passes.
2. Description contains trigger phrases you'd actually say.
3. SKILL.md < 500 lines; heavy content moved to `references/`.
4. Scripts executable, relative paths only.
5. README skills table updated.
