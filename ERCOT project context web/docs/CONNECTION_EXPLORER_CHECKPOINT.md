# Research Connection Explorer — purpose and development checkpoint

## Product decision
The website is a **read-only research reference** for the team's DSC 450 ERCOT project. Its sole application purpose is to make the project's documented connections easy to discover, interpret and follow.

It is **not** a slide builder, speech/script authoring interface, research packet exporter, production timeline, or Studio S integration. Former presentation-authoring features from Milestones 2 and 3 were removed from the active branch. Historical Git commits retain past work but the site no longer loads its scripts or offers authoring controls.

## Implemented reference experience
1. Default landing is **Connection map**, with the selected finding and adjacent graph concepts shown as labeled, readable cards.
2. Connections use curved SVG lines drawn against actual element positions on wide screens and reflow when the layout changes. On narrow screens a simple visible tree maintains connection cues.
3. **Solid arrows** indicate the original recorded dependency direction; **dashed connections** indicate an association. Neither proves causality.
4. Balanced selection avoids one dominant node category hiding the other scientific evidence. Category filters cover findings, models, metrics, figures, caveats, sources/data and questions/context. 'Show more' reveals all other direct relationships.
5. **Why linked?** shows the original relationship label, rationale, source/target IDs, graph direction, editorial strength and node verification status. Multiple graph edges between one pair are retained and inspectable.
6. Following links recenters the map; there is a back control, breadcrumbs, a reset command, and stable shareable \`#graph=<NODE_ID>\` URLs.
7. **Trace a path** finds a short route through documented relationships (at most six links), displays each recorded relation and directional qualification, and never treats reverse traversal as causal support.
8. Global search now navigates directly to the concept's connections. Overview, model comparisons, source registry, scientific findings and all 38 notebook figure previews remain available as reference views.
9. The original standalone offline Plotly viewer, Python graph inspector, source code, research graphs, figure files, metrics and scientific evidence statuses remain intact.

## Validation gate
CI runs the original scientific graph and figure SHA/dimension tests, rebuilt offline viewer, syntax checks, earlier dashboard/figure/model regression smoke tests and new connection map browser tests. Browser checks exercise filtering, relation explanation, following/backtracking, path search, deep links, no slide-authoring controls, and a mobile 390px layout without document overflow. Screenshots are archived as GitHub Actions artifacts. Read final pass/fail evidence from the current PR checks, not this documentation alone.

## Limits and future priorities
- Some older graph edges have generic boilerplate rationales. A reviewed curation pass could write more informative justifications **in the underlying graph builder**, while retaining provenance and avoiding overstated causal claims.
- The map deliberately displays up to 10 balanced direct neighbors first; expanding a high-degree concept requires more page space.
- The curved map shows local one-hop connections, not an automatic global layout of all 178 nodes. The original Plotly viewer remains available for full-network inspection.
- Path search considers edges as navigable in either direction for discovery. Directed causal inference is never established.
- Desktop edges are geometry-aware SVG curves; narrow-screen connections become an accessible vertical tree, not a physics simulation.
- Source file names may reference original notebooks or CSVs held separately by the team. The website does not invent public source download links.

### Recommended next iteration
Run a short usability review with someone unfamiliar with the project: ask them to trace the peak-demand claim to F17, numerical evidence, and the retrospective classification caveat. Count number of clicks and whether they can explain why the records are related. Then prioritize: (a) more informative link rationales, (b) a guided 2–3 concept comparison (e.g., overall vs peak-hour model ranking), and (c) a separate high-level whole-graph overview that does not sacrifice labels or accessibility.

**Do not reintroduce presentation, Studio S, or script-building workflows.**
