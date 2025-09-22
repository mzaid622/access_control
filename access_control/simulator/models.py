from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    min_access_level = models.IntegerField()
    open_time = models.TimeField()
    close_time = models.TimeField()
    cooldown = models.IntegerField()  # minutes

    def __str__(self):
        return self.name


class Employee(models.Model):
    emp_id = models.CharField(max_length=20)
    access_level = models.IntegerField()
    request_time = models.TimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.emp_id} ({self.room.name})"
