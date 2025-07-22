---
title: mpv.io (Media Player)
date: 2025-07-10
summary: MPV config + keybindings backup
tags:
  - mpv
  - media
  - backup
---

# 🎥 MPV Configuration

## 📄 `mpv.conf`

```ini
# ================================
# ▶️ Playback Settings
# ================================
hwdec=auto-safe          # Use safe hardware decoding
vo=gpu                   # Use GPU video output
profile=fast             # Fast performance profile
hr-seek=yes              # High-resolution (accurate) seeking

# ================================
# 🔁 Caching (for smooth streaming)
# ================================
cache=yes                # Enable caching
cache-secs=60            # Buffer 60 seconds ahead

# ================================
# 📺 YouTube / Streaming Settings
# ================================
ytdl-format=bv*+ba/best                              # Best video+audio format
script-opts=ytdl_hook-ytdl_path=C:\\Tools\\yt-dlp\\yt-dlp.exe  # Path to yt-dlp

# ================================
# 📝 Subtitle Settings
# ================================
sub-font-size=25         # Subtitle font size
sub-auto=fuzzy           # Auto-load subtitles with fuzzy match
sub-ass-override=force   # Override embedded styling

# ================================
# 🖥️ Interface and Behavior
# ================================
osc=no                   # Disable on-screen controller
save-position-on-quit    # Resume from last position
idle=once                # Idle after playback ends, then quit
keep-open=yes            # Keep window open after playback
autoload-files=yes       # Automatically load similar media files

# ================================
# 🛠️ Logging and OSD
# ================================
log-file=~/mpv.log       # Log output to file
osd-bar=yes              # Enable OSD progress bar
```

- `hwdec=auto-safe`: Enables hardware decoding safely
- `vo=gpu`: GPU-based video output
- `osc=no`: Disables on-screen controller for minimal UI
- `ytdl_hook-ytdl_path`: Uses local `yt-dlp.exe` for streaming

---

## 🎮 `input.conf` – Key Bindings

```conf
# Disable default behavior for 'r'
r ignore
r cycle video-rotate

# Rotate video using number keys
1 set video-rotate 0
2 set video-rotate 90
3 set video-rotate 180
4 set video-rotate 270

# Toggle stats
e script-binding stats/display-stats
E script-binding stats/display-stats-toggle
```

💡 Useful when watching portrait videos or debugging with stats overlay.

---

## 🗂 Folder Backup

Path: `C:\Users\AI\AppData\Roaming\mpv`

- ✅ `mpv.conf` – Settings
- ✅ `input.conf` – Custom keybindings
- ✅ `scripts/` – Lua or JS extensions
- ✅ `script-opts/` – Script-specific configs
- ✅ `fonts/` – Fonts for OSD/subtitles

---

## 🔄 Backup Instructions

1. Open PowerShell
2. Run:
   ```powershell
   Compress-Archive -Path "$env:APPDATA\mpv" -DestinationPath "$env:USERPROFILE\Desktop\mpv-backup.zip"
   ```

To restore:
```powershell
Expand-Archive -Path "$env:USERPROFILE\Desktop\mpv-backup.zip" -DestinationPath "$env:APPDATA"
```

---

