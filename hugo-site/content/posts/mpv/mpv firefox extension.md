---
title: ff2mpv on Firefox (Windows)
date: 2025-08-08
summary: How to set up ff2mpv on Firefox in Windows using native messaging
tags:
  - mpv
  - firefox
  - native-messaging
  - windows
---

# ff2mpv Setup for Firefox on Windows

This guide explains how I got **ff2mpv** working with **Firefox** on Windows.  
It launches videos directly in **MPV** from Firefox using native messaging.

---

## 1. Requirements
- **MPV** installed and available in PATH  
- **Python** (any modern version that can run `ff2mpv.py`)  
- **ff2mpv.py** script (from [woodruffw/ff2mpv](https://github.com/woodruffw/ff2mpv))  
- **ff2mpv Firefox extension** ([AMO link](https://addons.mozilla.org/en-US/firefox/addon/ff2mpv/))  

---

## 2. Folder Structure
I placed everything in:

C:\Users\AI\ff2mpv\

kotlin
Copy
Edit

Inside this folder:
ff2mpv.py
ff2mpv-windows.json

yaml
Copy
Edit

---

## 3. Create the Native Messaging Host JSON

In the **ff2mpv folder**, create a file called:

ff2mpv-windows.json


Contents:

```json
{
  "name": "ff2mpv",
  "description": "Launch videos in MPV from Firefox",
  "path": "C:\\Users\\AI\\ff2mpv\\ff2mpv.py",
  "type": "stdio",
  "allowed_extensions": ["ff2mpv@woodruffw.github.io"]
}
