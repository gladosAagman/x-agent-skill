# Security policy

## What this pack touches

Everything runs locally on files you give it. The only network access is in
tools that say so in their docstring (`pull.py` calls X's documented oEmbed API for URLs you supply; `weights.py` reads one public GitHub file).
No tool asks for, stores or transmits credentials. Your files under
`~/.claude/x/` stay on your machine.

Hardening already in place: the reply ledger neutralises cells that would be
read as spreadsheet formulas and validates every handle; calendar files
escape and fold every field; timezone names are validated before use.

## Reporting a vulnerability

Please do not open a public issue. Use GitHub's private vulnerability
reporting on this repository (Security -> Report a vulnerability). Expect an
acknowledgement within a week.
