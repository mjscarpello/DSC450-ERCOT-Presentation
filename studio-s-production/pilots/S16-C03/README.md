# S16-C03: native Studio S visual pilot (no narration)

This is a validated **single-file Studio S v2 source/Canvas pilot**, using the D05 figure and two transparent overlays with the exact same source image dimensions. The trial demonstrates 90,402 MWh actual demand versus an 83,898 MWh 50/50 hybrid prediction, a 6,504 MWh underforecast.

## Verified in Studio S v0.2.0-dev.8
- Core `compileSource` accepts the generated `pilot.source.json`, and core project validation reports zero errors.
- The original Studio S Canvas renderer draws the chart plus the transparent marker and bracket layers.
- 150 frames at 30 FPS were rendered, then encoded to an H264 MP4, 1280x760, five seconds.
- Source D05 SHA256: `c564cf0edd63cb65f01e096e962c415e267cfb2b6b7605868b02979405dc634c`.
- Marker source pixels: observed `(331,152)`; hybrid `(1240,189)`. Bracket at x=1083, y=152..189.
- Fixed demonstration entrances at frames 30 and 67 **do not represent real spoken timing**.

## Missing gates
Full modular workspace build, official CLI export, and desktop app import were **not** tested; installing the checkpoint dependencies failed in this environment. Real word-level narration alignment cannot be completed until audio is supplied.

## Get complete files
Use the conversation attachment `ERCOT_StudioS_S16_C03_Native_Render_Pilot.zip`: it includes the source JSON, compiled project, original source chart, transparent overlay PNGs, native renderer Python harness, MP4, three keyframes, source hashes and approval registry. These binary assets are **not** yet committed to GitHub. Extract its `studio_s_project/` and `native_render/` directories under this pilot folder before invoking the project here.

The pilot is a source-compatible visual test, **not** a compiled fully modular 19-scene presentation. See `cue_geometry.json` for source geometry and approval provenance.
