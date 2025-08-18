from django.shortcuts import render, redirect, get_object_or_404
from .models import Farmer, ItemCategory, Item, Distribution, Produce, FarmerCrop
from .forms import FarmerForm, ItemCategoryForm, ItemForm, DistributionForm
from collections import defaultdict
from decimal import Decimal
from django.db.models import Sum, F
from django.db.models import Prefetch

from django.shortcuts import render
from .models import Farmer

def farmer_list(request):
    farmers = Farmer.objects.prefetch_related(
        'farmercrop_set__distribution_set',
        'farmercrop_set__crop'
    )

    farmer_data = []

    for farmer in farmers:
        billed_distributions = []
        not_billed_distributions = []

        # Loop through each FarmerCrop
        for fc in farmer.farmercrop_set.all():
            distributions = fc.distribution_set.select_related('input_item', 'input_item__category')
            billed_distributions.extend([d for d in distributions if d.billed])
            not_billed_distributions.extend([d for d in distributions if not d.billed])

        farmer_data.append({
            'farmer': farmer,
            'billed_distributions': billed_distributions,
            'not_billed_distributions': not_billed_distributions,
        })

    return render(request, 'farmers/farmer_list.html', {'farmer_data': farmer_data})


# Create a new farmer
def farmer_create(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farmer_list')
    else:
        form = FarmerForm()
    return render(request, 'farmers/farmer_form.html', {'form': form, 'title': 'Add Farmer'})


# Update an existing farmer
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


# Delete a farmer
def farmer_delete(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.method == 'POST':
        farmer.delete()
        return redirect('farmer_list')
    return render(request, 'farmers/farmer_confirm_delete.html', {'farmer': farmer})



# Add a new distribution (per FarmerCrop)
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
    distributions = Distribution.objects.select_related(
        "farmer_crop", "farmer_crop__farmer", "farmer_crop__crop", "input_item", "input_item__category"
    ).all()
    return render(request, "farmers/distribution_list.html", {"distributions": distributions})

# Summary report
def summary(request):
    farmers = Farmer.objects.all()
    distributions = Distribution.objects.select_related(
        "farmer_crop", "farmer_crop__farmer", "farmer_crop__crop", "input_item", "input_item__category"
    ).all()

    # Sum acres via FarmerCrop
    total_acres = FarmerCrop.objects.aggregate(total_acres=Sum("acres"))["total_acres"] or 0

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

# List all produce
def produce_list(request):
    """
    Display all end-of-season produce per farmer, grouped by crop,
    with unit conversions and grand totals.
    """
    produces = Produce.objects.select_related(
        "farmer_crop", "farmer_crop__farmer", "farmer_crop__crop"
    ).all().order_by("farmer_crop__farmer__name")

    farmer_totals = {}
    grand_totals = defaultdict(lambda: Decimal("0"))

    # Define special crops (treated differently in template)
    special_crops = ["Maize", "Groundnuts"]

    for produce in produces:
        farmer_id = produce.farmer_crop.farmer.id
        crop_name = produce.farmer_crop.crop.name
        kg = produce.quantity_in_kg()        # Decimal
        unit_display = produce.get_unit_display()

        # Initialize farmer entry
        if farmer_id not in farmer_totals:
            farmer_totals[farmer_id] = {
                "farmer": produce.farmer_crop.farmer,
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

