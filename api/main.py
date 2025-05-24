from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Enable CORS (allow all origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load JSON data once on startup
json_path = os.path.join(os.path.dirname(__file__), "q-vercel-python.json")
with open(json_path) as f:
    student_data = json.load(f)

# Map: name -> marks
name_to_marks = {entry["name"]: entry["marks"] for entry in student_data}

@app.get("/")
def get_marks(request: Request):
    names = request.query_params.getlist("name")
    if not names:
        single_name = request.query_params.get("name")
        if single_name:
            names = [single_name]
    return {"marks": [name_to_marks.get(name, None) for name in names]}
