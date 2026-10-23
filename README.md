# AIDA Studio

A browser-first AI-native music studio prototype focused on preserving source performances while helping musicians create and mix backing tracks.

## Current prototype features

- Import local audio and display a waveform preview.
- Browser playback with basic high-pass EQ, compression, reverb and delay audition paths.
- Procedurally synthesized drum/bass backing ideas (not AI-generated music).
- Reference beat upload and a rough local audio profile report (duration, channel count, RMS/peak level, and rough low/mid/high energy estimates).
- DSP-based assisted WAV render with selectable balanced, vocal-forward, or warm processing.
- Track/master gain controls and WAV preview export.
- Project settings JSON export/import. Uploaded audio itself is not embedded.

## Run locally

The studio is a static page; no runtime dependency install is needed.

```bash
git clone -b feat/suno-inspired-studio-shell https://github.com/chaitanya-92/aidaw.git
cd aidaw
python3 -m http.server 8000
```

Open http://localhost:8000 in Chrome or Edge.

Run smoke tests with Node.js 20+:

```bash
npm test
```

## Important limitations

This is not yet a finished DAW or a professional AI mixing service.

- Reference beat analysis does not generate a similar beat. A true reference-conditioned generator requires a suitable model/inference backend and evaluation.
- The assisted mix is a conservative DSP chain, not a trained AI mixing engineer. It processes the currently uploaded audio file as one source; it cannot independently rebalance vocal and instrumental stems from a single stereo master.
- No pitch correction/autotune, full parametric EQ, clip editing, automation, MIDI piano roll, multitrack stem export, cloud sessions, accounts, or collaboration.
- Project JSON stores settings only; audio must be re-imported.
- WAV preview export does not yet reproduce every live effect identically.
- No remote AI inference service is connected. Audio stays in the browser in this prototype.

## Verification

GitHub Actions runs zero-dependency Node smoke tests for key controls, inline JavaScript syntax, audio workflow hooks, reference analysis, and assisted mix rendering. These are source-level checks, not subjective audio-quality tests or full browser integration tests.

## Commercial-use note

Review the licenses and terms for every dependency, model checkpoint, generated sample, and inference service before commercial distribution.
