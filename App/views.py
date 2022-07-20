from django.shortcuts import render
from django.http import HttpResponse
import qrcode
from os.path import exists
from .models import StockItem, Wetsuit

# Create your views here.
def index(request):
    return render(request, 'App/Index.html')

def wetsuit(request, brand, gender, size, number):
    fileName = brand+gender+str(size)+str(number)+'.png'
    print("Checking for QR code...")
    if(checkForQR(fileName)):
        #If QR code in image folder, load info page
        print("QR code found. Loading info page")
        qrPath = 'qrcodes\\'+brand+gender+str(size)+str(number)+'.png'
        return render(request, 'App/wetsuit.html', {'stockType' : 'Wetsuit', 'brand' : brand, 'gender' : gender, 'size' : size, 'number' : number, 'fileName' : fileName, 'qrPath' : qrPath})
    else:
        #If QR code not in image folder, load error page
        print("QR code not found!")
        return render(request, 'App/qrErrorPage.html')

def qrForms(request):
    return render(request, 'App/qrForms.html')

def wetsuitForm(request):
    return render(request, 'App/generateWetsuitForm.html')

def addNewWetsuit(request):
    if(request.method=='POST'):
        if(request.POST.get('brand')):
            newWetsuit=Wetsuit()
            newWetsuit.stockType='Wetsuit'
            newWetsuit.brand=request.POST.get('brand')
            newWetsuit.gender=request.POST.get('gender')
            newWetsuit.wetsuitSize=request.POST.get('size')
            newWetsuit.number=request.POST.get('num')

            fileName=newWetsuit.brand+newWetsuit.gender+newWetsuit.wetsuitSize+newWetsuit.number+'.png'
            print(newWetsuit.brand)
            print(newWetsuit.gender)
            print(newWetsuit.wetsuitSize)
            print(newWetsuit.number)
            #check if QR code matching info exists
            if(checkForQR(fileName)):
                #load wetsuit page wetsuit item's info
                return wetsuit(request, newWetsuit.brand, newWetsuit.gender, newWetsuit.wetsuitSize, newWetsuit.number)
            #create QR code from data
            else:
                generateWetsuitQR(newWetsuit.brand, newWetsuit.gender, newWetsuit.wetsuitSize, newWetsuit.number, fileName)
                newWetsuit.save()
                #redirect to wetsuit info page
                return wetsuit(request, newWetsuit.brand, newWetsuit.gender, newWetsuit.wetsuitSize, newWetsuit.number)
        else:
            return HttpResponse('Bad request...')

def generateWetsuitQR(brand, gender, size, number, fileName):
    print("Generating a new wetsuit QR code...")
    #Generate qrcode from data
    qrData = 'http://192.168.0.58:8000/wetsuit/'+brand+'&'+gender+'&'+str(size)+'&'+str(number)
    qr = qrcode.make(qrData)
    qr.save('static\\qrcodes\\'+fileName)
    print("QR code generated. Redirecting to wetsuit page...")

def checkForQR(fileName):
    path = 'static\\qrcodes\\'+fileName
    print(path)
    if(exists(path)):
        return True
    else:
        return False
