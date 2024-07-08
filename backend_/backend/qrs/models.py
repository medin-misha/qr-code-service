import qrcode
from django.core.files.base import ContentFile
from django.db import models

from io import BytesIO


def save_basic_qr_code(instance: "BasicQRCode", filename: str) -> str:
    return f"qrs/basic/{filename}"


class BasicQRCode(models.Model):
    """
    Класс, который хранит в себе классические qr коды без всяких наворотов.
    """
    data = models.TextField(max_length=1000, null=False, blank=False)
    qr_code = models.ImageField(null=True, upload_to=save_basic_qr_code)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)