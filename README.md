# AIDA Studio

A browser-first AI-native music studio prototype. It aims to help musicians preserve real vocal performances while creating, arranging, and mixing backing tracks.

## Current features

- Local audio import and waveform preview.
- Browser playback with high-pass EQ, compression, reverb and delay audition paths.
- Procedural drum/bass sketch generation (not AI-generated music).
- Reference audio analysis for rough duration, level and frequency-energy diagnostics.
- DSP-based assisted WAV render.
- **Optional ACE-Step 1.5 reference-conditioned music generation bridge**: upload a reference beat, describe a new instrumental, set duration and reference influence, and receive generated audio from a locally configured ACE-Step server.
- Project-settings JSON export/import. Audio files are not embedded in the JSON.

## Run the browser UI

```bash
git clone -b feat/suno-inspired-studio-shell https://github.com/chaitanya-92/aidaw.git
cd aidaw
python3 -m http.server 8000
```

Open http://localhost:8000.

## Enable actual AI beat generation

The AI generation feature requires ACE-Step 1.5 running locally; the repository does not bundle model weights or a hosted GPU. Follow the model's official setup: https://github.com/ace-step/ACE-Step-1.5 . Official API docs: https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/API.md

In another terminal, from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app:app --host 127.0.0.1 --port 8002
```

ACE-Step should be reachable at `http://127.0.0.1:8001` by default. Override with `ACE_STEP_URL` if needed. If the model server requires an API key, set `ACE_STEP_API_KEY` in the shell before starting the bridge. Never put model/API secrets in browser JavaScript.

Open the studio, choose **Vocal mix → Reference beat lab**, upload your reference, enter a prompt, and click **Generate reference-inspired beat**. The browser sends the reference audio to the configured model server, polls the task, and exposes the returned WAV.

## What this is not yet

- AI generation will only work after a compatible ACE-Step server is installed, downloaded, running, and tested on your hardware.
- Reference-conditioned generation can guide style; it does not promise an exact reproduction or guaranteed professional arrangement.
- The assisted mix is conventional DSP, not a trained AI mixing engineer. It does not automatically split a stereo master into vocal and instrumental stems.
- No pitch correction, full parametric EQ, true editable clip timeline, MIDI piano roll, full stem export, user accounts, cloud sessions, or collaboration.
- No browser integration test or subjective audio-quality test has been completed yet.

## Cost and licensing

The ACE-Step 1.5 model card lists an MIT license. Review the exact model/checkpoint, all dependencies and applicable terms before commercial distribution. Running locally avoids per-generation API charges but still requires compute, storage, downloads and electricity; hosted GPU services may cost money. Do not expose this local development bridge to the public internet without authentication and security hardening.
