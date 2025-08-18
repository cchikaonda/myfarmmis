from django import forms
from .models import Farmer, ItemCategory, Item, FarmerCrop, Distribution, Produce, Crop

# Farmer form
class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['name', 'phone', 'village']


# ItemCategory form
class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = ['name', 'description']


# Item form
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name', 'unit', 'market_cost']


# FarmerCrop form (assign crop to farmer with acres)
class FarmerCropForm(forms.ModelForm):
    class Meta:
        model = FarmerCrop
        fields = ['farmer', 'crop', 'acres']


# Distribution form (inputs given to farmer per crop)
class DistributionForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = ['farmer_crop', 'input_item', 'quantity', 'billed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: order by farmer name in dropdown
        self.fields['farmer_crop'].queryset = FarmerCrop.objects.select_related('farmer', 'crop').all().order_by('farmer__name')


# Produce form (record yield per farmer-crop)
class ProduceForm(forms.ModelForm):
    class Meta:
        model = Produce
        fields = ['farmer_crop', 'quantity', 'unit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: order farmer_crop choices by farmer name
        self.fields['farmer_crop'].queryset = FarmerCrop.objects.select_related('farmer', 'crop').all().order_by('farmer__name')
