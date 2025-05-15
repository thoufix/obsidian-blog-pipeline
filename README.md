# Obsidian-to-Blog: CI/CD Blog Pipeline with Hugo + GitHub + Raspberry Pi

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions)
![Hugo](https://img.shields.io/badge/Hugo-FF4088?style=for-the-badge&logo=hugo&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=raspberry-pi)

This project sets up an automated CI/CD pipeline for a personal blog using **Obsidian**, **Hugo**, **GitHub Actions**, and **Raspberry Pi**.

## Table of Contents
- [Project Overview](#-project-overview)
- [Tools Used](#%EF%B8%8F-tools-used)
- [Folder Structure](#folder-structure)
- [CI/CD Pipeline](#cicd-pipeline)
- [Getting Started](#-getting-started)
- [Bonus Features](#-bonus-features)
- [License](#license)

## 🚀 Project Overview

### What You'll Build:
- **Write**: Blog posts in **Obsidian** using Markdown
- **Sync**: Automatically sync posts to **GitHub**
- **CI/CD**: Use **GitHub Actions** to:
  - Build the site with **Hugo**
  - Deploy the static site to your **Raspberry Pi** via **SSH**
- **Host**: Serve the site on your Pi using **Caddy** or **Nginx**

This mirrors real-world DevOps workflows including:
- Git version control
- CI/CD automation
- Static site generation
- Self-hosting
- Secure deployments

## 🛠️ Tools Used
- **Obsidian**: Markdown writing
- **Hugo**: Static site generator
- **GitHub Actions**: CI/CD automation
- **Raspberry Pi**: Self-hosting
- **Caddy/Nginx**: Web servers
- **SSH**: Secure file transfer

## Folder Structure
```
obsidian-blog-pipeline/
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions workflow
├── content/
│   └── blog-posts.md        # Blog content
├── hugo-site/
│   └── config.toml          # Hugo config
├── scripts/
│   ├── deploy.sh            # Deployment script
│   └── setup-pi.sh          # Pi setup script
├── Dockerfile               # Optional Docker config
├── Caddyfile                # Optional Caddy config
└── README.md                # This file
```

## CI/CD Pipeline
1. **Write**: Create posts in Obsidian
2. **Sync**: Push to GitHub repository
3. **Build**: GitHub Actions runs Hugo build
4. **Deploy**: Built site transferred to Pi via SSH
5. **Serve**: Nginx/Caddy serves the static site

## 🏁 Getting Started

### Prerequisites
- GitHub account
- Raspberry Pi set up
- Basic terminal/SSH knowledge

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/obsidian-blog-pipeline.git
   cd obsidian-blog-pipeline
   ```

2. Configure Hugo:
   ```bash
   cd hugo-site
   hugo new site . --force
   ```

3. Set up GitHub Secrets for deployment:
   - `SSH_HOST`: Your Pi's IP
   - `SSH_USER`: Pi username
   - `SSH_KEY`: SSH private key

4. Configure your web server (Caddy example):
   ```bash
   sudo apt install caddy
   sudo cp Caddyfile /etc/caddy/
   sudo systemctl restart caddy
   ```

## ✨ Bonus Features
- **Custom Domain**: Configure with DuckDNS or Cloudflare
- **HTTPS**: Automatic SSL with Caddy
- **Monitoring**: Add Prometheus + Grafana
- **Backups**: Automated Pi backups

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
