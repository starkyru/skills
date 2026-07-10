---
# name: kebab-case, must match the directory name, max 64 chars
name: skill-name
# description: the ONLY text the agent sees before deciding to load this skill.
# Third person. State what it does AND when to trigger it (include the phrases
# a user would actually say). Max 1024 chars.
description: >-
  Does X for Y. Use when the user asks to "do X", mentions Z, or works with
  <file type / tool / situation>.
# Optional:
# license: MIT
# allowed-tools: Read, Grep, Bash
---

# Skill Name

One-paragraph summary of what this skill accomplishes.

## When to use

- Trigger situation 1
- Trigger situation 2

## Instructions

1. Step one — imperative, concrete. Include exact commands:
   ```bash
   scripts/example.sh --flag value
   ```
2. Step two. State the expected output so the agent can verify.
3. For detail that doesn't fit here, point to a reference file:
   read `references/details.md` when <condition>.

## Edge cases

- Known failure mode and how to handle it.

<!--
Authoring checklist (delete this comment):
- [ ] name matches directory, kebab-case
- [ ] description contains trigger phrases, third person
- [ ] SKILL.md under 500 lines; detail moved to references/
- [ ] bundled scripts are executable and use relative paths
- [ ] python3 scripts/validate.py passes
- [ ] README skills table updated
-->
