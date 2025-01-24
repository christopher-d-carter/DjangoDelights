from django.db import models
from decimal import Decimal

# Ingredient Model
class Ingredient(models.Model):
    ingredient = models.CharField(max_length=30)
    # price per unit of measure
    unit_price = models.DecimalField(max_digits=5, decimal_places=2) 
    unit = models.CharField(max_length=10) # unit of measure
    # quantity available per ingredient
    quantity = models.PositiveIntegerField(default=0)

    # Implement data constraints at the database level
    class Meta:
        constraints = [
            # Prevent unit prices less than or equal to zero
            models.CheckConstraint(
                check=models.Q(unit_price__gte=Decimal('0.01')),
                name='unit_price_gt_0'
            ),
            # Prevent quantity values less than zero
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name='ingredient_quantity_gte_0'
            )
        ]

# Menu Item Model
class MenuItem(models.Model):
    menu_item = models.CharField(max_length=40, blank=True)
    # item price
    item_price = models.DecimalField(max_digits=5, decimal_places=2)

    # Implement data constraints at the database level
    class Meta:
        constraints = [
            # Prevent item prices less than zero
            models.CheckConstraint(
                check=models.Q(item_price__gte=Decimal('0.0')),
                name='menu_item_price_gte_0'
            )
        ]

# Recipe Model
class RecipeRequirements(models.Model):
    # Quantity of an ingredient
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    # unit of measure
    unit = models.CharField(max_length=4)
    # connect associated models
    # MenuItem model
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    # Ingredient model required. 
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    # Implement data constraints at the database level
    class Meta:
        constraints = [
            # Prevent quantity values less than zero
            models.CheckConstraint(
                check=models.Q(quantity__gte=Decimal('0.0')),
                name='required_quantity_gte_0'
            )
        ]

# Purchase Model
class Purchase(models.Model):
    # connect to MenuItem model
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    # timestamp purchase
    timestamp = models.DateTimeField(auto_now=True)