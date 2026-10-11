# Ashee B Bansaal · Portfolio

The built site is `index.html`, `style.css`, `app.js`, plus `photos/` and `logos/`. It's plain static HTML, so you can host the repo root as-is (GitHub Pages, Netlify, etc.).

## Editing

**In the browser (easiest):**

```
python3 src/editor.py
```

This opens the site at `http://localhost:8000` in edit mode. Click any text to change it. Use the toolbar on each project card for links, images, reordering, copying and deleting. Then press **Save** (or ⌘S). Changes are written to `src/content.py` and the site is rebuilt. Edit mode only runs on your machine; the hosted site is read-only.

**By hand:** all text lives in `src/content.py`. Run `python3 src/build.py --watch`, edit and save, then refresh the page.

## Layout

| Path | What it is |
| --- | --- |
| `src/content.py` | All the words, links and project details |
| `src/build.py` | Generates `index.html`, `style.css`, `app.js` |
| `src/editor.py`, `editor.js`, `editor.css` | The local in-browser editor |
| `src/base.css`, `theme.css` | Styles (layout, then the scrapbook look) |
| `src/base.js`, `photos.js`, `julia.js`, `penguin.js` | Behaviour: nav and fade-ins, draggable photos, the fractal background, the penguins |
| `photos/`, `logos/` | Images used on the page |

Don't edit `index.html`, `style.css` or `app.js` directly. They're overwritten on every build.
