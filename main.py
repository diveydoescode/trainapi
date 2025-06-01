from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import json
import re

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = Query(...)) -> Dict[str, str]:
    # Ticket status
    match = re.match(r".*ticket\s+(\d+).*", q, re.IGNORECASE)
    if match:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({"ticket_id": int(match.group(1))})
        }

    # Schedule meeting
    match = re.match(r".*meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)\.", q, re.IGNORECASE)
    if match:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": match.group(1),
                "time": match.group(2),
                "meeting_room": match.group(3).strip()
            })
        }

    # Expense balance
    match = re.match(r".*expense balance.*employee (\d+)", q, re.IGNORECASE)
    if match:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({"employee_id": int(match.group(1))})
        }

    # Performance bonus
    match = re.match(r".*performance bonus.*employee (\d+).*?(\d{4})", q, re.IGNORECASE)
    if match:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(match.group(1)),
                "current_year": int(match.group(2))
            })
        }

    # Report office issue
    match = re.match(r".*office issue (\d+) for the ([\w\s]+) department", q, re.IGNORECASE)
    if match:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(match.group(1)),
                "department": match.group(2).strip()
            })
        }

    # No match
    return {"error": "Could not determine intent from query."}
