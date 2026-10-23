# AIDA Studio

A browser-first AI-native music studio focused on preserving real vocal performances while helping musicians create, arrange, and mix backing tracks.

## Product direction

- Original AIDA branding and a dark, Suno Studio-inspired workflow.
- Local vocal import and waveform preview.
- Browser audio playback with basic EQ, compression, optional reverb and delay audition sends.
- Procedurally synthesized drum/bass backing ideas.
- Track-level and master gain controls.
- WAV preview export and project-settings JSON export/import.

## Run locally

Requires Node.js 20+ for the smoke tests, but the studio itself is a static page.

```bash
git clone -b feat/suno-inspired-studio-shell https://github.com/chaitanya-92/aidaw.git
cd aidaw
python3 -m http.server 8000
```

Open http://localhost:8000 in Chrome or Edge.

Run source smoke tests:

```bash
npm test
```

## Current limitations — not yet a finished DAW

- The beat generator is procedural synthesis, not generative AI; it is only a rough musical sketch.
- The timeline is currently a visual arrangement scaffold, not a complete clip editor. Dragging, trimming, splitting, snapping, automation, and a piano roll are not implemented.
- Effects are basic browser audition effects; pitch correction, full parametric EQ, sidechain, bus routing, mastering, and plugin hosting are not implemented.
- WAV export renders a basic vocal + beat approximation; not every live effect is rendered identically and multitrack/stem export is not implemented.
- Project JSON stores settings, not the audio file. Re-import the vocal after loading a project.
- No AI inference backend, user accounts, cloud storage, collaboration, autosave, or production deployment exists yet.

## Verification

The smoke test checks for key controls, JavaScript syntax, core audio functions, project import/export hooks, and honest labeling of procedural generation. It does not replace testing in a real browser with real audio files.

## Commercial-use note

Review licenses for every dependency, model checkpoint, generated sample, and service before commercial distribution. This prototype currently has no third-party runtime dependencies.
