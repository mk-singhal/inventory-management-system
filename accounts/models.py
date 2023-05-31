from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    STATUS_CHOICES = (
        ('owner', 'OWNER'),
        ('staff', 'STAFF'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='defaultUser.png', upload_to='profiles_pics')
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='staff')

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     # instance.profile.save()
#     instance.profile.save()