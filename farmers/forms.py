from django import forms
from .models import Farmer, ItemCategory, Item, Distribution, Produce, Crop


class FarmerForm(forms.ModelForm):
    """Form for creating or updating farmers."""
    class Meta:
        model = Farmer
        fields = "__all__"


class ItemCategoryForm(forms.ModelForm):
    """Form for adding categories like Fertilizer, Seed, Food, Cash, Other."""
    class Meta:
        model = ItemCategory
        fields = "__all__"


class ItemForm(forms.ModelForm):
    """Form for specific items like NPK, Urea, Hybrid Seed, Maize Bags, etc."""
    class Meta:
        model = Item
        fields = "__all__"


class DistributionForm(forms.ModelForm):
    """Form to record distributions given to farmers (link farmer + item + qty + date + billed)."""
    class Meta:
        model = Distribution
        fields = "__all__"


class CropForm(forms.ModelForm):
    """Form to manage crops for produce tracking."""
    class Meta:
        model = Crop
        fields = "__all__"


class ProduceForm(forms.ModelForm):
    """Form to record end-of-season produce for each farmer."""
    class Meta:
        model = Produce
        fields = "__all__"
        widgets = {
            # Use the model field's choices instead of accessing a class attribute directly
            'unit': forms.Select(choices=Produce._meta.get_field('unit').choices),
        }
        help_texts = {
            'quantity': 'Enter quantity in the specified unit (e.g., Kg, 50 Kg Bag, 60 Kg Bag)',
        }
