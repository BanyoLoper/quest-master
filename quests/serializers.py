from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Quest, PlayerProfile, Achievement


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'icon']


class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ['id', 'title', 'description', 'points_reward', 'is_active']


class PlayerProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    achievements = AchievementSerializer(many=True, read_only=True)

    class Meta:
        model = PlayerProfile
        fields = ['username', 'xp', 'completed_quests', 'achievements']
