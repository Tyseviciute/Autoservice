from datetime import date

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from tinymce.models import HTMLField



# Create your models here.
class AutoModel(models.Model):
    make = models.CharField('Make name', max_length=50, help_text='Enter a car make')
    model = models.CharField('Model name', max_length=50, help_text='Enter a car model')

    class Meta:
        verbose_name = "Automodel"
        verbose_name_plural = "Automodels"

    def __str__(self):
        return f"{self.make}, {self.model}"


class Car(models.Model):
    valst_nr = models.CharField('Number', max_length=6, help_text='Enter the country registration number')
    vin_code = models.CharField('VIN_code', max_length=17, help_text='Enter a VIN code')
    client = models.CharField('Client', max_length=200, help_text='Enter client name and last name')
    description = HTMLField(default='Cia yra automobilio aprasymas')
    automodel = models.ForeignKey('AutoModel', on_delete=models.SET_NULL, null=True)
    cover = models.ImageField('Photo', upload_to='covers', null=True)


    # pervadinti laukus klasiu
    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def get_absolute_url(self):
        return reverse('car-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.automodel} - {self.client}: {self.valst_nr} - {self.vin_code}"


class Service(models.Model):
    name = models.CharField('Name', max_length=200, help_text='Enter a service name')
    price = models.FloatField('Price', help_text='Enter a service price')

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.name}: {self.price}"


class Order(models.Model):
    date = models.DateTimeField('Date', null=True, blank=True)
    suma = models.FloatField('Sum', help_text='Enter a sum of order')
    car = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True)
    returne = models.DateField('Return for client', null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'administrative'),
        ('r', 'repair'),
        ('e', 'repaired'),
        ('g', 'given away')
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Status'
    )

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overreturne(self):
        if self.returne and date.today() > self.returne:
            return True
        return False


    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def get_absolute_url(self):  # gauti linkus spec pavadinimas
        return reverse('order-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.car}: {self.date}, {self.suma}, {self.status}"


class OrderCar(models.Model):
    kiekis = models.IntegerField('How', help_text='Enter how much do you want to buy car')
    kaina = models.FloatField('Price', help_text='Enter a price')
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Ordercar"
        verbose_name_plural = "Ordercars"

    def __str__(self):
        return f"{self.order}, {self.service.name} - {self.kiekis}: {self.kaina}"
