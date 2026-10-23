# AIDA Studio

A browser-first AI-native music studio focused on preserving real vocal performances while helping musicians create, arrange, and mix backing tracks.

## Product direction

- Suno Studio-inspired workflow patterns: a dark creative workspace, multitrack arrangement, transport controls, a creation panel, and mixer.
- Original AIDA branding and original UI implementation; no Suno logos, names, or proprietary assets are reused.
- Keep uploaded audio local in the browser prototype.
- Build toward non-destructive vocal processing, editable arrangement, reference-guided mixing, and model-assisted accompaniment generation.

## Current prototype

The feature branch `feat/suno-inspired-studio-shell` contains a self-contained browser prototype in `index.html`.

Implemented interactions:
- Import and decode an audio file locally; display a waveform preview.
- Play/stop imported audio with optional simple high-pass EQ and dynamics compression.
- Generate a basic procedural drum/bass backing groove locally (this is not an AI music model).
- Adjust track/master levels.
- Save session settings to a JSON file.
- Render and download a WAV preview.

Known prototype limitations:
- Beat generation is procedural synthesis; it is not yet generative AI and won't sound like a finished commercial instrumental.
- Reverb and delay switches are surfaced in the UI but are not wired into the signal chain yet.
- The export renders the vocal and basic generated accompaniment but doesn't yet mirror every live effect or provide true multitrack/stem export.
- Project JSON does not embed audio files.
- No user accounts, cloud project storage, or backend inference service exists yet.

## Run locally

Because this prototype is a static page, you can open `index.html` directly in a modern browser. If the browser restricts local file playback, serve the repository with any static HTTP server, for example:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Verification checklist

1. Open the page in a recent Chrome or Edge browser.
2. Import a WAV/MP3 vocal recording and confirm a waveform appears.
3. Play and stop the recording.
4. Enable/disable EQ and compression; confirm future playback reflects the selected settings.
5. Generate the procedural beat and play it alongside the vocal.
6. Change BPM/key, adjust mixer levels, export WAV, and save session JSON.
7. Confirm no audio is uploaded to any remote service by this prototype.

## Commercial-use note

Review license terms for every dependency, model checkpoint, generated sample, and service before distributing a commercial product. This repository currently has no third-party runtime dependencies.
