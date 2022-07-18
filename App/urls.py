from django.urls import path
from . import views

urlpatterns = [
    #path('stockData/<str:stockType>&<int:total>', views.qrview, name='stockData'),
    path('wetsuit/<str:brand>&<str:size>', views.wetsuit, name='wetsuit'),
    path('createWetsuitQR/<str:brand>&<str:size>', views.createWetsuitQR, name='createWetsuitQR'),
]