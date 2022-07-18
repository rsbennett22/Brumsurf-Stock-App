from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def addWetsuit(request, size, brand):
    return render(request, 'App/result.html', {'stockType' : 'wetsuit', 'size' : size, 'brand' : brand})