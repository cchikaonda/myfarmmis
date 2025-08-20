from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, F
from collections import defaultdict
from decimal import Decimal

from .models import (
    Season, Farmer, InputCategory, FarmInput, Distribution,
    Produce, FarmerCrop, FarmerPayment, Crop
)
from .forms import (
    SeasonForm, FarmerForm, InputCategoryForm, FarmInputForm,
    DistributionForm, CropForm, FarmerCropForm
)

# ------------------------
# Dashboard
# ------------------------
def dashboard(request):
    show_welcome = request.session.pop("show_welcome", False)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
    ]
    context = {
        "show_welcome": show_welcome,
        "farmer_count": Farmer.objects.count(),
        "input_count": FarmInput.objects.count(),
        "distribution_count": Distribution.objects.count(),
        "payment_count": FarmerPayment.objects.count(),
        "breadcrumbs": breadcrumbs,
    }
    return render(request, "dashboard.html", context)

# ------------------------
# Season Views
# ------------------------
def season_list(request):
    seasons = Season.objects.all().order_by('-year')
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': None, 'name': 'Seasons', 'icon': '📅'},
    ]
    return render(request, 'seasons/season_list.html', {'seasons': seasons, 'breadcrumbs': breadcrumbs})

def season_create(request):
    form = SeasonForm(request.POST or None)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'season_list', 'name': 'Seasons', 'icon': '📅'},
        {'url': None, 'name': 'Add Season', 'icon': '➕'},
    ]
    if form.is_valid():
        season = form.save()
        messages.success(request, f"Season '{season.year}' created successfully!")
        return redirect('season_list')
    return render(request, 'seasons/season_form.html', {'form': form, 'title': 'Add Season', 'breadcrumbs': breadcrumbs})

def season_update(request, pk):
    season = get_object_or_404(Season, pk=pk)
    form = SeasonForm(request.POST or None, instance=season)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'season_list', 'name': 'Seasons', 'icon': '📅'},
        {'url': None, 'name': 'Edit Season', 'icon': '✏️'},
    ]
    if form.is_valid():
        season = form.save()
        messages.success(request, f"Season '{season.year}' updated successfully!")
        return redirect('season_list')
    return render(request, 'seasons/season_form.html', {'form': form, 'title': 'Edit Season', 'breadcrumbs': breadcrumbs})

def season_delete(request, pk):
    season = get_object_or_404(Season, pk=pk)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'season_list', 'name': 'Seasons', 'icon': '📅'},
        {'url': None, 'name': 'Delete Season', 'icon': '🗑️'},
    ]
    if request.method == 'POST':
        season_year = season.year
        season.delete()
        messages.success(request, f"Season '{season_year}' deleted successfully!")
        return redirect('season_list')
    return render(request, 'seasons/season_confirm_delete.html', {'object': season, 'breadcrumbs': breadcrumbs})

# ------------------------
# Farmer Views
# ------------------------
def farmer_list(request):
    farmers = Farmer.objects.all().order_by('name')
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': None, 'name': 'Farmers', 'icon': '👨‍🌾'},
    ]
    return render(request, 'farmers/farmer_list.html', {'farmers': farmers, 'breadcrumbs': breadcrumbs})

def farmer_create(request):
    form = FarmerForm(request.POST or None)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'farmer_list', 'name': 'Farmers', 'icon': '👨‍🌾'},
        {'url': None, 'name': 'Add Farmer', 'icon': '➕'},
    ]
    if form.is_valid():
        farmer = form.save()
        messages.success(request, f"Farmer '{farmer.name}' created successfully!")
        return redirect('farmer_list')
    return render(request, 'farmers/farmer_form.html', {'form': form, 'title': 'Add Farmer', 'breadcrumbs': breadcrumbs})

def farmer_update(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    form = FarmerForm(request.POST or None, instance=farmer)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'farmer_list', 'name': 'Farmers', 'icon': '👨‍🌾'},
        {'url': None, 'name': 'Edit Farmer', 'icon': '✏️'},
    ]
    if form.is_valid():
        farmer = form.save()
        messages.success(request, f"Farmer '{farmer.name}' updated successfully!")
        return redirect('farmer_list')
    return render(request, 'farmers/farmer_form.html', {'form': form, 'title': 'Edit Farmer', 'breadcrumbs': breadcrumbs})

def farmer_delete(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'farmer_list', 'name': 'Farmers', 'icon': '👨‍🌾'},
        {'url': None, 'name': 'Delete Farmer', 'icon': '🗑️'},
    ]
    if request.method == 'POST':
        farmer_name = farmer.name
        farmer.delete()
        messages.success(request, f"Farmer '{farmer_name}' deleted successfully!")
        return redirect('farmer_list')
    return render(request, 'farmers/farmer_confirm_delete.html', {'object': farmer, 'breadcrumbs': breadcrumbs})

# ------------------------
# InputCategory Views
# ------------------------
def inputcategory_list(request):
    categories = InputCategory.objects.all()
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': None, 'name': 'Input Categories', 'icon': '🌱'},
    ]
    return render(request, 'inputcategory/inputcategory_list.html', {'categories': categories, 'breadcrumbs': breadcrumbs})

def inputcategory_create(request):
    form = InputCategoryForm(request.POST or None)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'inputcategory_list', 'name': 'Input Categories', 'icon': '🌱'},
        {'url': None, 'name': 'Add Input Category', 'icon': '➕'},
    ]
    if form.is_valid():
        category = form.save()
        messages.success(request, f"Input Category '{category.name}' created successfully!")
        return redirect('inputcategory_list')
    return render(request, 'inputcategory/form.html', {'form': form, 'title': 'Add Input Category', 'breadcrumbs': breadcrumbs})

def inputcategory_update(request, pk):
    category = get_object_or_404(InputCategory, pk=pk)
    form = InputCategoryForm(request.POST or None, instance=category)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'inputcategory_list', 'name': 'Input Categories', 'icon': '🌱'},
        {'url': None, 'name': 'Edit Input Category', 'icon': '✏️'},
    ]
    if form.is_valid():
        category = form.save()
        messages.success(request, f"Input Category '{category.name}' updated successfully!")
        return redirect('inputcategory_list')
    return render(request, 'inputcategory/form.html', {'form': form, 'title': 'Edit Input Category', 'breadcrumbs': breadcrumbs})

def inputcategory_delete(request, pk):
    category = get_object_or_404(InputCategory, pk=pk)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'inputcategory_list', 'name': 'Input Categories', 'icon': '🌱'},
        {'url': None, 'name': 'Delete Input Category', 'icon': '🗑️'},
    ]
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f"Input Category '{name}' deleted successfully!")
        return redirect('inputcategory_list')
    return render(request, 'inputcategory/confirm_delete.html', {'object': category, 'breadcrumbs': breadcrumbs})

# ------------------------
# FarmInput Views
# ------------------------
def farminput_list(request):
    inputs = FarmInput.objects.all()
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': None, 'name': 'Farm Inputs', 'icon': '🌱'},
    ]
    return render(request, 'farminput/farminput_list.html', {'inputs': inputs, 'breadcrumbs': breadcrumbs})

def farminput_create(request):
    form = FarmInputForm(request.POST or None)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'farminput_list', 'name': 'Farm Inputs', 'icon': '🌱'},
        {'url': None, 'name': 'Add Farm Input', 'icon': '➕'},
    ]
    if form.is_valid():
        input_obj = form.save()
        messages.success(request, f"Farm Input '{input_obj.name}' created successfully!")
        return redirect('farminput_list')
    return render(request, 'farminput/form.html', {'form': form, 'title': 'Add Farm Input', 'breadcrumbs': breadcrumbs})

def farminput_update(request, pk):
    input_obj = get_object_or_404(FarmInput, pk=pk)
    form = FarmInputForm(request.POST or None, instance=input_obj)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'farminput_list', 'name': 'Farm Inputs', 'icon': '🌱'},
        {'url': None, 'name': 'Edit Farm Input', 'icon': '✏️'},
    ]
    if form.is_valid():
        input_obj = form.save()
        messages.success(request, f"Farm Input '{input_obj.name}' updated successfully!")
        return redirect('farminput_list')
    return render(request, 'farminput/form.html', {'form': form, 'title': 'Edit Farm Input', 'breadcrumbs': breadcrumbs})

def farminput_delete(request, pk):
    input_obj = get_object_or_404(FarmInput, pk=pk)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'farminput_list', 'name': 'Farm Inputs', 'icon': '🌱'},
        {'url': None, 'name': 'Delete Farm Input', 'icon': '🗑️'},
    ]
    if request.method == 'POST':
        name = input_obj.name
        input_obj.delete()
        messages.success(request, f"Farm Input '{name}' deleted successfully!")
        return redirect('farminput_list')
    return render(request, 'farminput/confirm_delete.html', {'object': input_obj, 'breadcrumbs': breadcrumbs})

# ------------------------
# Crop Views
# ------------------------
def crop_list(request):
    crops = Crop.objects.all()
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': None, 'name': 'Crops', 'icon': '🌾'},
    ]
    return render(request, 'crop/crop_list.html', {'crops': crops, 'breadcrumbs': breadcrumbs})

def crop_create(request):
    form = CropForm(request.POST or None)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'crop_list', 'name': 'Crops', 'icon': '🌾'},
        {'url': None, 'name': 'Add Crop', 'icon': '➕'},
    ]
    if form.is_valid():
        crop = form.save()
        messages.success(request, f"Crop '{crop.name}' created successfully!")
        return redirect('crop_list')
    return render(request, 'crop/form.html', {'form': form, 'title': 'Add Crop', 'breadcrumbs': breadcrumbs})

def crop_update(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    form = CropForm(request.POST or None, instance=crop)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'crop_list', 'name': 'Crops', 'icon': '🌾'},
        {'url': None, 'name': 'Edit Crop', 'icon': '✏️'},
    ]
    if form.is_valid():
        crop = form.save()
        messages.success(request, f"Crop '{crop.name}' updated successfully!")
        return redirect('crop_list')
    return render(request, 'crop/form.html', {'form': form, 'title': 'Edit Crop', 'breadcrumbs': breadcrumbs})

def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'crop_list', 'name': 'Crops', 'icon': '🌾'},
        {'url': None, 'name': 'Delete Crop', 'icon': '🗑️'},
    ]
    if request.method == 'POST':
        name = crop.name
        crop.delete()
        messages.success(request, f"Crop '{name}' deleted successfully!")
        return redirect('crop_list')
    return render(request, 'crop/confirm_delete.html', {'object': crop, 'breadcrumbs': breadcrumbs})

# ------------------------
# FarmerCrop Views
# ------------------------
def farmercrop_list(request):
    farmer_crops = FarmerCrop.objects.select_related('farmer', 'crop').all()
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': None, 'name': 'Farmer Crops', 'icon': '👩‍🌾'},
    ]
    return render(request, 'farmercrop/farmercrop_list.html', {'farmer_crops': farmer_crops, 'breadcrumbs': breadcrumbs})

def farmercrop_create(request):
    form = FarmerCropForm(request.POST or None)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'farmercrop_list', 'name': 'Farmer Crops', 'icon': '👩‍🌾'},
        {'url': None, 'name': 'Add Farmer Crop', 'icon': '➕'},
    ]
    if form.is_valid():
        fc = form.save()
        messages.success(request, f"Farmer Crop '{fc.farmer.name} - {fc.crop.name}' created successfully!")
        return redirect('farmercrop_list')
    return render(request, 'farmercrop/form.html', {'form': form, 'title': 'Add Farmer Crop', 'breadcrumbs': breadcrumbs})

def farmercrop_update(request, pk):
    fc = get_object_or_404(FarmerCrop, pk=pk)
    form = FarmerCropForm(request.POST or None, instance=fc)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'farmercrop_list', 'name': 'Farmer Crops', 'icon': '👩‍🌾'},
        {'url': None, 'name': 'Edit Farmer Crop', 'icon': '✏️'},
    ]
    if form.is_valid():
        fc = form.save()
        messages.success(request, f"Farmer Crop '{fc.farmer.name} - {fc.crop.name}' updated successfully!")
        return redirect('farmercrop_list')
    return render(request, 'farmercrop/form.html', {'form': form, 'title': 'Edit Farmer Crop', 'breadcrumbs': breadcrumbs})

def farmercrop_delete(request, pk):
    fc = get_object_or_404(FarmerCrop, pk=pk)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'farmercrop_list', 'name': 'Farmer Crops', 'icon': '👩‍🌾'},
        {'url': None, 'name': 'Delete Farmer Crop', 'icon': '🗑️'},
    ]
    if request.method == 'POST':
        name = f"{fc.farmer.name} - {fc.crop.name}"
        fc.delete()
        messages.success(request, f"Farmer Crop '{name}' deleted successfully!")
        return redirect('farmercrop_list')
    return render(request, 'farmercrop/confirm_delete.html', {'object': fc, 'breadcrumbs': breadcrumbs})

# ------------------------
# Distribution Views
# ------------------------
def distribution_list(request):
    season_id = request.GET.get("season")
    season = Season.objects.filter(id=season_id).first() if season_id else None

    distributions = Distribution.objects.select_related(
        "farmer_crop", "farmer_crop__farmer", "farmer_crop__crop",
        "farm_input", "farm_input__category", "season"
    )
    if season:
        distributions = distributions.filter(season=season)

    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': None, 'name': 'Distributions', 'icon': '🚚'},
    ]
    return render(request, "farmers/distribution_list.html", {
        "distributions": distributions,
        "selected_season": season,
        "breadcrumbs": breadcrumbs,
    })

def add_distribution(request):
    form = DistributionForm(request.POST or None)
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': 'distribution_list', 'name': 'Distributions', 'icon': '🚚'},
        {'url': None, 'name': 'Add Distribution', 'icon': '➕'},
    ]
    if form.is_valid():
        dist = form.save()
        messages.success(request, f"Distribution for '{dist.farmer_crop}' added successfully!")
        return redirect('distribution_list')
    return render(request, "farmers/distribution_form.html", {"form": form, "breadcrumbs": breadcrumbs})

# ------------------------
# Produce Views
# ------------------------
def produce_list(request):
    season_id = request.GET.get("season")
    season = Season.objects.filter(id=season_id).first() if season_id else None

    produces = Produce.objects.select_related(
        "farmer_crop", "farmer_crop__farmer", "farmer_crop__crop", "season"
    )
    if season:
        produces = produces.filter(season=season)
    produces = produces.order_by("farmer_crop__farmer__name")

    farmer_totals = {}
    grand_totals = defaultdict(lambda: Decimal("0"))
    special_crops = ["Maize", "Groundnuts"]

    for produce in produces:
        farmer_id = produce.farmer_crop.farmer.id
        crop_name = produce.farmer_crop.crop.name
        kg = produce.quantity_in_kg()
        unit_display = produce.get_unit_display()

        if farmer_id not in farmer_totals:
            farmer_totals[farmer_id] = {"farmer": produce.farmer_crop.farmer, "crop_totals": {}}

        if crop_name not in farmer_totals[farmer_id]["crop_totals"]:
            farmer_totals[farmer_id]["crop_totals"][crop_name] = {
                "quantity": produce.quantity,
                "unit_display": unit_display,
                "total_kg": kg,
                "total_50kg": kg / Decimal("50"),
                "total_60kg": kg / Decimal("60"),
            }
        else:
            farmer_totals[farmer_id]["crop_totals"][crop_name]["quantity"] += produce.quantity
            farmer_totals[farmer_id]["crop_totals"][crop_name]["total_kg"] += kg
            farmer_totals[farmer_id]["crop_totals"][crop_name]["total_50kg"] += kg / Decimal("50")
            farmer_totals[farmer_id]["crop_totals"][crop_name]["total_60kg"] += kg / Decimal("60")

        grand_totals[crop_name] += kg

    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': None, 'name': 'Produce', 'icon': '📦'},
    ]

    context = {
        "farmer_totals": farmer_totals,
        "grand_totals": grand_totals,
        "special_crops": special_crops,
        "season": season,
        "breadcrumbs": breadcrumbs,
    }
    return render(request, "farmers/produce_list.html", context)

# ------------------------
# Farmer Payments
# ------------------------
def farmer_payments(request):
    season_id = request.GET.get("season")
    season = Season.objects.filter(id=season_id).first() if season_id else None

    payments = []
    for farmer in Farmer.objects.all():
        total_kg = Decimal("0.0")
        for fc in FarmerCrop.objects.filter(farmer=farmer):
            produces = Produce.objects.filter(farmer_crop=fc)
            if season:
                produces = produces.filter(season=season)
            for p in produces:
                total_kg += p.quantity_in_kg()

        price_per_kg = Decimal("500.00")
        total_value = total_kg * price_per_kg
        payments.append({
            "farmer": farmer,
            "total_kg": total_kg,
            "price_per_kg": price_per_kg,
            "total_value": total_value,
        })

    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': None, 'name': 'Payments', 'icon': '💰'},
    ]

    return render(request, "farmers/farmer_payments.html", {"season": season, "payments": payments, "breadcrumbs": breadcrumbs})
