from django.db.models import ProtectedError
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Customer

@receiver(pre_delete, sender=Customer, dispatch_uid='post_pre_delete_signal')
def protect_default(sender, instance, using, **kwargs):
    if instance.id == 1:
        raise ProtectedError('Defalut Customer cannot be deleted!!')