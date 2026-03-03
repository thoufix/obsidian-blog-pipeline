---
title: OpenClaw notes
date: 2026-03-03
summary: Check Qwen token usage?
series: AI
tags:
  - raspberry-pi
  - openclaw
---

 1. Rate limit / Quota exhausted — You've used up your free tier tokens for this hour/day. Logging in again won't fix this — you need to wait for the quota to reset.
 2. Token actually expired — Less common, but possible. If the OAuth refresh failed, you'd need to re-authenticate.

 To check which it is:

 Run this in your terminal:

 ```bash
   openclaw gateway status
 ```

 Then try a simple test message. If you get auth errors (401/403), it's a token issue → re-auth needed.

 If you get "no output" or empty responses with no error, it's almost certainly rate limiting → wait for quota reset.

 To re-authenticate (if needed):

 ```bash
   openclaw auth login --provider qwen-portal