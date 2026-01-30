from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PlayerProfile, Achievement


@receiver(post_save, sender=PlayerProfile)
def check_achievements(sender, instance: PlayerProfile, created, **kwargs):
    if not created:
        if instance.xp >= 100:
            achievement, _ = Achievement.objects.get_or_create(
                name="Hunger for Quest",
                defaults={'descriptions': "You had reached 100 experience points!"}
            )

            if achievement not in instance.achievements.all():
                instance.achievements.add(achievement)
                print(f"¡ACHIEVEMENT UNLOCK FOR {instance.user.username}: {achievement.name}!")
