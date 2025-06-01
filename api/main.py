from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
import re

app = FastAPI()

# Enable CORS for ngrok and frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["https://abc.ngrok-free.app"] for stricter control
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load JSON student data
json_path = os.path.join(os.path.dirname(__file__), "q-vercel-python.json")
with open(json_path) as f:
    student_data = json.load(f)

# Map name → marks
name_to_marks = {entry["name"]: entry["marks"] for entry in student_data}


@app.get("/api")
def get_marks_api(request: Request):
    names = request.query_params.getlist("name")
    if not names:
        single_name = request.query_params.get("name")
        if single_name:
            names = [single_name]
    return {"marks": [name_to_marks.get(name, None) for name in names]}


@app.get("/")
def get_marks_root(request: Request):
    names = request.query_params.getlist("name")
    if not names:
        single_name = request.query_params.get("name")
        if single_name:
            names = [single_name]
    return {"marks": [name_to_marks.get(name, None) for name in names]}


# 👉 TechNova Assistant Endpoint
@app.get("/execute")
async def execute(q: str):
    # Match patterns in order

    # 1. Ticket status
    if match := re.match(r"What is the status of ticket (\d+)\?", q):
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({"ticket_id": int(match.group(1))})
        }

    # 2. Schedule meeting
    if match := re.match(r"Schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)\.", q):
        date, time, room = match.groups()
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": date,
                "time": time,
                "meeting_room": room
            })
        }

    # 3. Expense balance
    if match := re.match(r"Show my expense balance for employee (\d+)\.", q):
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({"employee_id": int(match.group(1))})
        }

    # 4. Performance bonus
    if match := re.match(r"Calculate performance bonus for employee (\d+) for (\d{4})\.", q):
        emp_id, year = match.groups()
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(emp_id),
                "current_year": int(year)
            })
        }

    # 5. Office issue report
    if match := re.match(r"Report office issue (\d+) for the (.+) department\.", q):
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(match.group(1)),
                "department": match.group(2)
            })
        }

    return JSONResponse(status_code=400, content={"error": "Unrecognized query format"})
