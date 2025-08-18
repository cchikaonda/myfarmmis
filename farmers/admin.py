from django.contrib import admin
from .models import (
    Season, Farmer, InputCategory, FarmInput, Crop,
    FarmerCrop, Produce, Distribution, FarmerPayment,
    FarmerLoan, LoanRepayment
)

# ------------------------
# Season Admin
# ------------------------
@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('year',)
    ordering = ('-year',)


# ------------------------
# Farmer Admin
# ------------------------
@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'village', 'registration_date')
    search_fields = ('name', 'village', 'phone')
    list_filter = ('registration_date',)


# ------------------------
# InputCategory Admin
# ------------------------
@admin.register(InputCategory)
class InputCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


# ------------------------
# FarmInput Admin
# ------------------------
@admin.register(FarmInput)
class FarmInputAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit', 'market_cost')
    list_filter = ('category', 'unit')
    search_fields = ('name',)


# ------------------------
# Crop Admin
# ------------------------
@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_unit')
    search_fields = ('name',)


# ------------------------
# FarmerCrop Admin
# ------------------------
@admin.register(FarmerCrop)
class FarmerCropAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'crop', 'acres')
    search_fields = ('farmer__name', 'crop__name')
    list_filter = ('crop',)


# ------------------------
# Produce Admin
# ------------------------
@admin.register(Produce)
class ProduceAdmin(admin.ModelAdmin):
    list_display = ('farmer_crop', 'season', 'quantity', 'unit', 'quantity_in_kg', 'date_recorded')
    search_fields = ('farmer_crop__farmer__name', 'farmer_crop__crop__name')
    list_filter = ('season', 'unit', 'date_recorded')


# ------------------------
# Distribution Admin
# ------------------------
@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('farmer_crop', 'season', 'farm_input', 'quantity', 'total_cost', 'billed', 'date_distributed')
    list_filter = ('season', 'farm_input__category', 'billed')
    search_fields = ('farmer_crop__farmer__name', 'farm_input__name')


# ------------------------
# FarmerLoan Admin
# ------------------------
@admin.register(FarmerLoan)
class FarmerLoanAdmin(admin.ModelAdmin):
    list_display = ("farmer", "season", "amount_given", "date_given")
    list_filter = ("season",)

# ------------------------
# LoanRepayment Admin
# ------------------------
@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ("loan", "amount_paid", "date_paid")
    list_filter = ("loan__season",)

# ------------------------
# FarmerPayment Admin
# ------------------------
@admin.register(FarmerPayment)
class FarmerPaymentAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'season', 'total_kg', 'price_per_kg', 'total_value', 'date_generated')
    list_filter = ('season',)
    search_fields = ('farmer__name',)
