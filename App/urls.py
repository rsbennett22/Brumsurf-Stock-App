from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stockFormsPage/', views.stockForms, name='stockFormsPage'),
    path('wetsuitFormPage/', views.wetsuitForm, name='wetsuitFormPage'),
    path('deleteItem/<int:pk>', views.deleteItem, name='deleteItem'),
    path('signOut/<int:pk>', views.signOut, name='signOut'),
    path('signIn/<int:pk>', views.signIn, name='signIn'),
    path('onTrip/<int:pk>', views.onTrip, name='onTrip'),
    path('inventory/', views.inventory, name='inventory'),
    path('surfboardFormPage/', views.surfboardForm, name='surfboardFormPage'),
    path('addNewItem/', views.addNewItem, name='addNewItem'),
    path('detail/<str:stockType>&<int:number>', views.itemDetail, name='wetsuit'),
]