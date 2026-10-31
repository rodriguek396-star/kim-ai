from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal, Any
from uuid import uuid4
import json
from .config import settings
from .db import db, init_db
from .services.assistant import answer

app = FastAPI(title='KIM API', version='1.0.0', description='Assistant d’orientation multilingue du Centre Ivoiro-Coréen')
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(',')], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
@app.on_event('startup')
def startup(): init_db()

class ChatIn(BaseModel): message: str = Field(min_length=1,max_length=3000); language: str='fr'; session_id: str='visitor'
class RequestIn(BaseModel): type: Literal['room','activity','partnership','contact']; payload: dict[str,Any]
class StatusIn(BaseModel): status: Literal['PENDING','IN_REVIEW','APPROVED','REJECTED','CONTACTED']; admin_note: str=''

@app.get('/api/health')
def health(): return {'status':'ok','storage':settings.storage_mode,'ai':settings.ai_provider}
@app.get('/api/activities')
def activities():
    with db() as c:
        if settings.storage_mode == 'snowflake':
            cur=c.cursor(); cur.execute('SELECT ID,NAME,CATEGORY,ELIGIBILITY,DESCRIPTION,PLACES,ACTIVE FROM ACTIVITIES WHERE ACTIVE=TRUE'); rows=cur.fetchall(); cur.close()
            return [dict(zip(['id','name','category','eligibility','description','places','active'],r)) for r in rows]
        return [dict(r) for r in c.execute('SELECT * FROM activities WHERE active=1').fetchall()]
@app.get('/api/rooms')
def rooms():
    with db() as c:
        if settings.storage_mode == 'snowflake':
            cur=c.cursor(); cur.execute('SELECT ID,NAME,CAPACITY,EQUIPMENT,ACTIVE FROM ROOMS WHERE ACTIVE=TRUE'); rows=cur.fetchall(); cur.close(); return [dict(zip(['id','name','capacity','equipment','active'],r)) for r in rows]
        return [dict(r) for r in c.execute('SELECT * FROM rooms WHERE active=1').fetchall()]
@app.post('/api/chat')
async def chat(data: ChatIn):
    result=await answer(data.message,data.language)
    with db() as c:
        if settings.storage_mode != 'snowflake':
            c.execute('INSERT INTO messages(session_id,role,content) VALUES(?,?,?)',(data.session_id,'user',data.message))
            c.execute('INSERT INTO messages(session_id,role,content) VALUES(?,?,?)',(data.session_id,'assistant',result['answer']))
    return result
@app.post('/api/requests')
def create_request(data: RequestIn):
    rid='KIM-'+uuid4().hex[:8].upper()
    with db() as c:
        if settings.storage_mode == 'snowflake':
            cur=c.cursor(); cur.execute('INSERT INTO REQUESTS(ID,TYPE,PAYLOAD,STATUS) SELECT %s,%s,PARSE_JSON(%s),%s',(rid,data.type,json.dumps(data.payload,ensure_ascii=False),'PENDING')); cur.close()
        else: c.execute('INSERT INTO requests(id,type,payload,status) VALUES(?,?,?,?)',(rid,data.type,json.dumps(data.payload,ensure_ascii=False),'PENDING'))
    return {'id':rid,'status':'PENDING','message':'Demande transmise. Elle reste en attente de validation humaine.'}
@app.get('/api/admin/overview')
def overview():
    with db() as c:
        if settings.storage_mode == 'snowflake':
            cur=c.cursor(); cur.execute("SELECT STATUS,COUNT(*) FROM REQUESTS GROUP BY STATUS"); rows=cur.fetchall(); cur.close(); counts={r[0]:r[1] for r in rows}; total=sum(counts.values()); pending=counts.get('PENDING',0); recent=[]
        else:
            total=c.execute('SELECT COUNT(*) FROM requests').fetchone()[0]; pending=c.execute("SELECT COUNT(*) FROM requests WHERE status='PENDING'").fetchone()[0]
            recent=[dict(r) for r in c.execute('SELECT id,type,payload,status,created_at FROM requests ORDER BY created_at DESC LIMIT 8').fetchall()]
    return {'total_requests':total,'pending':pending,'activities':len(activities()),'rooms':len(rooms()),'recent':recent}
@app.get('/api/admin/requests')
def list_requests(type: str|None=None):
    with db() as c:
        if settings.storage_mode == 'snowflake':
            cur=c.cursor(); sql='SELECT ID,TYPE,PAYLOAD,STATUS,CREATED_AT,ADMIN_NOTE FROM REQUESTS'; params=[]
            if type: sql+=' WHERE TYPE=%s'; params.append(type)
            sql+=' ORDER BY CREATED_AT DESC'; cur.execute(sql,params); rows=cur.fetchall(); cur.close(); return [{'id':r[0],'type':r[1],'payload':r[2],'status':r[3],'created_at':str(r[4]),'admin_note':r[5]} for r in rows]
        sql='SELECT * FROM requests'; params=[]
        if type: sql+=' WHERE type=?'; params.append(type)
        sql+=' ORDER BY created_at DESC'; rows=[dict(r) for r in c.execute(sql,params).fetchall()]
        for r in rows: r['payload']=json.loads(r['payload'])
        return rows
@app.patch('/api/admin/requests/{request_id}')
def update_request(request_id: str, data: StatusIn):
    with db() as c:
        if settings.storage_mode == 'snowflake':
            cur=c.cursor(); cur.execute('UPDATE REQUESTS SET STATUS=%s,ADMIN_NOTE=%s WHERE ID=%s',(data.status,data.admin_note,request_id)); cur.close()
        else:
            cur=c.execute('UPDATE requests SET status=?,admin_note=? WHERE id=?',(data.status,data.admin_note,request_id))
            if cur.rowcount==0: raise HTTPException(404,'Demande introuvable')
    return {'id':request_id,'status':data.status}
@app.get('/api/admin/conversations')
def conversations():
    with db() as c:
        if settings.storage_mode == 'snowflake': return []
        rows=c.execute('SELECT session_id,MAX(created_at) last_message,COUNT(*) messages FROM messages GROUP BY session_id ORDER BY last_message DESC').fetchall()
        return [dict(r) for r in rows]
