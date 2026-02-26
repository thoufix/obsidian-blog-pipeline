
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
/srv/blog/releases/TIMESTAMP/  
│  
│ ln -sfn (symlink swap)  
▼  
/srv/blog/current (Active Symlink)  
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
🌍 [https://blog.pilab.space](https://blog.pilab.space/)

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

````

---

### 2️⃣ GitHub Phase

- GitHub receives push
- Webhook triggers:  
  `https://woodpecker.pilab.space/hook`

---

### 3️⃣ CI Phase (Woodpecker)

Woodpecker detects `.woodpecker.yml`, clones repo at commit SHA, and executes the pipeline.

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
      - export DEPLOY_TS=$(date +%Y%m%d-%H%M%S)
      - export RELEASE_DIR=/srv/blog/releases/$DEPLOY_TS
      - mkdir -p $RELEASE_DIR
      - cp -r hugo-site/public/* $RELEASE_DIR/
      - |
        if [ ! -f "$RELEASE_DIR/index.html" ]; then
          echo "ERROR: index.html not found. Aborting."
          rm -rf $RELEASE_DIR
          exit 1
        fi
      - ln -sfn $RELEASE_DIR /srv/blog/current
      - ls -dt /srv/blog/releases/* | tail -n +6 | xargs rm -rf
````

---

### 4️⃣ Deployment Phase (Capistrano-Style Release)

1. New release directory created:  
    `/srv/blog/releases/YYYYMMDD-HHMMSS/`
    
2. Hugo output copied into it
    
3. `index.html` validated — if missing, release is deleted and pipeline aborts
    
4. `ln -sfn` atomically swaps `/srv/blog/current` to new release
    
5. Releases older than last 5 are automatically cleaned up
    

**Rollback:**

```bash
ln -sfn /srv/blog/releases/YYYYMMDD-HHMMSS /srv/blog/current
```

---

### 5️⃣ Serving Phase

Nginx serves static files from `/srv/blog/current` on port 80 internally.  
No public ports exposed.

---

### 6️⃣ Ingress Phase

Cloudflare Tunnel forwards `blog.pilab.space` to the internal Nginx container.  
Cloudflare handles SSL termination.

---

## 🖥 Infrastructure Layout (Pi)

```
Raspberry Pi 5 (pilab)
│
├── woodpecker-server
├── woodpecker-agent
├── blog-web (nginx)
├── cloudflared
└── /srv/blog/
    ├── current -> releases/YYYYMMDD-HHMMSS/
    └── releases/
        ├── 20260226-120000/
        ├── 20260225-184500/
        └── ...
```

---

## 🔐 Security Model

- No direct IPv4/IPv6 exposure
    
- No open ports 80/443
    
- Outbound-only Cloudflare Tunnel
    
- HTTPS enforced at Cloudflare Edge
    
- Internal traffic remains private
    

---

## ⚙ Obsidian Git Configuration

```
Auto pull interval:    5 minutes
Auto commit interval:  10 minutes
Auto push interval:    10 minutes
Pull on startup:       Enabled
Split timers:          Enabled
```

---

## 🧠 Design Principles

- **GitHub** = Source of Truth
    
- **CI/CD** = Automated, reproducible builds
    
- **Infrastructure** = Containerized
    
- **Deployment** = Timestamped releases with atomic symlink swap
    
- **Ingress** = Zero-trust (Cloudflare Tunnel)
    
- **No raw IP exposure**
    

---

## 🚀 What This Achieves

- Fully automated blog publishing
    
- Self-hosted CI on ARM64
    
- Zero-downtime deploys with instant rollback
    
- Secure global access via Cloudflare
    
- No reliance on VPS hosting
    

---

## 📌 Future Improvements

- Pin Hugo to a specific version (avoid `latest`)
    
- Failure notifications on pipeline error
    
- Preview builds for PRs
    

---

> **Status: Stable & Production-Ready**  
> Last verified: 2026-02-26