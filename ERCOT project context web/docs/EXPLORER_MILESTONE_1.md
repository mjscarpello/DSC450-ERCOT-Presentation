# Research Explorer — Milestone 1 review

## Objective
Make the research usable without starting from an unlabeled 178-node network. Preserve the authoritative Python graph, evidence statuses, all original figure assets, and the existing offline Plotly explorer.

## Delivered
- New static GitHub Pages entrypoint: `explorer.html`, with readable CSS and framework-free JavaScript.
- Overview: four source-derived project metrics, key finding cards, featured figures and a navigation path.
- Findings: keyword filtering and source-linked research detail dialogs.
- Models: eight matched-hour error series from `data/model_metrics.json`, with separate overall and retrospective highest-1% views.
- Figures: all 38 extracted notebook figures, grouped by research purpose, filterable and inspectable at larger size.
- Questions: report appendix questions and figure-specific research questions.
- Sources: inventory of source node records; filename and locator only when underlying source files are not published.
- Graph: legible focused neighborhood with category filters, direct-connection list and contextual inspection.
- Global search: searches ID, title, summary and question text with keyboard `/` and Ctrl/Cmd+K support.
- Direct node URLs using `#node=ID`; keyboard-accessible navigation; responsive layout.
- The project-root hub now points to the new explorer; the original offline graph remains available.

## Scientific integrity
- The explorer reads the existing JSON unchanged; no data or model recomputation occurs in browser code.
- Error bars show MAE (lower is better), not confidence, correlation, or causal coefficients.
- The team hybrid beats other **team** series overall; the ERCOT published benchmark retains the lowest overall MAE.
- The top 1% evaluation subset is identified **retrospectively** from observed demand, not predicted ahead of time.
- Matched target-hour scores do not imply identical forecast issuance horizons or predictor availability.
- Node verification statuses remain explicit; file locators are not presented as public URLs if originals aren't bundled.

## Run locally
From the repository root:
```bash
python -m http.server 8765
```
Then open:
`http://localhost:8765/ERCOT%20project%20context%20web/explorer.html`

Browser `file://` loading is intentionally **not supported** by the new modular viewer because browsers restrict JSON fetches from disk. For portable offline research, open the original generated `outputs/ERCOT_CONTEXT_WEB.html`, which embeds its graph and Plotly dependencies.

## Validation
CI runs:
1. JavaScript syntax check with Node.js.
2. Existing Python graph tests plus new graph/figure/metric invariants.
3. Rebuilding the original offline HTML viewer.
4. Chromium browser smoke tests on desktop and mobile: overview numeric values, model switch, all 38 figure previews, F17 detail, global search, evidence navigation, 390px viewport overflow check, JavaScript errors.
5. Save full-page screenshots as CI artifacts for visual review.

## Known limitations / not part of this milestone
- The focused graph deliberately shows direct neighbors rather than a full animated physics layout. The original full network remains accessible.
- The graph view uses manual radial node placement and may need pagination/zoom refinements for high-degree nodes.
- Source files referenced only by name cannot open until the research team publishes or maps the underlying artifacts.
- Detail dialogs support Escape and labelled close controls, but full focus trapping and return-focus for every navigation path need a dedicated accessibility audit.
- Figure extraction and captions reflect existing notebook content; some original notebook descriptions are long or truncated upstream.
- This version does not export presentation scene manifests or integrate directly with Studio S.
- New modular viewer requires a static HTTP host, unlike the retained offline bundle.

## Recommended next milestone (Milestone 2)
1. **Evidence-first reading view:** separate claims, direct numeric evidence, figure interpretation, scientific caveats, and provenance into a consistent annotated research narrative.
2. **Source resolution:** attach source registry entries to locally available/published report or notebook anchors; warn when files are unavailable.
3. **Presentation collections:** allow choosing figures, numeric claims and caveats as a reviewable scene packet, exported using stable IDs, with speaker-review flags.
4. **Graph usability:** reveal path-to-source, upstream/downstream dependency workflows from Python `trace` / `impact`, and support filtering without overplotting.
5. **Accessibility and mobile polish:** focus trap, keyboard movement through the graph, improved narrow-screen node layout, contrast checks, axe-based automated audits.
6. **Offline parity:** evaluate how to generate both a modular online version and an equivalent standalone offline bundle from shared templates and code, without duplicating logic.

## Acceptance criteria for Milestone 2
A researcher should be able to choose `FIND-PEAK`, identify its metric evidence, inspect F17, see `LIMIT-PEAK-BIN`, and export a human-reviewable collection with stable IDs and source locators. All four steps should be tested in browser automation.
