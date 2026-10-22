# Agent compatibility and installation

The canonical portable file is [SKILL.md](../skills/pattern-atlas/SKILL.md), with optional `references/`, `scripts/`, `data/`, `patterns/`, and `assets/`. Local install targets are intended paths, not proofs that every host revision supports the same discovery behavior.

| `--agent` value | Target relative to `--project` |
|---|---|
| `codex` | `.agents/skills/pattern-atlas` |
| `claude-code` | `.claude/skills/pattern-atlas` |
| `cursor` | `.cursor/skills/pattern-atlas` |
| `opencode` | `.opencode/skills/pattern-atlas` |
| `gemini` | `.gemini/skills/pattern-atlas` |
| `copilot` | `.github/skills/pattern-atlas` |
| `generic` | `.agents/skills/pattern-atlas` |

Use `npx skills add KaigorodovTuskul/Pattern-Atlas-Technical-Analysis-Agent-Skill --skill pattern-atlas` if your agent supports the ecosystem installer. Or run `python scripts/install.py --project . --agent codex --dry-run`, and then omit `--dry-run`. `--force` is required to replace an existing installation. Do not install a second copy in a competing discovery path unless needed. Pattern Atlas itself has no runtime pip dependencies.

Skill discovery, auto-invocation, context budgets and file access vary by client. For unsupported hosts, copy the instructions from `SKILL.md` and manually reference `references/REFERENCE_MAP.md`. No direct model/agent integration tests are asserted.
