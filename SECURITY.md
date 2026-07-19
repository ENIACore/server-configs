# Security Policy

## Supported Versions

This repository mirrors the maintainer's live server configuration on the
`main` branch and cuts tagged [releases](../../releases) from it
(`vMAJOR.MINOR.PATCH`, see [CHANGELOG.md](CHANGELOG.md)). Only the latest
release and the current `main` branch are supported; older releases do not
receive backported fixes.

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| Latest release (see [releases](../../releases)) | :white_check_mark: |
| Older releases | :x: |

## Reporting a Vulnerability

If you discover a security vulnerability in these scripts or configurations
(e.g. an Nginx misconfiguration that exposes internal services, a script
that mishandles secrets, an insecure default, or a privilege escalation
path), please **do not open a public issue**.

Instead, report it privately using one of the following methods:

1. **Preferred:** Open a [GitHub Security Advisory](../../security/advisories/new)
   for this repository.
2. Contact the maintainer directly via the email listed on
   [@ENIACore's GitHub profile](https://github.com/ENIACore).

Please include:

- A description of the vulnerability and its potential impact
- Steps to reproduce or proof-of-concept, if available
- Any suggested remediation

## What to expect

- You will receive an acknowledgment within a few days of your report.
- The maintainer will investigate and, if confirmed, work on a fix and
  coordinate a disclosure timeline with you.
- Credit will be given in the fix's commit message/changelog if desired.

## Scope

Because this repo configures a real, internet-facing personal server, please
report issues related to:

- Nginx/reverse proxy misconfigurations (e.g. missing rate limits, exposed
  admin panels, weak TLS settings)
- Fail2ban/UFW rules that fail open
- Scripts that could leak secrets, API keys, or credentials
- Privilege escalation or insecure file permissions introduced by setup
  scripts

Out of scope: vulnerabilities in third-party software this repo merely
configures (e.g. Nextcloud, Vaultwarden, Jellyfin itself) — please report
those to the respective upstream projects.
