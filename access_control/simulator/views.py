from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Room, Employee

# Store employee last access history in memory
history = {}

from datetime import datetime, date

def check_access(emp):
    rules = {
        "serverroom": {"level": 2, "open": "09:00", "close": "11:00", "cooldown": 15},
        "vault": {"level": 3, "open": "09:00", "close": "10:00", "cooldown": 30},
        "r&d lab": {"level": 1, "open": "08:00", "close": "12:00", "cooldown": 10},
    }

    room_key = emp.room.name.strip().lower()
    rule = rules.get(room_key)
    if not rule:
        return "Denied", f"Invalid room ({emp.room.name})"

    # 1. Check access level
    if emp.access_level < rule["level"]:
        return "Denied", f"Requires level {rule['level']}"

    # Convert to datetime for comparison
    request_time = datetime.combine(date.today(), emp.request_time)
    open_time = datetime.combine(date.today(), datetime.strptime(rule["open"], "%H:%M").time())
    close_time = datetime.combine(date.today(), datetime.strptime(rule["close"], "%H:%M").time())

    # 2. Check room open/close time
    if not (open_time <= request_time <= close_time):
        return "Denied", "Room closed at this time"

    # 3. Check cooldown
    key = (emp.emp_id, room_key)
    if key in history:
        last_access = history[key]
        diff = (request_time - last_access).total_seconds() / 60
        if diff < rule["cooldown"]:
            return "Denied", f"Cooldown not complete ({rule['cooldown']} min)"

    # If granted, update history
    history[key] = request_time
    return "Granted", f"Access granted to {emp.room.name}"





def index(request):
    employees = Employee.objects.all()
    results = []

    for emp in employees:
        status, reason = check_access(emp)
        results.append({
            "id": emp.emp_id,
            "access_level": emp.access_level,
            "request_time": emp.request_time.strftime("%H:%M"),
            "room": emp.room,
            "status": status,
            "reason": reason,
        })

    # 👇 render index.html
    return render(request, "simulator/index.html", {"results": results})

