# forms.py
from django import forms
from .models import RationFormulation, Ingredient

class RationFormulationForm(forms.ModelForm):
    available_ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select available ingredients"
    )

    class Meta:
        model = RationFormulation
        fields = ['animal', 'feed_type', 'total_weight', 'available_ingredients']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark checkbox fields
        for name, field in self.fields.items():
            field.is_checkbox = isinstance(field.widget, forms.CheckboxSelectMultiple)
