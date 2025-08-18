from django.urls import path
from . import views

urlpatterns = [
    path("", views.farmer_list, name="farmer_list"),
    path('farmers/', views.farmer_list, name='farmer_list'),
    path('farmers/add/', views.farmer_create, name='farmer_create'),
    path('farmers/<int:pk>/edit/', views.farmer_update, name='farmer_update'),
    path('farmers/<int:pk>/delete/', views.farmer_delete, name='farmer_delete'),
    path('distributions/add/', views.add_distribution, name='add_distribution'),
    # path('distributions/', views.distribution_list, name='distribution_list'),
    # path('distributions/<int:pk>/edit/', views.edit_distribution, name='edit_distribution'),
    # path('distributions/<int:pk>/delete/', views.delete_distribution, name='delete_distribution'),
    path('produce/', views.produce_list, name='produce_list'),
  #  path("add/", views.add_farmer, name="add_farmer"),
    path("summary/", views.summary, name="summary"),
]
