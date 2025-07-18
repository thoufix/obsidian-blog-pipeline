---
title: "Jellyfin Remote Access"
date: 2025-07-18
slug: jellyfin-remote
summary: "Access Jellyfin from anywhere using a secure setup."
---
## Overview  

This setup describes how to securely access a self-hosted **Jellyfin media server** running on a Raspberry Pi from anywhere on the internet using:

- A **free-tier VPS from Google Cloud Platform (GCP)**
- **Caddy** as a reverse proxy
- **Tailscale** for private connectivity between the VPS and Raspberry Pi
- **Cloudflare DNS** to map a public domain (e.g. `jelly.pilab.space`) to the VPS
---
## Architecture

```text

Client (Browser)

   ↓

Cloudflare DNS

   ↓

GCP VPS (Caddy Reverse Proxy)

   ↓

Tailscale VPN

   ↓

Raspberry Pi (Jellyfin server)

```

---
## Requirements

- ✅ A working **Jellyfin** instance on your home server (e.g. Raspberry Pi)

- ✅ A **Cloudflare** account managing your domain (e.g. `pilab.space`)

- ✅ A **free-tier VPS** (e.g. f1-micro on GCP)

- ✅ **Tailscale** installed on both Pi and VPS

- ✅ **Caddy** installed on the VPS

- ✅ Your domain must point to your VPS's **public IP**

---
## GCP VPS Setup

- **Instance Type**: `e2-micro` (under Always Free Tier)

- **OS**: Debian 12 minimal (or Ubuntu 22.04)

- **Firewall**: Allow TCP ports `80` and `443`

- **Hostname**: You can optionally assign a static external IP

---

## Step-by-Step Setup

### 1. Connect Pi and VPS over Tailscale

Install and authenticate Tailscale on both machines.

```bash

# On both VPS and Pi

curl -fsSL https://tailscale.com/install.sh | sh

sudo tailscale up

```

  

- Make note of the Pi's **Tailscale IP** (e.g. `100.x.x.x`)

- Ensure both can ping each other
---
### 2. Point Your Domain to the VPS

In your **Cloudflare DNS settings**, add:

- `A record`: `jelly.pilab.space → <VPS Public IP>`

- **Disable the orange cloud** (proxy mode) initially during testing

Wait for DNS to propagate. Confirm using:  

```bash

dig jelly.pilab.space +short

```
  

---
### 3. Install and Configure Caddy on VPS

  
Install Caddy:


```bash

sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https

curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg

curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list

sudo apt update && sudo apt install caddy

```

  
Then configure the Caddyfile:


```caddyfile

# /etc/caddy/Caddyfile

jelly.pilab.space {

    reverse_proxy 100.x.x.x:8096

}

```
  

Replace `100.x.x.x` with your **Pi’s Tailscale IP**.

---
### 4. Restart Caddy and Check HTTPS

```bash

sudo systemctl restart caddy

sudo systemctl status caddy

```

  
Caddy will automatically obtain and renew SSL certificates from Let's Encrypt.

---
### 5. Access Jellyfin from Anywhere

Visit:

```

https://jelly.pilab.space

```

and enjoy secure access to your media library, even remotely!

---

## Performance Notes

  
- 📉 **GCP VPS (f1-micro)** is suitable for routing traffic, but it **isn't optimized for video transcoding or heavy CPU load**.

- ✅ **Direct streaming (no transcoding)** works well via this architecture.

- 💡 For faster performance, **Cloudflare Tunnel** performs better in most cases compared to GCP reverse proxy, but this architecture is cloud-vendor agnostic and fully open source.
  
---
## Why Use This Architecture?

- 🔐 All traffic is end-to-end encrypted (HTTPS + Tailscale)

- ☁️ Your Pi stays **private** behind CGNAT/firewall

- 🌍 You get a **public domain URL** without needing port forwarding

- 💵 All services used are **free or have generous free tiers**

---
## Related Alternatives

  
| Method                  | Description                                                 |

|------------------------|-------------------------------------------------------------|

| Cloudflare Tunnel      | Fast and secure, but uses Cloudflare proxy layer            |

| Tailscale Funnel       | P2P-like setup, but only available with Tailscale Pro plans |

| Port forwarding (ISP)  | Risky & less secure, not viable under CGNAT                 |

---
## Final Thoughts

This architecture gives you full control over your reverse proxy and secure media streaming setup using industry-standard tools. It balances simplicity, privacy, and performance with minimal recurring costs.