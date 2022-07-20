from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wetsuit/<str:brand>&<str:size>&<str:gender>&<int:number>', views.wetsuit, name='wetsuit'),
    path('qrFormsPage/', views.qrForms, name="qrForms"),
    path('wetsuitFormPage/', views.wetsuitForm, name="wetsuitForm"),
    path('generateWetsuitQR/<str:brand>&<str:size>&<str:gender>&<int:number>', views.generateWetsuitQR, name='generateWetsuit'),
]