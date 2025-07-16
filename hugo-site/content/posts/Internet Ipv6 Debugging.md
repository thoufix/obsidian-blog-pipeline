## Problem Statement

After rebooting the OpenWrt router or Raspberry Pi, IPv6 connectivity breaks on clients (especially on the Raspberry Pi), even though an IPv6 address is assigned. Services like `ping6 google.com` fail, DNS resolution becomes slow, and the Pi often reverts to IPv4-only behavior.

IPv4 connectivity remains stable and unaffected.

