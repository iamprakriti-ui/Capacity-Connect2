courses=[await course_with_progress(user["id"],c) async for c in db.courses.find({}, {"_id":0})]
    skills=await db.skills.find({}, {"_id":0}).to_list(50); assessments=await db.assessments.find({}, {"_id":0}).to_list(50); certificates=await db.certificates.find({"user_id":user["id"]},{"_id":0}).to_list(50)
    return {"user":public(user),"stats":[{"label":"Capability score","value":"78","suffix":"/100","delta":"+6.4%","tone":"cyan"},{"label":"Learning progress","value":"64","suffix":"%","delta":"+12.8%","tone":"blue"},{"label":"Learning hours","value":"24.5","suffix":"hrs","delta":"+4.2h this month","tone":"violet"},{"label":"Certificates","value":f"{len(certificates):02d}","suffix":"earned","delta":"1 this quarter","tone":"green"}],"courses":courses,"skills":skills,"assessments":assessments,"certificates":certificates,"activity":[{"title":"Completed SQL for Analysts","meta":"Course completion · 2h ago","icon":"check"},{"title":"Earned Data Literacy certificate","meta":"Achievement · Yesterday","icon":"award"}]}
@app.get("/api/courses")
async def courses(user=Depends(current_user)):
    rows=[await course_with_progress(user["id"],c) async for c in db.courses.find({}, {"_id":0})]; return {"courses":rows}
@app.get("/api/courses/{course_id}")
async def course_detail(course_id: str, user=Depends(current_user)):
    course=await db.courses.find_one({"id":course_id},{"_id":0});
    if not course: raise HTTPException(404,"Course not found")
    return await course_with_progress(user["id"],course)
@app.post("/api/courses/{course_id}/progress")
async def update_progress(course_id: str, body: ProgressInput, user=Depends(current_user)):
    course=await db.courses.find_one({"id":course_id},{"_id":0});
    if not course: raise HTTPException(404,"Course not found")
    enrollment=await db.enrollments.find_one({"user_id":user["id"],"course_id":course_id}) or {"id":f"en-{secrets.token_hex(6)}","user_id":user["id"],"course_id":course_id,"progress":0,"completed_lessons":[]}
    done=set(enrollment.get("completed_lessons",[])); done.add(body.lesson_id); progress=round(len(done)/max(len(course.get("lessons",[])),1)*100)
    await db.enrollments.update_one({"id":enrollment["id"]},{"$set":{"completed_lessons":list(done),"progress":progress,"updated_at":now()}},upsert=True)
    if progress>=100: await db.certificates.update_one({"user_id":user["id"],"course_id":course_id},{"$setOnInsert":{"id":f"cert-{secrets.token_hex(6)}","user_id":user["id"],"course_id":course_id,"title":course["title"],"issuer":"CAPACITY CONNECT","date":now()[:10],"code":f"CC-{secrets.token_hex(3).upper()}"}},upsert=True)
    return {"progress":progress,"completed_lessons":list(done),"certificate_earned":progress>=100}
@app.get("/api/assessments")
async def assessments(user=Depends(current_user)): return {"assessments":await db.assessments.find({}, {"_id":0}).to_list(50)}
@app.post("/api/assessments/{assessment_id}/submit")
async def submit_assessment(assessment_id: str, body: QuizInput, user=Depends(current_user)):
    assessment=await db.assessments.find_one({"id":assessment_id},{"_id":0});
    if not assessment: raise HTTPException(404,"Assessment not found")
    score=min(100,round((sum(1 for answer in body.answers if answer == 1)/max(len(body.answers),1))*100)); await db.assessment_results.update_one({"assessment_id":assessment_id,"user_id":user["id"]},{"$set":{"score":score,"answers":body.answers,"submitted_at":now()}},upsert=True); return {"score":score,"passed":score>=70}
@app.get("/api/certificates")
async def certificates(user=Depends(current_user)): return {"certificates":await db.certificates.find({"user_id":user["id"]},{"_id":0}).to_list(50)}
@app.get("/api/skills")
async def skills(user=Depends(current_user)): return {"skills":await db.skills.find({}, {"_id":0}).to_list(50)}
