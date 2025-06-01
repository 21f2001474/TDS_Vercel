from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import re
import json

app = FastAPI()

# Enable CORS for all origins (safe for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
async def execute(q: str):
    try:
        # Pattern 1: Ticket status
        match = re.match(r"What is the status of ticket (\\d+)?", q)
        if match:
            return {
                "name": "get_ticket_status",
                "arguments": json.dumps({"ticket_id": int(match.group(1))})
            }

        # Pattern 2: Schedule meeting
        match = re.match(r"Schedule a meeting on (\\d{4}-\\d{2}-\\d{2}) at (\\d{2}:\\d{2}) in (.+).", q)
        if match:
            date, time, room = match.groups()
            return {
                "name": "schedule_meeting",
                "arguments": json.dumps({"date": date, "time": time, "meeting_room": room})
            }

        # Pattern 3: Expense balance
        match = re.match(r"Show my expense balance for employee (\\d+).", q)
        if match:
            return {
                "name": "get_expense_balance",
                "arguments": json.dumps({"employee_id": int(match.group(1))})
            }

        # Pattern 4: Performance bonus
        match = re.match(r"Calculate performance bonus for employee (\\d+) for (\\d{4}).", q)
        if match:
            emp_id, year = match.groups()
            return {
                "name": "calculate_performance_bonus",
                "arguments": json.dumps({"employee_id": int(emp_id), "current_year": int(year)})
            }

        # Pattern 5: Office issue
        match = re.match(r"Report office issue (\\d+) for the (.+) department.", q)
        if match:
            return {
                "name": "report_office_issue",
                "arguments": json.dumps({"issue_code": int(match.group(1)), "department": match.group(2)})
            }

        return JSONResponse(status_code=400, content={"error": "Unrecognized query"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
