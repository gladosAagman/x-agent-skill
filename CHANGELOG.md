# Changelog

## [2.0.0] - 2026-11-09

### Added
- `/x-voice` with `voice.py`: measures the user's voice from their own posts
  (sentence rhythm, casing, contractions, person, emoji, em dashes, numbers,
  recurring words and openers) and scores any draft for drift.
- `/x-engage` with `targets.py`: the reply ledger. Concentration warnings
  when three accounts take over half the round, the 5 / 3 / 2 tier mix, and
  who on the roster is overdue. Validates handles and neutralises spreadsheet
  formulas in notes.
- `/x-preflight` with `preflight.py`: count, hook score, humanizer panel and
  voice check on one draft, one READY or FIX FIRST.
- `/x-crisis`: pile-ons, ratios and mistakes. Correct, clarify, apologise or
  say nothing, then a 48-hour plan.
- `plan2ics.py` in `/x-plan`: the weekly plan as calendar reminders (.ics).
- Agents: `x-strategist` (the weekly loop) and `x-editor` (any draft to
  ready-to-paste).
- v2 sections in `/x-plan`, `/x-post`, `/x-comment` and `/x-reply` pointing at
  the new tools.

### Infrastructure
- `scripts/validate.py`: checks the plugin manifests, every skill's and agent's
  frontmatter, every JSON and Python file, and that the README documents every
  skill and agent.
- `tests/`: regression tests that pin the v1 tools' documented behaviour, and
  unit tests for every v2 tool covering normal input and edge cases (empty
  input, malformed rows, boundaries, injection).
- GitHub Actions CI on Linux, macOS and Windows, Python 3.10 and 3.13.
- Installable as a Claude Code plugin: `marketplace.json` gained the `owner`
  field and `plugin.json` gained author, repository, homepage and license.
- MIT license, CONTRIBUTING.md, SECURITY.md.

### Preserved
Every v1 skill, tool, data file and template is unchanged in behaviour. The
first commit in this repository is v1 exactly as it was; every v2 change to
an existing skill is an added section marked "(v2)".

## [1.0.0]

The original eleven skills.
