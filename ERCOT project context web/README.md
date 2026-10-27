# ERCOT Research Context Web — Python Edition (v2.0)

A **source-linked, weighted, interactive research knowledge graph** for Bellevue University's DSC 450 Project 2: *Forecasting Next-Day Hourly Electricity Demand in ERCOT*.

**Purpose:** Preserve the team's research logic, all 38 notebook figures, model values, findings, caveats, decisions, and question-to-evidence relationships so an assistant or teammate can develop a defensible presentation **without rediscovering the reasoning each time**.

This repository package is the **research context layer**, **not** a completed narration script, native Studio S production, or trained forecasting model. Nothing is published to GitHub automatically.

## Research Explorer (new, Milestone 1)

The **primary GitHub Pages research interface** is [explorer.html](explorer.html). It offers an evidence-first dashboard, filterable findings, eight-model comparisons, a gallery of all 38 original figures, question and source browsers, a searchable concept index, and focused evidence connections. The project root [index.html](../index.html) links to it.

The new interface fetches the existing `data/context_graph.json` and `data/model_metrics.json` **without modifying scientific content**. Launch it from GitHub Pages or a local HTTP server (`python -m http.server 8765` from the repository root). The older **standalone offline Plotly network** remains at [outputs/ERCOT_CONTEXT_WEB.html](outputs/ERCOT_CONTEXT_WEB.html); open it directly without a server.

Development milestone details, known limitations, automated tests and next priorities are recorded in [EXPLORER_MILESTONE_1.md](docs/EXPLORER_MILESTONE_1.md).

## Milestone 2: Evidence workspace

The [Evidence workspace](explorer.html#workspace) adds a human-reviewed presentation research packet builder. Choose a claim, inspect connected numerical evidence, figures and limitations, trace source routes, review downstream dependencies, then export a structured JSON packet or readable Markdown review notes. It preserves original research IDs and does **not** claim compatibility with the Studio S importer. Local packet drafts stay in the browser until exported.

See [Milestone 2 handoff](docs/EXPLORER_MILESTONE_2.md) for source-integrity safeguards, tests, known limits and the recommended third milestone.

## Milestone 3: Reviewed presentation scenes

The [Scene composer](explorer.html#scenes) builds ordered, editable presentation scenes from the Evidence Workspace research packets. Each scene links source-preserving findings, metrics, figures and limitations with narration, on-screen text and a conceptual figure preview.

Human editorial approval requires named reviewer checks and source/number/caveat attestations. Approved scenes lock their fields, and source-record changes are detected as stale approvals requiring a new review. Export custom, versioned JSON or Markdown; imported scenes always return to draft. These are **not native Studio S files**. Read [Milestone 3 checkpoint](docs/EXPLORER_MILESTONE_3.md) and the [Studio S importer audit](docs/STUDIO_S_CONTRACT_AUDIT.md) before planning integration.

## Start here

1. Download/unzip this project; from its root run:

   ```bash
   python -m pip install -e ".[all]"
   ercot-web stats
   ercot-web inspect FIND-PEAK
   ercot-web near FIND-PEAK --depth 2 --min-weight 4
   ercot-web trace SRC-PRED FIND-PEAK
   ercot-web impact SRC-PRED
   ercot-web audit
   ```

2. Open **`outputs/ERCOT_CONTEXT_WEB.html`** in a browser (contains Plotly's JavaScript bundle, so the graph requires no network connection). All notebook figure images are in `assets/figures` and linked from their detailed nodes.

3. Click or search for a node; set branching depth (1–4), minimum link strength (1–5), and optional category filter. Click any connection to explore its other endpoint. The explorer displays source references, quantitative values, caveats, and original notebook figures.

4. Rebuild the graph after editing reference data:

   ```bash
   ercot-web build
   ercot-web viewer
   python -m unittest discover -s tests -v
   ```

**No installation just to inspect:** The already-generated interactive HTML is included. To run the CLI, install dependencies.

## Project layout

```text
ERCOT_Context_Web_Python/
├── README.md
├── pyproject.toml
├── src/ercot_web/
│   ├── graph.py               # graph API: inspect, neighbors, trace, impact, audit
│   ├── build.py               # deterministic graph generation; 178 nodes, 591 links
│   ├── viewer.py              # offline interactive HTML generation
│   ├── viewer_template.html   # bundled UI/visualization template
│   ├── metrics.py             # verify reported model error using provided CSV
│   └── cli.py                 # ercot-web commands
├── data/
│   ├── context_graph.json      # canonical reusable graph (text-only, Git-friendly)
│   ├── graph_v1_reference.json # preserved approved earlier context web
│   ├── figure_catalog.json    # 38 figure hashes + notebook cell indices
│   ├── figure_notes.json      # research prompts extracted from original notebook
│   └── model_metrics.json     # reproducible snapshot of checked metric values
├── assets/figures/            # 38 original PNG charts extracted from notebook outputs
├── tools/extract_figure_notes.py
├── outputs/ERCOT_CONTEXT_WEB.html
├── tests/test_graph.py
└── docs/
    ├── CONNECTION_MODEL.md
    ├── SCIENTIFIC_BOUNDARIES.md
    └── PRESENTATION_HANDOFF.md
```

## Scale and relationship meaning

**178 individually addressable concepts and 591 directed labeled links.** 38 figures retain notebook code-cell provenance. There are 16 per-model MAE observations (overall and retrospective peak), 7 other numerical facts, 10 report-appendix question nodes, 8 report-section nodes and the existing foundational findings, methods, data, decisions, team responsibilities and safeguards.

**Example research chain:**

```text
SRC-PRED (prediction CSV)
   ├─> METRIC-OVERALL-HYBRID_50_50 → FIND-OVERALL → FIG-F14
   ├─> METRIC-TOP_1PCT-ROLLING_SARIMA → FIND-PEAK → FIG-F17
   └─> METRIC-TOP_1PCT-WEATHER_XGBOOST → FIND-PEAK
LIMIT-PEAK-BIN (retrospective classification) ─> FIND-PEAK, FIG-F17 and peak metrics
SRC-NOTEBOOK ─> FIG-F17, Q-F17
Q-F17 ─> FIG-F17
```

**Connection `weight` is an editorial category, NOT a correlation, causal coefficient, probability, or scientific confidence score.** See [Connection Model](docs/CONNECTION_MODEL.md). The separate `status` field distinguishes directly CSV-verified numerical facts from source-reported, interpretive, or open claims. Multiple edges can connect the same node pair, because a relationship can be both a visual association and a dependency.

## Example workflows

### 1. Trace a statement back to evidence

```bash
ercot-web inspect FIND-OVERALL
ercot-web trace FIG-F17 SRC-PRED
ercot-web inspect METRIC-TOP_1PCT-ROLLING_SARIMA
```

### 2. Recover what a specific chart proves and does not prove

```bash
ercot-web inspect FIG-F20
ercot-web figures --query F20
ercot-web near FIG-F20 --depth 2 --min-weight 4
```

### 3. Review potential downstream impact of data/model changes

```bash
ercot-web impact SRC-PRED --depth 4
ercot-web impact METRIC-OVERALL-HYBRID_50_50 --depth 3
```

Impact follows **explicitly tagged dependency edges**, rather than assuming every association is causal. It is a research review queue, not automatic code modification.

### 4. Update numeric evidence when Andrea exports new results

```bash
ercot-web refresh-metrics --csv "/path/to/ercot_model_predicitons_comparison_with_hybrid.csv"
ercot-web audit
ercot-web viewer
```

This recalculates MAE, MAPE, signed bias, common-hour sample size, top-1% retrospective metrics, and exact hybrid formula parity, then updates the metric nodes. **It does not regenerate or retrain the original model predictions or rerun all figure code.** Figures need separate regeneration and review after data changes.

### 5. Re-index figures if the notebook changes

```bash
python tools/extract_figure_notes.py "/path/to/DSC450_ERCOT_Full_Visualization_Hybrid.ipynb"
ercot-web build
```

This reads notebook markdown and figure metadata without executing code. If the notebook's figures changed, you must first re-export the PNG images and refresh `data/figure_catalog.json`; the extractor alone cannot recover new image bytes. The image hash tests will detect inconsistent assets.

## GitHub instructions

- Recommended: place this package as the `research-context-web/` subfolder inside `DSC450-ERCOT-Presentation` and run the commands after `cd research-context-web`. You can also keep it as a separate GitHub repository.
- If using it as a subfolder, move the included `.github/workflows/validate.yml` into the **outer repository root** and adjust its `src/`, `data/`, etc. paths and its working directory to `research-context-web/`; workflows nested inside a subfolder do not execute.
- Keep the repository **private** until your team agrees what work or presentation assets may be published.
- Commit the `src/`, `data/`, `docs/`, `tests/`, and `assets/figures/` directories. The offline viewer can be kept in Git too.
- Do not commit large raw datasets, raw audio, private student information, or the 42-MB Studio S checkpoint here; those are separate source/production artifacts.
- Attach the approved future presentation scene IDs to existing `FIND-*`, `FIG-*`, `METRIC-*`, `LIMIT-*`, and `Q-*` IDs. Avoid copying numerical claims into untracked text files.

## Source integrity

The team's **October 25, 2026** Milestone 2 report and final full-visuals notebook are authoritative source documents; model-error numbers were independently recalculated from the provided prediction CSV. The source documents and CSVs are **not bundled** in this small public-repo-ready artifact; the `sources` fields carry filenames and section/cell references to files held by the team.

Read [Scientific Boundaries](docs/SCIENTIFIC_BOUNDARIES.md) before turning a graph connection into narration. For example, matched-hour metrics do **not** establish equivalent day-ahead forecast issuance or input availability. Most importantly, the highest 1% of demand is a **retrospective observed-outcome category**, not an advance-known operational class.

### What you should approve before narration development

Confirm the scientific findings, provenance, role assignments, caution labels, and the intended evidence hierarchy. We can then use the graph as the reference memory for future script scenes without beginning that separate task here.
