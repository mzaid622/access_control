from django.core.management.base import BaseCommand
from simulator.models import Room

class Command(BaseCommand):
    help = "Load default rooms with rules"

    def handle(self, *args, **kwargs):
        rooms = [
            {"name": "ServerRoom", "min_access_level": 2, "open_time": "09:00", "close_time": "11:00", "cooldown": 15},
            {"name": "Vault", "min_access_level": 3, "open_time": "09:00", "close_time": "10:00", "cooldown": 30},
            {"name": "R&D Lab", "min_access_level": 1, "open_time": "08:00", "close_time": "12:00", "cooldown": 10},
        ]
        for r in rooms:
            Room.objects.update_or_create(
                name=r["name"],
                defaults={
                    "min_access_level": r["min_access_level"],
                    "open_time": r["open_time"],
                    "close_time": r["close_time"],
                    "cooldown": r["cooldown"],
                }
            )
        self.stdout.write(self.style.SUCCESS("✅ Rooms loaded successfully"))
