from .models import Car, AutoModel, OrderCar, Order, Service
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from django.http import HttpResponse


def index(request):
    num_service = Service.objects.all().count()

    num_order = Order.objects.all().count()

    num_car = Car.objects.all().count

    num_automodel = AutoModel.objects.all().count()

    num_visits = request.session.get('num_visits', 1)  # userio apsilaankymu skaiciavimas
    request.session['num_visits'] = num_visits + 1

    context = {'num_service': num_service,
               'num_order': num_order,
               'num_car': num_car,
               'num_automodel': num_automodel,
               'num_visits': num_visits}
    return render(request, 'index.html', context=context)


def cars(request):
    # cars = Car.objects.all()
    paginator = Paginator(Car.objects.all(), 1)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {'cars': paged_cars}
    return render(request, 'cars.html', context=context)


def car(request, car_id):
    single_car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', {'car': single_car})


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 1
    template_name = 'order_list.html'


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'


def search(request):
    query = request.GET.get("query")
    search_results = Car.objects.filter(
        Q(client__icontains=query) | Q(valst_nr__icontains=query) |
        Q(vin_code__icontains=query)
    )
    return render(request, 'search.html', {"cars": search_results,
                                           "query": query})
