from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import qrcode
from os.path import exists
from os import remove
from .models import StockItem, Wetsuit

def index(request):
    return render(request, 'App/Index.html')

def wetsuit(request, brand, gender, size, number):
    fileName = brand+gender+str(size)+str(number)+'.png'
    print("Checking for QR code...")
    if(checkForQR(fileName)):
        #If QR code in image folder, load info page
        print("QR code found. Loading info page")
        qrPath = 'qrcodes\\'+brand+gender+str(size)+str(number)+'.png'
        #Get pk of this wetsuit
        thisWetsuit = Wetsuit.objects.get(brand=brand, gender=gender, size=size, number=number)
        pk = thisWetsuit.pk
        return render(request, 'App/wetsuit.html', {'stockType' : 'wetsuit', 'brand' : brand, 'gender' : gender, 'size' : size, 'number' : number, 'qrPath' : qrPath, 'pk' : pk})
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
            newWetsuit.stockType='wetsuit'
            newWetsuit.brand=request.POST.get('brand')
            newWetsuit.gender=request.POST.get('gender')
            newWetsuit.size=request.POST.get('size')
            newWetsuit.number=request.POST.get('num')
            fileName=newWetsuit.brand+newWetsuit.gender+newWetsuit.size+newWetsuit.number+'.png'
            print(newWetsuit.brand)
            print(newWetsuit.gender)
            print(newWetsuit.size)
            print(newWetsuit.number)
            #Check if QR code matching info exists
            if(checkForQR(fileName)):
                #Load wetsuit page wetsuit item's info
                return wetsuit(request, newWetsuit.brand, newWetsuit.gender, newWetsuit.size, newWetsuit.number)
            #Create QR code from data
            else:
                generateWetsuitQR(newWetsuit.brand, newWetsuit.gender, newWetsuit.size, newWetsuit.number, fileName)
                #Add qr code to model instance
                newWetsuit.qrCode=fileName
                newWetsuit.save()
                #Redirect to wetsuit info page
                return wetsuit(request, newWetsuit.brand, newWetsuit.gender, newWetsuit.size, newWetsuit.number)
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

def deleteQRCode(fileName):
    path='static\\qrcodes\\'+fileName
    if(exists(path)):
        #Delete file
        remove(path)
        return print("File deleted successfully!")
    else:
        return print("Error! File does not exist!")

def deleteItem(request):
    pk = request.POST.get('pk')
    itemToDelete = StockItem(pk=pk)
    if(request.method=='POST'):
        print('Deleting item from database...')
        stockType = request.POST.get('stockType')
        brand = request.POST.get('brand')
        size = request.POST.get('size')
        number = request.POST.get('number')
        if(stockType=='wetsuit'):
            print('Deleting QR code...')
            gender = request.POST.get('gender')
            #Delete associated QR code
            fileName=brand+gender+size+number+'.png'
            deleteQRCode(fileName)
        else:
            fileName=brand+size+number+'.png'
            deleteQRCode(fileName)

        #Delete item from db
        itemToDelete.delete()
        return redirect('/')