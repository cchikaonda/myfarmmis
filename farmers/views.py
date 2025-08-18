from django.shortcuts import render, redirect
from .models import Farmer, ItemCategory, Item, Distribution, Produce
from .forms import FarmerForm, ItemCategoryForm, ItemForm, DistributionForm
from django.db.models import Sum, F

from django.shortcuts import render, redirect, get_object_or_404
from .models import Farmer, Distribution
from .forms import FarmerForm
from collections import defaultdict
from decimal import Decimal


def farmer_list(request):
    farmers = Farmer.objects.all()
    farmer_data = []

    total_billed_all = 0
    total_not_billed_all = 0

    for farmer in farmers:
        billed_items = farmer.distribution_set.filter(billed=True)
        not_billed_items = farmer.distribution_set.filter(billed=False)

        billed_total = sum([d.total_cost() for d in billed_items])
        not_billed_total = sum([d.total_cost() for d in not_billed_items])

        total_billed_all += billed_total
        total_not_billed_all += not_billed_total

        farmer_data.append({
            "farmer": farmer,
            "billed_items": billed_items,
            "not_billed_items": not_billed_items,
            "billed_total": billed_total,
            "not_billed_total": not_billed_total,
        })

    return render(request, "farmers/farmer_list.html", {
        "farmer_data": farmer_data,
        "total_billed_all": total_billed_all,
        "total_not_billed_all": total_not_billed_all,
    })

# Add a new farmer
def add_farmer(request):
    if request.method == "POST":
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("farmer_list")
    else:
        form = FarmerForm()
    return render(request, "farmers/farmer_form.html", {"form": form})

# Add a new distribution (seeds, fertilizer, food, cash)
def add_distribution(request):
    if request.method == "POST":
        form = DistributionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("distribution_list")
    else:
        form = DistributionForm()
    return render(request, "farmers/distribution_form.html", {"form": form})

# List all distributions
def distribution_list(request):
    distributions = Distribution.objects.select_related("farmer", "input_item", "input_item__category").all()
    return render(request, "farmers/distribution_list.html", {"distributions": distributions})

# Summary report
def summary(request):
    farmers = Farmer.objects.all()
    distributions = Distribution.objects.select_related("farmer", "input_item", "input_item__category").all()

    total_acres = farmers.aggregate(total_acres=Sum("acres"))["total_acres"] or 0
    total_distributions = distributions.aggregate(
        total_quantity=Sum("quantity"),
        total_cost=Sum(F("quantity") * F("input_item__market_cost"))
    )

    context = {
        "farmers": farmers,
        "distributions": distributions,
        "total_acres": total_acres,
        "total_quantity": total_distributions["total_quantity"] or 0,
        "total_cost": total_distributions["total_cost"] or 0,
    }
    return render(request, "farmers/summary.html", context)

def produce_list(request):
    """
    Display all end-of-season produce per farmer, grouped by crop,
    with unit conversions and grand totals.
    """
    produces = Produce.objects.select_related("farmer", "crop").all().order_by("farmer__name")

    farmer_totals = {}
    grand_totals = defaultdict(lambda: Decimal("0"))

    # Define special crops (treated differently in template)
    special_crops = ["Maize", "Groundnuts"]

    for produce in produces:
        farmer_id = produce.farmer.id
        crop_name = produce.crop.name
        kg = produce.quantity_in_kg()        # Decimal
        unit_display = produce.get_unit_display()

        # Initialize farmer entry
        if farmer_id not in farmer_totals:
            farmer_totals[farmer_id] = {
                "farmer": produce.farmer,
                "crop_totals": {}
            }

        # Initialize crop entry per farmer
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

        # Update grand totals
        grand_totals[crop_name] += kg

    context = {
        "farmer_totals": farmer_totals,
        "grand_totals": grand_totals,
        "special_crops": special_crops
    }
    return render(request, "farmers/produce_list.html", context)