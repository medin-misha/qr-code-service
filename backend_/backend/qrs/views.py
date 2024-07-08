from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from celery.result import AsyncResult

from .models import BasicQRCode
from .serializers import BasicQRCodeSerializer
from .tasks import create_basic_qr_code
class MakeQRAPIView(APIView):
    def get(self, request: Request) -> Response:
        serializer = BasicQRCodeSerializer(BasicQRCode.objects.all(), many=True)
        return Response(serializer.data)


    def post(self, request: Request) -> Response:
        data = request.data
        model: BasicQRCode = BasicQRCode.objects.create(data=data.get('data'))
        result: AsyncResult = create_basic_qr_code.s(model_pk=model.pk).apply_async()
        return Response({"key": result.id})

class GetQRCodeLinkAPIView(APIView):
    def get(self, request: Request, key: str) -> Response:
        task: AsyncResult = AsyncResult(key)
        if task.status == "SUCCESS":
            basic_qr_pk: int = task.result
            model: BasicQRCode = BasicQRCode.objects.get(pk=basic_qr_pk)
            serializer_data: dict = BasicQRCodeSerializer(model).data

            model.delete()
            return Response({"result": serializer_data})
        return Response({"status": task.status})