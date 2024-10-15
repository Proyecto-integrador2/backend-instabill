import os
from django.db import models

# Create your models here.


def custom_upload_to(instance, filename):
    # Extract the file extension
    extension = os.path.splitext(filename)[1]

    # Generate a new filename using the instance's ID (after it's been saved)
    new_filename = f"bill_{instance.id}{extension}"

    # You can store files in a subdirectory, e.g., "uploads/"
    return os.path.join("bills", new_filename)


class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to=custom_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill Date: {self.uploaded_at}"
