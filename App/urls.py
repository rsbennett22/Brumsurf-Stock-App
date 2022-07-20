from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wetsuit/<str:brand>&<str:gender>&<str:size>&<int:number>', views.wetsuit, name='wetsuit'),
    path('stockFormsPage/', views.stockForms, name='stockFormsPage'),
    path('wetsuitFormPage/', views.wetsuitForm, name='wetsuitFormPage'),
    path('addNewWetsuit/', views.addNewWetsuit, name='addNewWetsuit'),
    path('deleteItem/', views.deleteItem, name='deleteItem'),
]