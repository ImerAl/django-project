import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class GeneralCategory (models.Model):
    name = models.CharField(max_length=100, default='default')

    def __str__(self): #Muestra los nombres de las cosas en admin
        return self.name

class Batch (models.Model):
    batch_number = models.CharField(max_length=10, default='0000000000')
    insert_date = models.DateField()

    def __str__(self):  # Muestra los nombres de las cosas en admin
        return self.batch_number

class TypeC (models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):  # Muestra los nombres de las cosas en admin
        return self.name

class MoneyInformation (models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    insert_date = models.DateField(auto_now_add=True)
    done_date = models.DateField()
    transaction_type = models.BooleanField()
    category = models.ForeignKey(GeneralCategory, on_delete=models.CASCADE)
    description = models.TextField()
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    detained = models.BooleanField()
    type = models.ForeignKey(TypeC, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    pay_date = models.DateField(default=datetime.datetime.now)
    def __str__(self):
        return self.name

class Cut_Off (models.Model):
    cutoff_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)