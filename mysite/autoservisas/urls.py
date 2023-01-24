from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('car/', views.cars, name='car'),
    path('car/<int:car_id>', views.car, name='car-detail'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('search/', views.search, name='search'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("myorders/", views.LoanedOrderByUserListView.as_view(), name="my-ordered")
]
