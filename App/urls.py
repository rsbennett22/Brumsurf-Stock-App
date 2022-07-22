from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wetsuit/<str:brand>&<str:gender>&<str:size>&<int:number>', views.wetsuit, name='wetsuit'),
    path('stockFormsPage/', views.stockForms, name='stockFormsPage'),
    path('wetsuitFormPage/', views.wetsuitForm, name='wetsuitFormPage'),
    path('addNewWetsuit/', views.addNewWetsuit, name='addNewWetsuit'),
    path('deleteItem/<int:pk>', views.deleteItem, name='deleteItem'),
    path('signOut/<int:pk>', views.signOut, name='signOut'),
    path('signIn/<int:pk>', views.signIn, name='signIn'),
    path('onTrip/<int:pk>', views.onTrip, name='onTrip'),
]