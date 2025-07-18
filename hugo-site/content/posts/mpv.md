---
title: mpv.io
date: 2025-07-18
summary: Alternative experience from VLC
tags:
  - mpv
series: local video
---

# Config of mpv

hwdec=auto
vo=gpu
ytdl-format=bestvideo+bestaudio
script-opts=ytdl_hook-ytdl_path=yt-dlp.exe


ytdl-format=bv*+ba/best
hwdec=auto-safe
profile=fast