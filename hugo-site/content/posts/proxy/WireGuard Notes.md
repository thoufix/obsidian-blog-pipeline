---
title: "WireGuard Notes & Troubleshooting"
source: ""
author:
published: 2025-10-29
created: 2025-05-01
description: "Detailed WireGuard notes, key pairs, and troubleshooting attempts for Pilab Remote access."
tags:
  - "clippings"
---

## Key Pairs

### Server (OpenWrt)
- **Public Key**: `foZIK8sepTNbdK4MRH/VII9bT1eeurrZA18ixqqJVBI=`
- **Private Key**: `iJjeRLpQ2b1hp/O0Ya6TsBfqDYbAW4a4q9dbCEnzjEA=`

### Windows Client
- **Public Key**: `IaqWx3hrRnSxsuRZ3gHFmJ3vLV1AIU0Be38iT8ON4zQ=`
- **Private Key**: `4GwhgS4r0daD+BGEiGbOwn+B5Q6X2Ojth/YSjUyUknE=`

## Configurations

### Client Config (Public IP attempt)
```ini
[Interface]
PrivateKey = 4GwhgS4r0daD+BGEiGbOwn+B5Q6X2Ojth/YSjUyUknE=
Address = 10.0.0.2/24, fd42:42:42::2/64
DNS = 1.1.1.1, 1.0.0.1

[Peer]
PublicKey = foZIK8sepTNbdK4MRH/VII9bT1eeurrZA18ixqqJVBI=
AllowedIPs = 10.0.0.0/24, 10.1.1.0/24, 0.0.0.0/0, ::/0
Endpoint = 183.82.25.90:51820
PersistentKeepalive = 25
```

## Troubleshooting Notes
- **Current Public IP (as of setup)**: `183.82.25.90`
- **Issue**: No handshake and no internet access despite correct endpoint and config.
- **Verification Commands**:
  - Server: `wg show`
  - Client: `ping 10.0.0.1`
