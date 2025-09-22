import json
from django.core.management.base import BaseCommand
from simulator.models import Employee, Room

class Command(BaseCommand):
    help = "Load employees from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Path to JSON file")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file"]
        with open(file_path, "r") as f:
            data = json.load(f)

        for emp in data:
            try:
                room = Room.objects.get(name=emp["room"])
                Employee.objects.create(
                    emp_id=emp["id"],
                    access_level=emp["access_level"],
                    request_time=emp["request_time"],
                    room=room,
                )
                self.stdout.write(self.style.SUCCESS(f"Added {emp['id']}"))
            except Room.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Room not found: {emp['room']}"))
