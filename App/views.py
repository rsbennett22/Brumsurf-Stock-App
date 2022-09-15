from django.shortcuts import render, redirect
from django.http import HttpResponse
import qrcode
from os.path import exists
from os import remove
from .models import StockItem, Wetsuit, Surfboard, Surfskate, Boot, Glove, Hood
import socket
import csv, io

'''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]
'''

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
    #print(IP)
    return render(request, 'App/index.html',print(bcolors.OKBLUE+'Successfully loaded home page!'+bcolors.ENDC))

def inventory(request):
    print(bcolors.OKBLUE+"Successfully loaded inventory page!"+bcolors.ENDC)
    #This page displays a list of all stock items in a table like format
    #User can click on an item and see it's detail page
    wetsuits = Wetsuit.objects.all().order_by('wetsuitNumber')
    surfboards = Surfboard.objects.all().order_by('surfboardNumber')
    surfskates = Surfskate.objects.all().order_by('surfskateNumber')
    boots = Boot.objects.all().order_by('pk')
    gloves = Glove.objects.all().order_by('pk')
    hoods = Hood.objects.all().order_by('pk')
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
                    matchingBoot = Boot.objects.get(size=size)
                    #If match item, load detail page
                    return accessoryDetail(request, matchingBoot.pk)
                except:
                    #No matching item
                    #Set amount and save
                    amount = request.POST.get('amount')
                    #Create new boot instance
                    newBoot = Boot()
                    newBoot.stockType=stockType
                    newBoot.brand=''
                    newBoot.size=size
                    newBoot.bootAmount=amount
                    newBoot.url=''
                    #Save boot
                    newBoot.save()
                    #Get newboot pk
                    bootMade = Boot.objects.get(size=size)
                    pk = bootMade.pk
                    bootMade.url = 'http://0.0.0.0:8000/detail/'+str(pk)
                    bootMade.save()
                    #Load accessory details page
                    return accessoryDetail(request, pk)
            elif(stockType=='glove'):
                #Check for matching item
                try:
                    matchingGlove = Glove.objects.get(size=size)
                    #If match item, load detail page
                    return accessoryDetail(request, matchingGlove.pk)
                except:
                    #No matching item
                    #Set amount and save
                    amount = request.POST.get('amount')
                    #Create new boot instance
                    newGlove = Glove()
                    newGlove.stockType=stockType
                    newGlove.brand=''
                    newGlove.size=size
                    newGlove.gloveAmount=amount
                    newGlove.url=''
                    #Save boot
                    newGlove.save()
                    #Get newboot pk
                    gloveMade = Glove.objects.get(size=size)
                    pk = gloveMade.pk
                    gloveMade.url = 'http://0.0.0.0:8000/detail/'+str(pk)
                    gloveMade.save()
                    #Load accessory details page
                    return accessoryDetail(request, pk)
            else:
                #Check for matching item
                try:
                    matchingHood = Hood.objects.get(size=size)
                    #If match item, load detail page
                    return accessoryDetail(request, matchingHood.pk)
                except:
                    #No matching item
                    #Set amount and save
                    amount = request.POST.get('amount')
                    #Create new boot instance
                    newHood = Hood()
                    newHood.stockType=stockType
                    newHood.brand=''
                    newHood.size=size
                    newHood.hoodAmount=amount
                    newHood.url=''
                    #Save boot
                    newHood.save()
                    #Get newboot pk
                    hoodMade = Hood.objects.get(size=size)
                    pk = hoodMade.pk
                    hoodMade.url = 'http://0.0.0.0:8000/detail/'+str(pk)
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
                generateQRCode(stockType, number, fileName)
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
                    newWetsuit.url='http://0.0.0.0:8000/detail/'+stockType+'&'+str(number)
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
                    newBoard.url='http://0.0.0.0:8000/detail/'+stockType+'&'+str(number)
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
                    newBoard.url='http://0.0.0.0:8000/detail/'+stockType+'&'+str(number)
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

def generateQRCode(stockType, number, fileName):
    print(bcolors.OKGREEN+"Generating a new "+stockType+" QR code..."+bcolors.ENDC)
    #Generate qrcode from data
    qrData = 'http://0.0.0.0:8000/detail/'+stockType+'&'+str(number)
    print(bcolors.FAIL+qrData+bcolors.ENDC)
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

def importData(request):
    csvFile = request.FILES['file']
    if not csvFile.name.endswith('.csv'):
        #redirect to an error page
        print('error')

    data = csvFile.read().decode('UTF-8')
    print(data)
    print(type(data))

    stockType = ''

    ioString = io.StringIO(data)
    for column in csv.reader(ioString, delimiter=','):
        #Only print rows that contain data
        if len(column)>0:
            #Check if col[0] is a row that isn't data
            #if column[0]=='Brand' or column[0]=='Surfboards' or column[0]=='Surfskates' or column[0]=='Boots' or column[0]=='Gloves' or column[0]=='Hoods' or column[0]=='Size' or column[0]=='Female Wetsuits' or column[0]=='Male Wetsuits':
            #    continue
            #Check what type of stock currently on
            if column[0]=='Male Wetsuits' or column[0]=='Female Wetsuits':
                stockType = 'wetsuit'
                continue
            elif column[0]=='Surfboards':
                stockType = 'surfboard'
                continue
            elif column[0]=='Surfskates':
                stockType='surfskate'
                continue
            elif column[0]=='Boots':
                stockType = 'boot'
                continue
            elif column[0]=='Gloves':
                stockType = 'glove'
                continue
            elif column[0]=='Hoods':
                stockType = 'hood'
                continue
            elif column[0]=='Brand' or column[0]=='Size':
                continue
            else:
                print(stockType)
                print(column)
                #Check what the current stocktype is
                if stockType=='wetsuit':
                    #Set variable attributes of wetsuit
                    wetsuitNumber = column[3]
                    print(wetsuitNumber)
                    wetsuit = Wetsuit()
                    wetsuit.stockType=stockType
                    wetsuit.brand=column[0]
                    wetsuit.gender=column[1]
                    wetsuit.size=column[2]
                    wetsuit.onTrip=column[4]
                    wetsuit.signedOut=column[5]
                    wetsuit.signedIn=column[6]
                    wetsuit.name=column[7]
                    wetsuit.studentId=column[8]
                    wetsuit.url='http://0.0.0.0:8000/detail/'+stockType+'&'+wetsuitNumber
                    wetsuit.qrCode=stockType+column[0]+column[1]+column[2]+column[3]+'.png'
                    try:
                        suitToUpdate = Wetsuit.objects.get(wetsuitNumber=wetsuitNumber)
                        #If find a suit, update suit
                        #compate attributes and update as necessary
                        print('Updating old wetsuit')
                        suitToUpdate = compareAndUpdateWetsuit(suitToUpdate, wetsuit)
                        suitToUpdate.save()
                        print(suitToUpdate.url)
                    except:
                        #If not find a suit, save the created one
                        print('Creating new wetsuit')
                        wetsuit.wetsuitNumber=wetsuitNumber
                        wetsuit.save()
                elif stockType=='surfboard':
                    #Set variable attributes of surfboard
                    surfboardNumber = column[2]
                    print(surfboardNumber)
                    surfboard = Surfboard()
                    surfboard.stockType=stockType
                    surfboard.brand=column[0]
                    surfboard.size=column[1]
                    surfboard.onTrip=column[3]
                    surfboard.signedOut=column[4]
                    surfboard.signedIn=column[5]
                    surfboard.name=column[6]
                    surfboard.studentId=column[7]
                    surfboard.url='http://0.0.0.0:8000/detail/'+stockType+'&'+surfboardNumber
                    surfboard.qrCode=stockType+column[0]+column[1]+column[2]+'.png'
                    try:
                        boardToUpdate = Surfboard.objects.get(surfboardNumber=surfboardNumber)
                        #If find a board, update board
                        #compate attributes and update as necessary
                        print('Updating old surfboard')
                        boardToUpdate = compareAndUpdateSurfboard(boardToUpdate, surfboard)
                        boardToUpdate.save()
                        print(boardToUpdate.url)
                    except:
                        #If not find a suit, save the created one
                        print('Creating new surfboard')
                        surfboard.surfboardNumber=surfboardNumber
                        surfboard.save()
                elif stockType=='surfskate':
                    #Set variable attributes of surfskate
                    surfskateNumber = column[1]
                    print(surfskateNumber)
                    surfskate = Surfskate()
                    surfskate.stockType=stockType
                    surfskate.brand=column[0]
                    surfskate.onTrip=column[2]
                    surfskate.signedOut=column[3]
                    surfskate.signedIn=column[4]
                    surfskate.name=column[5]
                    surfskate.studentId=column[6]
                    surfskate.url='http://0.0.0.0:8000/detail/'+stockType+'&'+surfskateNumber
                    surfskate.qrCode=stockType+column[0]+column[1]+'.png'
                    try:
                        boardToUpdate = Surfskate.objects.get(surfskateNumber=surfskateNumber)
                        #If find a skate, update skate
                        #compate attributes and update as necessary
                        print('Updating old surfskate')
                        boardToUpdate = compareAndUpdateSurfskate(boardToUpdate, surfskate)
                        boardToUpdate.save()
                        print(boardToUpdate.url)
                    except:
                        #If not find a suit, save the created one
                        print('Creating new surfskate')
                        surfskate.surfskateNumber=surfskateNumber
                        surfskate.save()
                else:
                    #Set variable attributes of boot
                    accessory = None
                    size = column[0]
                    if stockType=='boot':
                        accessory = Boot()
                        accessory.bootAmount=column[1]
                    if stockType=='glove':
                        accessory = Glove()
                        accessory.gloveAmount=column[1]
                    if stockType=='hood':
                        accessory = Hood()
                        accessory.hoodAmount=column[1]

                    accessory.stockType=stockType
                    accessory.size=column[0]
                    accessory.url=''
                    accessory.brand=''
                    try:
                        if stockType=='boot':
                            accessoryToUpdate = Boot.objects.get(size=size)
                        elif stockType=='glove':
                            accessoryToUpdate = Glove.objects.get(size=size)
                        elif stockType=='hood':
                            accessoryToUpdate = Hood.objects.get(size=size)
                        #If find a suit, update suit
                        #compate attributes and update as necessary
                        print('Updating old accessory')
                        accessoryToUpdate = compareAndUpdateAccessory(stockType, accessoryToUpdate, accessory)
                        accessoryToUpdate.save()
                        print(accessoryToUpdate.url)
                    except:
                        #If not find a suit, save the created one
                        print('Creating new accessory')
                        accessory.save()
                        #Then update the url of the boot
                        accessory.url = 'http://0.0.0.0:8000/detail/'+str(accessory.pk)
                        accessory.save()

    return inventory(request)

#fileName=stockType+brand+gender+str(size)+str(number)+'.png'

def compareAndUpdateWetsuit(old, new):
    hasUrlUpdated = False
    if old.brand!=new.brand:
        old.brand=new.brand
    if old.gender!=new.gender:
        old.gender=new.gender
    if old.size!=new.size:
        old.size=new.size
    if old.onTrip!=new.onTrip:
        old.onTrip=new.onTrip
    if old.signedOut!=new.signedOut:
        old.signedOut=new.signedOut
    if old.signedIn!=new.signedIn:
        old.signedIn=new.signedIn
    if old.name!=new.name:
        old.name=new.name
    if old.studentId!=new.studentId:
        old.studentId=new.studentId
    if old.url!=new.url:
        old.url=new.url
        hasUrlUpdated=True
    if old.qrCode!=new.qrCode:
        old.qrCode=new.qrCode
    if hasUrlUpdated:
        createOrUpdateQR(old.url, old.qrCode)
    return old

def compareAndUpdateSurfboard(old, new):
    hasUrlUpdated = False
    if old.brand!=new.brand:
        old.brand=new.brand
    if old.size!=new.size:
        old.size=new.size
    if old.onTrip!=new.onTrip:
        old.onTrip=new.onTrip
    if old.signedOut!=new.signedOut:
        old.signedOut=new.signedOut
    if old.signedIn!=new.signedIn:
        old.signedIn=new.signedIn
    if old.name!=new.name:
        old.name=new.name
    if old.studentId!=new.studentId:
        old.studentId=new.studentId
    if old.url!=new.url:
        old.url=new.url
        hasUrlUpdated = True
    if old.qrCode!=new.qrCode:
        old.qrCode=new.qrCode
    if hasUrlUpdated:
        createOrUpdateQR(old.url, old.qrCode)
    return old

def compareAndUpdateSurfskate(old, new):
    hasUrlUpdated = False
    if old.brand!=new.brand:
        old.brand=new.brand
    if old.onTrip!=new.onTrip:
        old.onTrip=new.onTrip
    if old.signedOut!=new.signedOut:
        old.signedOut=new.signedOut
    if old.signedIn!=new.signedIn:
        old.signedIn=new.signedIn
    if old.name!=new.name:
        old.name=new.name
    if old.studentId!=new.studentId:
        old.studentId=new.studentId
    if old.url!=new.url:
        old.url=new.url
        hasUrlUpdated = True
    if old.qrCode!=new.qrCode:
        old.qrCode=new.qrCode
    if hasUrlUpdated:
        createOrUpdateQR(old.url, old.qrCode)
    return old

def compareAndUpdateAccessory(stockType, old, new):
    if stockType=='boot':
        if old.bootAmount!=new.bootAmount:
            old.bootAmount=new.bootAmount
    if stockType=='glove':
        if old.gloveAmount!=new.gloveAmount:
            old.gloveAmount=new.gloveAmount
    if stockType=='hood':
        if old.hoodAmount!=new.hoodAmount:
            old.hoodAmount=new.hoodAmount
    if old.size!=new.size:
        old.size=new.size
    if old.url!=new.url:
        old.url='http://0.0.0.0:8000/detail/'+str(old.pk)
    return old

def generateQRCodeFromUploadCSV(url, fileName):
    print(bcolors.OKGREEN+"Generating a new QR code..."+bcolors.ENDC)
    #Generate qrcode from data
    print(bcolors.FAIL+url+bcolors.ENDC)
    qr = qrcode.make(url)
    print(bcolors.OKGREEN+"Saving generated QR code..."+bcolors.ENDC)
    path = 'static/qrcodes/'+str(fileName)
    qr.save(path)
    if(exists(path)):
        return print(bcolors.OKBLUE+"Successfully generated and saved QR code!"+bcolors.ENDC)
    else:
        return print(bcolors.FAIL+"QR code failed to save!"+bcolors.ENDC)

def createOrUpdateQR(url, fileName):
    #Check if a qr code exists
    isQrPresent = checkForQR(str(fileName))
    print(isQrPresent)
    if isQrPresent:
        deleteQRCode(str(fileName))
    #Generate a new qr code
    generateQRCodeFromUploadCSV(url, fileName)
