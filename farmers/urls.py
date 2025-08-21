from django.urls import path
from . import views

urlpatterns = [
    path("/", views.dashboard, name="dashboard"),
    path('farmers/', views.farmer_list, name='farmer_list'),
    path('farmers/add/', views.farmer_create, name='farmer_create'),
    path('farmers/<int:pk>/edit/', views.farmer_update, name='farmer_update'),
    path('farmers/<int:pk>/delete/', views.farmer_delete, name='farmer_delete'),
    path('seasons/', views.season_list, name='season_list'),
    path('seasons/add/', views.season_create, name='season_create'),
    path('seasons/<int:pk>/edit/', views.season_update, name='season_update'),
    path('seasons/<int:pk>/delete/', views.season_delete, name='season_delete'),
     # InputCategory
    path('categories/', views.inputcategory_list, name='inputcategory_list'),
    path('categories/add/', views.inputcategory_create, name='inputcategory_create'),
    path('categories/<int:pk>/edit/', views.inputcategory_update, name='inputcategory_update'),
    path('categories/<int:pk>/delete/', views.inputcategory_delete, name='inputcategory_delete'),

    # FarmInput
    path('inputs/', views.farminput_list, name='farminput_list'),
    path('inputs/add/', views.farminput_create, name='farminput_create'),
    path('inputs/<int:pk>/edit/', views.farminput_update, name='farminput_update'),
    path('inputs/<int:pk>/delete/', views.farminput_delete, name='farminput_delete'),

    # Crop
    path('crops/', views.crop_list, name='crop_list'),
    path('crops/add/', views.crop_create, name='crop_create'),
    path('crops/<int:pk>/edit/', views.crop_update, name='crop_update'),
    path('crops/<int:pk>/delete/', views.crop_delete, name='crop_delete'),

    # FarmerCrop
    path('farmer-crops/', views.farmercrop_list, name='farmercrop_list'),
    path('farmer-crops/add/', views.farmercrop_create, name='farmercrop_create'),
    path('farmer-crops/<int:pk>/edit/', views.farmercrop_update, name='farmercrop_update'),
    path('farmer-crops/<int:pk>/delete/', views.farmercrop_delete, name='farmercrop_delete'),

    path('distributions/add/', views.add_distribution, name='add_distribution'),
    
    # path('distributions/', views.distribution_list, name='distribution_list'),
    # path('distributions/<int:pk>/edit/', views.edit_distribution, name='edit_distribution'),
    # path('distributions/<int:pk>/delete/', views.delete_distribution, name='delete_distribution'),
    path('produce/', views.produce_list, name='produce_list'),
    path('produce/add/', views.produce_create, name='produce_add'),
    path('produce/<int:pk>/edit/', views.produce_edit, name='produce_edit'),
    path('produce/<int:pk>/delete/', views.produce_delete, name='produce_delete'),
    path('produce/<int:pk>/', views.produce_detail, name='produce_detail'),
    path('farmer-payments/<int:season_year>/', views.farmer_payments, name='farmer_payments'),
    # path("add/", views.add_farmer, name="add_farmer"),
    #path("summary/", views.summary, name="summary"),
]
