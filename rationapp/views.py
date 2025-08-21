from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RationFormulationForm
from .models import Animal, FeedType, Ingredient, RationFormulation, RationIngredient
from .utils import formulate_ration
from django.http import JsonResponse

@login_required
def list_animals(request):
    animals = Animal.objects.all()
    return render(request, "ration/animal_list.html", {"animals": animals})


# views.py
from django.shortcuts import render

from django.shortcuts import render

def poultry_type_selection(request):
    """
    View to display the three poultry types: Layers, Broilers, Breeders,
    with breadcrumb navigation including icons.
    """
    poultry_types = [
        {
            "name": "Layers",
            "icon": "🐔",
            "description": "For egg production",
            "url_name": "poultry_layers",
            "btn_class": "btn-primary",
        },
        {
            "name": "Broilers",
            "icon": "🍗",
            "description": "For meat production",
            "url_name": "poultry_broilers",
            "btn_class": "btn-success",
        },
        {
            "name": "Breeders",
            "icon": "🪶",
            "description": "For reproduction & fertility",
            "url_name": "poultry_breeders",
            "btn_class": "btn-warning",
        },
    ]

    # Breadcrumbs with icons
    breadcrumbs = [
        {'url': 'dashboard', 'name': 'Dashboard', 'icon': '🏠'},
        {'url': None, 'name': 'Poultry Rations', 'icon': '🐓'},
    ]

    context = {
        "poultry_types": poultry_types,
        "breadcrumbs": breadcrumbs,
    }
    return render(request, "poultry/poultry_type.html", context)



@login_required
def create_ration(request):
    initial = {}
    animal_param = request.GET.get("animal")
    if animal_param:
        try:
            initial["animal"] = int(animal_param)  # preselect animal if passed in GET
        except ValueError:
            pass

    if request.method == "POST":
        form = RationFormulationForm(request.POST)  # <-- remove animal_type_id!
        if form.is_valid():
            total_weight = form.cleaned_data["total_weight"]
            ingredient_ids = [i.id for i in form.cleaned_data.get("available_ingredients")] if form.cleaned_data.get("available_ingredients") else None

            # LP solver
            lp_result = formulate_ration(
                nutrient_reqs={
                    "protein": form.cleaned_data.get("protein_req"),
                    "energy": form.cleaned_data.get("energy_req"),
                    "calcium": form.cleaned_data.get("calcium_req"),
                    "phosphorus": form.cleaned_data.get("phosphorus_req"),
                    "fiber": form.cleaned_data.get("fiber_req"),
                    "lysine": form.cleaned_data.get("lysine_req"),
                    "methionine": form.cleaned_data.get("methionine_req"),
                },
                ingredient_ids=ingredient_ids,
                total_weight=total_weight
            )

            if lp_result["status"] == "Optimal":
                ration = RationFormulation.objects.create(
                    user=request.user,
                    animal=form.cleaned_data["animal"],   # correct field
                    feed_type=form.cleaned_data["feed_type"],
                    total_weight=total_weight,
                    total_cost=lp_result["total_cost"],
                )

                for ing_name, kg in lp_result["solution"].items():
                    if kg > 0:
                        ing = Ingredient.objects.get(name=ing_name)
                        RationIngredient.objects.create(
                            formulation=ration,
                            ingredient=ing,
                            amount_kg=kg
                        )

                messages.success(request, "Ration formulated and saved successfully.")
                return redirect("ration_detail", ration_id=ration.id)
            else:
                messages.error(request, f"Formulation failed: {lp_result.get('details')}")

    else:
        form = RationFormulationForm(initial=initial)  # <-- also remove animal_type_id

    return render(request, "create_ration.html", {"form": form})

@login_required
def feedtypes_for_animal(request):
    animal_id = request.GET.get("animal_id")
    if animal_id:
        feedtypes = FeedType.objects.filter(animal_id=animal_id).values("id", "name")
        feedtypes_list = list(feedtypes)
    else:
        feedtypes_list = []

    return JsonResponse(feedtypes_list, safe=False)


@login_required
def ration_detail(request, ration_id):
    # Get the ration
    ration = get_object_or_404(RationFormulation, id=ration_id, user=request.user)
    
    # Fetch all related RationIngredient objects
    ingredients = ration.ingredients.select_related("ingredient").all()

    # Compute solution list for display (ingredient name + kg)
    solution_list = [(ri.ingredient.name, ri.amount_kg) for ri in ingredients]

    # Compute total nutrients per kg of ration
    total_weight = sum(ri.amount_kg for ri in ingredients) or ration.total_weight
    total_nutrients = {
        "protein": sum(ri.amount_kg * ri.ingredient.protein / total_weight for ri in ingredients),
        "energy": sum(ri.amount_kg * ri.ingredient.energy / total_weight for ri in ingredients),
        "calcium": sum(ri.amount_kg * (ri.ingredient.calcium or 0) / total_weight for ri in ingredients),
        "phosphorus": sum(ri.amount_kg * (ri.ingredient.phosphorus or 0) / total_weight for ri in ingredients),
        "fiber": sum(ri.amount_kg * (ri.ingredient.fiber or 0) / total_weight for ri in ingredients),
        "lysine": sum(ri.amount_kg * (ri.ingredient.lysine or 0) / total_weight for ri in ingredients),
        "methionine": sum(ri.amount_kg * (ri.ingredient.methionine or 0) / total_weight for ri in ingredients),
    }

    total_nutrients_list = [(k, v) for k, v in total_nutrients.items()]

    return render(request, "ration_detail.html", {
        "ration": ration,
        "ingredients": ingredients,
        "solution_list": solution_list,
        "total_nutrients_list": total_nutrients_list,
    })


@login_required
def saved_rations(request):
    rations = RationFormulation.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "saved_rations.html", {"rations": rations})
