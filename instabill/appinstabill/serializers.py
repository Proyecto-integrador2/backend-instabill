from rest_framework.serializers import ModelSerializer
from .models import Bill


class BillSerializer(ModelSerializer):
    class Meta:
        model = Bill
        fields = ("id", "file", "uploaded_at")

    def create(self, validated_data):
        file = validated_data.pop("file", None)

        # Save the instance first to get an ID
        instance = Bill.objects.create(**validated_data)

        if file:
            # Now attach the file to the instance and save it again
            instance.file = file
            instance.save()

        return instance
