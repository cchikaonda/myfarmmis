from django.db import migrations

def populate_initial_data(apps, schema_editor):
    Animal = apps.get_model("rationapp", "Animal")
    Ingredient = apps.get_model("rationapp", "Ingredient")

    # Prepopulate Animals
    animals = [
        ("Dairy Cattle", "Cows kept for milk production"),
        ("Beef Cattle", "Cows kept for beef production"),
        ("Goats", "Goats for milk or meat"),
        ("Sheep", "Wool and meat sheep"),
        ("Poultry - Layers", "Egg-producing chickens"),
        ("Poultry - Broilers", "Meat-producing chickens"),
        ("Pigs", "Swine for pork production"),
    ]
    for name, desc in animals:
        Animal.objects.get_or_create(name=name, defaults={"description": desc})

    # Prepopulate Ingredients (example values)
    ingredients = [
        {
            "name": "Maize Bran",
            "cost_per_kg": 0.20,
            "protein": 7.0,
            "energy": 11.5,
            "calcium": 0.02,
            "phosphorus": 0.8,
            "fiber": 10.0,
            "lysine": 0.2,
            "methionine": 0.05,
            "min_inclusion": 0,
            "max_inclusion": 60,
        },
        {
            "name": "Soybean Meal",
            "cost_per_kg": 0.60,
            "protein": 44.0,
            "energy": 12.5,
            "calcium": 0.25,
            "phosphorus": 0.65,
            "fiber": 7.0,
            "lysine": 2.8,
            "methionine": 0.65,
            "min_inclusion": 0,
            "max_inclusion": 30,
        },
        {
            "name": "Groundnut Cake",
            "cost_per_kg": 0.45,
            "protein": 40.0,
            "energy": 12.0,
            "calcium": 0.2,
            "phosphorus": 0.6,
            "fiber": 8.0,
            "lysine": 1.5,
            "methionine": 0.3,
            "min_inclusion": 0,
            "max_inclusion": 25,
        },
        {
            "name": "Molasses",
            "cost_per_kg": 0.15,
            "protein": 4.0,
            "energy": 12.5,
            "calcium": 0.9,
            "phosphorus": 0.1,
            "fiber": 0.0,
            "lysine": 0.0,
            "methionine": 0.0,
            "min_inclusion": 0,
            "max_inclusion": 20,
        },
        {
            "name": "Lucerne (Alfalfa Hay)",
            "cost_per_kg": 0.30,
            "protein": 20.0,
            "energy": 10.0,
            "calcium": 1.2,
            "phosphorus": 0.25,
            "fiber": 40.0,
            "lysine": 0.7,
            "methionine": 0.15,
            "min_inclusion": 0,
            "max_inclusion": 40,
        },
        {
            "name": "Urea",
            "cost_per_kg": 0.25,
            "protein": 281.0,
            "energy": 0.0,
            "calcium": 0.0,
            "phosphorus": 0.0,
            "fiber": 0.0,
            "lysine": 0.0,
            "methionine": 0.0,
            "min_inclusion": 0,
            "max_inclusion": 1,
        },
        {
            "name": "Mineral Premix",
            "cost_per_kg": 1.0,
            "protein": 0.0,
            "energy": 0.0,
            "calcium": 20.0,
            "phosphorus": 10.0,
            "fiber": 0.0,
            "lysine": 0.0,
            "methionine": 0.0,
            "min_inclusion": 0,
            "max_inclusion": 5,
        },
    ]

    for ing in ingredients:
        Ingredient.objects.get_or_create(name=ing["name"], defaults=ing)


def reverse_func(apps, schema_editor):
    Animal = apps.get_model("rationapp", "Animal")
    Ingredient = apps.get_model("rationapp", "Ingredient")
    Animal.objects.all().delete()
    Ingredient.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("rationapp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_initial_data, reverse_func),
    ]
