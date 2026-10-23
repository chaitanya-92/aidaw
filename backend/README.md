# AIDA local AI music bridge

This optional FastAPI bridge connects the browser studio to a locally running ACE-Step 1.5 API server. It does not include model weights or a hosted GPU service.

## Requirements

- Python 3.10+
- ACE-Step 1.5 installed and running on `http://127.0.0.1:8001`
- Compatible compute, storage and model weights. The browser alone cannot run the music model.

Install and start ACE-Step using its official instructions: https://github.com/ace-step/ACE-Step-1.5 . Its documented API workflow is here: https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/API.md

## Start the AIDA bridge

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app:app --host 127.0.0.1 --port 8002
```

If your model server uses a different address, export `ACE_STEP_URL` before starting Uvicorn. If it requires authentication, export `ACE_STEP_API_KEY` as well. Never place secrets in browser JavaScript.

Serve the UI in a second terminal:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000`, go to **Vocal mix → Reference beat lab**, upload a reference audio file, enter a new instrumental prompt, and choose **Generate reference-inspired beat**. The app submits a reference-conditioned task to ACE-Step and polls until an audio file is ready.

## Privacy and cost

The reference file is sent to the configured ACE-Step URL. If that server is local, inference can stay on your machine. Model downloads use storage and bandwidth; inference uses compute and electricity. A hosted GPU may cost money. Do not expose this development bridge directly to the public internet.

## Commercial use

The ACE-Step 1.5 model card currently lists an MIT license, but review the exact checkpoint, dependencies, dataset/model terms, and generated-output risks before commercial release. This integration does not guarantee that generated music is non-infringing or professionally mixed.
