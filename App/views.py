from django.shortcuts import render, redirect
from django.http import HttpResponse
import qrcode
from os.path import exists
from os import remove
from .models import StockItem, Wetsuit
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]

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
    return render(request, 'App/index.html',print(bcolors.OKBLUE+'Successfully loaded home page!'+bcolors.ENDC))

def wetsuit(request, brand, gender, size, number):

    #REMOVED QR CHECK HERE

    qrPath = 'qrcodes\\'+brand+gender+str(size)+str(number)+'.png'
    #Get pk of this wetsuit
    print(bcolors.OKGREEN+"Trying to get wetsuit object..."+bcolors.ENDC)
    try:
        thisWetsuit = Wetsuit.objects.get(brand=brand, gender=gender, size=size, number=number)
        print(bcolors.OKBLUE+"Successfully retrieved wetsuit object!"+bcolors.ENDC)
    except:
        print(bcolors.FAIL+"Error! Wetsuit does not exist!"+bcolors.ENDC)
        return render(request, 'App/qrErrorPage.html')

    pk = thisWetsuit.pk
    signedOut=thisWetsuit.signedOut
    signedIn=thisWetsuit.signedIn
    onTrip=thisWetsuit.onTrip
    qrPath = 'qrCodes\\'+str(thisWetsuit.qrCode)
    print(bcolors.OKGREEN+"Loading info page"+bcolors.ENDC)
    deleteUrl='../deleteItem/'+str(pk)
    signOutUrl='../signOut/'+str(pk)
    signInUrl='../signIn/'+str(pk)
    onTripUrl='../onTrip/'+str(pk)
    return render(request, 'App/wetsuit.html', {
        'stockType' : 'wetsuit', 
        'brand' : brand, 
        'gender' : gender, 
        'size' : size, 
        'number' : number, 
        'signedIn': signedIn,
        'signedOut': signedOut,
        'onTrip': onTrip,
        'qrPath' : qrPath, 
        'pk' : pk, 
        'deleteUrl' : deleteUrl, 
        'signOutUrl': signOutUrl,
        'signInUrl': signInUrl,
        'onTripUrl': onTripUrl,
        }, print(bcolors.OKBLUE+"Successfully loaded wetsuit info page!"+bcolors.ENDC))

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
            

            #Implement feature that checks if wetsuit number already exists, if does, loop to find the next possible number
            print(bcolors.OKGREEN+"Checking if wetsuit number is unique..."+bcolors.ENDC)
            try:
                numWetsuit = Wetsuit.objects.get(number=newWetsuit.number)
                print(bcolors.WARNING+"A wetsuit with that number exists!"+bcolors.ENDC)
                #Get the next available wetsuit number
                newWetsuit.number = getNextWetsuitNum(1)
            except:
                print(bcolors.OKBLUE+"Wetsuit number is ok!"+bcolors.ENDC)
            fileName=newWetsuit.brand+newWetsuit.gender+str(newWetsuit.size)+str(newWetsuit.number)+'.png'
            print(bcolors.OKGREEN+"Checking if QR code matching "+fileName+" exists..."+bcolors.ENDC)
            #Check if QR code matching info exists
            if(checkForQR(fileName)):
                #Load wetsuit page wetsuit item's info
                print(bcolors.OKGREEN+"Loading wetsuit info page..."+bcolors.ENDC)
                return wetsuit(request, newWetsuit.brand, newWetsuit.gender, newWetsuit.size, newWetsuit.number)
            #Create QR code from data
            else:
                generateWetsuitQR(newWetsuit.brand, newWetsuit.gender, newWetsuit.size, newWetsuit.number, fileName)
                #Add qr code to model instance
                newWetsuit.qrCode=fileName
                #Add url to model instance
                newWetsuit.url='http://'+IP+':8000/wetsuit/'+newWetsuit.brand+'&'+newWetsuit.gender+'&'+str(newWetsuit.size)+'&'+str(newWetsuit.number)
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
    qrData = 'http://'+IP+':8000/wetsuit/'+brand+'&'+gender+'&'+str(size)+'&'+str(number)
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
        print(bcolors.OKBLUE+"QR code already exists!"+bcolors.ENDC)
        return True
    else:
        print(bcolors.WARNING+"QR code does not exist!"+bcolors.ENDC)
        return False

def deleteQRCode(fileName):
    path='static\\qrcodes\\'+fileName
    print(bcolors.OKGREEN+"Checking if file to be deleted exists..."+bcolors.ENDC)
    if(exists(path)):
        #Delete file
        print(bcolors.OKBLUE+"File exists!"+bcolors.ENDC)
        print(bcolors.WARNING+"Deleting file..."+bcolors.ENDC)
        remove(path)
        return print(bcolors.OKBLUE+"File deleted successfully!"+bcolors.ENDC)
    else:
        return print(bcolors.FAIL+"Error! File does not exist!"+bcolors.ENDC)

def deleteItem(request, pk):
    itemToDelete = StockItem.objects.get(pk=pk)
    if(request.method=='POST'):
        print(bcolors.OKGREEN+"Getting item info..."+bcolors.ENDC)
        stockType = itemToDelete.stockType
        brand = itemToDelete.brand
        size = itemToDelete.size
        number = itemToDelete.number
        print(bcolors.OKBLUE+"Obtained item info: "+stockType, brand, str(size), str(number)+bcolors.ENDC)
        if(stockType=='wetsuit'):
            print(bcolors.WARNING+'Deleting QR code...'+bcolors.ENDC)
            gender = Wetsuit.objects.get(pk=pk).gender
            #Delete associated QR code
            fileName=brand+gender+str(size)+str(number)+'.png'
            deleteQRCode(fileName)
        else:
            print(bcolors.WARNING+'Deleting QR code...'+bcolors.ENDC)
            fileName=brand+str(size)+str(number)+'.png'
            deleteQRCode(fileName)

        #Delete item from db
        print(bcolors.WARNING+"Deleting item from database..."+bcolors.ENDC)
        itemToDelete.delete()
        print(bcolors.OKBLUE+"Successfully deleted item from database!"+bcolors.ENDC)
        return redirect('/')

def signOut(request, pk):
    print(bcolors.OKGREEN+"Attempting to sign out item..."+bcolors.ENDC)
    itemToSignOut = StockItem.objects.get(pk=pk)
    prevUrl = itemToSignOut.url
    if(request.method=='POST'):
        print(bcolors.OKGREEN+"Checking if item already signed out..."+bcolors.ENDC)
        signedOutStatus = itemToSignOut.signedOut
        if(signedOutStatus):
            print(bcolors.FAIL+"Item already signed out!"+bcolors.ENDC)
            return redirect(prevUrl)
        else:
            itemToSignOut.signedOut=True
            itemToSignOut.signedIn=False
            itemToSignOut.onTrip=False
            print(bcolors.OKGREEN+"Checking for student name and id..."+bcolors.ENDC)
            studentName = request.POST.get('studentName')
            studentId = request.POST.get('studentId')
            #Check if either are null
            if(studentName!='' and studentId!=''):
                print(bcolors.OKBLUE+"Retrieved a name and id!"+bcolors.ENDC)
                itemToSignOut.name = studentName
                itemToSignOut.studentId = studentId
                print(bcolors.OKGREEN+"Attempting to sign out item..."+bcolors.ENDC)
                itemToSignOut.save()
                print(bcolors.OKBLUE+"Item successfully signed out!"+bcolors.ENDC)
                return redirect(prevUrl)
            else:
                print(bcolors.OKBLUE+"Name and id not found"+bcolors.ENDC)
                print(bcolors.OKGREEN+"Attempting to sign out item..."+bcolors.ENDC)
                itemToSignOut.save()
                print(bcolors.OKBLUE+"Item successfully signed out!"+bcolors.ENDC)
                return redirect(prevUrl)

def signIn(request, pk):
    print(bcolors.OKGREEN+"Attempting to sign in item..."+bcolors.ENDC)
    itemToSignIn = StockItem.objects.get(pk=pk)
    prevUrl = itemToSignIn.url
    if(request.method=='POST'):
        print(bcolors.OKGREEN+"Checking if item already signed in..."+bcolors.ENDC)
        signedInStatus = itemToSignIn.signedIn
        if(signedInStatus):
            print(bcolors.FAIL+"Item already signed in!"+bcolors.ENDC)
            return redirect(prevUrl)
        else:
            itemToSignIn.signedOut=False
            itemToSignIn.onTrip=False
            itemToSignIn.signedIn=True
            itemToSignIn.name = 'brumsurf'
            itemToSignIn.studentId = '0000000'
            itemToSignIn.save()
            print(bcolors.OKBLUE+"Item successfully signed in!"+bcolors.ENDC)
            return redirect(prevUrl)

def onTrip(request, pk):
    print(bcolors.OKGREEN+"Attempting to trip sign out item..."+bcolors.ENDC)
    itemToTrip = StockItem.objects.get(pk=pk)
    prevUrl = itemToTrip.url
    if(request.method=='POST'):
        print(bcolors.OKGREEN+"Checking if item already signed in..."+bcolors.ENDC)
        tripStatus = itemToTrip.onTrip
        if(tripStatus):
            print(bcolors.FAIL+"Item already signed in!"+bcolors.ENDC)
            return redirect(prevUrl)
        else:
            itemToTrip.signedOut=False
            itemToTrip.onTrip=True
            itemToTrip.signedIn=False
            itemToTrip.save()
            print(bcolors.OKBLUE+"Item successfully signed out on trip!"+bcolors.ENDC)
            return redirect(prevUrl)

def inventory(request):
    print(bcolors.OKBLUE+"Successfully loaded inventory page!"+bcolors.ENDC)
    #This page displays a list of all stock items in a table like format
    #User can click on an item and see it's detail page
    wetsuits = Wetsuit.objects.all().order_by('number')
    #surfboards = StockItem.objects.get(stockType='surfboard')
    return render(request, 'App/inventory.html', {'wetsuits' : wetsuits})

def getNextWetsuitNum(number):
    try:
        #If no exception, recursive call number+1
        availableNum = Wetsuit.objects.get(number=number)
        num = number + 1
        return getNextWetsuitNum(num)
    except:
        print(bcolors.FAIL+"NUMBER: "+str(number)+bcolors.ENDC)
        return number
