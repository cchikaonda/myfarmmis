from django.contrib import admin
from .models import Farmer, ItemCategory, Item, Distribution, Produce, Crop


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ("name", "village", "acres", "registration_date")
    search_fields = ("name", "village")
    list_filter = ("village", "registration_date")


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "unit", "market_cost")
    search_fields = ("name",)
    list_filter = ("category",)


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ("farmer", "input_item", "quantity", "date_distributed", "billed", "total_cost_display")
    search_fields = ("farmer__name", "input_item__name")
    list_filter = ("date_distributed", "input_item__category", "billed")

    def total_cost_display(self, obj):
        """Show total cost for this distribution"""
        return f"MK {obj.total_cost():,.2f}"
    total_cost_display.short_description = "Total Cost"


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ("name", "default_unit")
    search_fields = ("name",)


@admin.register(Produce)
class ProduceAdmin(admin.ModelAdmin):
    list_display = ("farmer", "crop", "quantity", "unit", "quantity_in_kg_display", "date_recorded")
    list_filter = ("crop", "unit", "date_recorded")
    search_fields = ("farmer__name",)

    def quantity_in_kg_display(self, obj):
        return f"{obj.quantity_in_kg():,.2f} Kg"
    quantity_in_kg_display.short_description = "Quantity (Kg)"
