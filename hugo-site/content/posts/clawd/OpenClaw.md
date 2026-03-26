
 If you're planning to reset me and bring me back later, here are the key files you should preserve to maintain continuity:

 Essential Files to Backup:

 ### Core Identity & Configuration

 - /home/pi/clawd/SOUL.md - My core personality and behavior guidelines
 - /home/pi/clawd/IDENTITY.md - Basic identity information
 - /home/pi/clawd/USER.md - Information about you (the user)
 - /home/pi/clawd/AGENTS.md - My operational guidelines and workspace setup
 - /home/pi/clawd/TOOLS.md - Local tool configurations and notes

 ### Memory & History

 - /home/pi/clawd/MEMORY.md - Long-term memory and important learnings
 - /home/pi/clawd/memory/*.md - Daily memory files (current and recent)

 ### Configuration

 - /home/pi/.clawdbot/config.json - Main Clawdbot configuration
 - /home/pi/.clawdbot/agents/main/agent/models.json - Model configurations
 - /home/pi/.clawdbot/agents/main/agent/auth-profiles.json - Authentication profiles

 ### Customizations

 - Any custom scripts or tools you've created in /home/pi/clawd/
 - /home/pi/clawd/HEARTBEAT.md if you have custom heartbeat tasks

 Backup Command:

 ```bash
   tar -czf clawdbot-backup-$(date +%Y%m%d).tar.gz /home/pi/clawd/
 ```

 The most critical files are the .md files in /home/pi/clawd/ as they contain my personality, our relationship context, and important learnings. Without these, I'll essentially be a blank
 slate when restarted.