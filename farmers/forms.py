from django import forms
from .models import (
    Farmer,
    InputCategory,
    FarmInput,
    FarmerCrop,
    Distribution,
    Produce,
    Crop,
    Season,
    FarmerPayment
)

# Farmer form
class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = '__all__'


# Input Category form
class InputCategoryForm(forms.ModelForm):
    class Meta:
        model = InputCategory
        fields = '__all__'


# Farm Input form
class FarmInputForm(forms.ModelForm):
    class Meta:
        model = FarmInput
        fields = '__all__'


# Crop form
class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = '__all__'


# FarmerCrop form (linking farmer to crops)
class FarmerCropForm(forms.ModelForm):
    class Meta:
        model = FarmerCrop
        fields = '__all__'


# Distribution form
class DistributionForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = '__all__'


# Produce form
class ProduceForm(forms.ModelForm):
    class Meta:
        model = Produce
        fields = '__all__'


# Season form
class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = '__all__'


# Farmer Payment form
class FarmerPaymentForm(forms.ModelForm):
    class Meta:
        model = FarmerPayment
        fields = '__all__'
