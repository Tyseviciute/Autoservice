from .models import Car, AutoModel, OrderCar, Order, Service
from django.views import generic
from django.shortcuts import render, get_object_or_404



from django.http import HttpResponse


def index(request):

    num_service = Service.objects.all().count()

    num_order = Order.objects.all().count()

    num_car = Car.objects.all().count

    num_automodel = AutoModel.objects.all().count()

    context = {'num_service': num_service,
               'num_order': num_order,
               'num_car': num_car,
               'num_automodel': num_automodel}
    return render(request, 'index.html', context=context)

def cars(request):
    cars = Car.objects.all()
    context = {'cars': cars}
    return render(request, 'cars.html', context=context)


def car(request, car_id):
    single_car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', {'car': single_car})


class OrderListView(generic.ListView):
    model = Order
    template_name = 'order_list.html'

