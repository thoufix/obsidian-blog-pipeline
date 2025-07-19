---
title: Telegram Automation with n8n and Raspberry Pi
tags: [automation, raspberry-pi, telegram, n8n, bot]
aliases: [telegram bot automation, n8n telegram raspberry pi]
created: 2025-07-19
updated: 2025-07-19
---

# 🤖 Telegram Automation with n8n and Raspberry Pi

## 📝 Overview

This project integrates **n8n**, a powerful open-source workflow automation tool, with **Telegram**, allowing real-time control and monitoring of your **Raspberry Pi 5 (pilab)**.

You can:

- Receive **alerts** (CPU, RAM, disk, etc.) directly via Telegram  
- **Send commands** like `/restart_jellyfin` to trigger shell scripts or systemd services  
- Automate status updates, reboot notices, download completions, and more  

---

## 🧱 Project Components

| Component       | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| Raspberry Pi 5 | Host machine for n8n and system automation                                  |
| n8n            | Workflow orchestrator with UI + webhooks                                    |
| Telegram Bot   | Created via [BotFather](https://t.me/BotFather), receives and sends messages |
| Shell Scripts  | Executes tasks on Pi like service restarts, logs                            |
| Cron / Schedulers | Optional timed triggers in n8n                                           |

---

## 🚦 Sample Use Cases

- 🔔 **Alert** when CPU > 85% or RAM > 90%  
- 📦 Notify when download to `/downloads/complete` finishes  
- 🧹 Run cleanup script via `/clean_temp` command  
- 🟢 `/start_jellyfin` → starts media server  
- 🔴 `/stop_jellyfin` → stops service  

---

## 🌐 Workflow Architecture

```
User ↔ Telegram Bot ↔ n8n (HTTP Trigger Node) ↔ Execute Shell Command on Pi
                         ↕
                 Schedule Nodes for Periodic Alerts
```

---

## 🔐 Security Tips

- Use `SECRET_COMMAND` prefixes for sensitive triggers (e.g. `/secure_restart`)  
- Store bot token in `.env` or n8n credential vault  
- Limit who can talk to your bot (via Telegram user ID check in n8n)  

---

## 🧰 What’s Next?

- [ ] Create Telegram bot and get token  
- [ ] Set up n8n on pilab and expose webhook (e.g., via Tailscale/Cloudflare Tunnel)  
- [ ] Build basic alert + command workflow  
- [ ] Test end-to-end with simple shell script trigger
- [ ] need to stop jellyfin and want to spin up whenever I need 
- [ ] like that I need prowlarr and sonarr and radarr to stop and spin up whenever I need 