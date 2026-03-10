from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import firebase_admin
from firebase_admin import credentials, firestore

from agents.task_agent import nexus_agent

app = FastAPI(
    title="Nexus AI Backend",
    version="1.0.0"
)

# Allow Flutter / Web apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Firebase Initialization
# -----------------------------
db = None

try:

    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")

    if os.path.exists(cred_path):

        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        db = firestore.client()
        print("Firebase initialized")

    else:
        print("Firebase credentials not found. Running without Firebase.")

except Exception as e:
    print(f"Firebase Initialization Failed: {e}")


# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def root():
    return {"message": "Nexus AI Backend Running"}


@app.post("/agent/analyze-task")
async def analyze_task(data: dict):

    description = data.get("description")

    if not description:
        return {"error": "No description provided"}

    ai_response = await nexus_agent.analyze_requirement(description)

    # Save to Firestore if available
    if db:
        db.collection("tasks").add({
            "description": description,
            "response": ai_response
        })

    return {
        "response": ai_response
    }


@app.get("/agent/history")
def get_history():

    if not db:
        return {"tasks": []}

    tasks = []

    docs = db.collection("tasks").stream()

    for doc in docs:
        tasks.append(doc.to_dict())

    return {"tasks": tasks}
