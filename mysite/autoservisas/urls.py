from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car/', views.cars, name='car'),
    path('car/<int:car_id>', views.car, name='car-detail'),
    path('orders/', views.OrderListView.as_view(), name='orders')
]
