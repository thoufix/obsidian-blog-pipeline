---
title: Lab Hardware Inventory
date: 2026-03-27
time: 11:23
tags:
  - homelab
  - hardware
  - inventory
  - infrastructure
created: 2026-03-27T11:23:32+05:30
updated: 2026-03-27T11:23:32+05:30
---

  

# 🖥️ Lab Hardware Inventory

  

> Last checked: **2026-03-27 at 11:23 IST**

> All machines verified online and healthy at time of writing.

  

---

  

## Machines at a Glance

  

| Machine | Role | CPU | RAM | Storage | Temp |

|---|---|---|---|---|---|

| [[#pilab — Raspberry Pi 5\|pilab]] | Workload / Media / CI | ARM Cortex-A76 × 4 @ 2.4 GHz | 8 GB | 238 GB NVMe | 52.1°C |

| [[#pico — Raspberry Pi 4\|pico]] | Control Node / Monitoring | ARM Cortex-A72 × 4 @ 1.8 GHz | 8 GB | 119 GB microSD | 42.8°C |

| [[#Oracle VPS — Cloud VM\|Oracle VPS]] | Ingress / Proxy | AMD EPYC 7551 × 2 vCPU | 1 GB | 46 GB SSD | — |

| [[#OpenWrt Router — TP-Link Archer AX23 v1\|Router]] | Network Routing | MIPS 1004Kc × 4 logical @ ~880 MHz | 128 MB | 8 MB flash | — |

| [[#stellarhost — GCP VM\|stellarhost]] | Unknown / Unused | — | — | — | Unreachable |

  

---

  

## pilab — Raspberry Pi 5

  

> **Local IP:** `10.1.1.118` | **WireGuard IP:** `10.10.0.2` | **SSH:** `pilab`

  

### CPU

- **Model:** ARM Cortex-A76

- **Architecture:** aarch64

- **Cores:** 4 (single-thread per core)

- **Max Clock:** 2400 MHz

- **Min Clock:** 1500 MHz

- **Stepping:** r4p1

- **BogoMIPS:** 108.00

  

### Memory

- **Total RAM:** 7.9 GB

- **Used:** 2.5 GB

- **Available:** 5.4 GB

- **Swap:** 512 MB (3 MB used)

  

### Storage

| Device | Size | Type | Filesystem | Mountpoint |

|---|---|---|---|---|

| nvme0n1 | 238.5 GB | NVMe SSD | — | — |

| nvme0n1p1 | 512 MB | partition | vfat | `/boot/firmware` |

| nvme0n1p2 | 238 GB | partition | ext4 | `/` |

| sda | 28.7 GB | USB disk | — | — |

| sda1 | 28.7 GB | partition | ext4 | — |

  

### System

- **OS:** Debian GNU/Linux 12 (Bookworm)

- **Kernel:** 6.12.62+rpt-rpi-2712

- **Temperature:** 52.1°C

  

### Running Containers (20)

- Woodpecker CI server + agent

- Arr stack: Jackett, Bazarr, Prowlarr, FlareSolverr, qBittorrent, Radarr, Sonarr

- Jellyfin, CouchDB, blog/nginx, Copyparty

- Homepage, Portainer, node-exporter

- Vaultwarden + tunnel, Cloudflare DDNS, Watchtower

  

---

  

## pico — Raspberry Pi 4

  

> **Local IP:** `10.1.1.144` | **WireGuard IP:** `10.10.0.4` | **SSH:** `ssh pico` (key: `pico_ed25519`)

  

### CPU

- **Model:** ARM Cortex-A72

- **Architecture:** aarch64

- **Cores:** 4 (single-thread per core)

- **Max Clock:** 1800 MHz

- **Min Clock:** 600 MHz

- **Stepping:** r0p3

- **BogoMIPS:** 108.00

  

### Memory

- **Total RAM:** 7.6 GB

- **Used:** 843 MB

- **Available:** 6.8 GB

- **Swap:** 2 GB zram (0 used)

  

### Storage

| Device | Size | Type | Filesystem | Mountpoint |

|---|---|---|---|---|

| mmcblk0 | 119.1 GB | microSD | — | — |

| mmcblk0p1 | 512 MB | partition | vfat | `/boot/firmware` |

| mmcblk0p2 | 118.6 GB | partition | ext4 | `/` |

| zram0 | 2 GB | zram | swap | `[SWAP]` |

  

### System

- **OS:** Debian GNU/Linux 13 (Trixie)

- **Kernel:** 6.12.62+rpt-rpi-v8

- **Temperature:** 42.8°C

  

### Running Containers (8)

- Prometheus, Grafana, Glances

- Uptime Kuma, Portainer Agent, node-exporter

- Copyparty, speedtest-exporter ⚠️ (unhealthy)

  

---

  

## Oracle VPS — Cloud VM

  

> **Public IP:** `140.245.244.98` | **WireGuard IP:** `10.10.0.1` | **Internal:** `10.0.0.251`

> **Provider:** Oracle Cloud Infrastructure (OCI) — Always Free tier

  

### CPU

- **Model:** AMD EPYC 7551 32-Core Processor (host)

- **Architecture:** x86_64

- **vCPUs:** 2 (1 core × 2 threads — hyperthreaded)

- **Vendor:** AuthenticAMD

- **Stepping:** 2

- **BogoMIPS:** 3992.49

  

### Memory

- **Total RAM:** 956 MB (~1 GB)

- **Used:** 268 MB

- **Available:** 524 MB

- **Swap:** None ⚠️

  

### Storage

| Device | Size | Type | Filesystem | Mountpoint |

|---|---|---|---|---|

| sda | 46.6 GB | SSD | — | — |

| sda1 | 46.5 GB | partition | ext4 | `/` |

| sda14 | 4 MB | partition | — | — |

| sda15 | 106 MB | partition | vfat | `/boot/efi` |

  

### System

- **OS:** Ubuntu 22.04.5 LTS (Jammy Jellyfish)

- **Kernel:** 6.8.0-1044-oracle

  

### Services

- **WireGuard Hub:** `wg0` — hub for all peers (pilab, pico, Windows PC)

- **Caddy:** Reverse proxy + SSL termination for all `*.pilab.space` domains

  

---

  

## OpenWrt Router — TP-Link Archer AX23 v1

  

> **IP:** `10.1.1.1` | **SSH:** `ssh root@10.1.1.1` (passwordless)

  

### CPU

- **SoC:** MediaTek MT7621 ver:1 eco:3

- **Model:** MIPS 1004Kc V2.15

- **Architecture:** MIPSEL 24kc

- **Cores:** 2 physical cores × 2 VPEs = **4 logical CPUs**

- **Clock:** ~880 MHz

- **BogoMIPS:** 586.13

- **ISA:** MIPS32r2 + DSP + MT ASEs

  

### Memory

- **Total RAM:** 128 MB (~119 MB reported)

- **Used:** 71 MB

- **Available:** 17 MB ⚠️ (tight — limit extra packages)

- **Swap:** None

  

### Storage

- **Flash:** 8.1 MB overlay filesystem

- **Used:** 3.6 MB

- **Free:** 4.5 MB

  

### System

- **OS:** OpenWrt 24.10.0 (r28427-6df0e3d02a)

- **Target:** ramips/mt7621

  

### Network Interfaces

- `br-lan` — LAN bridge (lan1–lan4)

- `wan` — WAN uplink

- `wg0` — WireGuard client to Oracle VPS

- `phy0-ap0`, `phy1-ap0` — WiFi radios (2.4 GHz + 5 GHz)

  

---

  

## stellarhost — GCP VM

  

> **Public IP:** `34.30.244.13` | **SSH:** `thoufics@34.30.244.13` (key: `id_ed25519_gcp`)

> **Provider:** Google Cloud Platform (GCP)

  

> [!warning] Unreachable

> SSH timed out during this check. Machine is likely stopped/deallocated.

> Role is unclear after Oracle VPS was added as the primary ingress node.

  

---

  

## Capability Comparison

  

| | pilab (Pi 5) | pico (Pi 4) | Oracle VPS | Router | stellarhost |

|---|---|---|---|---|---|

| **CPU Arch** | ARM A76 | ARM A72 | x86_64 (EPYC) | MIPS 1004Kc | x86_64 |

| **Logical CPUs** | 4 | 4 | 2 | 4 | — |

| **Max Clock** | 2.4 GHz | 1.8 GHz | ~2.0 GHz (server) | ~880 MHz | — |

| **Single-core perf** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | — |

| **RAM** | 8 GB | 8 GB | 1 GB | 128 MB | — |

| **Storage type** | NVMe SSD | microSD | Cloud SSD | Flash | — |

| **Storage size** | 238 GB | 119 GB | 46 GB | 8 MB | — |

| **Docker** | Yes (20) | Yes (8) | Yes (minimal) | No | — |

| **Best for** | Heavy workloads, media, CI | Monitoring, GitOps | Ingress only | Routing only | — |

  

### Notes

- **pilab** is the clear workhorse — fastest CPU (A76 > A72), NVMe gives it a massive I/O edge over pico's SD card

- **pico** has identical RAM but slower CPU and SD storage — perfectly sized for its lightweight monitoring and control-node role

- **Oracle VPS** is RAM-constrained (1 GB, no swap) — keep it stateless as ingress/proxy only

- **Router** is purpose-built for networking — 17 MB free RAM is a hard ceiling for extra packages

- **stellarhost** role should be re-evaluated; likely replaceable by Oracle VPS for any remaining needs