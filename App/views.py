from django.shortcuts import render, redirect
from django.http import HttpResponse
import qrcode
from os.path import exists
from os import remove
from .models import StockItem, Wetsuit, Surfboard
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

def stockForms(request):
    print(bcolors.OKBLUE+"Successfully loaded stock form selection page!"+bcolors.ENDC)
    return render(request, 'App/stockForms.html')

def wetsuitForm(request):
    stockType='Wetsuit'
    return render(request, 'App/generateItemForm.html', {'stockType': stockType},print(bcolors.OKBLUE+"Successfully loaded wetsuit form page!"+bcolors.ENDC))

def surfboardForm(request):
    stockType='Surfboard'
    return render(request, 'App/generateItemForm.html', {'stockType': stockType},print(bcolors.OKBLUE+"Successfully loaded surfboard form page!"+bcolors.ENDC))

def itemDetail(request, stockType, number):
    if(stockType=='wetsuit'):
        #Get wetsuit
        thisWetty = Wetsuit.objects.get(wetsuitNumber=number)
        #Send relevant info to html page
        brand = thisWetty.brand
        gender = thisWetty.gender
        size = thisWetty.size
        onTrip = thisWetty.onTrip
        signedOut = thisWetty.signedOut
        signedIn = thisWetty.signedIn
        qrCode = thisWetty.qrCode
        pk = thisWetty.pk
        deleteUrl = '../deleteItem/'+str(pk)
        signOutUrl='../signOut/'+str(pk)
        signInUrl='../signIn/'+str(pk)
        onTripUrl='../onTrip/'+str(pk)
        #Load detail page
        return render(request, 'App/itemDetail.html', {
            'stockType': stockType,
            'brand': brand,
            'gender': gender,
            'size': size,
            'number': number,
            'onTrip': onTrip,
            'signedOut': signedOut,
            'signedIn': signedIn,
            'qrCode': 'qrCodes\\'+str(qrCode),
            'pk': pk,
            'deleteUrl': deleteUrl,
            'signOutUrl': signOutUrl,
            'signInUrl': signInUrl,
            'onTripUrl': onTripUrl,
        }, print('Loaded item detail page!'))
    elif(stockType=='surfboard'):
        #Get surfboard
        thisBoard = Surfboard.objects.get(surfboardNumber=number)
        #Send relevant info to html page
        brand = thisBoard.brand
        size = thisBoard.size
        onTrip = thisBoard.onTrip
        signedOut = thisBoard.signedOut
        signedIn = thisBoard.signedIn
        qrCode = thisBoard.qrCode
        pk = thisBoard.pk
        deleteUrl = '../deleteItem/'+str(pk)
        signOutUrl='../signOut/'+str(pk)
        signInUrl='../signIn/'+str(pk)
        onTripUrl='../onTrip/'+str(pk)
        #Load detail page
        return render(request, 'App/itemDetail.html', {
            'stockType': stockType,
            'brand': brand,
            'size': size,
            'number': number,
            'onTrip': onTrip,
            'signedOut': signedOut,
            'signedIn': signedIn,
            'qrCode': 'qrCodes\\'+str(qrCode),
            'pk': pk,
            'deleteUrl': deleteUrl,
            'signOutUrl': signOutUrl,
            'signInUrl': signInUrl,
            'onTripUrl': onTripUrl,
        }, print('Loaded item detail page!'))

def addNewItem(request):
    if(request.method=='POST'):
        #Check stockType
        if(request.POST.get('stockType')=='Wetsuit'):
            print(bcolors.OKGREEN+"Attempting to add new wetsuit to db..."+bcolors.ENDC)
            stockType = 'wetsuit'
            gender = request.POST.get('gender')
            brand = request.POST.get('brand')
            size = request.POST.get('size')
            number = checkForMatchingNum(stockType, request.POST.get('num'))
            print(bcolors.OKBLUE+"Retrieved item info: "+stockType, brand, gender, str(size), str(number)+bcolors.ENDC)
            
            #Create a filename for the qr code using data from request
            fileName=stockType+brand+gender+str(size)+str(number)+'.png'
            #Check if qr code matchng filename exists
            if(checkForQR(fileName)):
                #Load surfboard info page
                return itemDetail(request, stockType, number)
            else:
                #Generate QR code for item
                generateQRCode(stockType, brand, gender, size, number, fileName)
                #Create a new item object and add it to db
                newWetsuit = Wetsuit()
                newWetsuit.stockType=stockType
                newWetsuit.brand=brand
                newWetsuit.gender=gender
                newWetsuit.size=size
                newWetsuit.wetsuitNumber=number
                newWetsuit.qrCode=fileName
                newWetsuit.url='http://'+IP+':8000/detail/'+stockType+'&'+str(number)
                newWetsuit.save()
                return itemDetail(request, stockType, number)

        elif(request.POST.get('stockType')=='Surfboard'):
            print(bcolors.OKGREEN+'Attempting to add new surfboard to db...'+bcolors.ENDC)
            #Get all info from request
            stockType = 'surfboard'
            brand = request.POST.get('brand')
            size = request.POST.get('size')
            number = checkForMatchingNum(stockType, request.POST.get('num'))
            gender=''
            print(bcolors.OKBLUE+"Retrieved item info: "+stockType, brand, str(size), str(number)+bcolors.ENDC)
            #Create a filename for the qr code using data from request
            fileName=stockType+brand+gender+str(size)+str(number)+'.png'
            #Check if qr code matchng filename exists
            if(checkForQR(fileName)):
                #Load surfboard info page
                return itemDetail(request, stockType, number)
            else:
                #Generate QR code for item
                generateQRCode(stockType, brand, gender, size, number, fileName)
                #Create a new item object and add it to db
                newSurfboard = Surfboard()
                newSurfboard.stockType=stockType
                newSurfboard.brand=brand
                newSurfboard.size=size
                newSurfboard.surfboardNumber=number
                newSurfboard.qrCode=fileName
                newSurfboard.url='http://'+IP+':8000/detail/'+stockType+'&'+str(number)
                newSurfboard.save()
                return itemDetail(request, stockType, number)
    else:
        return HttpResponse('fail')

def generateQRCode(stockType, brand, gender, size, number, fileName):
    if(stockType=='wetsuit'):
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
    elif(stockType=='surfboard'):
        print(bcolors.OKGREEN+"Generating a new surfboard QR code..."+bcolors.ENDC)
        #Generate qrcode from data
        qrData = 'http://'+IP+':8000/surfboard/'+brand+'&'+str(size)+'&'+str(number)
        qr = qrcode.make(qrData)
        print(bcolors.OKGREEN+"Saving generated QR code..."+bcolors.ENDC)
        path = 'static\\qrcodes\\'+fileName
        qr.save(path)
        if(exists(path)):
            return print(bcolors.OKBLUE+"Successfully generated and saved QR code!"+bcolors.ENDC)
        else:
            return print(bcolors.FAIL+"QR code failed to save!"+bcolors.ENDC)

def checkForMatchingNum(stockType, number):
    #Check if item with same item num exists
    try:
        #If item found with Id, get next available
        if(stockType=='wetsuit'):
            numItem = Wetsuit.objects.get(wetsuitNumber=number)
            number = getNextNum(1, 'wetsuit')
            return number
        elif(stockType=='surfboard'):
            numItem = Surfboard.objects.get(surfboardNumber=number)
            number = getNextNum(1, 'surfboard')
            return number
    except:
        #If not found, continue
        print(bcolors.OKBLUE+stockType+" number is ok!"+bcolors.ENDC)
        return number

def getNextNum(number, stockType):
    if(stockType=='wetsuit'):
        try:
            #If no exception, recursive call number+1
            availableNum = Wetsuit.objects.get(wetsuitNumber=number)
            num = number + 1
            return getNextNum(num, 'wetsuit')
        except:
            print(bcolors.FAIL+"NUMBER: "+str(number)+bcolors.ENDC)
            return number
    elif(stockType=='surfboard'):
        try:
            #If no exception, recursive call number+1
            availableNum = Surfboard.objects.get(surfboardNumber=number)
            num = number + 1
            return getNextNum(num, 'surfboard')
        except:
            print(bcolors.OKBLUE+"New number: "+str(number)+bcolors.ENDC)
            return number

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
        if(stockType=='wetsuit'):
            print(bcolors.WARNING+'Deleting QR code...'+bcolors.ENDC)
            gender = Wetsuit.objects.get(pk=pk).gender
            wetsuitNumber = Wetsuit.objects.get(pk=pk).wetsuitNumber
            print(bcolors.OKBLUE+"Obtained item info: "+stockType, brand, gender, str(size), str(wetsuitNumber)+bcolors.ENDC)
            #Delete associated QR code
            fileName=stockType+brand+gender+str(size)+str(wetsuitNumber)+'.png'
            deleteQRCode(fileName)
        elif(stockType=='surfboard'):
            print(bcolors.WARNING+'Deleting QR code...'+bcolors.ENDC)
            gender = Surfboard.objects.get(pk=pk).gender
            surfboardNumber = Wetsuit.objects.get(pk=pk).surfboardNumber
            print(bcolors.OKBLUE+"Obtained item info: "+stockType, brand, str(size), str(surfboardNumber)+bcolors.ENDC)
            #Delete associated QR code
            fileName=stockType+brand+str(size)+str(surfboardNumber)+'.png'
            deleteQRCode(fileName)
        else:
            print(bcolors.FAIL+'Invalid stocktype!'+bcolors.ENDC)

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
    wetsuits = Wetsuit.objects.all().order_by('wetsuitNumber')
    surfboards = Surfboard.objects.all().order_by('surfboardNumber')
    #surfboards = StockItem.objects.get(stockType='surfboard')
    return render(request, 'App/inventory.html', {'wetsuits' : wetsuits, 'surfboards': surfboards})