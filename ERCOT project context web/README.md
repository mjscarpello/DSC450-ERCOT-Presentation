# ERCOT Research Connections

A **source-linked, interactive research reference** for Bellevue University's DSC 450 Project 2: *Forecasting Next-Day Hourly Electricity Demand in ERCOT*.

## Purpose

Understand **how the research connects**. This viewer is an explorable map of the project's data, models, numerical evidence, notebook visualizations, research findings, and limitations. It is not a presentation authoring tool, video editor, slide builder, or Studio S integration. The earlier presentation-workflow features have been retired from the active site.

The original evidence has **178 nodes, 591 recorded graph edges and 38 notebook figures**. Some nodes share multiple documented links, so the number of unique neighbors may be smaller than the number of edges.

## Start exploring

Open [the Research Explorer](explorer.html), or start a local server from the **outer repository root**:

```bash
python -m http.server 8765
```

Then visit:

`http://localhost:8765/ERCOT%20project%20context%20web/explorer.html`

The viewer opens on the **Connection map**. Choose a concept at the top, then:

1. **Follow a connection.** Lines curve from the selected concept to related items. Select *Follow* to center that concept without losing the ability to go back.
2. **Understand why it is linked.** Select *Why linked?* to read the stored relation, rationale, graph direction, evidence status and source context.
3. **Focus the view.** Filter relationships to findings, metrics, figures, limitations, sources/data, or questions/context. The default balances categories instead of displaying only whichever kind has the most nodes.
4. **Trace a path.** Choose *Trace a path*, pick two research records and inspect the actual recorded links between them. A path is for exploration only, not causal proof.
5. **Inspect the source.** Open any research record to view its source file references, notebook figure, exact recorded values and connected concepts.

Other sidebar sections retain overview metrics, model comparisons, the full figure gallery, research questions and a source registry. All of these are **read-only reference views**.

The [original standalone network viewer](outputs/ERCOT_CONTEXT_WEB.html) remains available for offline use with its full Plotly graph. The new modular explorer requires a local HTTP server or GitHub Pages because it loads the JSON data with browser fetch.

## How to read the connections

- **Solid curves with arrowheads** follow the graph's documented dependency direction. A stored dependency is not by itself proof of causality.
- **Dotted curves** are associations, for example two research ideas appearing together or an explanatory figure linked to a claim.
- **Colors** classify destination concepts: findings, metrics, figures, caveats, sources, or other context. Colors are not confidence scores.
- **Connection strength (1–5)** is an editorial description of relationship closeness, not a model metric, correlation, probability or statistical significance.
- **Research status** distinguishes arithmetic verified against the supplied prediction CSV from narrative claims sourced from the team's reports, interpretations and open questions.

Links can run in either direction and multiple links can join the same pair. The detail view displays their original direction and wording. A path search can traverse associations or dependencies in either direction for discovery, but this never establishes reverse causality.

See [Connection Model](docs/CONNECTION_MODEL.md) and [Scientific Boundaries](docs/SCIENTIFIC_BOUNDARIES.md).

## Scientific cautions

The team's 50/50 hybrid was strongest **among the team's own models** on the common comparison period; the published ERCOT day-ahead benchmark had lower overall MAE. The *highest 1% demand* subset was chosen **after observing actual demand**; it is a retrospective diagnostic, not an advance-known operational condition. Equal target hours also do not guarantee equivalent forecast issue times and predictor availability.

The report, notebook and prediction CSV sources are referenced in the graph, but not all underlying files are included in this public repository. Verify originals before relying on source statements.

## Data and project layout

- `data/context_graph.json` — authoritative research node and directed relation snapshot.
- `data/model_metrics.json` — evaluated error-metric snapshot.
- `data/figure_catalog.json`, `data/figure_notes.json` — original figure provenance, dimensions, hashes, and notebook context.
- `assets/figures/` — the 38 notebook PNG figures.
- `explorer.html`, `explorer.js`, `explorer.css` — static research interface.
- `connection-explorer.js`, `connection-explorer.css` — focused relationship map and explanation paths.
- `src/ercot_web/` — Python graph construction, inspection, CLI, and original offline viewer generator.
- `tests/` — figure/graph integrity and browser navigation checks.

No original scientific graph nodes, source references or figures were removed when presentation authoring was retired.

## Optional Python inspection

From **this subdirectory**:

```bash
python -m pip install -e '.[all]'
ercot-web inspect FIND-PEAK
ercot-web near FIND-PEAK --depth 2 --min-weight 4
ercot-web trace SRC-PRED FIND-PEAK
ercot-web impact SRC-PRED
ercot-web audit
python -m unittest discover -s tests -v
```

`trace` follows explanation links; `impact` follows directed dependency links. They do not retrain forecasting models. If an original figure changes, update its image metadata/hashes and run integrity checks.

## Workflow principles

Make research content changes in the source graph builder or reviewed data files, **not** by typing alternative conclusions into the UI. Keep the source links, statuses, scientific caveats, and direction of graph edges intact. The interface is a reference for understanding the project, not a mechanism for approving claims or generating slides.

Historical changes are preserved in Git history; the active website contains only the research reference functionality.
