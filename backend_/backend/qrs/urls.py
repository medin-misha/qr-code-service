from django.urls import path
from .views import MakeQRAPIView, GetQRCodeLinkAPIView

app_name = "qrs"
urlpatterns = [
    path("basic", MakeQRAPIView.as_view(), name="basic_qr"),
    path("get-result/<str:key>", GetQRCodeLinkAPIView.as_view(), name="get_link")
]
