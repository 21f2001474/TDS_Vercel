# /api/main.py
from flask import Flask, request, jsonify
import re
import json

app = Flask(__name__)

@app.route("/execute", methods=["GET"])
def execute():
    q = request.args.get("q", "")

    # Pattern 1: Ticket status
    if match := re.match(r"What is the status of ticket (\d+)\?", q):
        return jsonify({
            "name": "get_ticket_status",
            "arguments": json.dumps({"ticket_id": int(match.group(1))})
        })

    # Pattern 2: Schedule meeting
    if match := re.match(r"Schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)\.", q):
        date, time, room = match.groups()
        return jsonify({
            "name": "schedule_meeting",
            "arguments": json.dumps({"date": date, "time": time, "meeting_room": room})
        })

    # Pattern 3: Expense balance
    if match := re.match(r"Show my expense balance for employee (\d+)\.", q):
        return jsonify({
            "name": "get_expense_balance",
            "arguments": json.dumps({"employee_id": int(match.group(1))})
        })

    # Pattern 4: Performance bonus
    if match := re.match(r"Calculate performance bonus for employee (\d+) for (\d{4})\.", q):
        eid, year = match.groups()
        return jsonify({
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({"employee_id": int(eid), "current_year": int(year)})
        })

    # Pattern 5: Office issue
    if match := re.match(r"Report office issue (\d+) for the (.+) department\.", q):
        return jsonify({
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(match.group(1)),
                "department": match.group(2)
            })
        })

    return jsonify({"error": "Unrecognized query"}), 400
