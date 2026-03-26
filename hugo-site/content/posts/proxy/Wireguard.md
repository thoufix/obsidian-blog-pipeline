---
title: "WireGuard VPN Setup Summary: OpenWrt and Windows Client"
source: ""
author:
published: 2025-03-23
created: 2025-03-15
description: "Setup summary for WireGuard VPN server on OpenWrt and Windows client connection."
tags:
  - "clippings"
---

## Setup Details
- **OpenWrt Router**: IP (LAN) `192.168.1.1`, IP (WAN) `192.168.10.12`, WireGuard IP `10.0.0.1/24`, Port `51820`
- **Windows Client**: WireGuard IP `10.0.0.2/24`, DNS `8.8.8.8`
- **OptiLink Router**: Public IP `59.92.126.43`

## Configuration

### Windows Client Config
```ini
[Interface]
PrivateKey = sEMJAJNEH7mnCnNc6MRPYuy20jpYqsdTFhbgmh62tHg=
Address = 10.0.0.2/24
DNS = 8.8.8.8

[Peer]
PublicKey = fFQNtOVMRh67EqljC3hl8Doiz4cQsRE7TF/vtRtrpmQ=
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = 59.92.126.43:51820
PersistentKeepalive = 25
```

### OpenWrt Firewall Rules
- **Allow Port**: UDP `51820` on WAN
- **VPN Zone**: Input/Output/Forward `ACCEPT`, Masquerading `ON`
- **Forwarding**: `vpn` -> `lan`, `vpn` -> `wan`

## Performance & Notes
- **Direct Streaming**: Works well via BSNL/OptiLink.
- **External Access**: Verified working via Jio network.
- **IPv6**: Included in routing (`::/0`) but untested.
