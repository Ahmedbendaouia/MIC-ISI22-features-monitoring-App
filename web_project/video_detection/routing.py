from django.urls import path

from .consumers import FlotationFrothParameters, ImageProccessStreaming

ws_urlpatterns = [
    path('ws/flotationFroth/', FlotationFrothParameters.as_asgi()),
    path('ws/image_proccces/', ImageProccessStreaming.as_asgi()),
]