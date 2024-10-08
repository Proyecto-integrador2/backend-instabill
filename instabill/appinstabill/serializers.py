from rest_framework.serializers import ModelSerializer
from .models import Bill


class BillSerializer(ModelSerializer):
    class Meta:
        model = Bill
        fields = ("id", "file", "uploaded_at")
