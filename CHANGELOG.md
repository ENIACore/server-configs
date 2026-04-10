# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-09-22

Initial versioned release. Everything up to this point was developed as a
single rolling `main` branch; this tag marks the first snapshot considered
stable enough to install on a fresh server.

### Added

- `install.py` bootstrap installer: copies commands to `/usr/local/sbin`,
  collects initial server configuration, and prepares Nginx templates for
  the configured domain.
- Shared Python helpers in `lib/` (`common`, `checks`, `config`, `docker`,
  `formatting`, `logger`, `install-scripts`, `setup`) used across all
  service and infrastructure scripts.
- Nginx reverse proxy setup with SSL termination, Cloudflare real-IP
  handling, rate limiting, exploit-blocking snippets, and per-service
  config templates (`nginx-setup`, `nginx-enable`, `nginx-disable`,
  `nginx-reload`, `nginx-tail-logs`).
- Cloudflare DNS automation for root and wildcard record updates, plus
  scheduled DNS refresh and certificate creation (`cf-setup`, `cf-update-dns`,
  `cf-schedule`, `cf-create-cert`).
- UFW firewall setup and scheduling (`ufw-setup`, `ufw-schedule`).
- Fail2ban setup, status, and reload commands (`f2b-setup`, `f2b-status`,
  `f2b-reload`).
- Service installers: Nextcloud, Vaultwarden, Jellyfin, jfa-go,
  qBittorrent (via the hotio image with built-in WireGuard), Jackett,
  FlareSolverr, a Fabric Minecraft server with Lithium, PostgreSQL, and a
