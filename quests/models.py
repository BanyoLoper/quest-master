from django.db import models
from django.contrib.auth.models import User

class Quest(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    points_reward = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="🏆")

    def __str__(self):
        return self.name

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    completed_quests = models.ManyToManyField(Quest, blank=True)
    achievements = models.ManyToManyField(Achievement, blank=True)
