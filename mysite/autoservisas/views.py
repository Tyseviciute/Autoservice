from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .forms import OrderReviewForm
from .models import Car, AutoModel, OrderCar, Order, Service
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin


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


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'order_detail.html'
    form_class = OrderReviewForm

    class Meta:
        ordering = ['car']

    # nukreipimas po sekmingo komentaro papostinimo atgal i knygos views
    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_valid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)


def search(request):
    query = request.GET.get("query")
    search_results = Car.objects.filter(
        Q(client__icontains=query) | Q(valst_nr__icontains=query) |
        Q(vin_code__icontains=query)
    )
    return render(request, 'search.html', {"cars": search_results,
                                           "query": query})


class LoanedOrderByUserListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'client_orders.html'

    def get_queryset(self):
        return Order.objects.all()


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reiksmes is formos lauku
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password"]
        password2 = request.POST["password2"]
        # ar sutampa passwordai
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"User name {username} is busy")
                return redirect("register")
            else:
                # ar nera tokio pacio email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"Email adress {email} existing")
                    return redirect("register")
                else:
                    # taskas kai viskas tvarkoje  ir visi tikrinimai praeiti
                    User.objects.create_user(username=username, email=email, password=password1)
                    messages.info(request, f"User {username} was successfuly registred")
                    return redirect("login")
        else:
            messages.error(request, f"Passwords does not match")
            return redirect("register")
    return render(request, 'register.html')
