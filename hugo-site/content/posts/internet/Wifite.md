Kali on Raspberry Pi 4, headless

---

### # Wifite workflow — Safe start/stop scripts (Nexmon + Pi)

> Quick reference you can paste into Obsidian. Keeps your Pi safe when enabling monitor/injection for `wifite`, and restores network after testing.

---

## Why keep this

- The Raspberry Pi internal Broadcom Wi‑Fi (with Nexmon firmware) can be made to support monitor + injection, but system services (NetworkManager, wpa_supplicant, dhcpcd) often interfere.
    
- These scripts put the system into a clean state for `wifite`, and restore it afterward, saving your SSH/Tailscale session where possible.
    
- Also documents common pitfalls (`Undervoltage detected!`) and manual recovery steps.
    

---

## Safety notes

- **If you're SSH'd in:** these scripts warn you before continuing and save service states so they can be restored. Still, stopping network services may drop your SSH session—use local console when possible.
    
- **Power:** repeated `Undervoltage detected!` messages mean your power supply is unstable. Use a good 5V 3A+ USB‑C supply or a powered USB hub for dongles.
    
- **Persistence:** `mon0` (monitor interface) created manually will not necessarily persist after reboot. Re-run the start script after reboot, or create a systemd service if you need persistence.
    

---

## Paste-ready: `~/start-wifite.sh`

```bash
#!/usr/bin/env bash
set -eu

# Warn if likely remote SSH (if SSH_CONNECTION exists, we will still continue but warn)
if [ -n "${SSH_CONNECTION:-}" ]; then
  echo "WARNING: You're over SSH. Running this may drop the connection. Continue in 5s (Ctrl-C to abort)..."
  sleep 5
fi

# Save current service states so we can restore them later
services=(NetworkManager wpa_supplicant dhcpcd)
declare -A BEFORE_STATE
for s in "${services[@]}"; do
  if systemctl list-unit-files --type=service | grep -q "^${s}.service"; then
    BEFORE_STATE[$s]=$(systemctl is-enabled --quiet "$s" && echo enabled || echo disabled) || BEFORE_STATE[$s]=disabled
    BEFORE_STATE["$s,running"]=$(systemctl is-active --quiet "$s" && echo running || echo stopped)
  else
    BEFORE_STATE[$s]=absent
    BEFORE_STATE["$s,running"]=absent
  fi
done

# Persist the BEFORE_STATE so stop script can read it (in /tmp)
statefile="/tmp/wifite_service_state_$$"
declare -p BEFORE_STATE > "$statefile"

# Stop interfering services
sudo systemctl stop NetworkManager wpa_supplicant 2>/dev/null || true
sudo systemctl stop dhcpcd 2>/dev/null || true

# Ensure wlan0 in managed mode then up
sudo ip link set wlan0 down 2>/dev/null || true
sudo iw dev wlan0 set type managed 2>/dev/null || true
sudo ip link set wlan0 up

# Remove lingering monitor interfaces (safe)
for ifn in $(iw dev | awk '/Interface/ {print $2}'); do
  if [[ "$ifn" == mon* || "$ifn" == wlan*mon ]]; then
    sudo ip link set "$ifn" down 2>/dev/null || true
    sudo iw dev "$ifn" del 2>/dev/null || true
  fi
done

echo "[+] Ready for 'sudo wifite' (monitor/injection prepped). Service state saved: $statefile"
```

---

## Paste-ready: `~/stop-wifite.sh`

```bash
#!/usr/bin/env bash
set -eu

statefile_glob="/tmp/wifite_service_state_*"
# pick the latest statefile (safe for multiple runs)
statefile=$(ls -t $statefile_glob 2>/dev/null | head -n1 || true)
if [ -z "$statefile" ]; then
  echo "No saved service state found in /tmp. Will try a sensible restore."
fi

# Kill attack/sniff processes
sudo pkill -f "airodump-ng|aireplay-ng|wifite" 2>/dev/null || true

# Delete any monitor interfaces we created
for ifn in $(iw dev | awk '/Interface/ {print $2}'); do
  if [[ "$ifn" == mon* || "$ifn" == wlan*mon ]]; then
    sudo ip link set "$ifn" down 2>/dev/null || true
    sudo iw dev "$ifn" del 2>/dev/null || true
  fi
done
sudo hcxdumptool -i wlan0 --enable_status=1 -o capture.pcapng
# Put wlan0 back to managed and up
sudo iw dev wlan0 set type managed 2>/dev/null || true
sudo ip link set wlan0 up 2>/dev/null || true

# Restore services from statefile if present
if [ -n "$statefile" ]; then
  # shellcheck disable=SC1090
  eval "$(sed -n '1,200p' "$statefile")"  # restores BEFORE_STATE associative array
  for s in NetworkManager wpa_supplicant dhcpcd; do
    val=${BEFORE_STATE[$s]:-absent}
    runstate=${BEFORE_STATE["$s,running"]:-absent}
    if [ "$val" = "enabled" ]; then
      sudo systemctl enable "$s" 2>/dev/null || true
    fi
    if [ "$runstate" = "running" ]; then
      sudo systemctl start "$s" 2>/dev/null || true
    fi
  done
  # remove statefile to avoid confusion later
  rm -f "$statefile"
else
  # Best-effort start services
  sudo systemctl start NetworkManager 2>/dev/null || true
  sudo systemctl start dhcpcd 2>/dev/null || true
fi

echo "[+] Network restored. If you used SSH/Tailscale and lost connectivity, reconnect now."
```

---

## Usage

1. Make the scripts executable:
    

```bash
chmod +x ~/start-wifite.sh ~/stop-wifite.sh
```

2. Start the safe state then run `wifite`:
    

```bash
~/start-wifite.sh
sudo wifite -i mon0    # or: sudo wifite (it will enable monitor on wlan0)
```

3. When finished, stop and restore:
    

```bash
~/stop-wifite.sh
```

---

## Manual quick commands (one-shot)

If you prefer to run commands manually instead of scripts, this sequence recreates what the scripts do:

```bash
sudo systemctl stop NetworkManager wpa_supplicant
sudo systemctl stop dhcpcd
sudo ip link set wlan0 down
sudo modprobe -r brcmfmac brcmutil || true
sudo modprobe brcmfmac
sudo iw phy phy0 interface add mon0 type monitor
sudo ip link set mon0 up
sudo iw dev
# test injection
sudo airodump-ng mon0 --band abg & sleep 6; sudo pkill airodump-ng
sudo aireplay-ng --test mon0
```

---

## Troubleshooting

- **`Undervoltage detected!`**: Use a better PSU (5V 3A+), or a powered USB hub for dongles.
    
- **`Operation not supported` when adding monitor interface**: ensure `brcmfmac` is Nexmon-patched and you reloaded the module after installing the Nexmon firmware. Re-run `modprobe -r brcmfmac; modprobe brcmfmac`.
    
- **`airodump` sees APs but wifite sees 0 targets**: create `mon0` via the `iw phy` method above and ensure `aireplay-ng --test mon0` returns `Injection is working!`.
    

---

## Making the workflow persist (optional)

If you want `mon0` created automatically at boot (advanced), create a small systemd service that runs the `iw phy` + `ip link` commands early in boot. Note: this may interfere with normal wifi-managed connections; do this only if you understand the implications.

---

## References

- Nexmon: [https://github.com/seemoo-lab/nexmon](https://github.com/seemoo-lab/nexmon)
    
- Aircrack-ng: [https://www.aircrack-ng.org/](https://www.aircrack-ng.org/)
    

---

_Save this file in Obsidian as your canonical runbook for `wifite` on Raspberry Pi (Nexmon)._