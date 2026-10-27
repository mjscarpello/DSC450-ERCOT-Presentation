# Research-highlight to Studio S mapping

**Verified against the supplied Studio S v0.2.0-dev.8 M01F checkpoint** (workspace spec `0.1.0-draft.1`, graph v2). The screenshot editor and modular compiler do not accept arbitrary executable Python; use Python to generate reviewed, data-only JSON first.

| Source item | Target |
| --- | --- |
| Original raster pixel box | Asset `regions.<id>.rectNormalized`, based on *image* width/height |
| Region ID | Focus-outline object `region` value |
| Scene image object | Focus-outline `target` reference |
| Approved narrated phrase | Named speech cue after exact audio and timed transcript anchor are available |
| Exact start/end | Clip sample-based speech anchor resolved by the Studio S compiler, not an estimated text timestamp |
| Scene duration / placement | Reviewed Studio S modular scene/audio/cue source JSON |

**Different coordinate spaces:** the image's native pixels and normalized region are not the presentation canvas coordinates. When an image object is fit with margins, account for its object layout and letterboxing before drawing previews.

**Known audit discrepancy:** the source stakeholder scene plan's S18 includes visual cues for F26 and D09 but its asset list omits them. Resolve/approve these asset references before generating S18 native code.

**Source privacy:** the full narration scripts remain on OneDrive; use stable line IDs and hashes rather than checking all teammates' lines or recordings into a public repository.

**Gates:** review source figures including the corrected F09; quantify ROI with reproducible source plots or image inspection; approve overlays; align audio; compile and render one test scene; extend to the full show.
