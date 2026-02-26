---
title: Pilab Blog Pipeline Architecture
date: 2026-02-26
summary: Fully automated CI/CD pipeline for a personal blog using Obsidian, GitHub, Woodpecker CI, Hugo, Nginx, and Cloudflare Tunnel on a Raspberry Pi 5
series: pilab
tags:
  - woodpecker
  - hugo
  - nginx
  - cloudflare
  - raspberry-pi
  - ci-cd
  - obsidian
---

## 🧭 Overview

This project implements a fully automated CI/CD pipeline for a personal blog using:

- Obsidian (Windows)
- Git + GitHub
- Woodpecker CI (self-hosted on Raspberry Pi 5)
- Hugo (Extended, ARM64)
- Nginx (Docker)
- Cloudflare Tunnel
- Cloudflare Edge SSL

Everything is self-hosted on `pilab` (Raspberry Pi 5) and exposed securely via Cloudflare Tunnel.

---

## 🏗 High-Level Architecture Flow
```
Obsidian (Windows)
        │
        │ Auto Commit + Push
        ▼
GitHub Repository
        │
        │ Webhook (push event)
        ▼
Woodpecker CI (Docker on Pi)
        │
        │ Clone Repo
        ▼
Hugo Build (ARM64 container)
        │
        │ Generate static site
        ▼
/srv/blog/public (Host Volume)
        │
        ▼
Nginx Container (blog-web)
        │
        ▼
Cloudflare Tunnel (cloudflared)
        │
        ▼
Cloudflare Edge (SSL)
        │
        ▼
🌍 https://blog.pilab.space
```

---

## 🔄 Detailed Execution Flow

### 1️⃣ Writing Phase

Blog posts written in Obsidian, markdown files saved under:
```
hugo-site/content/posts/
```

Obsidian Git plugin performs:
```
pull → commit → push
```

---

### 2️⃣ GitHub Phase

- GitHub receives push
- Webhook triggers:
```
https://woodpecker.pilab.space/hook
```

---

### 3️⃣ CI Phase (Woodpecker)

Woodpecker:

- Detects `.woodpecker.yml`
- Clones repo at commit SHA
- Executes pipeline

#### Pipeline Config
```yaml
steps:
  build:
    image: ghcr.io/gohugoio/hugo:latest
    commands:
      - cd hugo-site
      - hugo --minify
  deploy:
    image: alpine:latest
    volumes:
      - /srv/blog:/srv/blog
    commands:
      - rm -rf /srv/blog/public/*
      - cp -r hugo-site/public/* /srv/blog/public/
```

---

### 4️⃣ Deployment Phase

Generated static files are copied to:
```
/srv/blog/public
```

This directory is mounted into the Nginx container.

---

### 5️⃣ Serving Phase

Nginx container:

- Serves static files
- Listens internally on port 80

No public ports are exposed.

---

### 6️⃣ Ingress Phase

Cloudflare Tunnel:

- Forwards `blog.pilab.space`
- To internal Nginx container

Cloudflare:

- Handles HTTPS (SSL termination)
- Provides secure public access

---

## 🖥 Infrastructure Layout (Pi)
```
Raspberry Pi 5 (pilab)
│
├── woodpecker-server
├── woodpecker-agent
├── blog-web (nginx)
├── cloudflared
└── Shared volume: /srv/blog/public
```

All services are Dockerized.

---

## 🔐 Security Model

- No direct IPv4/IPv6 exposure
- No open ports 80/443
- Outbound-only Cloudflare Tunnel
- HTTPS enforced at Cloudflare Edge
- Internal traffic remains private

---

## ⚙ Obsidian Git Configuration

Recommended stable setup:
```
Auto pull interval:    5 minutes
Auto commit interval:  10 minutes
Auto push interval:    10 minutes
Pull on startup:       Enabled
Split timers:          Enabled
```

Windows is the only editing environment. Pi does not manually modify the repository.

---

## 🧠 Design Principles

- **GitHub** = Source of Truth
- **CI/CD** = Automated, reproducible builds
- **Infrastructure** = Containerized
- **Deployment** = Atomic file replacement
- **Ingress** = Zero-trust (Cloudflare Tunnel)
- **No raw IP exposure**

---

## 🚀 What This Achieves

- Fully automated blog publishing
- Self-hosted CI on ARM64
- Secure global access
- No reliance on VPS hosting
- Real-world DevOps workflow on Raspberry Pi

---

## 📌 Future Improvements

- Atomic deploy swap (avoid `rm -rf`)
- Build caching
- Preview builds for PRs
- Health checks
- Monitoring (Prometheus + Grafana)

---

> **Status: Stable & Production-Ready**  
> Last verified: CI auto-triggers on push