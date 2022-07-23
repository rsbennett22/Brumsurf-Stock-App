from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inventory/', views.inventory, name='inventory'),
    path('stockFormsPage/', views.stockForms, name='stockFormsPage'),
    path('wetsuitFormPage/', views.wetsuitForm, name='wetsuitFormPage'),
    path('surfboardFormPage/', views.surfboardForm, name='surfboardFormPage'),
    path('surfskateFormPage/', views.surfskateForm, name='surfskateFormPage'),
    path('bootFormPage/', views.bootForm, name='bootFormPage'),
    path('gloveFormPage/', views.gloveForm, name='gloveFormPage'),
    path('hoodFormPage/', views.hoodForm, name='hoodFormPage'),
    path('addNewItem/', views.addNewItem, name='addNewItem'),
    path('detail/<str:stockType>&<int:number>', views.itemDetail, name='detail'),
    path('detail/<int:pk>', views.accessoryDetail, name='accessoryDetail'),
    path('deleteItem/<int:pk>', views.deleteItem, name='deleteItem'),
    path('updateItem/<int:pk>&<int:amount>', views.updateItem, name='updateItem'),
    path('signOut/<int:pk>', views.signOut, name='signOut'),
    path('signIn/<int:pk>', views.signIn, name='signIn'),
    path('onTrip/<int:pk>', views.onTrip, name='onTrip'),
]