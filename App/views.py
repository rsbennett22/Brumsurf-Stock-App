from distutils.dep_util import newer_pairwise
from multiprocessing.context import BaseContext
from django.shortcuts import render, redirect
from django.http import HttpResponse
import qrcode
from os.path import exists
from os import remove
from .models import StockItem, Wetsuit, Surfboard, Surfskate, Boot, Glove, Hood
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

def inventory(request):
    print(bcolors.OKBLUE+"Successfully loaded inventory page!"+bcolors.ENDC)
    #This page displays a list of all stock items in a table like format
    #User can click on an item and see it's detail page
    wetsuits = Wetsuit.objects.all().order_by('wetsuitNumber')
    surfboards = Surfboard.objects.all().order_by('surfboardNumber')
    surfskates = Surfskate.objects.all().order_by('surfskateNumber')
    boots = Boot.objects.all().order_by('bootAmount')
    gloves = Glove.objects.all().order_by('gloveAmount')
    hoods = Hood.objects.all().order_by('hoodAmount')
    return render(request, 'App/inventory.html', {'wetsuits' : wetsuits, 'surfboards': surfboards, 'surfskates': surfskates, 'boots': boots, 'gloves': gloves, 'hoods': hoods})

def stockForms(request):
    print(bcolors.OKBLUE+"Successfully loaded stock form selection page!"+bcolors.ENDC)
    return render(request, 'App/stockForms.html')

def wetsuitForm(request):
    stockType='Wetsuit'
    return render(request, 'App/generateItemForm.html', {'stockType': stockType},print(bcolors.OKBLUE+"Successfully loaded wetsuit form page!"+bcolors.ENDC))

def surfboardForm(request):
    stockType='Surfboard'
    return render(request, 'App/generateItemForm.html', {'stockType': stockType},print(bcolors.OKBLUE+"Successfully loaded surfboard form page!"+bcolors.ENDC))

def surfskateForm(request):
    stockType='Surfskate'
    return render(request, 'App/generateItemForm.html', {'stockType': stockType},print(bcolors.OKBLUE+"Successfully loaded surfskate form page!"+bcolors.ENDC))

def bootForm(request):
    stockType='Boot'
    return render(request, 'App/generateItemForm.html', {'stockType': stockType},print(bcolors.OKBLUE+"Successfully loaded boots form page!"+bcolors.ENDC))

def gloveForm(request):
    stockType='Glove'
    return render(request, 'App/generateItemForm.html', {'stockType': stockType},print(bcolors.OKBLUE+"Successfully loaded glove form page!"+bcolors.ENDC))

def hoodForm(request):
    stockType='Hood'
    return render(request, 'App/generateItemForm.html', {'stockType': stockType},print(bcolors.OKBLUE+"Successfully loaded hood form page!"+bcolors.ENDC))

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
        elif(request.POST.get('stockType')=='Surfskate'):
            print(bcolors.OKGREEN+"Setting stocktype to surfskate..."+bcolors.ENDC)
            stockType = 'surfskate'
            print(bcolors.OKBLUE+"Successfully set stocktype to surfskate!"+bcolors.ENDC)
        elif(request.POST.get('stockType')=='Boot'):
            print(bcolors.OKGREEN+"Setting stocktype to boot..."+bcolors.ENDC)
            stockType = 'boot'
            print(bcolors.OKBLUE+"Successfully set stocktype to boot!"+bcolors.ENDC)
        elif(request.POST.get('stockType')=='Glove'):
            print(bcolors.OKGREEN+"Setting stocktype to glove..."+bcolors.ENDC)
            stockType = 'glove'
            print(bcolors.OKBLUE+"Successfully set stocktype to glove!"+bcolors.ENDC)
        else:
            print(bcolors.OKGREEN+"Setting stocktype to hood..."+bcolors.ENDC)
            stockType = 'hood'
            print(bcolors.OKBLUE+"Successfully set stocktype to hood!"+bcolors.ENDC)

        print(bcolors.OKGREEN+"Attempting to add new "+stockType+" to db..."+bcolors.ENDC)
        brand = request.POST.get('brand')
        size = request.POST.get('size')
        if(size==None):
            size=''
        print(bcolors.FAIL+str(request.POST)+bcolors.ENDC)
        number = checkForMatchingNum(stockType, request.POST.get('num'))
        print(bcolors.OKBLUE+"Retrieved item info: "+stockType, brand, gender, str(size), str(number)+bcolors.ENDC)
        
        if(stockType=='boot' or stockType=='glove' or stockType=='hood'):
            if(stockType=='boot'):
                #Check for matching item
                try:
                    matchingBoot = Boot.objects.get(brand=brand, size=size)
                    #If match item, load detail page
                    return accessoryDetail(request, matchingBoot.pk)
                except:
                    #No matching item
                    #Set amount and save
                    amount = request.POST.get('amount')
                    #Create new boot instance
                    newBoot = Boot()
                    newBoot.stockType=stockType
                    newBoot.brand=brand
                    newBoot.size=size
                    newBoot.bootAmount=amount
                    newBoot.url=''
                    #Save boot
                    newBoot.save()
                    #Get newboot pk
                    bootMade = Boot.objects.get(brand=brand, size=size)
                    pk = bootMade.pk
                    bootMade.url = 'http://192.168.0.72:8000/detail/'+str(pk)
                    bootMade.save()
                    #Load accessory details page
                    return accessoryDetail(request, pk)
            elif(stockType=='glove'):
                #Check for matching item
                try:
                    matchingGlove = Glove.objects.get(brand=brand, size=size)
                    #If match item, load detail page
                    return accessoryDetail(request, matchingGlove.pk)
                except:
                    #No matching item
                    #Set amount and save
                    amount = request.POST.get('amount')
                    #Create new boot instance
                    newGlove = Glove()
                    newGlove.stockType=stockType
                    newGlove.brand=brand
                    newGlove.size=size
                    newGlove.gloveAmount=amount
                    newGlove.url=''
                    #Save boot
                    newGlove.save()
                    #Get newboot pk
                    gloveMade = Glove.objects.get(brand=brand, size=size)
                    pk = gloveMade.pk
                    gloveMade.url = 'http://192.168.0.72:8000/detail/'+str(pk)
                    gloveMade.save()
                    #Load accessory details page
                    return accessoryDetail(request, pk)
            else:
                #Check for matching item
                try:
                    matchingHood = Hood.objects.get(brand=brand, size=size)
                    #If match item, load detail page
                    return accessoryDetail(request, matchingHood.pk)
                except:
                    #No matching item
                    #Set amount and save
                    amount = request.POST.get('amount')
                    #Create new boot instance
                    newHood = Hood()
                    newHood.stockType=stockType
                    newHood.brand=brand
                    newHood.size=size
                    newHood.hoodAmount=amount
                    newHood.url=''
                    #Save boot
                    newHood.save()
                    #Get newboot pk
                    hoodMade = Hood.objects.get(brand=brand, size=size)
                    pk = hoodMade.pk
                    hoodMade.url = 'http://192.168.0.72:8000/detail/'+str(pk)
                    hoodMade.save()
                    #Load accessory details page
                    return accessoryDetail(request, pk)
                
        else:
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
                    newWetsuit.url='http://192.168.0.72:8000/detail/'+stockType+'&'+str(number)
                    print(bcolors.OKBLUE+"New wetsuit info: "+str(newWetsuit)+bcolors.ENDC)
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
                    newBoard.url='http://192.168.0.72:8000/detail/'+stockType+'&'+str(number)
                    newBoard.save()
                    print(bcolors.OKBLUE+"Successfully created a new "+stockType+" instance!"+bcolors.ENDC)
                    return itemDetail(request, stockType, number)
                elif(stockType=='surfskate'):
                    print(bcolors.OKGREEN+"Creating a new "+stockType+" instance!"+bcolors.ENDC)
                    newBoard = Surfskate()
                    newBoard.stockType=stockType
                    newBoard.brand=brand
                    newBoard.size=size
                    newBoard.surfskateNumber=number
                    newBoard.qrCode=fileName
                    newBoard.url='http://192.168.0.72:8000/detail/'+stockType+'&'+str(number)
                    newBoard.save()
                    print(bcolors.OKBLUE+"Successfully created a new "+stockType+" instance!"+bcolors.ENDC)
                    return itemDetail(request, stockType, number)

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
    elif(stockType=='surfskate'):
        #Get surfboard details
        print(bcolors.OKGREEN+"Getting "+stockType+" specific details..."+bcolors.ENDC)
        thisBoard = Surfskate.objects.get(surfskateNumber=number)
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
        'qrCode': 'qrcodes/'+str(qrCode),
        'pk': pk,
        'deleteUrl': deleteUrl,
        'signOutUrl': signOutUrl,
        'signInUrl': signInUrl,
        'onTripUrl': onTripUrl,
    }, print(bcolors.OKBLUE+'Loaded item detail page!'+bcolors.ENDC))

def accessoryDetail(request, pk):
    #Get item info
    item = StockItem.objects.get(pk=pk)
    stockType = item.stockType
    brand = item.brand
    size = item.size
    amount = ''
    if(stockType=='boot'):
        amount=Boot.objects.get(pk=pk).bootAmount
    elif(stockType=='glove'):
        amount=Glove.objects.get(pk=pk).gloveAmount
    else:
        amount=Hood.objects.get(pk=pk).hoodAmount
    
    deleteUrl = '../deleteItem/'+str(pk)
    updateUrl = '../updateItem/'+str(pk)

    #Load detail page
    return render(request, 'App/accessoryDetail.html', {'stockType': stockType, 'brand': brand, 'size': size, 'amount': amount, 'pk': pk, 'deleteUrl': deleteUrl, 'updateUrl': updateUrl})

def generateQRCode(stockType, brand, gender, size, number, fileName):
    print(bcolors.OKGREEN+"Generating a new"+stockType+" QR code..."+bcolors.ENDC)
    #Generate qrcode from data
    qrData = 'http://192.168.0.72:8000/'+stockType+'/'+brand+'&'+gender+'&'+str(size)+'&'+str(number)
    qr = qrcode.make(qrData)
    print(bcolors.OKGREEN+"Saving generated QR code..."+bcolors.ENDC)
    path = 'static/qrcodes/'+fileName
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
        elif(stockType=='surfskate'):
            numItem = Surfskate.objects.get(surfskateNumber=number)
            number = getNextNum(1, 'surfskate')
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
    elif(stockType=='surfskate'):
        try:
            #If no exception, recursive call number+1
            availableNum = Surfskate.objects.get(surfskateNumber=number)
            num = number + 1
            return getNextNum(num, 'surfskate')
        except:
            print(bcolors.OKBLUE+"New number: "+str(number)+bcolors.ENDC)
            return number

def checkForQR(fileName):
    path = 'static/qrcodes/'+fileName
    print(path)
    if(exists(path)):
        print(bcolors.OKBLUE+"QR code already exists!"+bcolors.ENDC)
        return True
    else:
        print(bcolors.WARNING+"QR code does not exist!"+bcolors.ENDC)
        return False

def deleteItem(request, pk):
    itemToDelete = StockItem.objects.get(pk=pk)
    stockType=itemToDelete.stockType
    if(stockType=='boot' or stockType=='glove' or stockType=='hood'):
        itemToDelete.delete()
        return redirect('/')
    else:
        qrCode = str(itemToDelete.qrCode)
        deleteQRCode(qrCode)
        itemToDelete.delete()
        return redirect('/')

def deleteQRCode(fileName):
    path='static/qrcodes/'+fileName
    print(bcolors.OKGREEN+"Checking if file to be deleted exists..."+bcolors.ENDC)
    if(exists(path)):
        #Delete file
        print(bcolors.OKBLUE+"File exists!"+bcolors.ENDC)
        print(bcolors.WARNING+"Deleting file..."+bcolors.ENDC)
        remove(path)
        return print(bcolors.OKBLUE+"File deleted successfully!"+bcolors.ENDC)
    else:
        return print(bcolors.FAIL+"Error! File does not exist!"+bcolors.ENDC)

def updateItem(request, pk, amount):
    print(bcolors.OKGREEN+"Trying to update item..."+bcolors.ENDC)
    try:
        itemToUpdate = StockItem.objects.get(pk=pk)
        if(itemToUpdate.stockType=='boot'):
            print(bcolors.OKGREEN+"Setting new amount value..."+bcolors.ENDC)
            bootToUpdate=Boot.objects.get(pk=pk)
            bootToUpdate.bootAmount = amount
            bootToUpdate.save()
            print(bcolors.OKBLUE+"Item updated successfully!"+bcolors.ENDC)
            return accessoryDetail(request, pk)
        elif(itemToUpdate.stockType=='glove'):
            print(bcolors.OKGREEN+"Setting new amount value..."+bcolors.ENDC)
            gloveToUpdate=Glove.objects.get(pk=pk)
            gloveToUpdate.gloveAmount = amount
            gloveToUpdate.save()
            print(bcolors.OKBLUE+"Item updated successfully!"+bcolors.ENDC)
            return accessoryDetail(request, pk)
        else:
            print(bcolors.OKGREEN+"Setting new amount value..."+bcolors.ENDC)
            hoodToUpdate=Hood.objects.get(pk=pk)
            hoodToUpdate.hoodAmount = amount
            hoodToUpdate.save()
            print(bcolors.OKBLUE+"Item updated successfully!"+bcolors.ENDC)
            return accessoryDetail(request, pk)
    except:
        return (accessoryDetail(request, pk),print(bcolors.FAIL+"Failed to update item!"+bcolors.ENDC))


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
