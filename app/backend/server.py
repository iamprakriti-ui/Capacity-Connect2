from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from typing import List
from datetime import datetime, timezone
import os
from emergentintegrations.llm.chat import LlmChat, UserMessage, TextDelta, StreamDone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")
app = FastAPI(title="CAPACITY CONNECT API")

COURSES = [
    {"id":"c1","title":"Advanced Data Analytics","category":"Data & Insights","skill":"Data Analytics","level":"Advanced","duration":"6h 20m","progress":68,"lessons":12,"trainer":"Maya Chen","match":96,"image":"https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80"},
    {"id":"c2","title":"Strategic Communication","category":"Leadership","skill":"Communication","level":"Intermediate","duration":"3h 45m","progress":34,"lessons":8,"trainer":"Ethan Cole","match":89,"image":"https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=800&q=80"},
    {"id":"c3","title":"Leading With Influence","category":"Leadership","skill":"Leadership","level":"Intermediate","duration":"4h 10m","progress":0,"lessons":10,"trainer":"Priya Shah","match":84,"image":"https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80"},
]
SKILLS = [
    {"name":"Data Analytics","current":62,"required":85,"gap":23,"trend":"+8%"},
    {"name":"Strategic Thinking","current":74,"required":82,"gap":8,"trend":"+4%"},
    {"name":"Communication","current":78,"required":88,"gap":10,"trend":"+12%"},
    {"name":"Leadership","current":54,"required":80,"gap":26,"trend":"+2%"},
    {"name":"Project Management","current":91,"required":90,"gap":0,"trend":"+6%"},
]

class RecommendationRequest(BaseModel):
    skill: str = "Data Analytics"

@app.get("/api/")
async def root(): return {"message":"CAPACITY CONNECT API is ready"}

@app.get("/api/dashboard")
async def dashboard():
    return {"user":{"name":"Jordan Mitchell","role":"EMPLOYEE","team":"Product Operations","initials":"JM"},"stats":[{"label":"Capability score","value":"78","suffix":"/100","delta":"+6.4%","tone":"cyan"},{"label":"Learning progress","value":"64","suffix":"%","delta":"+12.8%","tone":"blue"},{"label":"Learning hours","value":"24.5","suffix":"hrs","delta":"+4.2h this month","tone":"violet"},{"label":"Certificates","value":"06","suffix":"earned","delta":"2 this quarter","tone":"green"}],"courses":COURSES,"skills":SKILLS,"assessments":[{"title":"Data Storytelling Fundamentals","course":"Advanced Data Analytics","date":"Today · 3:30 PM","type":"Quiz","status":"Due soon"},{"title":"Communication Style Index","course":"Strategic Communication","date":"Tomorrow · 11:00 AM","type":"Assessment","status":"Scheduled"}],"activity":[{"title":"Completed SQL for Analysts","meta":"Course completion · 2h ago","icon":"check"},{"title":"Earned Data Literacy certificate","meta":"Achievement · Yesterday","icon":"award"},{"title":"Started Strategic Communication","meta":"Learning activity · 3 days ago","icon":"play"}]}

@app.get("/api/courses")
async def courses(): return {"courses":COURSES}

@app.get("/api/skills")
async def skills(): return {"skills":SKILLS}

@app.get("/api/assessments")
async def assessments(): return {"assessments":[{"title":"Data Storytelling Fundamentals","course":"Advanced Data Analytics","date":"Today · 3:30 PM","type":"Quiz","status":"Due soon","questions":18,"duration":"25 min"},{"title":"Communication Style Index","course":"Strategic Communication","date":"Tomorrow · 11:00 AM","type":"Assessment","status":"Scheduled","questions":32,"duration":"40 min"},{"title":"Project Planning Checkpoint","course":"Project Management Essentials","date":"Jun 18 · 10:00 AM","type":"Quiz","status":"Scheduled","questions":12,"duration":"20 min"}]}

@app.get("/api/certificates")
async def certificates(): return {"certificates":[{"title":"Data Literacy Foundations","issuer":"CAPACITY CONNECT","date":"May 24, 2025","code":"CC-DL-2405","color":"cyan"},{"title":"SQL for Analysts","issuer":"CAPACITY CONNECT","date":"May 12, 2025","code":"CC-SQL-1205","color":"blue"},{"title":"Agile Project Essentials","issuer":"CAPACITY CONNECT","date":"Apr 29, 2025","code":"CC-AG-2904","color":"violet"}]}

@app.post("/api/ai/recommendations")
async def ai_recommendations(request: RecommendationRequest):
    key = os.environ.get("EMERGENT_LLM_KEY")
    async def stream():
        if not key:
            yield "data: Your profile shows a meaningful opportunity to strengthen advanced data analytics.\n\n"; return
        chat = LlmChat(api_key=key, session_id=f"capacity-{request.skill}", system_message="You are Capacity Connect's premium learning advisor. Give concise, practical advice for an employee skill gap. Keep it under 90 words and mention why the skill matters, one action, and confidence.").with_model("openai", "gpt-5.4")
        try:
            async for event in chat.stream_message(UserMessage(text=f"Analyze this skill gap: {request.skill}. Recommend the best next learning step.")):
                if isinstance(event, TextDelta): yield f"data: {event.content}\n\n"
                elif isinstance(event, StreamDone): break
        except Exception:
            yield "data: Your profile shows a meaningful opportunity to strengthen advanced data analytics. Start with the recommended course to build confidence through applied practice.\n\n"
    return StreamingResponse(stream(), media_type="text/event-stream", headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})

app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","), allow_methods=["*"], allow_headers=["*"])

@app.on_event("shutdown")
async def shutdown_db_client(): pass
