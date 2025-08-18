from django.db import models

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    acres = models.DecimalField(max_digits=5, decimal_places=2)
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


class Distribution(models.Model):
    """Track what is given to farmers"""
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    input_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    date_distributed = models.DateField(auto_now_add=True)
    billed = models.BooleanField(default=False)

    def total_cost(self):
        return self.quantity * self.input_item.market_cost

    def __str__(self):
        return f"{self.farmer.name} - {self.input_item.name}"


class Crop(models.Model):
    """List of all crops for Produce tracking"""
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


class Produce(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
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
        return f"{self.farmer.name} - {self.quantity} {self.unit} {self.crop.name}"
