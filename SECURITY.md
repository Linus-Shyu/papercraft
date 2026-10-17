# Security

## Supported versions

The `main` branch is supported. Releases are tagged from it.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting:
**Security → Report a vulnerability** on this repository.

Do not open a public issue for a vulnerability that could affect users.

## Threat model

Papercraft is a local tool that reads and writes files in a paper repository.

- **Template archives are untrusted.** `fetch_template.py` allows HTTPS only
  (localhost HTTP for tests), caps archive and extracted size, rejects path
  traversal, absolute paths, symlinks, and devices, and extracts only document
  types. It never executes files from the archive.
- **`check_repro.py --run` executes commands from a manifest.** Treat the
  manifest as trusted input; do not run a manifest from an untrusted source.
  Commands run in a temporary copy, not in the source tree.
- **No secrets by default.** The tools do not read `.env` or API keys. Do not put
  secrets in `paper_state/` or in manifests.
- **Anonymity scanning is best-effort.** It checks the manuscript and `code/` or
  `scripts/` via `--extra`; it does not scan PDF metadata or binary assets.
- **Network access is opt-in** (template download; optional artifact commands).

## If something goes wrong

1. Stop the command.
2. Remove any downloaded archive.
3. Rotate any exposed credential.
4. Open a private advisory with the command, file, and error.
