# Contributing to server-configs

Thanks for your interest in improving this project! This repository holds the
automation scripts and Nginx/Docker configs behind Server-AIO, an all-in-one
self-hosted server setup toolkit. Contributions of all sizes are welcome —
bug fixes, documentation improvements, new service installers, and general
hardening suggestions.

## Before you start

- Please read the [Code of Conduct](CODE_OF_CONDUCT.md).
- For anything beyond a small fix, open an issue first to discuss the change
  before investing time in a pull request.
- This project is tailored to a specific homelab setup. Contributions that
  make scripts more generic/configurable (instead of hardcoding paths or
  domains) are especially appreciated.

## Reporting bugs

Use the **Bug report** issue template and include:

- The script/file involved
- Steps to reproduce
- Expected vs. actual behavior
- Relevant logs (redact any secrets, domains, or IPs)

## Suggesting features

Use the **Feature request** issue template. Describe the problem you're
solving, not just the solution — it helps evaluate whether it fits the
project's scope.

## Development setup

1. Fork and clone the repository.
2. Scripts are Python 3 (see `lib/` for shared utilities) and are formatted
   with [ruff](https://docs.astral.sh/ruff/) (`ruff.toml` at the repo root).
3. Run `ruff check .` and `ruff format .` before committing.
4. Test any install/setup script changes on a disposable VM or container —
   never against a production server.

## Pull requests

1. Create a branch from `main`: `git checkout -b feature/short-description`.
2. Keep changes focused — one logical change per PR.
3. Make sure no secrets, real domains, IP addresses, or credentials are
   included in diffs (check templates under `keys/` and `nginx/templates/`
   carefully).
4. Fill out the pull request template completely.
5. Ensure `ruff check .` passes with no new warnings.
6. A maintainer will review and may request changes before merging.

## Style guidelines

- Prefer the shared helpers in `lib/` (`common.py`, `checks.py`, `config.py`,
  `logger.py`) over duplicating logic in per-service scripts.
- Keep config templates (`*.template`) free of real secrets — use
  placeholders consistent with existing templates.
- Write clear, imperative commit messages (e.g. "Add healthcheck cron
  script" rather than "Added stuff").

## Questions

Open a [discussion](../../discussions) or issue if you're unsure where a
change belongs. Thanks again for contributing!
