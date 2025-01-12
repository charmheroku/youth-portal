from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ReadingSprint, SprintProgress


@receiver(post_save, sender=ReadingSprint)
def create_sprint_progress(sender, instance, created, **kwargs):
    """
    Automatically creates SprintProgress for all group participants
    when a new sprint is created.
    """
    if created:
        participants = instance.group.participants.all()
        SprintProgress.objects.bulk_create(
            [
                SprintProgress(user=participant, sprint=instance)
                for participant in participants
            ]
        )
