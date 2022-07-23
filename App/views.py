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
    print(IP)
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
    gender = ''
    pk = ''
    if(stockType=='wetsuit'):
        #Get wetsuit details
        print(bcolors.OKGREEN+"Getting "+stockType+" specific details..."+bcolors.ENDC)
        thisWetty = Wetsuit.objects.get(wetsuitNumber=number)
        gender=thisWetty.gender
        pk = thisWetty.pk
        print(bcolors.OKBLUE+"Retrieved gender: "+gender+" and pk: "+str(pk)+bcolors.ENDC)
    elif(stockType=='surfboard'):
        #Get surfboard details
        print(bcolors.OKGREEN+"Getting "+stockType+" specific details..."+bcolors.ENDC)
        thisBoard = Surfboard.objects.get(surfboardNumber=number)
        pk = thisBoard.pk
        print(bcolors.OKBLUE+"Retrieved pk: "+str(pk)+bcolors.ENDC)

    #Get common details
    print(bcolors.OKGREEN+"Getting common item details..."+bcolors.ENDC)
    item = StockItem.objects.get(pk=pk)
    brand = item.brand
    size = item.size
    onTrip = item.onTrip
    signedOut = item.signedOut
    signedIn = item.signedIn
    qrCode = item.qrCode
    deleteUrl = '../deleteItem/'+str(pk)
    signOutUrl='../signOut/'+str(pk)
    signInUrl='../signIn/'+str(pk)
    onTripUrl='../onTrip/'+str(pk)
    print(bcolors.OKBLUE+"Brand:"+brand+" Size:"+str(size)+" onTrip:"+str(onTrip)+" signedOut:"+str(signedOut)+" signedIn:"+str(signedIn)
    +" qrCode:"+str(qrCode)+" deleteUrl:"+deleteUrl+" signedOutUrl:"+signOutUrl+" signInUrl:"+signInUrl+" onTripUrl:"+onTripUrl+bcolors.ENDC)
    #Load detail page
    print(bcolors.OKGREEN+'Attempting to load details page...'+bcolors.ENDC)
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
    }, print(bcolors.OKBLUE+'Loaded item detail page!'+bcolors.ENDC))

def addNewItem(request):
    if(request.method=='POST'):
        stockType=''
        brand=''
        gender=''
        size=''
        number=''
        #Check stockType
        if(request.POST.get('stockType')=='Wetsuit'):
            print(bcolors.OKGREEN+"Setting wetsuit specific details..."+bcolors.ENDC)
            stockType = 'wetsuit'
            gender = request.POST.get('gender')
            print(bcolors.OKBLUE+"Successfully set details: stockType: "+stockType+" and gender: "+gender+"!"+bcolors.ENDC)
        elif(request.POST.get('stockType')=='Surfboard'):
            print(bcolors.OKGREEN+"Setting stocktype to surfboard..."+bcolors.ENDC)
            stockType = 'surfboard'
            print(bcolors.OKBLUE+"Successfully set stocktype to surfboard!"+bcolors.ENDC)

        print(bcolors.OKGREEN+"Attempting to add new "+stockType+" to db..."+bcolors.ENDC)
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
            if(stockType=='wetsuit'):
                print(bcolors.OKGREEN+"Creating a new "+stockType+" instance!"+bcolors.ENDC)
                newWetsuit = Wetsuit()
                newWetsuit.stockType=stockType
                newWetsuit.brand=brand
                newWetsuit.gender=gender
                newWetsuit.size=size
                newWetsuit.wetsuitNumber=number
                newWetsuit.qrCode=fileName
                newWetsuit.url='http://192.168.0.58:8000/detail/'+stockType+'&'+str(number)
                newWetsuit.save()
                print(bcolors.OKBLUE+"Successfully created a new "+stockType+" instance!"+bcolors.ENDC)
                return itemDetail(request, stockType, number)
            elif(stockType=='surfboard'):
                print(bcolors.OKGREEN+"Creating a new "+stockType+" instance!"+bcolors.ENDC)
                newBoard = Surfboard()
                newBoard.stockType=stockType
                newBoard.brand=brand
                newBoard.size=size
                newBoard.surfboardNumber=number
                newBoard.qrCode=fileName
                newBoard.url='http://192.168.0.58:8000/detail/'+stockType+'&'+str(number)
                newBoard.save()
                print(bcolors.OKBLUE+"Successfully created a new "+stockType+" instance!"+bcolors.ENDC)
                return itemDetail(request, stockType, number)

def generateQRCode(stockType, brand, gender, size, number, fileName):
    print(bcolors.OKGREEN+"Generating a new"+stockType+" QR code..."+bcolors.ENDC)
    #Generate qrcode from data
    qrData = 'http://192.168.0.58:8000/'+stockType+'/'+brand+'&'+gender+'&'+str(size)+'&'+str(number)
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
            print(bcolors.OKBLUE+"New number: "+str(number)+bcolors.ENDC)
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
    qrCode = str(itemToDelete.qrCode)
    deleteQRCode(qrCode)
    itemToDelete.delete()
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