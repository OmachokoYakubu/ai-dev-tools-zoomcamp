from django.db import models
from django.utils import timezone

class Housemate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Chore(models.Model):
    class Recurrence(models.TextChoices):
        DAILY = 'DAILY', 'Daily'
        WEEKLY = 'WEEKLY', 'Weekly'
        MONTHLY = 'MONTHLY', 'Monthly'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        DONE = 'DONE', 'Completed'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    recurrence = models.CharField(
        max_length=20,
        choices=Recurrence.choices,
        default=Recurrence.WEEKLY
    )
    assigned_to = models.ForeignKey(
        Housemate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chores'
    )
    due_date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

class ChoreLog(models.Model):
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE, related_name='logs')
    completed_by = models.ForeignKey(Housemate, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.chore.title} completed by {self.completed_by.name} at {self.completed_at}"
