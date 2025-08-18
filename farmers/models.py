from django.db import models
from decimal import Decimal

class Season(models.Model):
    year = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.year)


class Farmer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class InputCategory(models.Model):
    """Categories of support: Fertilizer, Seed, Food, Cash, Other"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class FarmInput(models.Model):
    """Specific input under a category with market cost"""
    category = models.ForeignKey(InputCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)  # Kg, Bag, MWK
    market_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.unit})"


class Crop(models.Model):
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
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    acres = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('farmer', 'crop')

    def __str__(self):
        return f"{self.farmer.name} - {self.crop.name} ({self.acres} acres)"


class Produce(models.Model):
    farmer_crop = models.ForeignKey(FarmerCrop, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=10, choices=Crop.default_unit.field.choices, default='KG')
    date_recorded = models.DateField(auto_now_add=True)

    def quantity_in_kg(self):
        if self.unit == 'KG':
            return self.quantity
        elif self.unit == 'BAG_50':
            return self.quantity * 50
        elif self.unit == 'BAG_60':
            return self.quantity * 60
        return self.quantity

    def __str__(self):
        return f"{self.farmer_crop.farmer.name} - {self.quantity} {self.unit} {self.farmer_crop.crop.name} ({self.season.year})"


class Distribution(models.Model):
    farmer_crop = models.ForeignKey(FarmerCrop, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    farm_input = models.ForeignKey(FarmInput, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    date_distributed = models.DateField(auto_now_add=True)
    billed = models.BooleanField(default=False)

    def total_cost(self):
        return self.quantity * self.farm_input.market_cost

    def __str__(self):
        return f"{self.farmer_crop.farmer.name} - {self.farm_input.name} ({self.farmer_crop.crop.name}) - {self.season.year}"


class FarmerLoan(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="loans")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="loans")
    amount_given = models.DecimalField(max_digits=12, decimal_places=2)
    date_given = models.DateField(auto_now_add=True)
    purpose = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Loan {self.amount_given} to {self.farmer} ({self.season})"


class LoanRepayment(models.Model):
    loan = models.ForeignKey(FarmerLoan, on_delete=models.CASCADE, related_name="repayments")
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Repayment {self.amount_paid} for {self.loan.farmer} ({self.loan.season})"

    @property
    def balance(self):
        total_repaid = sum(rep.amount_paid for rep in self.loan.repayments.all())
        return self.loan.amount_given - total_repaid

class FarmerPayment(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    total_kg = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('500.00'))
    total_value = models.DecimalField(max_digits=14, decimal_places=2)
    date_generated = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('farmer', 'season')

    def save(self, *args, **kwargs):
        if not self.total_value:
            self.total_value = self.total_kg * self.price_per_kg
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.farmer.name} - {self.season.year} - MK {self.total_value:.2f}"
