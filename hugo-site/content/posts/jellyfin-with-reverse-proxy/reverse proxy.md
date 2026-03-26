# Jellyfin Playback Scenario – Self-Diagnostics & Setup Review

## 🖥️ System Overview

| Component         | Details                                                                                                          |
| ----------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Media Server**  | Jellyfin running on a Raspberry Pi 5 (pilab) at home                                                             |
| **Connectivity**  | Private LAN + Tailscale mesh VPN                                                                                 |
| **Remote Access** | Public URLs: `https://jelly.pilab.space` (via GCP+Caddy), `https://jellyfin.pilab.space` (via Cloudflare Tunnel) |
| **Security**      | TLS via Let’s Encrypt (Caddy) and Cloudflare Tunnel                                                              |
| **Domain**        | `jelly.pilab.space`, `jellyfin.pilab.space`                                                                      |
|                   |                                                                                                                  |

---

## 🔁 Routing Pathways

| Route Name                        | Path                                                                        |
| --------------------------------- | --------------------------------------------------------------------------- |
| **Route 1 – Direct VPN**          | Client → Tailscale VPN → Raspberry Pi (Jellyfin)                            |
| **Route 2 – Reverse Proxy (GCP)** | Client → Cloudflare DNS/Proxy → Caddy (GCP VPS) → Tailscale → Pi (Jellyfin) |
| **Route 3 – Cloudflare Tunnel**   | Client → Cloudflare Tunnel → Raspberry Pi (Jellyfin)                        |

---

## 🔍 Observations

| Method | Performance | CPU Load | Notes |
|--------|-------------|----------|-------|
| **Tailscale VPN** | 🔹 Very fast & smooth | 🔹 Low | Best experience for personal use |
| **GCP Reverse Proxy (`jelly.pilab.space`)** | ⚠️ Slower, higher latency, buffering | ⚠️ High CPU spike on Pi | Involves more hops & encryption overhead |
| **Cloudflare Tunnel (`jellyfin.pilab.space`)** | ✅ Fast & responsive | ✅ No CPU spike on Pi | Performs better than GCP route, suitable for personal & guest use |

---

## 🧪 Test Summary – Cloudflare Tunnel (`jellyfin.pilab.space`)

- ✅ Added `jellyfin.pilab.space` to Cloudflare Tunnel
- ✅ Connected tunnel directly from Cloudflare to Raspberry Pi (port 8096)
- ✅ No GCP or Caddy involved in this path
- ✅ TLS is handled by Cloudflare Tunnel
- ✅ Fast UI & media playback
- ✅ No CPU spike on the Raspberry Pi

---

## 🧠 Questions to Ask Myself

- Why does the GCP+Caddy reverse proxy route cause higher CPU usage and slower playback?
- Should I rely fully on Cloudflare Tunnel and Tailscale instead of maintaining a GCP VPS?
- Is there still a valid reason to use the GCP+Caddy path (e.g., advanced routing, external API integration)?
- What’s the most sustainable, secure, and efficient path for:
  - Personal, high-speed access?
  - Guest-friendly, public web access?

---

## 💡 Possible Hypotheses

| Hypothesis | Explanation |
|------------|-------------|
| **Bandwidth Bottleneck** | GCP VPS may have limited upload/download throughput. |
| **Encryption Overhead** | Multiple TLS/proxy layers (Cloudflare → Caddy → Tailscale) increase CPU load. |
| **CPU Load from Caddy** | Caddy and streaming tasks together may overload the Raspberry Pi. |
| **Extra Hops** | More intermediaries between client and Jellyfin increases latency. |
| **Cloudflare Tunnel Optimization** | Tunnel may be more efficient than proxying for continuous media streams. |
| **Tailscale NAT Latency** | GCP → Pi via Tailscale may take a slower path compared to direct Tailscale or Tunnel. |

---

## ✅ Desired Outcome

- 🔐 **Secure** access for both myself and occasional guests.
- ⚡ **High-performance** playback without CPU spikes or buffering.
- 🤝 **Simple maintenance** — fewer moving parts, no need to manage unnecessary infrastructure (like VPS).
- ☁️ **Domain-level public access** with TLS, but optimized for performance and privacy.

---

## 📌 Related Technologies

| Tool/Service | Role |
|--------------|------|
| **Tailscale** | Private VPN for direct access |
| **Caddy (GCP VPS)** | Reverse proxy + TLS termination |
| **Cloudflare Tunnel** | Public access route directly to Pi |
| **Cloudflare DNS** | Domain + TLS handling |
| **Let’s Encrypt** | Certificate provider used with Caddy |



