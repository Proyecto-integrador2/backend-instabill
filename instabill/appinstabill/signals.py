import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Bill


@receiver(post_delete, sender=Bill)
def delete_file_on_bill_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
