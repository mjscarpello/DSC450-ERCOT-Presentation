# ERCOT Research Explorer — Milestone 2 development handoff

## Summary
Milestone 2 turns the research browser into an evidence-to-presentation preparation workspace. It remains **human-reviewed**, scientifically cautious, and separate from the Studio S application and any unverified script/audio pipeline.

**New entry:** [explorer.html](../explorer.html#workspace) → Evidence workspace.

## What is implemented
1. **Evidence-focused reading:** Choose any of the 178 source-linked graph records and inspect its title, description, verification status, direct numerical metrics, original notebook figures, scientific limitations, and recorded source-file locators.
2. **Source tracing:** Explore shortest documented explanation paths through `evidence`, `provenance`, `quantitative`, `reasoning`, `dataflow`, and inherited `original-link` relationships to source nodes. Paths are descriptive and **not causal proofs**.
3. **Change-impact review:** Starting from the selected node, inspect documented outgoing dependency edges up to three hops. This produces a **review checklist**, not an automatic assessment of correctness or a causal influence analysis.
4. **Presentation research packet builder:** Add individual records or a group of directly connected metrics, figures, and caveats to a stable-ID packet. The packet includes a title, optional reviewer and narration-planning notes, plus a presence checklist for findings, numerical evidence, figure(s), and limitations.
5. **Portable exports:** Download a versioned JSON research packet or readable Markdown review notes. The JSON preserves every selected node ID, node evidence status, recorded source file and locator, relevant original figure path, numerical observations, selected-node graph relationships, and required scientific-review warnings.
6. **Local continuity:** Draft packets persist within this browser using localStorage (when enabled). The app supports importing previously exported valid version-1 JSON packets with a 1 MB and 60-record limit and rejects unknown node IDs.
7. **Navigation:** New Evidence workspace sidebar section, overview callout and drill-through controls from all research detail dialogs; keyboard focus trapping in search/details overlays.

## Source integrity and important scientific boundaries
- All research text, values, figures and relationship records come from existing `data/context_graph.json`, `data/model_metrics.json` and `assets/figures`; model predictions and graph relationships are **not recomputed or rewritten** by the web UI.
- A `source-supported` node means documented in a supplied source but not independently reproduced. A `csv-verified` metric means arithmetic recalculated from the provided prediction CSV, not that original training or forecast-origin conditions were audited.
- The 50/50 hybrid is the best performing **team-developed** approach overall. The official ERCOT day-ahead benchmark outperforms it on the same matched-hour sample, with forecast-issuance caveats.
- The highest 1% demand hours are classified **retrospectively** using actual observed demand, not identified by the future forecast model in advance.
- Connection weights are an authored relationship-strength scale (1–5), **not** statistical confidence, correlation or proof of causality.
- Underlying report, notebook and prediction CSV files are not necessarily included in the public web artifact. The source locator remains a reference and must be checked against original files held by the team.
- Exports have `status: "draft-human-review"` and explicitly say they are **not validated Studio S native scene manifests**.

## JSON packet version 1
A downloaded packet is a standalone record with these keys:
`schema`, `status`, `research_source`, `metrics_source`, `exported_at`, `title`, `speaker`, `editorial_notes`, `selected_node_ids`, `claim_ids`, `metric_ids`, `figure_ids`, `limitation_ids`, `source_references`, `research_records`, `linked_relationships`, `scientific_review_rules`, `studio_s_importer_compatibility`.

`research_records` includes an authoritative node title, type, summary, evidence status, source locators, and a numeric observation or figure reference if present. Exported `linked_relationships` retain graph directions and kinds and should not be reversed to imply causality. Other content fields are human editorial notes, not validated scientific results.

## Validation plan and audit
CI validates:
- JavaScript syntax for both primary and workspace scripts.
- Existing Python research-graph integrity and scientific metric invariants.
- Rebuild of the retained standalone offline context web.
- All Milestone 1 desktop and mobile smoke tests.
- Milestone 2 browser tests: selected claim inspection, batch collection of graph-linked evidence, JSON and Markdown downloads, scientific review flags, source traces, change-impact view, local draft persistence, import/rejection rules, deep links from detail drawer, and 390px mobile layout.
- Screenshots of desktop and mobile evidence workspace are attached as GitHub Actions artifacts.

## How to run
From repository root:
```bash
python -m http.server 8765
```
Open `http://localhost:8765/ERCOT%20project%20context%20web/explorer.html#workspace`. No separate build step is needed.
Run Python tests using `python -m unittest discover -s "ERCOT project context web/tests" -p "test_*.py" -v`.
CI uses Playwright for browser tests; install with `npm install --no-save playwright@1.56.1` and `npx playwright install chromium` before running `node "ERCOT project context web/tests/smoke-workspace.cjs"`.

## Known limitations
- An edge in the graph is an editorial or source-derived claim, not a verified statement of experimental causality. Traces traverse some relationships in either direction for discovery; directional paths are not evidence of reverse causal direction.
- Packet completeness indicates **presence of record types**, not substantive quality or teammate approval. A draft packet with a caveat still requires careful interpretation.
- The 60-node import/export cap is intentional for human-reviewable scenes. There is currently no team-synced packet service or merge/conflict management.
- Browser localStorage can be cleared, unavailable in privacy contexts, or device specific. **Export JSON to keep a durable copy**.
- Narrative notes are not collaboratively edited or source approved.
- Source locator text may point to a private report or notebook held outside this public GitHub repository; no broken public URL is invented.
- The online modular explorer requires an HTTP server or GitHub Pages. The original standalone offline viewer remains available and unmodified.
- The native Studio S schema and importer have not been audited; do not pass these packets directly to the software expecting it to understand them.
- End-to-end accessibility deserves an axe audit and real keyboard/screen-reader user testing even though dialogs now have focus containment.

## Recommended Milestone 3: Review-and-author scenes
1. **Review approvals:** Add human claim approval states with reviewer name/time, flagged missing-source checks and freeze/version evidence packets before narration.
2. **Scene composer:** Map research packets into ordered presentation scenes with clearly separated on-screen text, narration, figure and caveat slots; keep source IDs immutable.
3. **Studio S contract audit:** Inspect the real Studio S checkpoint and importer contract before building a validated adapter. Record unimplemented fields rather than inventing native capabilities.
4. **Provenance quality:** Detect weak source links, stale numerical figures and potential contradictory claims; compare old/new metric snapshots when the team changes model exports.
5. **Portable offline distribution:** Unify online and standalone generation so all review tools can be exported without requiring a server.
6. **Usability:** Human task evaluation (find peak evidence, confirm origin limitations, build/review/export one scene) with success and error tracking, mobile readability, keyboard/axe audit.

### Milestone 3 acceptance scenario
From `FIND-PEAK`, a team member must be able to gather `FIG-F17`, at least one relevant metric and `LIMIT-PEAK-BIN`, request/record approval, write a reviewed narration statement, then export a scene JSON whose source IDs and review status can be verified before any Studio S-specific transformation.
