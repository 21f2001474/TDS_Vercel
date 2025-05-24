from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the JSON file only once
json_path = os.path.join(os.path.dirname(__file__), "q-vercel-python.json")
with open(json_path, "r") as f:
    student_data = json.load(f)

# Create name → marks map
name_to_marks = {entry["name"]: entry["marks"] for entry in student_data}

@app.get("/")
def get_marks(request: Request):
    names = request.query_params.getlist("name")
    result = [name_to_marks.get(name, None) for name in names]
    return {"marks": result}
