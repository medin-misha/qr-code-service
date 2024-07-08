import os

from celery import shared_task
from django.core.files.base import ContentFile
import qrcode
from django.conf import settings
from io import BytesIO
import shutil
from .models import BasicQRCode


@shared_task
def create_basic_qr_code(model_pk: int):
    """функция получает model и создаёт для модели qr code который связывает с этой моделью
    """
    model: BasicQRCode = BasicQRCode.objects.get(pk=model_pk)
    # Генерация QR-кода
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(model.data)
    qr.make(fit=True)

    # Создание изображения QR-кода
    img = qr.make_image(fill_color="black", back_color="white")

    # Сохранение изображения в поле qr_code
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    filename = f"qrcode.png"  # Можете изменить формат файла на свой выбор
    model.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
    model.save()
    return model_pk


