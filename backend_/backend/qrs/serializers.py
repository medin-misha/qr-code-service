from .models import BasicQRCode
from rest_framework import serializers


class BasicQRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicQRCode
        fields = ["data", "qr_code"]
