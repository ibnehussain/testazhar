"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

# ============================================================
# UAT-LOCKED: This route has passed UAT. DO NOT MODIFY.
# ============================================================
@app.get("/activities")
def get_activities():
    return activities


# ============================================================
# UAT-LOCKED: This route has passed UAT. DO NOT MODIFY.
# ============================================================
@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.get("/activities/{activity_name}/is-full")
def is_activity_full(activity_name: str):
    """Check whether an activity has reached its maximum capacity."""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    participants_count = len(activity["participants"])
    max_participants = activity["max_participants"]

    if participants_count >= max_participants:
        return {"activity": activity_name, "is_full": True}

    return {
        "activity": activity_name,
        "is_full": False,
        "spots_remaining": max_participants - participants_count,
    }


# ============================================================
# Capstone: Query Classification and Ask Endpoint
# ============================================================

def classify_query(question: str) -> str:
    """Classify a question as RAG, Text2SQL, or unknown.
    
    Determines the type of query based on keyword matching:
    - RAG (qualitative): what, describe, tell me about, how does, explain
    - Text2SQL (quantitative): how many, which, list, count, total, how much, how full
    - Unknown: anything else
    
    Args:
        question: The user's question as a string
        
    Returns:
        "rag" for qualitative questions, "text2sql" for quantitative questions, 
        "unknown" for anything else
    """
    q_lower = question.lower()
    
    # Qualitative keywords (RAG)
    qualitative_keywords = ["what", "describe", "tell me about", "how does", "explain"]
    for keyword in qualitative_keywords:
        if keyword in q_lower:
            return "rag"
    
    # Quantitative keywords (Text2SQL)
    quantitative_keywords = ["how many", "which", "list", "count", "total", "how much", "how full"]
    for keyword in quantitative_keywords:
        if keyword in q_lower:
            return "text2sql"
    
    return "unknown"


@app.post("/api/ask")
async def ask(request: Request):
    """Handle questions about activities using RAG or Text2SQL.
    
    Reads a JSON request with a 'question' field, classifies the question type,
    and routes to the appropriate tool (RAG for qualitative, Text2SQL for quantitative).
    
    Request body: {"question": str}
    Response: {"answer": str, "source": str, "confidence": float}
    
    Returns:
        - 200: Successful response with answer
        - 400: Missing or empty question field
        - 500: Error during classification or tool execution
    """
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "question field required"}, status_code=400)
    
    # Validate question field
    if not data or "question" not in data or not data.get("question"):
        return JSONResponse({"error": "question field required"}, status_code=400)
    
    question = data["question"]
    
    try:
        route = classify_query(question)
        
        if route == "rag":
            # Route to RAG tool
            try:
                from src.rag.kb_search import search_kb
                results = search_kb(question)
                
                if results:
                    answer = " ".join([
                        f"{r.get('title', 'Unknown')}: {r.get('description', '')}" 
                        for r in results
                    ])
                else:
                    answer = "No relevant activities found for your question."
                
                return JSONResponse({
                    "answer": answer,
                    "source": "rag",
                    "confidence": 0.8
                })
            except Exception as e:
                return JSONResponse({"error": "classification failed"}, status_code=500)
        
        elif route == "text2sql":
            # Route to Text2SQL tool
            try:
                from src.text2sql.queries import SQL_QUERIES
                # Placeholder for text2sql execution
                answer = f"Query for: {question}"
                return JSONResponse({
                    "answer": answer,
                    "source": "text2sql",
                    "confidence": 0.7
                })
            except Exception as e:
                return JSONResponse({"error": "classification failed"}, status_code=500)
        
        else:
            # Unknown query type
            return JSONResponse({
                "answer": "I can only answer questions about activities. Try asking what an activity is about, or how many students have joined.",
                "source": "direct",
                "confidence": 1.0
            })
    
    except Exception as e:
        return JSONResponse({"error": "classification failed"}, status_code=500)


# Stubs — Developer B will replace with real implementations
def rag_search(question: str) -> dict:
    """Placeholder: returns stub RAG answer."""
    return {
        "answer": f"[RAG stub] Answer about: {question}",
        "source": "rag",
        "confidence": 0.0
    }

def run_text2sql(question: str) -> dict:
    """Placeholder: returns stub Text2SQL answer."""
    return {
        "answer": f"[Text2SQL stub] Data answer for: {question}",
        "source": "text2sql",
        "confidence": 0.0
    }