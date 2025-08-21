from django.contrib import admin
from .models import (
    Animal, FeedType, Ingredient, FeedIngredient,
    RationFormulation, RationIngredient, UserAvailableIngredient
)

# -------------------------
# Animal
# -------------------------
@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

# -------------------------
# Feed Type
# -------------------------
class FeedIngredientInline(admin.TabularInline):
    model = FeedIngredient
    extra = 1
    autocomplete_fields = ("ingredient",)

@admin.register(FeedType)
class FeedTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "animal")
    list_filter = ("animal",)
    search_fields = ("name",)
    inlines = [FeedIngredientInline]

# -------------------------
# Ingredient
# -------------------------
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "cost_per_kg", "protein_content", "energy_content", "fiber_content")
    search_fields = ("name",)

    def protein_content(self, obj):
        return obj.protein
    protein_content.short_description = "Protein (%)"

    def energy_content(self, obj):
        return obj.energy
    energy_content.short_description = "Energy (Kcal/kg)"

    def fiber_content(self, obj):
        return obj.fiber
    fiber_content.short_description = "Fiber (%)"


# -------------------------
# Ration Formulation
# -------------------------
class RationIngredientInline(admin.TabularInline):
    model = RationIngredient
    extra = 1
    autocomplete_fields = ("ingredient",)

@admin.register(RationFormulation)
class RationFormulationAdmin(admin.ModelAdmin):
    list_display = ("animal", "feed_type", "total_weight", "total_cost", "created_at")
    list_filter = ("animal", "feed_type", "created_at")
    inlines = [RationIngredientInline]
    readonly_fields = ("created_at",)

# -------------------------
# User Available Ingredients
# -------------------------
@admin.register(UserAvailableIngredient)
class UserAvailableIngredientAdmin(admin.ModelAdmin):
    list_display = ("user", "ingredient", "available_weight")
    search_fields = ("user__username", "ingredient__name")
