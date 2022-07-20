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

class stockItem(models.Model):
    brand = models.CharField(max_length=30)
    size = models.CharField(max_length=10)
    Number = models.PositiveBigIntegerField(default=0, validators=[MinValueValidator(1)])
    onTrip = models.BooleanField(default=False)
    signedOut = models.BooleanField(default=False)
    signedIn = models.BooleanField(default=True)
    name = models.CharField(default='brumsurf', max_length=50)
    studentId = models.CharField(default='0000000', max_length=7, validators=[MinLengthValidator(7)])

class wetsuit(stockItem):
    MALE_SIZES = [
        ('S', 'Small'), 
        ('M', 'Medium'), 
        ('MT', 'Medium-Tall'), 
        ('L', 'Large'), 
        ('XL', 'X-Large')
        ]
    FEMALE_SIZES = [
        ('4', 'Four'), 
        ('6', 'Six'), 
        ('8', 'Eight'), 
        ('10', 'Ten'), 
        ('12', 'Twelve'), 
        ('14', 'Fourteen'), 
        ('16', 'Sixteen')
        ]
    GENDERS = [
        ('M', 'Male'), 
        ('F', 'Female')
        ]
    gender = models.CharField(max_length=6, choices=GENDERS)
    if(gender=='Male'):
        wetsuitSize = models.CharField(max_length=10, choices=MALE_SIZES)
    else:
        wetsuitSize = models.CharField(max_length=10, choices=FEMALE_SIZES)
