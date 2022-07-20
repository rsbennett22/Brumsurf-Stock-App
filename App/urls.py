from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wetsuit/<str:brand>&<str:gender>&<str:size>&<int:number>', views.wetsuit, name='wetsuit'),
    path('qrFormsPage/', views.qrForms, name='qrFormsPage'),
    path('wetsuitFormPage/', views.wetsuitForm, name='wetsuitFormPage'),
    path('addNewWetsuit/', views.addNewWetsuit, name='addNewWetsuit'),
    path('deleteItem/', views.deleteItem, name='deleteItem'),
]