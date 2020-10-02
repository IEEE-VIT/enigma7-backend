from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserStatus , User

@receiver(post_save , sender = User)
def create_userstatus(sender , instance , created , **kwargs):
    
    if created:
        UserStatus.objects.create(user = instance)

@receiver(post_save , sender = User)
def update_userstatus(sender , instance , created , **kwargs):
    
    if created == False:
        instance.user_status.save()