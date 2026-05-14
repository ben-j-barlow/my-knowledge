# Learnings

Notes on workflows, gotchas, and decisions made while building and using this knowledge base.

---

## Images / Assets After Web Clipping

The Obsidian Web Clipper saves articles with remote image URLs — it does not download images locally by default.

To download images locally after clipping:
1. Open the clipped article in Obsidian
2. Go to **Settings → Hotkeys → search "Download attachments"** and bind a hotkey (e.g. `Ctrl+Shift+D`)
3. Hit the hotkey — Obsidian downloads all images to the attachment folder and rewrites URLs to relative paths

**Current attachment folder**: `raw/assets/` (global, set in `.obsidian/app.json`). This is not per-topic — all images land here regardless of topic. To change it per-topic you'd need to update Settings → Files and links → Attachment folder path manually in Obsidian each time.

**When to bother**: optional for text-heavy articles. Worth doing for image-heavy content (papers with diagrams, architecture charts) where you want Claude to be able to view the images alongside the text.
