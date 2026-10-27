# Native Studio S orchestration integration: three approved highlights

The full source, figures, transparent overlays, already compiled v2 `.sproj`, scripts, 315-frame MP4, native Canvas screenshots and reproducibility evidence were created in this conversation in `ERCOT_StudioS_Native_Integration_Review.zip`. **They are not yet uploaded as binaries/code to this GitHub branch.** Extract that ZIP and copy the included `ERCOT_StudioS_Native_Integration_Test/` folder here if you want the complete GitHub-hosted source.

## Verified with Studio S v0.2.0-dev.8

- **Native official CLI build PASSED** on `studio-s-source` JSON: three scenes / 315 frames.
- Studio S native core `assertValid` + `validateProject`: **PASS**, zero errors.
- Python JSON Schema validation against Studio S's canonical `studio-project-v2.schema.json`: **PASS**.
- Source figure PNGs: D03R SHA256 `c170375976dd8ec06aed2c81179ae416c54db2797b3e2096522d1b3e59bc9326`; D05 SHA256 `c564cf0edd63cb65f01e096e962c415e267cfb2b6b7605868b02979405dc634c`.
- Renderer: original Studio S `src/core/timebase.js`, `src/core/animation.js`, and `src/render/canvas.js`, exercised through Chromium with Python Playwright. **PASS** 315 frames / 30 fps / 10.5 seconds, 1280×760 MP4. Six entrance checks passed.
- Tested narration cue IDs: `S15-C01`, `S15-C02`, `S16-C03`. These are **visual review approvals**, not audio-synced scenes.
- Original D03R and D05 source chart pixels are preserved; overlay rasters are transparent, source-pixel-sized PNGs with identical object layouts and animation clips.

## Corrected integration issues

1. Studio S requires object IDs unique **across** scenes. The build caught duplicate IDs and the source generator was fixed to prefix every object ID with its scene ID.
2. The 52% improvement callout had overflowing text; the label was shortened, its bounding region tightened, and frames were reviewed again.
3. The source chart, markers and bracket are separate timed layers rather than permanently painted onto the source image.

## Unverified here / setup requirements

- This extracted Studio S checkpoint lacks complete `node_modules` contents. Official CLI `validate` failed for missing **ajv**; official CLI `render` failed for missing Node **playwright**. Registry access in this container is unavailable. The integrated fallback uses original Studio S native core validation + source compiler + Canvas renderer, not substitute drawing code.
- On your Mac run `npm ci`, `npx playwright install chromium` in the Studio S checkpoint, install the Python dependencies detailed in the ZIP README and then run `RUN_STUDIO_S.command /path/to/Studio_S_v0.2_Development`.
- Native **modular workspace compilation**, desktop editor import, and official export need acceptance tests after the dependency installation.
- Audio and narration words are unavailable; all animation timings in this test are **demonstration-only** and must not be taken as real word alignments.

The next gate is successful official CLI `validate` and `render` on the user's Mac. Do not merge the development branch to main before approved scripts, source assets, and binary outputs have been uploaded and reviewed.
