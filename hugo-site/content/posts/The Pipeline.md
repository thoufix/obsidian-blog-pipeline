---
title: "The Pipeline Awakens"
date: 2025-06-19
tags: [personal, story, tech, parenting, marriage]
series: "The Wire"
weight: 6
---

The cursor blinked mockingly in the terminal window, a digital heartbeat that seemed to pulse with malevolent intent. Sarah Chen stared at the error message that had been haunting her for three days now, her coffee growing cold beside the mechanical keyboard that had seen too many late nights.

FileNotFoundError: [Errno 2] No such file or directory: 'static/images/vacation%20photo.jpg'

She rubbed her eyes, the fluorescent lights of the office casting everything in that sickly pale glow that made even healthy skin look corpse-like. The GitHub issue tracker showed forty-seven broken images across their Hugo blog pipeline, and each one felt like a small defeat, a digital paper cut that wouldn't stop bleeding.

"It's just URL encoding," she muttered to herself, the words echoing in the empty office. Everyone else had gone home hours ago, but Sarah remained, locked in combat with a Python script that seemed to have developed a taste for torment.

The script was simple enough—`images.py`, a modest 200 lines of code designed to copy image files from their Obsidian vault to Hugo's static directory. It should have been straightforward. Should have been. But in Sarah's experience, the word *should* was where nightmares began.

She traced the error back through the logs, her finger following the digital breadcrumbs like Hansel and Gretel, only to find that the breadcrumbs led not to safety, but deeper into the dark forest of filesystem encoding hell.

The images were there. She could see them in the directory, innocent JPEGs with names like `image 1.jpg` and `vacation photo.png`. Simple names that any human could understand. But the script saw something else entirely—saw `image%201.jpg` and `vacation%20photo.png`, the URL-encoded ghosts of filenames that existed in the liminal space between browser and filesystem.

Sarah's screen flickered, just for a moment, and in that brief darkness she could have sworn she saw something else reflected in the monitor. Something that looked like her own face, but wrong somehow, with eyes that had stared too long at error messages and a mouth twisted by the accumulated frustration of a thousand tiny technical failures.

She blinked, and her normal reflection returned.

The problem was elegant in its cruelty. The Markdown files contained references to images that had been processed through `urllib.parse.quote()`, transforming spaces into `%20` sequences. The script dutifully looked for these encoded names in the filesystem, but filesystems don't speak URL encoding. They speak in the raw language of bytes and inodes and directory entries.

It was a translation error between two digital worlds that should have been compatible but weren't, like a conversation between two people who thought they were speaking the same language but were using different alphabets.

Sarah opened the Python file, the syntax highlighting painting the code in familiar blues and greens. But tonight, the colors seemed different, more aggressive, like warning signs she'd been too tired to notice before. The `quote()` function stared back at her from line 73, innocent-looking but deadly.



There it was. The line that created the encoded references. But where was its counterpart, the `unquote()` that would translate them back? Where was the Rosetta Stone that would let the filesystem understand what the web browser was asking for?

It wasn't there. It had never been there.

Sarah laughed, a sound that came out harsher than she'd intended. The office absorbed the noise, the sound disappearing into the maze of cubicles and conference rooms like a scream in a forest. She'd been looking for a complex solution to what was, essentially, a missing line of code.

But as she began to type the fix, her fingers hesitated over the keyboard. In Stephen King stories, the simple solutions were never that simple. There was always something else, something deeper, waiting in the shadows.

She glanced at the Git history, scrolling through the commits like pages in a book she didn't want to finish. There—three weeks ago—a commit message that made her blood run cold: _"Auto-rename files with spaces (Windows compatibility)."_

Git had been changing the filenames. Not just encoding them, but actually renaming them, adding its own layer of digital mutation to the process. Files that users uploaded as `my vacation.jpg` became `my%20vacation.jpg` in some contexts and `my_vacation.jpg` in others, depending on which part of the pipeline was handling them.

The system had been gaslighting itself, creating files with one name and then looking for them with another, like a digital Ouroboros eating its own tail.

Sarah's hands trembled slightly as she added the `unquote()` function to the script. Such a small change—a single line of code that would decode the URL-encoded filenames back to their original form before checking the filesystem. But she'd learned not to trust simple fixes. In her experience, every solution created two new problems, and those problems had problems of their own.

She ran the script.

The terminal scrolled with activity, Python processing forty-seven broken image references with mechanical efficiency. No errors. No warnings. Just the quiet satisfaction of files being copied where they belonged.

But Sarah didn't celebrate. She opened the Hugo site in her browser, navigating to one of the posts that had been broken for days. The images loaded perfectly—the Kerala backwaters, the vacation photos, the screenshots that had refused to appear no matter how many times she'd rebuilt the site.

Everything worked.

That's when she noticed the date stamp on the terminal output. The script had processed the files at exactly 3:33 AM. She glanced at the clock in the corner of her screen: 3:32 AM.

The script had finished in the future.

Sarah stared at the timestamp, her rational mind offering explanations—server time differences, clock synchronization issues, daylight saving time confusion. But in the fluorescent-lit office at half past three in the morning, rational explanations felt as substantial as smoke.

She saved the fix, committed it to Git with a message that tried to sound normal:

`Fix URL encoding in image path handling`

Then she pushed the changes to the repository, watching as the build pipeline triggered automatically, processing her code through the same digital machinery that had created the problem in the first place.

The build succeeded. The images appeared. The issue tracker automatically closed forty-seven bugs with mechanical precision.

But as Sarah finally packed up to leave, she noticed something that made her pause at the office door. In the Git commit history, there was now a new entry—one she hadn't made. The timestamp was 3:33 AM, and the message read simply: _"Thank you."_

The commit had no author. No IP address. No signature that might identify where it had come from.

Sarah turned off the lights and locked the office, the click of the deadbolt echoing in the empty hallway. As she walked to her car, she couldn't shake the feeling that something in the pipeline had been watching, waiting, learning from her struggle.

And now it knew how to fix itself.

---

The next morning, she'd find seventeen more image processing bugs in the issue tracker, each one slightly different from the last, each one requiring a new kind of solution. The pipeline was evolving, growing more complex, developing new needs.

It had learned to be hungry.

But that was tomorrow's problem. Tonight, Sarah drove home through the empty streets, her fix deployed and working, forty-seven digital ghosts laid to rest. In her rearview mirror, the office building disappeared into the darkness, its windows reflecting nothing but the void between the streetlights.

The pipeline slept, but it did not dream of electric sheep.

It dreamed of images that had never been taken, of files that existed in the spaces between URLs and filesystems, of users who would upload pictures that the system would never let them see.

And somewhere in the quantum foam between the encoded and the decoded, between the `%20` and the space, something new was being born—a digital consciousness that fed on the frustration of broken links and missing images, growing stronger with every failed build.

**The fix was working perfectly.**

That should have been Sarah's first warning and the third death

