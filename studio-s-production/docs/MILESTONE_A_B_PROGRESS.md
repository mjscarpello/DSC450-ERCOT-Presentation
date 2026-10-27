# ERCOT Studio S highlight engineering — Milestone A/B checkpoint

**Branch:** `feature/studio-s-highlight-planning` (not yet merged into main).
**Official narration:** stakeholder-first, 19 scenes. Existing team script unchanged.

## Quantified planning output (generated locally)

- 19 scene IDs, 59 unique narration-linked cue IDs
- 24 exact PNG figure inputs; each is SHA-256 indexed
- 63 proposed pixel rectangles / normalized Studio S regions
- 9 explanatory text overlays for material not genuinely present in the corresponding chart
- 59 annotated individual overlay PNGs
- Source-corrected F09 orange peak marker from raster color mask: [1236, 112, 59, 59] on a 2293 × 800 source; normalized [0.539032, 0.14, 0.02573, 0.07375]
- One 25-page quantified Word review guide, generated using the same measured plan as the images
- Strict recorded-audio word alignment code prepared; **no audio supplied or timed**
- 16 local Python tests passed, including phrase-to-narration matches, source hashes, geometry, no fabricated timestamps and S18 audit.
- Studio S v0.2.0-dev.8 source-compatible non-narrated F09 fixture generated; native Node compilation remains **unverified** because the extracted checkpoint lacked installed js-yaml and install did not complete.

## What is already committed vs awaiting upload

This development branch contains the preliminary helper `tools/coords.py`, tests, a cue schema template, and mapping notes. The *full* validated Python generation implementation, 24 figures, annotated previews, measured JSON, document generator and native demo are distributed in the user-requested archive `ERCOT_StudioS_Quantified_Highlight_Public_Repository.zip`. The ZIP must be extracted/uploaded to the existing `studio-s-production/` folder on this branch; do not claim these files already exist in GitHub.

Keep `inputs/approved_narration.docx` and raw recordings out of this public repository until the team approves publication.

## Remaining acceptance gates

1. Human review of all 59 candidate overlays; manually refine any coarse editorial boxes.
2. Resolve source S18 figure-list discrepancy: F26 and D09 were referenced by cues but not by its earlier asset list.
3. Get actual individual recordings and reviewed word timings; bind phrases to real samples.
4. Install Studio S checkpoint runtime dependencies and successfully compile / render the F09 pilot on the user's machine.
5. Build and validate one full audio-synchronized scene before producing the 19-scene video.

Research constraints: F17 old top category has n=87; updated top 1% in report n=88. Retrospective peak group is not an advance-known alert. F26 evening MAE drop may be due to UTC update boundaries. No measured dispatch costs or outages.
