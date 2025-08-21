from django.db import models
from django.contrib.auth.models import User

# -------------------------
# Animal
# -------------------------
class Animal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# -------------------------
# Feed Type
# -------------------------
class FeedType(models.Model):
    name = models.CharField(max_length=100)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="feed_types")

    def __str__(self):
        return f"{self.name} ({self.animal.name})"

# -------------------------
# Ingredient
# -------------------------
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    cost_per_kg = models.FloatField()

    # Nutrients per kg
    protein = models.FloatField(help_text="Crude protein (%)")
    energy = models.FloatField(help_text="Energy (Kcal/kg)")
    calcium = models.FloatField(null=True, blank=True)
    phosphorus = models.FloatField(null=True, blank=True)
    fiber = models.FloatField(null=True, blank=True)
    lysine = models.FloatField(null=True, blank=True)
    methionine = models.FloatField(null=True, blank=True)

    min_inclusion = models.FloatField(default=0, help_text="Minimum inclusion rate (%)")
    max_inclusion = models.FloatField(default=100, help_text="Maximum inclusion rate (%)")

    def __str__(self):
        return self.name

# -------------------------
# Feed Ingredients
# -------------------------
class FeedIngredient(models.Model):
    feed_type = models.ForeignKey(FeedType, on_delete=models.CASCADE, related_name="ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    inclusion_rate = models.FloatField(help_text="Default inclusion rate (%)")

    def __str__(self):
        return f"{self.ingredient.name} in {self.feed_type.name}"

# -------------------------
# Ration Formulation
# -------------------------
class RationFormulation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    feed_type = models.ForeignKey(FeedType, on_delete=models.CASCADE)
    total_weight = models.FloatField(help_text="Total feed (Kg)")
    total_cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal.name} - {self.feed_type.name} ({self.total_weight} Kg)"

# -------------------------
# Ration Ingredients
# -------------------------
class RationIngredient(models.Model):
    formulation = models.ForeignKey(RationFormulation, on_delete=models.CASCADE, related_name="ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount_kg = models.FloatField()

    def __str__(self):
        return f"{self.ingredient.name} - {self.amount_kg} Kg"

# -------------------------
# User Available Ingredients
# -------------------------
class UserAvailableIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    available_weight = models.FloatField(help_text="Available weight (Kg)")

    def __str__(self):
        return f"{self.user.username} - {self.ingredient.name}"
