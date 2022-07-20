from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import qrcode
from os.path import exists

# Create your views here.
def index(request):
    return render(request, 'App/Index.html')

def wetsuit(request, brand, size, gender, number):
    fileName = brand+str(size)+gender+str(number)+'.png'
    print("Checking for QR code...")
    if(checkForQR(fileName)):
        #If QR code in image folder, load info page
        print("QR code found. Loading info page")
        qrPath = 'qrcodes\\'+brand+str(size)+gender+str(number)+'.png'
        return render(request, 'App/wetsuit.html', {'stockType' : 'Wetsuit', 'brand' : brand, 'size' : size, 'gender' : gender, 'number' : number, 'fileName' : fileName, 'qrPath' : qrPath})
    else:
        #If QR code not in image folder, load error page
        print("QR code not found!")
        return render(request, 'App/qrErrorPage.html')

def qrForms(request):
    return render(request, 'App/qrForms.html')

def wetsuitForm(request):
    return render(request, 'App/generateWetsuitForm.html')

def generateWetsuitQR(request, brand, size, gender, number):
    fileName = brand+str(size)+gender+str(number)+'.png'
    qrPath = 'qrcodes\\'+brand+size+gender+str(number)+'.png'
    print("Checking if QR code has already been generated...")
    if(checkForQR(fileName)):
        print("Matching QR code found. Redirecting to wetsuit info page...")
        return render(request, 'App/redirectToWetsuitPage.html', {'stockType' : 'wetsuit', 'size' : size, 'brand' : brand ,'number' : number, 'gender' : gender, 'qrPath' : qrPath, 'fileName' : fileName})
    else:
        print("QR code not found")
        print("Generating QR code...")
        #Generate qrcode from data
        qrData = 'http://192.168.0.58:8000/wetsuit/'+brand+'&'+str(size)+'&'+gender+'&'+str(number)
        qr = qrcode.make(qrData)
        qr.save('static\\qrcodes\\'+fileName)
        print("QR code generated. Redirecting to wetsuit info page...")
        return render(request, 'App/redirectToWetsuitPage.html', {'stockType' : 'wetsuit', 'size' : size, 'brand' : brand ,'number' : number, 'gender' : gender, 'qrPath' : qrPath, 'fileName' : fileName})

def checkForQR(fileName):
    path = 'static\\qrcodes\\'+fileName
    print(path)
    if(exists(path)):
        return True
    else:
        return False