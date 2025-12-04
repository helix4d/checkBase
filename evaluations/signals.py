from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import InstructorStats, Score


@receiver(post_save, sender=Score)
def update_stats_on_save(sender, instance: Score, **kwargs):
    InstructorStats.recompute_for(instance.instructor)


@receiver(post_delete, sender=Score)
def update_stats_on_delete(sender, instance: Score, **kwargs):
    InstructorStats.recompute_for(instance.instructor)
