import json, os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote
import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

load_dotenv(Path(__file__).with_name('.env'))
BASE = os.getenv('ACE_STEP_URL', 'http://127.0.0.1:8001').rstrip('/')
TOKEN = os.getenv('ACE_STEP_API_KEY', '')
app = FastAPI(title='AIDA Studio AI Bridge', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:8000','http://127.0.0.1:8000','http://localhost:3000','http://127.0.0.1:3000'], allow_methods=['GET','POST','OPTIONS'], allow_headers=['*'])
def headers(): return {'Authorization': 'Bearer '+TOKEN} if TOKEN else {}
def unwrap(x):
    if isinstance(x,dict) and x.get('error'): raise HTTPException(502, str(x['error']))
    return x.get('data',x) if isinstance(x,dict) else x

@app.get('/api/health')
async def health():
    try:
        async with httpx.AsyncClient(timeout=4) as c: r=await c.get(BASE+'/health',headers=headers())
        return {'bridge':'ok','model_server':'reachable' if r.is_success else 'unhealthy'}
    except httpx.HTTPError: return {'bridge':'ok','model_server':'offline','hint':'Start ACE-Step API server; see backend/README.md'}

@app.post('/api/generate')
async def generate(prompt:str=Form(...),duration:int=Form(30),bpm:int=Form(92),key_scale:str=Form('Am'),influence:float=Form(.65),reference_audio:UploadFile=File(...)):
    prompt=prompt.strip()
    if not prompt or len(prompt)>2000: raise HTTPException(400,'Prompt must be 1–2000 characters.')
    if not 10<=duration<=180: raise HTTPException(400,'Duration must be 10–180 seconds.')
    if not 30<=bpm<=220: raise HTTPException(400,'BPM must be 30–220.')
    if not 0<=influence<=1: raise HTTPException(400,'Influence must be between 0 and 1.')
    if reference_audio.content_type and not reference_audio.content_type.startswith('audio/') and reference_audio.content_type!='application/octet-stream': raise HTTPException(415,'Upload an audio file.')
    data=await reference_audio.read(100*1024*1024+1)
    if not data or len(data)>100*1024*1024: raise HTTPException(413,'Reference audio must be smaller than 100 MB.')
    name=reference_audio.filename or 'reference.wav'; ext=os.path.splitext(name)[1].lower()
    if ext not in {'.wav','.mp3','.flac','.m4a','.aac','.ogg','.webm'}: ext='.wav'
    fields={'prompt':prompt,'task_type':'text2music','audio_format':'wav','audio_duration':str(duration),'bpm':str(bpm),'key_scale':key_scale[:32],'audio_cover_strength':str(influence),'model':'acestep-v15-turbo','thinking':'true'}
    try:
        async with httpx.AsyncClient(timeout=120) as c:
            r=await c.post(BASE+'/release_task',data=fields,files={'reference_audio':('reference'+ext,data,reference_audio.content_type or 'application/octet-stream')},headers=headers()); r.raise_for_status(); payload=unwrap(r.json())
    except httpx.ConnectError: raise HTTPException(503,'ACE-Step is offline. Start it using backend/README.md.')
    except httpx.HTTPStatusError as e: raise HTTPException(502,'ACE-Step rejected the request: '+e.response.text[:300])
    except (httpx.HTTPError,ValueError) as e: raise HTTPException(502,'Could not submit generation: '+str(e))
    task=payload.get('task_id') if isinstance(payload,dict) else None
    if not task: raise HTTPException(502,'ACE-Step did not return a task ID.')
    return {'task_id':task,'status':'queued','message':'Generation submitted to ACE-Step.'}

@app.get('/api/jobs/{task_id}')
async def status(task_id:str):
    if not task_id or len(task_id)>128 or not all(x.isalnum() or x in '-_' for x in task_id): raise HTTPException(400,'Invalid task ID.')
    try:
        async with httpx.AsyncClient(timeout=20) as c: r=await c.post(BASE+'/query_result',json={'task_id_list':[task_id]},headers=headers()); r.raise_for_status(); payload=unwrap(r.json())
    except httpx.ConnectError: raise HTTPException(503,'ACE-Step is offline.')
    except (httpx.HTTPError,ValueError) as e: raise HTTPException(502,'Could not query model: '+str(e))
    rows=payload if isinstance(payload,list) else payload.get('results',[]) if isinstance(payload,dict) else []
    row=next((x for x in rows if x.get('task_id')==task_id),rows[0] if rows else None)
    if not row: return {'task_id':task_id,'status':'running','message':'Waiting for model result.'}
    state=row.get('status',0)
    if state==2: return {'task_id':task_id,'status':'failed','message':str(row.get('error') or 'Generation failed.')[:400]}
    if state!=1: return {'task_id':task_id,'status':'running','message':'Generating audio…'}
    try:
        result=row.get('result',''); items=json.loads(result) if isinstance(result,str) else result; item=items[0] if isinstance(items,list) and items else items; path=item.get('file') or item.get('audio_path') or item.get('path')
    except (ValueError,TypeError,AttributeError): path=None
    if not path: return {'task_id':task_id,'status':'failed','message':'Model finished but did not return an audio path.'}
    return {'task_id':task_id,'status':'succeeded','audio_url':'/api/audio?path='+quote(str(path),safe=''),'message':'Generated audio is ready.'}

@app.get('/api/audio')
async def audio(path:str):
    if not path or len(path)>2048 or '..' in path or not path.startswith('/'): raise HTTPException(400,'Invalid audio path.')
    try:
        async with httpx.AsyncClient(timeout=120) as c:
            r=await c.get(BASE+path,headers=headers()) if path.startswith('/v1/audio?') else await c.get(BASE+'/v1/audio',params={'path':path},headers=headers()); r.raise_for_status()
            ct=r.headers.get('content-type','audio/wav')
            if not ct.startswith('audio/') and 'octet-stream' not in ct: raise HTTPException(502,'Model server did not return audio.')
            return Response(r.content,media_type=ct,headers={'Content-Disposition':'attachment; filename=aida-reference-beat.wav','Cache-Control':'no-store'})
    except httpx.HTTPError as e: raise HTTPException(502,'Could not download generated audio: '+str(e))
