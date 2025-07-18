---
title: Monitor jellyfin speed and CPU spikes
date: 2025-07-18
slug: jellyfin-remote
summary: Results of all three ways of accessing jellyfin
series: jellyfin
---

## System Snapshot Comparison: Full Analysis

## System Overview

All snapshots were recorded from a Debain Bookworm-based Raspberry Pi 5 (Cortex-A76, 4 CPU cores, 8GB RAM, NVMe SSD root), running a similar stack of media, storage, and proxy services. Below is a direct comparative analysis of all available logs, including before and during usage of Cloudflare Tunnel, tailscale, and Google Cloud reverse proxy routing.

## Key Metrics Across All Snapshots

| Metric             | Previous Reports                                    | Cloudflare Tunnel log                    | GCP Reverse Proxy log                        |
| ------------------ | --------------------------------------------------- | ---------------------------------------- | -------------------------------------------- |
| **OS/Platform**    | Debian Bookworm, kernel 6.12.34, aarch64            | Same                                     | Same                                         |
| **CPU**            | 4x Cortex-A76                                       | Same                                     | Same                                         |
| **Memory (Total)** | 8063 MB                                             | 8063 MB                                  | 8063 MB                                      |
| **Memory (Used)**  | ~2800–3040 MB                                       | ~3000–3100 MB                            | ~3000 MB                                     |
| **Memory (Free)**  | ~320–400 MB                                         | 250–310 MB                               | 280–297 MB                                   |
| **Swap Used**      | 2 MB                                                | 2 MB                                     | 2 MB                                         |
| **Disk / Root**    | 235 GB total, 153 GB used, 69% usage                | No change                                | No change                                    |
| **CPU Usage**      | 1–8% base, rare peaks                               | More bursty (up to 10–12%)               | More bursty (up to ~8%), some intervals 2–5% |
| **Load Average**   | 0.13–0.20                                           | 0.18–0.31 (with peaks ~0.53)             | 0.23–0.53 (with transient peaks)             |
| **Disk I/O**       | Very light (rare spikes)                            | Slightly elevated, more bursts           | More bursts, but unsaturated                 |
| **Top Processes**  | Media stack (Jellyfin, Sonarr, Radarr, etc), Docker | Same plus Cloudflared roles more visible | Caddy, Cloudflared, Docker, etc.             |
| **Network**        | Not detailed/normal                                 | Tunnel: no bottlenecks                   | GCP: not detail, but stable                  |

## Detailed Observations

## 1. **CPU & Memory Usage Patterns**

- **Base usage consistently low:** Core system remains 94–98% idle in all logs.
    
- **Cloudflare/GCP Tunnels introduce occasional bursts:** Tunnel daemons (cloudflared/tailscaled) and media processes (Jellyfin, etc.) show short CPU and RAM spikes, which do not lead to prolonged high utilization.
    
- **High process count:** All logs show ~360–370 processes running, but only 1–2 in running state.
    

## 2. **Disk and I/O**

- **Storage utilization unchanged:** Disk usage stays at 69% of root NVMe, indicating no significant data growth.
    
- **I/O slightly more variable in tunnel logs:** More frequent write spikes (up to 73–249 KB/s), but overall %util never approaches disk bottleneck (always <1% most of the time).
    

## 3. **Memory and Swap**

- **Free memory slightly decreasing trend:** From ~400 MB free in early reports, now hovers between 276–297 MB free with similar cache/buffer sizes. This is still healthy for an 8GB RAM system.
    
- **Swap essentially unused:** All snapshots report 2 MB swap usage, indicating no memory pressure or thrashing.
    

## 4. **Process Landscape**

- **Consistent stack:** Docker, Jellyfin, Sonarr, Radarr, Prowlarr, Minio, Immich, Caddy, Nginx, Cloudflared, Tailscaled, Backup, etc. always visible.
    
- **Cloudflared and Tailscaled:** Prominent only in tunnel snapshots, showing slightly increased %CPU during bursts.
    
- **No abnormal OOM-kills or zombie processes across any sample.**
    

## 5. **Load Average**

- **Generally low:** Even during highest sampling, load averages top out at 0.53, well below even 1.0—meaning the 4-core system is rarely loaded more than ~1/8th of its full capability.
    

## 6. **Network**

- **No bottlenecks in any sample:** Outbound and inbound, the network is not under strain, with all services reporting healthy states.
    

## Summary Table of Key Differences

| Area           | Early Snapshots       | Tunnel Snapshots           | GCP Reverse Proxy Snapshot | Change/Trend                      |
| -------------- | --------------------- | -------------------------- | -------------------------- | --------------------------------- |
| CPU            | Idle, <8% typical     | Occasional peaks up to 12% | Occasional peaks to ~8%    | More frequent, short-lived bursts |
| RAM            | ~2.8–3.0 GB used      | ~3.0–3.1 GB used           | ~3.0 GB used               | Slightly higher, by ~200 MB       |
| Disk I/O       | Occasional low spikes | More frequent, mid spikes  | Frequent small bursts      | Mild increase, but not impactful  |
| Processes      | Media, Docker         | +Cloudflared prominent     | +Cloudflared, +Caddy       | Only process profile varies       |
| Swap           | 2 MB                  | 2 MB                       | 2 MB                       | No change                         |
| Load Avg       | 0.13–0.20             | 0.18–0.53 (peak at 0.53)   | 0.23–0.53                  | Small increases during load       |
| Service Errors | None                  | None                       | None                       | All remain healthy                |

## Practical Implications

- **No major resource or system health issues are present in any report.**
    
- **Recent logs (Tunnel/Proxy) show modest, expected increases in CPU/memory/disk I/O volatility**—a direct consequence of routing and encryption overhead, but still with ample resource headroom.
    
- **Service stack remains stable and responsive:** No indications of contention or memory/CPU starvation, no services killed.
    
- **Performance headroom remains high:** All critical metrics are well within safe operational ranges.
    

## Conclusion

The core difference when using Cloudflare or GCP tunnels is a **slightly brisker pace of short-lived resource spikes**, mainly in CPU and disk I/O, with a gradual minor reduction in free memory. Overall load, memory, and disk utilization remain healthy, with the server continuing to exhibit robust stability and reserve capacity for additional demand.

_No critical bottlenecks are detected; small increases in system turbulence are expected and well within Raspberry Pi 5's capabilities._
