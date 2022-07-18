from django.shortcuts import render
from django.http import HttpResponse
import qrcode

# Create your views here.
def wetsuit(request, brand, size):
    return render(request, 'App/wetsuit.html', {'stockType' : 'wetsuit', 'size' : size, 'brand' : brand})

def createWetsuitQR(request, brand, size):
    #Generate qrcode from data
    qrData = 'http://192.168.0.58:8000/wetsuit/'+brand+'&'+size
    qr = qrcode.make(qrData)
    fileName = brand+size+'.png'
    qr.save('static\\qrcodes\\'+fileName)
    return render(request, 'App/generatedQR.html', {'stockType' : 'wetsuit', 'size' : size, 'brand' : brand})