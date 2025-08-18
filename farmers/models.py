from django.db import models

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class ItemCategory(models.Model):
    """Categories of support: Fertilizer, Seed, Food, Cash, Other"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    """Specific item under a category with market cost"""
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)  # Kg, Bag, MWK
    market_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.unit})"


class Crop(models.Model):
    """List of all crops for produce tracking"""
    name = models.CharField(max_length=50, unique=True)
    default_unit = models.CharField(
        max_length=10,
        choices=[
            ('KG', 'Kilogram'),
            ('BAG_50', '50 Kg Bag'),
            ('BAG_60', '60 Kg Bag')
        ],
        default='KG'
    )

    def __str__(self):
        return self.name


class FarmerCrop(models.Model):
    """Tracks which farmer grows which crop and on how many acres"""
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    acres = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('farmer', 'crop')

    def __str__(self):
        return f"{self.farmer.name} - {self.crop.name} ({self.acres} acres)"


class Produce(models.Model):
    """Track crop yield per farmer-crop combination"""
    farmer_crop = models.ForeignKey(FarmerCrop, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, help_text="Quantity in specified unit")
    unit = models.CharField(max_length=10, choices=Crop.default_unit.field.choices, default='KG')
    date_recorded = models.DateField(auto_now_add=True)

    def quantity_in_kg(self):
        """Convert quantity to kilograms."""
        if self.unit == 'KG':
            return self.quantity
        elif self.unit == 'BAG_50':
            return self.quantity * 50
        elif self.unit == 'BAG_60':
            return self.quantity * 60
        return self.quantity

    def __str__(self):
        return f"{self.farmer_crop.farmer.name} - {self.quantity} {self.unit} {self.farmer_crop.crop.name}"


class Distribution(models.Model):
    """Track inputs given to farmers, optionally per crop"""
    farmer_crop = models.ForeignKey(FarmerCrop, on_delete=models.CASCADE)
    input_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    date_distributed = models.DateField(auto_now_add=True)
    billed = models.BooleanField(default=False)

    def total_cost(self):
        return self.quantity * self.input_item.market_cost

    def __str__(self):
        return f"{self.farmer_crop.farmer.name} - {self.input_item.name} ({self.farmer_crop.crop.name})"
