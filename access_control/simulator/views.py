from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Room, Employee

# Store employee last access history in memory
history = {}

def check_access(emp):
    rules = {
        "ServerRoom": 2,
        "Vault": 3,
        "R&D Lab": 1,
    }
    required_level = rules.get(emp.room, 0)
    if emp.access_level >= required_level:
        return "Granted", "Access granted"
    else:
        return "Denied", f"Requires level {required_level}"

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

