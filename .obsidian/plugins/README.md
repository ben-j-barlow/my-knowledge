# Recommended Obsidian Plugins

Install these from Obsidian → Settings → Community Plugins → Browse.

## Essential

### Dataview
Query wiki pages by frontmatter tags. Used by `wiki/index.md` to generate filtered views by topic.

Example query — all investing pages:
```dataview
TABLE summary, tags
FROM "wiki"
WHERE contains(tags, "investing")
SORT file.name ASC
```

### Marp (marp-it or Slides)
Renders Marp-format slide decks inside Obsidian. Outputs from the LLM may use Marp format (`marp: true` in frontmatter).

## Useful

### Graph View (built-in)
Visualizes cross-topic link structure. Cross-topic wiki pages show up as bridge nodes between topic clusters — a good way to spot emerging themes.

### Dataview (advanced use)
With YAML frontmatter on every wiki page, you can build dynamic dashboards:
```dataview
TABLE updated, length(sources) AS "Sources"
FROM "wiki"
WHERE contains(tags, "concept")
SORT updated DESC
```

## Browser Extension (not an Obsidian plugin)

### Obsidian Web Clipper
Clips web articles to markdown. Install from the Obsidian website or browser extension store.

**Image download tip**: After clipping an article in Obsidian, use the hotkey "Download attachments for current file" (bind it in Settings → Hotkeys → search "Download") to pull all images to local `raw/<topic>/assets/`. Suggested binding: `Ctrl+Shift+D`.
