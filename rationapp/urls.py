# ration_formulation/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_ration, name='create_ration'),
    path("feedtypes-for-animal/", views.feedtypes_for_animal, name="feedtypes_for_animal"),
    path('saved/', views.saved_rations, name='saved_rations'),
    path('ration/<int:ration_id>/', views.ration_detail, name='ration_detail'),

    path('poultry/', views.poultry_type_selection, name='poultry_type_selection'),
    #path('poultry/layers/', views.layers_ration_form, name='poultry_layers'),
    #path('poultry/broilers/', views.broilers_ration_form, name='poultry_broilers'),
    #path('poultry/breeders/', views.breeders_ration_form, name='poultry_breeders'),
]
