# skills

Personal collection of [Agent Skills](https://code.claude.com/docs/en/skills) — reusable, self-contained capabilities for Claude Code and other SKILL.md-compatible agents.

## What is a skill?

A skill is a directory containing a `SKILL.md` file with YAML frontmatter (`name`, `description`) and Markdown instructions. Agents load the description at startup and read the full skill only when it becomes relevant — so descriptions carry the trigger conditions, and bodies carry the how-to. Skills can bundle supporting `references/`, `scripts/`, and `assets/` that are loaded or executed on demand.

## Repository structure

```
skills/
├── README.md            # this file
├── CLAUDE.md            # authoring conventions enforced in this repo
├── docs/
│   └── authoring.md     # full skill authoring guide
├── template/
│   └── SKILL.md         # annotated skeleton — copy to start a new skill
├── scripts/
│   └── validate.py      # frontmatter/structure linter (also runs in CI)
└── skills/
    └── <skill-name>/    # one directory per skill
        ├── SKILL.md     # required — frontmatter + instructions
        ├── references/  # optional — docs loaded on demand
        ├── scripts/     # optional — executable helpers
        └── assets/      # optional — templates, files used in output
```

## Skills

<!-- Add a row per skill. Keep alphabetical. -->

| Skill | Description |
|-------|-------------|
| _none yet_ | |

## Installation

**Personal (all projects):** copy or symlink a skill into `~/.claude/skills/`:

```bash
ln -s "$(pwd)/skills/<skill-name>" ~/.claude/skills/<skill-name>
```

**Project-scoped:** copy into a project's `.claude/skills/` directory.

Symlinking keeps installed skills in sync with this repo; copying pins a snapshot.

## Creating a new skill

1. Copy the template: `cp -r template skills/<skill-name>`
2. Edit `SKILL.md` — see [docs/authoring.md](docs/authoring.md) for naming, description, and structure rules.
3. Validate: `python3 scripts/validate.py`
4. Add the skill to the table above.

## Validation

`scripts/validate.py` checks every `skills/*/SKILL.md` for required frontmatter, kebab-case names matching the directory, and size limits. CI runs it on every push and pull request.

```bash
python3 scripts/validate.py
```

## License

[MIT](LICENSE)
