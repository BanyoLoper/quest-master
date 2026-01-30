from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User

from .models import Quest, PlayerProfile
from .serializers import QuestSerializer, UserRegisterSerializer


class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.filter(is_active=True)
    serializer_class = QuestSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def complete_quest(self, request, pk=None):
        quest = self.get_object()
        player_profile: PlayerProfile = request.user.playerprofile

        if quest in player_profile.completed_quests.all():
            return Response({"error": "Mission already completed"}, status=status.HTTP_400_BAD_REQUEST)

        # Reward Logic
        player_profile.completed_quests.add(quest)
        player_profile.xp += quest.points_reward
        player_profile.save()

        return Response({"status": "Mission Completed!", "new_xp": player_profile.xp})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer