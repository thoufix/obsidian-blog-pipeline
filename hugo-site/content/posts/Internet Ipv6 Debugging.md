## Problem Statement

After rebooting the OpenWrt router or Raspberry Pi, IPv6 connectivity breaks on clients (especially on the Raspberry Pi), even though an IPv6 address is assigned. Services like `ping6 google.com` fail, DNS resolution becomes slow, and the Pi often reverts to IPv4-only behavior.

IPv4 connectivity remains stable and unaffected.

## Devices Involved

* OpenWrt router (TP-Link AX23)
* ISP ONT router (primary, ACT Fibernet)
* Raspberry Pi 4 (pico)
* Raspberry Pi 5 (pilab)
* Windows laptop
* Tailscale installed on pilab, pico, and Windows

## Goals

1. Keep IPv6 enabled on OpenWrt.
2. Ensure clients (e.g., Raspberry Pi) receive usable IPv6 with working routing.
3. Prevent breakage of IPv6 routing after reboots.

---

## What I Tried

### Prefix Delegation

* Confirmed that ONT provides a /64 prefix via DHCPv6.
* Attempted to increase the requested prefix:

  ```bash
  uci set network.wan6.reqprefix='56'
  uci commit network
  /etc/init.d/network restart
  ```

  * Result: Still only received /64 prefix.

### RA and DHCPv6 Tuning

* Adjusted RA and DHCPv6 settings on LAN:

  ```bash
  uci set dhcp.lan.dhcpv6='server'
  uci set dhcp.lan.ra='server'
  uci set dhcp.lan.ra_management='1'
  uci commit dhcp
  /etc/init.d/odhcpd restart
  ```

### Firewall Rules

* Added rules to allow ICMPv6 and forwarding.
* Tried IPv6 masquerading:

  ```bash
  uci set firewall.@zone[1].masq6='1'
  uci commit firewall
  /etc/init.d/firewall restart
  ```

  * Result: IPv6 routing worked temporarily, but internet speed slowed significantly.

### Disabled Masquerading

* Reverted masquerading and flow offloading:

  ```bash
  uci delete firewall.@zone[1].masq6
  uci delete firewall.@defaults[0].flow_offloading
  uci delete firewall.@defaults[0].flow_offloading_hw
  uci commit firewall
  /etc/init.d/firewall restart
  ```

### Disabled IPv6 on LAN as Temporary Fix

* Disabled IPv6 on LAN to avoid connectivity issues:

  ```bash
  uci set network.lan.ipv6='0'
  uci set dhcp.lan.dhcpv6='disabled'
  uci set dhcp.lan.ra='disabled'
  uci commit
  /etc/init.d/network restart
  ```

### Confirmed DHCPv6 Addressing from ONT

* ONT router delegates a global IPv6 address:

  ```json
  "ipv6-address": [
    {
      "address": "2406:7400:bb:a723:f209:dff:fe2d:b569",
      "mask": 64
    }
  ]
  ```

### Tested Connectivity from Clients

* Clients receive global IPv6 but experience routing failure unless masquerading is used.
* `ping6 google.com` fails without masquerading but works with it (albeit slowly).

### Reconnected Client Directly to ONT Wi-Fi

* Connected Raspberry Pi (pico) directly to ONT router (SSID: PiFi\_5G).
* Received IPv6 address:

  ```
  inet6 2406:7400:bb:a723::13e/128
  ```
* Still failed to ping google.com until IPv6 route was restored manually.

### Additional Configuration State Captured

* WAN6 UCI settings:

  ```bash
  uci show network.wan6
  # output includes reqprefix=auto, reqaddress=try, extendprefix=1, norelease=1, delegate=1, accept_ra=0
  ```
* LAN UCI settings:

  ```bash
  uci show network.lan
  # includes ip6assign=64, ip6ra=server, dhcpv6=server, ip6prefix, ip6addr (ULA), etc.
  ```
* DHCP LAN settings:

  ```bash
  uci show dhcp.lan
  # dhcpv6=server, ra=server, ra_flags='managed-config other-config', ra_default=1, custom DNS set
  ```
* Verified successful IPv6 ping:

  ```bash
  ping6 -c 4 2001:4860:4860::8888
  ```
* IPv6 routing table observed:

  ```bash
  ip -6 route show
  # includes default route via WAN, unreachable route to ip6prefix, etc.
  ```
* ip6tables/iptables not found on the system.

### Tailscale

* Tailscale is already installed on pilab, pico, and Windows.
* Decided not to install on OpenWrt as the devices already maintain direct mesh.

---

## Questions for ISP 

1. Can you delegate more than a /64 IPv6 prefix? (e.g., /56)
2. Is prefix delegation stable across reboots?
3. Are there any DHCPv6 options required by the ONT for clients to retain IPv6?
4. Can the TP-Link ONT router forward RA or delegated prefixes properly?

---

## Conclusion

The issue likely lies with how the ONT handles DHCPv6 prefix delegation or RA. Temporary fixes like masquerading or disabling IPv6 on LAN are not ideal. A more robust solution will require cooperation from the ISP or switching to a fully bridged ONT setup.

The journal captures all diagnostic steps, changes, and their results, and can be referred back to for future adjustments or escalation.

```mermaid
graph LR
    subgraph Internet
        I[Internet (IPv6)]
    end

    subgraph ISP_Network[ISP Network]
        ISP_ONT[ISP ONT Router] --- I
    end

    subgraph Home_Network[Your Home Network]
        ISP_ONT --- WAN[OpenWrt Router - WAN Interface]
        WAN -- IPv4/IPv6 Traffic --> OpenWrt[OpenWrt Router]
        OpenWrt --- LAN[OpenWrt Router - LAN Interface]

        subgraph LAN_Clients[LAN Clients (Wireless/Wired)]
            LAN --- RP4[Raspberry Pi 4 - pico]
            LAN --- RP5[Raspberry Pi 5 - pilab]
            LAN --- WL[Windows Laptop]
        end
    end

    subgraph Problem_Area[Problem Area]
        direction LR
        ISP_ONT -- Delegates /64 Prefix --> OpenWrt
        OpenWrt -- Assigns IPv6 Addresses (via RA/DHCPv6) --> LAN_Clients

        subgraph IPv6_Issue[IPv6 Connectivity Issue]
            direction TB
            RP4_FAIL[RP4: ping6 google.com fails after reboot]
            RP5_FAIL[RP5: ping6 google.com fails after reboot]
            WL_SLOW[WL: DNS slow, IPv4-only behavior]
        end

        ISP_ONT -- Direct Connect --> RP4_DIRECT[RP4 direct to ONT WiFi]
        RP4_DIRECT -- Still Fails Ping6 --> IPv6_ROUTE_ISSUE[IPv6 Routing Issue]
    end

    %% Styling
    style OpenWrt fill:#f9f,stroke:#333,stroke-width:2px
    style ISP_ONT fill:#f9f,stroke:#333,stroke-width:2px
    style LAN_Clients fill:#f9f,stroke:#333,stroke-width:2px
    style IPv6_Issue fill:#fcc,stroke:#333,stroke-width:2px
    style IPv6_ROUTE_ISSUE fill:#fcc,stroke:#333,stroke-width:2px

    %% Flow Arrows
    I -- IPv6 Traffic --> ISP_ONT
    ISP_ONT -- IPv6 Prefix Delegation (/64) --> WAN
    WAN -- IPv6 Traffic (Router Advertisement / DHCPv6) --> OpenWrt
    OpenWrt -- IPv6 Traffic (Router Advertisement / DHCPv6) --> LAN
    LAN -- IPv6 Addresses / Routing Attempts --> RP4
    LAN -- IPv6 Addresses / Routing Attempts --> RP5
    LAN -- IPv6 Addresses / Routing Attempts --> WL

    RP4 -- IPv6 Ping Fail --> RP4_FAIL
    RP5 -- IPv6 Ping Fail --> RP5_FAIL
    WL -- IPv6 Slowness --> WL_SLOW

    %% Tried Solutions (as notes)
    OpenWrt -- Attempts Prefix Delegation /56 (Failed) --> OpenWrt
    OpenWrt -- RA/DHCPv6 Tuning --> OpenWrt
    OpenWrt -- Firewall Rules (Masquerading - Temporary Fix, Slow) --> OpenWrt
    OpenWrt -- Disable Masquerading / Flow Offloading --> OpenWrt
    OpenWrt -- Disable IPv6 on LAN (Temporary Fix) --> OpenWrt

    ISP_ONT -- Confirmed DHCPv6 Address Delegation --> OpenWrt
    RP4_DIRECT -- Confirmed IPv6 Address (but no routing) --> ISP_ONT

    %% Tailscale (External to IPv6 routing problem)
    RP4 -.-> TS[Tailscale Mesh]
    RP5 -.-> TS
    WL -.-> TS

    %% Problem Summary
    IPv6_Issue -- "IPv6 breaks after reboot, despite address assignment" --> ISP_ONT
    IPv6_Issue -- "Problem: Usable IPv6 with working routing after reboots" --> OpenWrt
    IPv6_Issue -- "Root Cause Suspected: ONT DHCPv6 Prefix Delegation / RA Handling" --> ISP_ONT
```
