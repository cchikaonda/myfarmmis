from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus
from .models import Ingredient

def formulate_ration(nutrient_reqs, ingredient_ids=None, total_weight=50):
    """
    nutrient_reqs: dict with min protein, energy, etc.
    ingredient_ids: list of ingredient ids available to use
    total_weight: total kg of feed
    """
    ingredients = Ingredient.objects.filter(id__in=ingredient_ids) if ingredient_ids else Ingredient.objects.all()
    if not ingredients.exists():
        return {
            "status": "No Ingredients",
            "solution": {},
            "total_cost": 0,
            "details": "No ingredients available to formulate the ration."
        }

    prob = LpProblem("Ration_Optimization", LpMinimize)

    # Map ingredient names to objects
    ing_dict = {ing.name.replace(" ", "_"): ing for ing in ingredients}

    # Variables: kg of each ingredient
    x = {var_name: LpVariable(f"x_{var_name}", lowBound=0) for var_name in ing_dict}

    # Objective: minimize cost
    prob += lpSum([x[var_name] * ing_dict[var_name].cost_per_kg for var_name in x])

    # Constraint: total weight
    prob += lpSum([x[var_name] for var_name in x]) == total_weight

    # Nutrient constraints
    if nutrient_reqs.get("protein") is not None:
        prob += lpSum([x[var_name] * ing_dict[var_name].protein / 100 for var_name in x]) >= nutrient_reqs["protein"] * total_weight / 100
    if nutrient_reqs.get("energy") is not None:
        prob += lpSum([x[var_name] * ing_dict[var_name].energy for var_name in x]) >= nutrient_reqs["energy"] * total_weight
    if nutrient_reqs.get("calcium") is not None:
        prob += lpSum([x[var_name] * (ing_dict[var_name].calcium or 0) / 100 for var_name in x]) >= nutrient_reqs["calcium"] * total_weight / 100
    if nutrient_reqs.get("phosphorus") is not None:
        prob += lpSum([x[var_name] * (ing_dict[var_name].phosphorus or 0) / 100 for var_name in x]) >= nutrient_reqs["phosphorus"] * total_weight / 100
    if nutrient_reqs.get("lysine") is not None:
        prob += lpSum([x[var_name] * (ing_dict[var_name].lysine or 0) / 100 for var_name in x]) >= nutrient_reqs["lysine"] * total_weight / 100
    if nutrient_reqs.get("methionine") is not None:
        prob += lpSum([x[var_name] * (ing_dict[var_name].methionine or 0) / 100 for var_name in x]) >= nutrient_reqs["methionine"] * total_weight / 100
    if nutrient_reqs.get("fiber") is not None:
        prob += lpSum([x[var_name] * (ing_dict[var_name].fiber or 0) / 100 for var_name in x]) >= nutrient_reqs["fiber"] * total_weight / 100

    # Solve
    prob.solve()

    # Build solution using actual ingredient objects
    solution = {}
    for var_name, var in x.items():
        if var.varValue and var.varValue > 0:
            solution[ing_dict[var_name].name] = var.varValue

    total_cost = sum(var_value * ing_dict[name.replace(" ", "_")].cost_per_kg for name, var_value in solution.items())

    return {
        "status": LpStatus[prob.status],
        "solution": solution,
        "total_cost": total_cost
    }
