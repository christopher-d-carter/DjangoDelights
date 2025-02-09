from django.db import models
from decimal import Decimal
import logging, sys

# create logger
logger = logging.getLogger(__name__)
# create handlers for log output to console and file
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("django_delights_inventory.log")
# set logging format
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s [%(message)s] [%(name)s: %(lineno)d]')
#info_fmt = logging.Formatter('[%(asctime)s] %(levelname)s [%(message)s]')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
# add handlers to logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
# set the logging level
logger.setLevel(logging.INFO)


# Ingredient Model
class Ingredient(models.Model):
    name = models.CharField(max_length=30, blank=True)
    # price per unit of measure
    unit_price = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('0.0')) 
    # unit of measure
    unit_measure = models.CharField(max_length=10, blank=True) 
    # quantity available per ingredient
    quantity = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('0.0')
    )

    def __str__(self):
        return self.name

    # Implement data constraints at the database level
    class Meta:
        constraints = [
            # Prevent unit prices less than or equal to zero
            models.CheckConstraint(
                check=models.Q(unit_price__gte=Decimal('0.0')),
                name='unit_price_gt_0'
            ),
            # Prevent quantity values less than zero
            models.CheckConstraint(
                check=models.Q(quantity__gte=Decimal('0.0')),
                name='ingredient_quantity_gte_0'
            )
        ]

# Menu Item Model
class MenuItem(models.Model):
    name = models.CharField(max_length=40, blank=True)
    # item price
    item_price = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('0.0'))
    
    def __str__(self):
        return self.name

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
class RecipeRequirement(models.Model):
    # connect associated models
    # MenuItem model
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    # Ingredient model required. 
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    # Quantity of an ingredient
    quantity = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('0.0'))
    
    def __str__(self):
        return str(self.menu_item)

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
    menu_item = models.ForeignKey(
        MenuItem, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # timestamp purchase
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.timestamp.strftime("%Y-%m-%d %H:%M "))\
            + self.menu_item.name + " $" + str(self.menu_item.item_price)
 
    @property
    def process_purchase(self):
        # Get recipe requirements for the requested menu item
        recipe = RecipeRequirement.objects.filter(menu_item_id=self.menu_item.pk)
        # if the menu item does not have a recipe, return false
        if not recipe.exists():
            logger.info('Menu Items require a recipe')
            return False
        # loop through the ingredients list
        # if there are not enough ingredients to make an item, return false
        for item in recipe:
            if item.quantity > Ingredient.objects.get(id=item.ingredient.pk).quantity:
                logger.info(self.menu_item.name + ': insufficient ingredient stock')
                return False
        # if there are enough ingredients to make a menu item,
        # deduct the quantity of all required ingredients from inventory       
        for item in recipe:
            # Get Ingredient Object from Ingredient database
            ingredient = Ingredient.objects.get(id=item.ingredient.pk)
            logger.debug(ingredient.name + " " + str(ingredient.quantity))

            # Update Ingredient Object quantity
            # using variables to shorten line length
            filter = Ingredient.objects.filter(pk=item.ingredient.pk)   
            filter.update(quantity = ingredient.quantity - item.quantity)
            # Get updated Ingredient Object for logging
            ingredient = Ingredient.objects.get(id=item.ingredient.pk)
            logger.debug(ingredient.name + " " + str(ingredient.quantity))
        
        logger.info('Purchase processed')
        return True