# Studio S presentation highlight planning (foundation)

This subproject converts the ERCOT presentation's narration-linked editorial cues into **measured image regions and reviewable Studio S instructions**. It does not replace the existing `ERCOT project context web/` research graph.

**Current state:** preliminary development branch. Main, the website and the posted OneDrive scripts remain unchanged.

## Development goals

1. Link every approved narration line ID to figure ID and highlight cue ID.
2. Measure region geometry in **original image pixels**, then convert to source-image normalized `[x,y,width,height]`.
3. Preserve source hashes, original figures, overlay previews, review decisions and editor notes.
4. Align verified spoken phrases to actual audio clips once recordings exist. Never guess exact word times.
5. Generate image asset regions and focus-outline scene objects for Studio S v0.2.0-dev.8; validate with its real modular compiler.
6. Generate an updated readable visual highlight guide from the **same** verified cue data.

The complete initial working prototype and 19-scene/59-cue audit are in the downloadable foundation ZIP supplied in the conversation. Only a small non-destructive GitHub starter is committed here while its architecture is under review.

## Requirements and verification

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
```

Do not publish raw team audio or private OneDrive materials to this public GitHub repository without team authorization. Read `docs/STUDIO_S_MAPPING.md` before implementing the exporter.
