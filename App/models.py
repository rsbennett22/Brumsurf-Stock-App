from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
# Create your models here.

#Stock model info:

#Wetsuits: Brand, Size, Gender, Number
#Surfboards: Brand, Size, Number
#Surfskates: Brand, Size, Number
#Boots: Brand, Size, Number
#Gloves: Brand, Size, Number
#Hoods: Brand, Size, Number

#Signing in and out info:

#On-Trip
#Signed Out
#Signed In
#Name
#Student ID

class StockItem(models.Model):
    stockType = models.CharField(max_length=15)
    brand = models.CharField(max_length=30)
    size = models.CharField(max_length=10)
    onTrip = models.BooleanField(default=False)
    signedOut = models.BooleanField(default=False)
    signedIn = models.BooleanField(default=True)
    name = models.CharField(default='brumsurf', max_length=50)
    studentId = models.CharField(default='0000000', max_length=7, validators=[MinLengthValidator(7)])
    qrCode = models.ImageField()
    url = models.URLField(default=None)
    number=0

    def __str__(self):
        return (self.stockType+'_'+self.brand+'_'+self.size+'_'+str(self.number))

class Wetsuit(StockItem):
    gender = models.CharField(max_length=6)
    wetsuitNumber = models.PositiveIntegerField(default=0, unique=True)
    def __str__(self):
        return (self.stockType+'_'+self.brand+'_'+self.gender+'_'+self.size+'_'+str(self.wetsuitNumber))

class Surfboard(StockItem):
    surfboardNumber = models.PositiveIntegerField(default=0, unique=True)
    def __str__(self):
        return (self.stockType+'_'+self.brand+'_'+self.size+'_'+str(self.surfboardNumber))