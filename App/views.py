from base64 import b32hexdecode
from email.quoprimime import body_check
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import qrcode
from os.path import exists
from os import remove
from .models import StockItem, Wetsuit

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def index(request):
    return render(request, 'App/Index.html',print(bcolors.OKBLUE+'Successfully loaded home page!'+bcolors.ENDC))

def wetsuit(request, brand, gender, size, number):

    #REMOVED QR CHECK HERE

    qrPath = 'qrcodes\\'+brand+gender+str(size)+str(number)+'.png'
    #Get pk of this wetsuit
    print(bcolors.OKGREEN+"Getting pk of this wetsuit object..."+bcolors.ENDC)
    thisWetsuit = Wetsuit.objects.get(brand=brand, gender=gender, size=size, number=number)
    pk = thisWetsuit.pk
    if(pk!=None):
        print(bcolors.OKBLUE+"PK succesfully obtained!"+bcolors.ENDC)
        print(bcolors.OKGREEN+"Loading info page"+bcolors.ENDC)
        return render(request, 'App/wetsuit.html', {'stockType' : 'wetsuit', 'brand' : brand, 'gender' : gender, 'size' : size, 'number' : number, 'qrPath' : qrPath, 'pk' : pk}, print(bcolors.OKBLUE+"Successfully loaded wetsuit info page!"+bcolors.ENDC))
    else:
        print(bcolors.FAIL+"Error, PK is None!")
        return render(request, 'App/pkErrorPage.html', print(bcolors.WARNING+'Successfully loaded pk error page'+bcolors.ENDC))

def stockForms(request):
    print(bcolors.OKBLUE+"Successfully loaded stock form selection page!"+bcolors.ENDC)
    return render(request, 'App/stockForms.html')

def wetsuitForm(request):
    return render(request, 'App/generateWetsuitForm.html', print(bcolors.OKBLUE+"Successfully loaded wetsuit form page!"+bcolors.ENDC))

def addNewWetsuit(request):
    if(request.method=='POST'):
        if(request.POST.get('brand')):
            newWetsuit=Wetsuit()
            newWetsuit.stockType='wetsuit'

            print(bcolors.OKGREEN+"Getting wetsuit brand..."+bcolors.ENDC)
            newWetsuit.brand=request.POST.get('brand')
            if(newWetsuit.brand!=None):
                print(bcolors.OKBLUE+"Successfully obtained wetsuit brand: "+bcolors.ENDC+newWetsuit.brand)
            else:
                return print(bcolors.FAIL+"Error, brand is None!"+bcolors.ENDC)
            
            print(bcolors.OKGREEN+"Getting wetsuit gender..."+bcolors.ENDC)
            newWetsuit.gender=request.POST.get('gender')
            if(newWetsuit.gender!=None):
                print(bcolors.OKBLUE+"Successfully obtained wetsuit gender: "+bcolors.ENDC+newWetsuit.gender)
            else:
                return print(bcolors.FAIL+"Error, gender is None!"+bcolors.ENDC)
            
            print(bcolors.OKGREEN+"Getting wetsuit size..."+bcolors.ENDC)
            newWetsuit.size=request.POST.get('size')
            if(newWetsuit.size!=None):
                print(bcolors.OKBLUE+"Successfully obtained wetsuit size: "+bcolors.ENDC+newWetsuit.size)
            else:
                return print(bcolors.FAIL+"Error, size is None!"+bcolors.ENDC)
            
            print(bcolors.OKGREEN+"Getting wetsuit number..."+bcolors.ENDC)
            newWetsuit.number=request.POST.get('num')
            if(newWetsuit.number!=None):
                print(bcolors.OKBLUE+"Successfully obtained wetsuit number: "+bcolors.ENDC+newWetsuit.number)
            else:
                return print(bcolors.FAIL+"Error, number is None!"+bcolors.ENDC)
            
            fileName=newWetsuit.brand+newWetsuit.gender+newWetsuit.size+newWetsuit.number+'.png'
            print(bcolors.OKGREEN+"Checking if QR code matching "+fileName+" exists..."+bcolors.ENDC)
            #Check if QR code matching info exists
            if(checkForQR(fileName)):
                #Load wetsuit page wetsuit item's info
                print(bcolors.OKBLUE+"QR code already exists!"+bcolors.ENDC)
                print(bcolors.OKGREEN+"Loading wetsuit info page..."+bcolors.ENDC)
                return wetsuit(request, newWetsuit.brand, newWetsuit.gender, newWetsuit.size, newWetsuit.number)
            #Create QR code from data
            else:
                print(bcolors.WARNING+"QR code does not exist!"+bcolors.ENDC)
                generateWetsuitQR(newWetsuit.brand, newWetsuit.gender, newWetsuit.size, newWetsuit.number, fileName)
                #Add qr code to model instance
                newWetsuit.qrCode=fileName
                print(bcolors.OKGREEN+"Adding new wetsuit to database..."+bcolors.ENDC)
                newWetsuit.save()
                print(bcolors.OKBLUE+"Successfully added new wetsuit to database!"+bcolors.ENDC)
                #Redirect to wetsuit info page
                print(bcolors.OKGREEN+"Loading wetsuit info page..."+bcolors.ENDC)
                return wetsuit(request, newWetsuit.brand, newWetsuit.gender, newWetsuit.size, newWetsuit.number)
        else:
            return HttpResponse('Bad request...')

def generateWetsuitQR(brand, gender, size, number, fileName):
    print(bcolors.OKGREEN+"Generating a new wetsuit QR code..."+bcolors.ENDC)
    #Generate qrcode from data
    qrData = 'http://192.168.0.58:8000/wetsuit/'+brand+'&'+gender+'&'+str(size)+'&'+str(number)
    qr = qrcode.make(qrData)
    print(bcolors.OKGREEN+"Saving generated QR code..."+bcolors.ENDC)
    path = 'static\\qrcodes\\'+fileName
    qr.save(path)
    if(exists(path)):
        return print(bcolors.OKBLUE+"Successfully generated and saved QR code!"+bcolors.ENDC)
    else:
        return print(bcolors.FAIL+"QR code failed to save!"+bcolors.ENDC)

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