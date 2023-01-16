from django.shortcuts import render
from .models import Car, AutoModel, OrderCar, Order, Service

from django.http import HttpResponse


def index(request):


    context = {}
    return render(request, 'index.html', context=context)

# Create your views here.
