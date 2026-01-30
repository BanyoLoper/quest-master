from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Quest, PlayerProfile


class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ["id", "title", "description", "points_reward", "is_active"]


class PlayerProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = PlayerProfile
        fields = ["username", "xp", "completed_quests"]
