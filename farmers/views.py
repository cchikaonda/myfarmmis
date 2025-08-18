from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Season, Farmer, InputCategory, FarmInput, Distribution,
    Produce, FarmerCrop, FarmerPayment
)
from .forms import FarmerForm, InputCategoryForm, FarmInputForm, DistributionForm
from collections import defaultdict
from decimal import Decimal
from django.db.models import Sum, F

# ------------------------
# Farmer Views
# ------------------------
def farmer_list(request):
    season_id = request.GET.get("season")
    season = Season.objects.filter(id=season_id).first() if season_id else None

    farmers = Farmer.objects.prefetch_related(
        'farmercrop_set__distribution_set',
        'farmercrop_set__crop'
    )

    farmer_data = []
    for farmer in farmers:
        billed_distributions = []
        not_billed_distributions = []

        for fc in farmer.farmercrop_set.all():
            distributions = fc.distribution_set.select_related('farm_input', 'farm_input__category', 'season')
            if season:
                distributions = distributions.filter(season=season)
            billed_distributions.extend([d for d in distributions if d.billed])
            not_billed_distributions.extend([d for d in distributions if not d.billed])

        farmer_data.append({
            'farmer': farmer,
            'billed_distributions': billed_distributions,
            'not_billed_distributions': not_billed_distributions,
        })

    return render(request, 'farmers/farmer_list.html', {
        'farmer_data': farmer_data,
        'selected_season': season
    })


def farmer_create(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farmer_list')
    else:
        form = FarmerForm()
    return render(request, 'farmers/farmer_form.html', {'form': form, 'title': 'Add Farmer'})


def farmer_update(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.method == 'POST':
        form = FarmerForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            return redirect('farmer_list')
    else:
        form = FarmerForm(instance=farmer)
    return render(request, 'farmers/farmer_form.html', {'form': form, 'title': 'Edit Farmer'})


def farmer_delete(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.method == 'POST':
        farmer.delete()
        return redirect('farmer_list')
    return render(request, 'farmers/farmer_confirm_delete.html', {'farmer': farmer})


# ------------------------
# Distribution Views
# ------------------------
def add_distribution(request):
    if request.method == "POST":
        form = DistributionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("distribution_list")
    else:
        form = DistributionForm()
    return render(request, "farmers/distribution_form.html", {"form": form})


def distribution_list(request):
    season_id = request.GET.get("season")
    season = Season.objects.filter(id=season_id).first() if season_id else None

    distributions = Distribution.objects.select_related(
        "farmer_crop", "farmer_crop__farmer", "farmer_crop__crop",
        "farm_input", "farm_input__category", "season"
    )
    if season:
        distributions = distributions.filter(season=season)

    return render(request, "farmers/distribution_list.html", {
        "distributions": distributions,
        "selected_season": season
    })


# ------------------------
# Summary Report
# ------------------------
def summary(request):
    season_id = request.GET.get("season")
    season = Season.objects.filter(id=season_id).first() if season_id else None

    farmers = Farmer.objects.all()
    distributions = Distribution.objects.select_related(
        "farmer_crop", "farmer_crop__farmer", "farmer_crop__crop",
        "farm_input", "farm_input__category", "season"
    )
    if season:
        distributions = distributions.filter(season=season)

    total_acres = FarmerCrop.objects.aggregate(total_acres=Sum("acres"))["total_acres"] or 0
    total_distributions = distributions.aggregate(
        total_quantity=Sum("quantity"),
        total_cost=Sum(F("quantity") * F("farm_input__market_cost"))
    )

    context = {
        "farmers": farmers,
        "distributions": distributions,
        "season": season,
        "total_acres": total_acres,
        "total_quantity": total_distributions["total_quantity"] or 0,
        "total_cost": total_distributions["total_cost"] or 0,
    }
    return render(request, "farmers/summary.html", context)


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

    context = {
        "farmer_totals": farmer_totals,
        "grand_totals": grand_totals,
        "special_crops": special_crops,
        "season": season
    }
    return render(request, "farmers/produce_list.html", context)


# ------------------------
# Farmer Payments View
# ------------------------
def farmer_payments(request):
    season_id = request.GET.get("season")
    season = Season.objects.filter(id=season_id).first() if season_id else None

    payments = []
    for farmer in Farmer.objects.all():
        total_kg = Decimal("0.0")
        farmer_crops = FarmerCrop.objects.filter(farmer=farmer)
        for fc in farmer_crops:
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

    context = {"season": season, "payments": payments}
    return render(request, "farmers/farmer_payments.html", context)
