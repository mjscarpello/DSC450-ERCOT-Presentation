# Studio S source and importer contract — Milestone 3 assessment

## What could be inspected
- The ERCOT repository (GitHub main at the beginning of this milestone) includes the research JSON graph, model metrics, 38 exported PNG notebook figures, Plotly offline viewer, and Milestones 1–2 research interfaces.
- A historical October 14, 2026 Studio S development status document was available from the user's prior work. It records an earlier checkpoint tagged v0.2.0-dev.1 and describes a v2 canonical project graph, scene/layer ordering, cues, keyframes, media/audio/caption support, JSON/YAML compiler, TypeScript/JavaScript SDK and CLI.
- The historical report says external executable TypeScript builders require an explicit `--allow-code` option and emphasizes preserving source/override regeneration.
- These are **historical descriptions**, not directly validated against current Studio S implementation.

## What could not be verified
- Current Studio S application source, its package version and Git HEAD, current JSON Schema for scene creation, exact import/export entry point, media asset resolution, reproducible render behavior for ERCOT figures, and Mac acceptance.
- Native runtime compatibility with proposed research scene exports.
- Asset packaging, timeline frame positioning and narration synchronization with the actual current Studio S build.

## Field-by-field gap before a native adapter

| Research scene authoring field | Probable Studio S target | Verification needed |
| --- | --- | --- |
| `scene_id`, `order`, `title` | Stable scene IDs and track/scene order | Exact v2 IDs, legal scene order, collision policy |
| `narration`, `narrator` | Audio asset and transcript/caption time span | Real recording path, codec, sample rate, script-to-audio timing |
| `on_screen_text` | Timeline text object and animation entry/exit | Object schema, typography, frame coordinates |
| Figure PNG and notebook provenance | Media asset and optional callout/animation region | Local asset path containment, hashes, manifest and render reconciliation |
| Numeric evidence and caveats | Context metadata/text overlays | Source fidelity, unit visibility and approved presentation placement |
| `review` status | External editorial approval metadata | No claim current Studio S imports such fields |
| Source graph relationships | External research provenance | Separate metadata sidecar or verified supported extension point |
| Presentation length | Frame/scene duration | Scene timeline frames, audio anchors and intro/outro timings |

## Decision
**Do not implement or invoke a native Studio S importer from this repository yet.** The authoring export is `ercot-scene-sequence/v1` and explicitly non-native. It is suitable for preserving research and preparing an implementation-independent handoff, not for direct execution or deterministic video rendering.

## What the next coding task requires
Access to a current Studio S ZIP or linked repository with `package.json`, live schema/compiler, SDK/CLI, tests and sample scene. Validate the real interface in a disposable fixture. Confirm actual support for each above field, write a mapping spec and negative tests, then implement the minimum adapter. Preserve Electron + Canvas, the v2 graph, source/override edits and code execution gates. Never silently discard unattached proof or source references.
