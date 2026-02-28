---
title: mpv.io (Media Player)
date: 2025-07-10
summary: MPV config + keybindings backup
tags:
  - mpv
  - media
  - backup
---

# ðŸŽ¥ MPV Configuration

## ðŸ“„ `mpv.conf`

```ini
# â–¶ï¸ Playback Settings
vo=gpu-next                  # Modern GPU output for better speed
hwdec=auto-safe               # Use hardware decoding if possible
profile=fast
hr-seek=yes
video-sync=display-resample
interpolation=yes

# ================================
# ðŸ” Caching
# ================================
cache=yes
cache-secs=30
demuxer-max-bytes=200MiB
demuxer-max-back-bytes=50MiB
demuxer-readahead-secs=10
stream-buffer-size=32768

# ================================
# ðŸ“º YouTube High Quality
# ================================
ytdl-format=bestvideo[vcodec^=av01]+bestaudio/bestvideo[vcodec^=vp9]+bestaudio/best

ytdl-raw-options=\
    no-part,\
    no-mtime,\
    no-subs,\
    cookies=C:\Users\AI\cookies\instagram.txt,\
    extractor-retries=2,\
    fragment-retries=2,\
    http-chunk-size=1048576,\
    format-sort=size,br,res,fps,\
    format-sort-force=yes


network-timeout=15

# ================================
# ðŸ“ Subtitles
# ================================
sub-auto=no
sub-ass-override=force
sub-font='SF Pro Display'
sub-font-size=24
sub-color='#FFFFFF'
sub-border-color='#73000000'   # Black with ~45% opacity (AARRGGBB hex)
sub-border-size=2.5
sub-shadow-offset=0
sub-margin-y=15

# ================================
# ðŸ–¥ï¸ Interface
# ================================
osc=no
save-position-on-quit=yes
idle=once
keep-open=yes
autoload-files=yes
video-zoom=0
video-unscaled=no
keepaspect=yes
autofit=960x540

# ================================
# ðŸ› ï¸ Logging
# ================================
osd-bar=yes
osd-on-seek=msg-bar
osd-duration=2000
msg-level=all=v

# Cursor
cursor-autohide=1000
cursor-autohide-fs-only=no
```

- `hwdec=auto-safe`: Enables hardware decoding safely
- `vo=gpu`: GPU-based video output
- `osc=no`: Disables on-screen controller for minimal UI
- `ytdl_hook-ytdl_path`: Uses local `yt-dlp.exe` for streaming

---

## ðŸŽ® `input.conf` â€“ Key Bindings

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

ðŸ’¡ Useful when watching portrait videos or debugging with stats overlay.

---

## ðŸ—‚ Folder Backup

Path: `C:\Users\AI\AppData\Roaming\mpv`

- âœ… `mpv.conf` â€“ Settings
- âœ… `input.conf` â€“ Custom keybindings
- âœ… `scripts/` â€“ Lua or JS extensions
- âœ… `script-opts/` â€“ Script-specific configs
- âœ… `fonts/` â€“ Fonts for OSD/subtitles

---

## ðŸ”„ Backup Instructions

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


