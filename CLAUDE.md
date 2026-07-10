# Repository conventions

This repo holds personal Agent Skills. When authoring or editing skills here, follow these rules.

## Layout

- One skill per directory under `skills/<skill-name>/`, containing `SKILL.md`.
- Supporting material goes in `references/` (docs read on demand), `scripts/` (executable helpers), `assets/` (templates and files used in output). Never inline large reference material into `SKILL.md`.
- `template/SKILL.md` is the canonical skeleton — keep it in sync with these rules.

## Frontmatter

- `name`: kebab-case, must equal the directory name, max 64 chars.
- `description`: third person, states both what the skill does and when to use it (trigger phrases). Max 1024 chars. This is the only text the agent sees before deciding to load the skill — write it for retrieval.
- Optional keys: `license`, `allowed-tools`, `metadata`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `model`.

## Body

- Keep `SKILL.md` under 500 lines; push detail into `references/`.
- Write instructions for an agent, not a human reader: imperative steps, concrete commands, expected outputs.
- Scripts referenced by a skill must be executable (`chmod +x`) and runnable from the skill directory.
- No secrets, tokens, or machine-specific absolute paths in any skill file.

## Workflow

- Any change that adds, renames, or removes a skill MUST update the README `## Skills` table in the same change: one row per skill, alphabetical, linked as `skills/<name>/`, with a one-line description consistent with the skill's frontmatter. A skill without a README row is an incomplete change — do not stop or commit until the table is updated.
- Run `python3 scripts/validate.py` after every skill change; it must pass before committing.
