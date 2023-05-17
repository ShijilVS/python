from django.db import models
from django.contrib.auth.models import User

class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(blank=True, null=True)
    elapsed_time = models.DurationField(blank=True, null=True)

    def __str__(self):
        return f"Timer for {self.user.username} on {self.date}"

from django.db import models
from django.contrib.auth.models import User

class ElapsedTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    elapsed_time = models.DurationField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Elapsed Time for {self.user} on {self.date}"
