from django.urls import path
from . import views

urlpatterns = [path("deliveries/", views.DeliveryTime.as_view({"get": "list"}))]
