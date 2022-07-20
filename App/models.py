from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
# Create your models here.

class StockItem(models.Model):
    stockType = models.CharField(max_length=15)
    brand = models.CharField(max_length=30)
    size = models.CharField(max_length=10)
    number = models.PositiveBigIntegerField(default=0, validators=[MinValueValidator(1)])
    onTrip = models.BooleanField(default=False)
    signedOut = models.BooleanField(default=False)
    signedIn = models.BooleanField(default=True)
    name = models.CharField(default='brumsurf', max_length=50)
    studentId = models.CharField(default='0000000', max_length=7, validators=[MinLengthValidator(7)])

    def __str__(self):
        return (self.stockType+'_'+self.brand+'_'+str(self.number))

class Wetsuit(StockItem):
    size=None
    gender = models.CharField(max_length=6)
    wetsuitSize = models.CharField(max_length=10)
