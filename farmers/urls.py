from django.urls import path
from . import views

urlpatterns = [
    path("", views.farmer_list, name="farmer_list"),
    path("add/", views.add_farmer, name="add_farmer"),
    path("summary/", views.summary, name="summary"),
    path('produce/', views.produce_list, name='produce_list'),
]
