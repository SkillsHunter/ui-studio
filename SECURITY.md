# Security policy

## What UI Studio is, and what it can do

UI Studio is a set of instructions for Claude (`SKILL.md` and `references/`) plus one optional script, `scripts/check.py`.

- It registers no hooks, MCP servers or background processes. Nothing runs unless Claude decides to run the checker.
- `check.py` uses only the Python standard library, plus Playwright if it is installed. It never makes network requests of its own. While rendering a page, it blocks every request except local files and Google Fonts unless you pass `--allow-network`.
- It writes only screenshots, to `.ui-studio-check/` next to the page or to the folder given with `--out`.

## Supported versions

Only the latest release gets fixes.

## Verify what you install

Download the zips from the [Releases page](https://github.com/SkillsHunter/ui-studio/releases), not from a copy someone sent you. Every release is built by GitHub Actions from the tagged source and ships with checksums and a signed provenance attestation:

```
sha256sum -c SHA256SUMS
gh attestation verify ui-studio.zip --repo SkillsHunter/ui-studio
```

## Reporting a vulnerability

Please report privately through GitHub: **Security → Report a vulnerability** on this repository. Don't open a public issue.

Useful things to report include instructions that could make Claude act against the user (prompt injection, hidden actions, data leaving the machine), a way for `check.py` to read or write outside what it should, and a release zip that doesn't match the tagged source.

You'll get an answer within 7 days. Confirmed problems are fixed in a new release, and credited to you if you like.
