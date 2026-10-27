# Studio S ERCOT S16-C03 native render pilot

## Results

**PASS:** The native Studio S `0.2.0-dev.8` source compiler accepted the S16-C03 single-file v2 project. Its native Canvas renderer drew all 150 frames at 30 FPS and the frames were encoded with FFmpeg into an H264 MP4. Numeric source values and original chart-pixel geometry were verified.

**Not yet claimed:** modular workspace compilation, Studio S desktop editor integration, official Studio S CLI video export, or alignment to real recorded audio. Node packages could not be installed in this environment, so full modular CLI tests were not possible.

## Files

- `native_render/S16_C03_NATIVE_STUDIOS_CANVAS.mp4` — five-second native Canvas rendering (demo timing)
- `native_render/01_original_chart.png` — before highlight
- `native_render/02_markers_visible.png` — observed + hybrid bar-top markers
- `native_render/03_markers_and_bracket.png` — final frame with comparison bracket
- `cue_geometry.json` — approved cue, exact coordinates and source asset hashes
- `reviews/approval_registry.json` — 59 cues' known review statuses and preview references
- `reviews/approved_previews/` — the 10 individually approved visual references
- `studio_s_project/pilot.source.json` — editable data-only Studio S v2 native source
- `studio_s_project/pilot.sproj` — native Studio S compiled v2 project (single file)
- `studio_s_project/compile_core.cjs` — reproduce a native source compilation against the checkpoint
- `studio_s_project/native_canvas_render.py` — reproduce native Canvas frames and MP4 locally
- `VALIDATION_REPORT.json` — verified test scope and limitations

## Rebuild in Studio S on your Mac

Use Node 22+, Studio S v0.2.0-dev.8 installed dependencies, Chromium/Playwright, FFmpeg, and Python Pillow:

```bash
# In the actual Studio S checkpoint root
npm ci
node packages/cli.cjs build /absolute/path/to/studio_s_project/pilot.source.json
node packages/cli.cjs validate /absolute/path/to/studio_s_project/pilot.sproj
node packages/cli.cjs render /absolute/path/to/studio_s_project/pilot.sproj -o /absolute/path/to/studio_s_project/pilot_full_studio_export.mp4
```

The precompiled `pilot.sproj` is available even if the module workspace loader is unavailable. Opening in the desktop app and official CLI output still require testing on the user's Mac. It is a **single-file** Studio S v2 project; extending this to the repository's modular build is a separate gate.

A low-dependency fallback runs the original Studio S core compiler and Canvas implementation using the included harness (does not validate the modular build):

```bash
STUDIO_S_SOURCE=/absolute/path/to/Studio_S_v0.2_Development node studio_s_project/compile_core.cjs
STUDIO_S_SOURCE=/absolute/path/to/Studio_S_v0.2_Development python3 studio_s_project/native_canvas_render.py
```

The low-dependency compilation path requires `js-yaml` (use the dependency installed with Studio S) and Python Playwright + local Chromium. The animation uses fixed **demonstration** timing. Replace with verified word/audio cues later.

## Important mapping rule

The source D05 image and the two transparent PNG layers have the *same source pixel dimensions (1732×796)* and must use the *identical display rectangle*. Scaling only one overlay separately will misalign the markers and bracket. Do not flatten the highlight into the source chart before narration timing is available.

## Status registry

The ten highlighted approvals are editorial approvals in this conversation. The three earlier concept acceptances still need precise geometry, and S04-C02 and S17-C01 need review. The other cues await individual attention. The code plan is reproducible but not yet integrated into GitHub or the full 19-scene production.

## Regenerating the highlight overlays

Run `python3 studio_s_project/rebuild_overlays.py` from the extracted pilot package after installing Pillow. This regenerates both transparent overlay images using the figure's original pixels and the source-locked cue geometry, and reports whether their SHA256 values match the delivered approved versions. The original chart's SHA256 is verified first. Font fallback on a different OS may change the bracket-label raster: in that case, approve the new result before updating the asset hash or the compiled project.
