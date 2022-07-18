from django.urls import path
from . import views

urlpatterns = [
    #path('stockData/<str:stockType>&<int:total>', views.qrview, name='stockData'),
    path('wetsuit/<str:size>&<str:brand>', views.addWetsuit, name='addWetsuit')
]