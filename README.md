<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Latest Release][release-shield]][release-url]

<br />
<div align="center">
  <h3 align="center">Server-AIO</h3>

  <p align="center">
    All-in-one, self-hosted server setup with security hardening and reverse proxy configuration
    <br />
    <a href="https://github.com/ENIACore/server-configs"><strong>Explore the docs</strong></a>
    <br />
    <br />
    <a href="https://github.com/ENIACore/server-configs/issues/new">Report Bug</a>
    &middot;
    <a href="https://github.com/ENIACore/server-configs/issues/new">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#what-gets-installed">What Gets Installed</a></li>
    <li><a href="#demo">Demo</a></li>
    <li><a href="#screenshots">Screenshots</a></li>
    <li><a href="#releases">Releases</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

Server-AIO is an all-in-one setup toolkit that turns a fresh Ubuntu Server into a repeatable self-hosted platform — in the same spirit as [nextcloud-aio](https://github.com/nextcloud/all-in-one), but for the whole server rather than a single app. One installer bootstraps the shared infrastructure (Cloudflare DNS updates, a Docker-based Nginx reverse proxy, UFW, Fail2ban, and a shared Docker network), then separate setup commands bring up individual services such as Nextcloud, Vaultwarden, and Jellyfin on top of it.
