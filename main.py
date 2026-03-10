import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import datetime

# 1. INITIALIZE FIREBASE
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    print("✅ Firebase Initialized Successfully")

except Exception as e:
    print(f"❌ Firebase Initialization Failed: {e}")


# 2. INITIALIZE GEMINI AI (NEW SDK)
import os
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


app = FastAPI(title="Nexus AI Backend")

# 3. CONFIGURE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Model
class TaskRequest(BaseModel):
    description: str


@app.get("/")
def read_root():
    return {
        "status": "Nexus AI Server is Live",
        "timestamp": datetime.datetime.now()
    }


# 4. AI TASK ANALYZER
@app.post("/agent/analyze-task")
async def analyze_task(request: TaskRequest):
    try:

        prompt = (
            f"As the Nexus AI Architect, analyze this task: '{request.description}'. "
            "Provide a concise Title, a 3-step technical roadmap, and a priority level."
        )

        # Gemini AI call
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt
        )

        ai_output = response.text

        task_data = {
            "title": request.description[:50],
            "full_description": request.description,
            "ai_analysis": ai_output,
            "status": "analyzed",
            "created_at": datetime.datetime.now(datetime.timezone.utc)
        }

        doc_ref = db.collection("tasks").add(task_data)

        return {
            "status": "success",
            "analysis": ai_output
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 5. GET TASK HISTORY
@app.get("/agent/history")
async def get_history():
    try:

        tasks_ref = db.collection("tasks").order_by(
            "created_at",
            direction=firestore.Query.DESCENDING
        )

        docs = tasks_ref.stream()

        history = [
            {**doc.to_dict(), "id": doc.id}
            for doc in docs
        ]

        return {"tasks": history}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 6. RUN SERVER
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
