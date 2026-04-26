from fastapi import FastAPI
from pydantic import BaseModel

# ✅ Correct imports (IMPORTANT FIX)
from backend.agents.generator import generator_agent
from backend.agents.reviewer import reviewer_agent

app = FastAPI()


# ✅ Request Body Model
class InputData(BaseModel):
    grade: int
    topic: str


# ✅ API Endpoint
@app.post("/generate")
def run_pipeline(data: InputData):
    grade = data.grade
    topic = data.topic

    # Step 1: Generator
    gen_output = generator_agent(grade, topic)

    # Step 2: Reviewer
    review = reviewer_agent(gen_output, grade)

    # Step 3: Refinement (if fail)
    if review["status"] == "fail":
        refined = generator_agent(grade, topic, review["feedback"])
        return {
            "initial": gen_output,
            "review": review,
            "refined": refined
        }

    return {
        "initial": gen_output,
        "review": review
    }


# ✅ Health check route
@app.get("/")
def home():
    return {"message": "AI Agent System Running 🚀"}