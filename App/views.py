from django.shortcuts import render
from django.http import HttpResponse
import qrcode

# Create your views here.
def index(request):
    return render(request, 'App/Index.html')

def wetsuit(request, brand, size, gender, number):
    fileName = brand+size+gender+number+'.png'
    return render(request, 'App/wetsuit.html', {'stockType' : 'Wetsuit', 'brand' : brand, 'size' : size, 'gender' : gender, 'number' : number, 'fileName' : fileName})

def qrForms(request):
    return render(request, 'App/qrForms.html')

def wetsuitForm(request):
    return render(request, 'App/generateWetsuitForm.html')

def generateWetsuitQR(request, brand, size, gender, number):
    #Generate qrcode from data
    qrData = 'http://192.168.0.58:8000/wetsuit/'+brand+'&'+size+'&'+gender+'&'+str(number)
    qr = qrcode.make(qrData)
    fileName = brand+size+gender+str(number)+'.png'
    qrImg = 'qrcodes\\'+brand+size+gender+str(number)+'.png'
    qr.save('static\\qrcodes\\'+fileName)
    return render(request, 'App/wetsuit.html', {'stockType' : 'wetsuit', 'size' : size, 'brand' : brand ,'number' : number, 'gender' : gender, 'qrImg' : qrImg})