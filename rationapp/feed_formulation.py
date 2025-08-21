# rationapp/utils/feed_formulation.py
import pulp
from .models import Ingredient

KCAL_PER_MJ = 239.005736

def formulate_ration(
    nutrient_reqs,
    ingredient_ids=None,
    total_weight=50.0,
    debug=False,
):
    """
    Least-cost formulation.

    nutrient_reqs: dict may contain:
        - protein_min (percent)
        - protein_max (percent)
        - energy_kcal_min (kcal/kg) or energy_mj_min (MJ/kg)
        - calcium_min (percent)
        - phosphorus_min (percent)
        - fiber_max (percent)
        - lysine_min (percent)
        - methionine_min (percent)

    ingredient_ids: iterable of Ingredient.id to restrict search (or None -> all)
    total_weight: kg of final mix

    Returns dict: status, solution (pct), solution_scaled (kg), total_cost, total_nutrients, debug
    """
    qs = Ingredient.objects.all()
    if ingredient_ids:
        qs = qs.filter(pk__in=ingredient_ids)

    ingredients = list(qs)
    if not ingredients:
        return {"status": "Error", "details": "No ingredients available."}

    prob = pulp.LpProblem("LeastCostFeed", pulp.LpMinimize)

    # Variables: kg of each ingredient
    x = {ing.id: pulp.LpVariable(f"x_{ing.id}", lowBound=0) for ing in ingredients}

    # Objective: minimize total cost (cost_per_kg * kg)
    prob += pulp.lpSum([x[ing.id] * ing.cost_per_kg for ing in ingredients]), "TotalCost"

    # Total weight equality
    prob += pulp.lpSum([x[ing.id] for ing in ingredients]) == total_weight, "TotalWeight"

    # Inclusion min/max (percent of final mix -> kg)
    for ing in ingredients:
        min_pct = ing.min_inclusion or 0.0
        max_pct = ing.max_inclusion if (ing.max_inclusion is not None) else 100.0
        min_kg = (min_pct / 100.0) * total_weight
        max_kg = (max_pct / 100.0) * total_weight
        if min_kg > 0:
            prob += x[ing.id] >= min_kg, f"min_incl_{ing.id}"
        prob += x[ing.id] <= max_kg, f"max_incl_{ing.id}"

    def nug(ing, attr):
        v = getattr(ing, attr, None)
        return float(v) if v not in (None, "") else 0.0

    # Protein constraints
    protein_min = nutrient_reqs.get("protein_min")
    protein_max = nutrient_reqs.get("protein_max")
    if protein_min is not None:
        prob += (
            pulp.lpSum([x[ing.id] * (nug(ing, "protein") / 100.0) for ing in ingredients])
            >= (protein_min / 100.0) * total_weight,
            "ProteinMin",
        )
    if protein_max is not None:
        prob += (
            pulp.lpSum([x[ing.id] * (nug(ing, "protein") / 100.0) for ing in ingredients])
            <= (protein_max / 100.0) * total_weight,
            "ProteinMax",
        )

    # Energy
    energy_kcal_min = nutrient_reqs.get("energy_kcal_min")
    energy_mj_min = nutrient_reqs.get("energy_mj_min")
    if energy_mj_min is not None and energy_kcal_min is None:
        energy_kcal_min = energy_mj_min * KCAL_PER_MJ
    if energy_kcal_min is not None:
        prob += (
            pulp.lpSum([x[ing.id] * nug(ing, "energy") for ing in ingredients])
            >= energy_kcal_min * total_weight,
            "EnergyMin",
        )

    # Calcium
    calcium_min = nutrient_reqs.get("calcium_min")
    if calcium_min is not None:
        prob += (
            pulp.lpSum([x[ing.id] * (nug(ing, "calcium") / 100.0) for ing in ingredients])
            >= (calcium_min / 100.0) * total_weight,
            "CalciumMin",
        )

    # Phosphorus
    phosphorus_min = nutrient_reqs.get("phosphorus_min")
    if phosphorus_min is not None:
        prob += (
            pulp.lpSum([x[ing.id] * (nug(ing, "phosphorus") / 100.0) for ing in ingredients])
            >= (phosphorus_min / 100.0) * total_weight,
            "PhosphorusMin",
        )

    # Fiber upper bound
    fiber_max = nutrient_reqs.get("fiber_max")
    if fiber_max is not None:
        prob += (
            pulp.lpSum([x[ing.id] * (nug(ing, "fiber") / 100.0) for ing in ingredients])
            <= (fiber_max / 100.0) * total_weight,
            "FiberMax",
        )

    # Lysine
    lysine_min = nutrient_reqs.get("lysine_min")
    if lysine_min is not None:
        prob += (
            pulp.lpSum([x[ing.id] * (nug(ing, "lysine") / 100.0) for ing in ingredients])
            >= (lysine_min / 100.0) * total_weight,
            "LysineMin",
        )

    # Methionine
    methionine_min = nutrient_reqs.get("methionine_min")
    if methionine_min is not None:
        prob += (
            pulp.lpSum([x[ing.id] * (nug(ing, "methionine") / 100.0) for ing in ingredients])
            >= (methionine_min / 100.0) * total_weight,
            "MethionineMin",
        )

    # Solve
    solver = pulp.PULP_CBC_CMD(msg=1 if debug else 0)
    prob.solve(solver)

    status_text = pulp.LpStatus[prob.status]

    if status_text != "Optimal":
        return {"status": status_text, "details": "Solver did not find an optimal solution."}

    # Build solution
    solution_kg = {}
    solution_pct = {}
    for ing in ingredients:
        val = pulp.value(x[ing.id]) or 0.0
        solution_kg[ing.name] = round(val, 4)
        solution_pct[ing.name] = round((val / total_weight) * 100.0 if total_weight > 0 else 0.0, 4)

    total_cost = sum(solution_kg[ing.name] * ing.cost_per_kg for ing in ingredients)

    # Total nutrients (percent of diet and absolute g)
    total_nutrients = {}
    total_protein_g = sum(solution_kg[ing.name] * (nug(ing, "protein") / 100.0) * 1000.0 for ing in ingredients)
    protein_pct = (total_protein_g / (total_weight * 1000.0)) * 100.0 if total_weight > 0 else 0.0
    total_energy_kcal = sum(solution_kg[ing.name] * nug(ing, "energy") for ing in ingredients)

    total_nutrients["protein_pct"] = round(protein_pct, 4)
    total_nutrients["protein_g"] = round(total_protein_g, 2)
    total_nutrients["energy_kcal_per_kg"] = round(total_energy_kcal / total_weight if total_weight > 0 else 0.0, 2)

    for attr in ("calcium", "phosphorus", "fiber", "lysine", "methionine"):
        total = sum(solution_kg[ing.name] * (nug(ing, attr) / 100.0) for ing in ingredients)
        pct = (total / total_weight) * 100.0 if total_weight > 0 else 0.0
        total_nutrients[f"{attr}_pct"] = round(pct, 4)
        total_nutrients[f"{attr}_g"] = round(total * 1000.0, 2)

    result = {
        "status": "Optimal",
        "solution": solution_pct,
        "solution_scaled": solution_kg,
        "total_cost": round(total_cost, 2),
        "total_nutrients": total_nutrients,
    }
    if debug:
        result["debug"] = {"ingredients": [ing.name for ing in ingredients], "pulp_status": status_text}
    return result
