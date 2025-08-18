from django.contrib import admin
from .models import (
    Farmer, ItemCategory, Item, Crop,
    FarmerCrop, Produce, Distribution
)


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'village', 'registration_date')
    search_fields = ('name', 'village', 'phone')
    list_filter = ('village',)


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit', 'market_cost')
    search_fields = ('name',)
    list_filter = ('category',)


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_unit')
    search_fields = ('name',)
    list_filter = ('default_unit',)


@admin.register(FarmerCrop)
class FarmerCropAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'crop', 'acres')
    search_fields = ('farmer__name', 'crop__name')
    list_filter = ('crop', 'farmer')


@admin.register(Produce)
class ProduceAdmin(admin.ModelAdmin):
    list_display = ('farmer_crop', 'quantity', 'unit', 'date_recorded', 'quantity_in_kg')
    search_fields = ('farmer_crop__farmer__name', 'farmer_crop__crop__name')
    list_filter = ('unit', 'date_recorded')


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('farmer_crop', 'input_item', 'quantity', 'total_cost', 'date_distributed', 'billed')
    search_fields = ('farmer_crop__farmer__name', 'input_item__name', 'farmer_crop__crop__name')
    list_filter = ('billed', 'date_distributed', 'input_item__category')
