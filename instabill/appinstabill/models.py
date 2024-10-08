from django.db import models

# Create your models here.


class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="bills/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill Date: {self.uploaded_at}"
