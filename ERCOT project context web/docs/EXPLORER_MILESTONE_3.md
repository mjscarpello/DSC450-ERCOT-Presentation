# Research Explorer — Milestone 3 checkpoint
**Scope:** Review-and-author scenes on top of the merged Milestone 2 evidence workspace.  
**Status:** Development branch / draft pull request; do not describe as published until merged and GitHub Pages has deployed.

## 1. Implemented features
1. **Scene sequence composer:** create blank scenes or initialize a scene using the current Milestone 2 evidence packet. Up to 30 scenes, 999 potential stable SCENE-XXX identifiers and explicit up/down reordering.
2. **Scene authoring:** separate editable scene title, learning objective, speaker, narration, on-screen statement and presenter/editing notes. The preview uses the original notebook figure, not a newly synthesized image or an executable presentation.
3. **Evidence bindings:** attach stable graph node IDs for claims, CSV-metric nodes, original FIG-* notebook images and LIMIT-* scientific caveats; add or remove individual references, inspect details before including and preserve source locators.
4. **Review gate:** require one of each evidence type, title, objective, narration, on-screen statement, named human reviewer, and three separate reviewer attestations (original source evidence, numerical interpretation/forecast constraints, scientific caveats). Record reviewer, ISO time and a deterministic change-detection checksum *only when explicitly approved*. Approval makes scene fields read-only.
5. **Change detection:** approve against the exact scene content plus graph node text, source locators and authored links. If those records change, the approval is marked **stale** and cannot be reapproved without explicitly reopening and repeating the review. Reopening resets attestation flags. The checksum is non-cryptographic and **not a proof of authenticity or truth**.
6. **Safe scene export:** a custom versioned JSON schema and human-readable Markdown. Exports embed source-linked record summaries, evidence statuses, original file locators, graph relationships, review data and scientific limits. Marked explicitly **not native Studio S**.
7. **Draft import:** JSON import validates scene count, identifiers, selected record types and linkable graph node IDs. Imported approvals are **always reset to drafts**, even if an imported file claims prior signoff. 2 MB maximum import; unknown IDs rejected. Drafts persist locally when storage is available.
8. **Navigation:** a new Scene composer in the research explorer sidebar and direct Create Scene from Milestone 2 evidence packet. Older graph, figures, metrics and offline research viewer preserved.

## 2. Key decisions and non-goals
- **The existing research graph is the source of truth.** Do not modify model metrics, figure data, statuses, source locators, or graph relationships to support an editorial storyline.
- A reviewed scene is an **editorial attestation** that the named team reviewer states they checked sources, numbers and limitations. It does not represent independent model reproduction, scientific review by the platform, a digital signature or teacher approval.
- The checksum detects accidental edits to content included in the scene and is not tamper-resistant.
- **No direct Studio S importer is implemented.** A historical Studio S October 14 handoff describes v2 graph, scene/keyframe/caption functionality, but the actual code, current schema and importer acceptance tests are not present in this ERCOT repository. See [STUDIO_S_CONTRACT_AUDIT.md](STUDIO_S_CONTRACT_AUDIT.md).
- This milestone neither creates rendered presentation videos nor edits native Studio S project sources. Such integration requires the actual application sources and a verified mapping of scene IDs, assets, audio and cue coordinates.

## 3. Export contract
The versioned JSON schema lives at [data/scene-sequence.schema.json](../data/scene-sequence.schema.json); its root discriminator is `ercot-scene-sequence/v1`. Each scene contains:
- Stable `scene_id`, explicit `order`, `title`, `objective`, `narrator`, `narration`, `on_screen_text`, editorial `notes`.
- `selected_ids` partitioned into `claims`, `metrics`, `figures`, `limitations`.
- `records` containing text, status, original figure reference, value/unit when applicable, and document/notebook/CSV locators.
- `authored_relationships` preserving source graph directions and editorial link classifications.
- `review.status` (draft, approved or stale), reviewer and attestations, review time and content checksum if current.
- Explicit `studio_s_compatibility` warning and required scientific review rules.

**Review status cannot be treated as scientific confidence;** link weight and timestamp cannot be used as certification.

## 4. How to use
From repository root:
```bash
python -m http.server 8765
```
Visit `http://localhost:8765/ERCOT%20project%20context%20web/explorer.html#workspace`, select `FIND-PEAK`, choose **Add connected evidence**, then choose **Create presentation scene**. Review figure F17, the relevant peak metrics and limitation `LIMIT-PEAK-BIN`; enter clear audience narration and on-screen text, confirm the primary documents and evidence assumptions, then record reviewer approval.

Switch to **Scene composer** to reorder scenes, inspect linked records and export JSON/Markdown. Export before clearing your browser storage.

## 5. Validation and evidence
The GitHub Actions validation pipeline exercises:
- Milestone 1 and 2 regression tests (graph, metric/figure integrity, desktop/mobile navigation and research packet round-trip).
- JavaScript syntax checks and rebuilding the original offline research viewer.
- Scene creation from packet, node ID preservation, required review checks, approval and field locking.
- Persistence and invalidation on a changed underlying figure description.
- Reopening and resetting review attestations, scene reorder, JSON/Markdown export, lossless IDs and scientific caveats.
- Imported scene approvals reset to draft; unknown figure IDs rejected.
- Chromium mobile 390px visual layout, horizontal overflow and JavaScript errors.

Every run uploads captured screenshots for review. Test results should be read from the relevant GitHub Actions run rather than assumed by this document.

## 6. Known limits
- Drafts are stored only in this browser (localStorage). Storage may be cleared or unavailable; export JSON to keep a durable copy. No multiuser live collaboration, access controls or review signing.
- Direct references show source locators; the original DOCX, CSV and notebooks are not necessarily included publicly. Human review of those files is required.
- No automated fact checking, model training audit, citations to inaccessible sources, or automated contradiction detection.
- No audio tracks, word timings, keyframe animation, editable charts, native Studio S timeline compilation, video export or guarantees of importer compatibility.
- Scene preview is an illustrative thumbnail using notebook PNG, not timing-accurate presentation rendering.
- Additional accessibility/contrast testing and keyboard user-testing remain necessary.
- No protected backend; a user can edit browser storage. A reviewer attestation is not a security boundary.
- `SCENE-XXX` IDs are local authoring references; a future Studio S adapter must map them through a validated naming and collision policy.

## 7. Recommended Milestone 4
**Verified Studio S integration planning + source quality checks.**
1. Obtain the actual current Studio S source archive and inspect its runtime schema and importer; run its baseline tests, and map scene data without touching production examples.
2. Define a validated, versioned adapter with explicit handling for figures, assets, captions, slide timing, cue anchors, narration and unresolved fields. Do not execute generated TS or JS.
3. Introduce authored-scene dependency audits for CSV refreshes and figure hash changes, showing exact affected scenes.
4. Add scene-to-scene storyline review, duplicated claims warnings, missing-source flags, export diff, explicit team signoff provenance and approval revision history.
5. Improve keyboard/tab focus in the editor, contrast and screen-reader feedback; add axe and human usability checks.
6. Evaluate a **standalone offline build** of the new research+scene interface, preserving the existing offline network bundle.

**Milestone 4 acceptance:** the same approved evidence packet must yield a schema-validated, deterministic draft scene project using verified actual Studio S interfaces; import/preview/export tested against the application source, with missing narration assets and unapproved research reported as actionable errors. No such integration is claimed as of Milestone 3.
