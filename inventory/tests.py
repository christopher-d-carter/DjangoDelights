from django.test import TestCase, Client
from django.db.utils import IntegrityError
from decimal import Decimal
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from datetime import datetime

class TestModels(TestCase):
    # hold a timestamp for purchase model test
    TIME = datetime.now()
    # Populate database before each test
    # Teardown is automatic in Django and isn't declared here
    def setUp(self):
        # populate Ingredient database model
        self.ingredient = Ingredient.objects.create(
            name='Flour',
            unit_price=Decimal('0.30'),
            unit_measure='ounces',
            quantity=Decimal('16.5')
        )
        # populate MenuItem database model
        self.menu_item = MenuItem.objects.create(
            name='Cake',
            item_price=Decimal('5.99')
        )
        # populate RecipeRequirement database model
        self.recipe = RecipeRequirement.objects.create(
            menu_item=self.menu_item,
            ingredient=self.ingredient,
            quantity=Decimal('2.2')
        )
        # populate Purchase database model
        self.purchase = Purchase.objects.create(
            menu_item=self.menu_item,
            timestamp=self.TIME
        )
    
    ''' Test the Ingredient Model '''
    # validate model fields
    def test_ingredient_mod_is_instance(self):
        self.assertIsInstance(self.ingredient, Ingredient)

    def test_ingredient_mod_name(self):
        self.assertEqual(str(self.ingredient), 'Flour')

    def test_ingredient_mod_price(self):
        self.assertEqual(self.ingredient.unit_price, Decimal('0.30'))

    def test_ingredient_mod_quantity(self):
        self.assertEqual(self.ingredient.quantity, Decimal('16.5'))

    # validate model constraints 
    def test_ingredient_price_constraint(self):
        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(
                name='Vanilla',
                unit_price=Decimal('-2.2'),
                unit_measure='ounces',
                quantity=Decimal('20')
            )

    def test_ingredient_quantity_constraint(self):
        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(
                name='Vanilla',
                unit_price=Decimal('3.3'),
                unit_measure='ounces',
                quantity=Decimal('-10.2')
            )            

    ''' Test the MenuItem Model '''
    # validate model fields
    def test_menu_item_is_instance(self):
        self.assertIsInstance(self.menu_item, MenuItem)

    def test_menu_item_mod_name(self):
        self.assertEqual(str(self.menu_item), 'Cake')

    def test_menu_item_price(self):
        self.assertEqual(self.menu_item.item_price, Decimal('5.99'))

    # validate model constraints
    def test_menu_item_price_constraint(self):
        with self.assertRaises(IntegrityError):
            MenuItem.objects.create(
                name='Cupcake',
                item_price=Decimal('-7.99')
            )

    ''' Test the RecipeRequirement Model '''
    # validate model fields
    def test_recipe_is_instance(self):
        self.assertIsInstance(self.recipe, RecipeRequirement)

    def test_recipe_mod_name(self):
        self.assertEqual(str(self.recipe), 'Cake')
    
    def test_recipe_mod_ingredient(self):
        self.assertEqual(self.recipe.ingredient.name, 'Flour')

    def test_recipe_ingredient_quantity(self):
        self.assertEqual(self.recipe.quantity, Decimal('2.2'))

    # validate model constraints
    def test_recipe_ingredient_quantity_constraint(self):
        with self.assertRaises(IntegrityError):
            RecipeRequirement.objects.create(
                menu_item=self.menu_item,
                ingredient=self.ingredient,
                quantity=Decimal('-5.2')
            )
    
    ''' Test the Purchase Model '''
    # validate model fields
    def test_purchase_is_instance(self):
        self.assertIsInstance(self.purchase, Purchase)

    def test_purchase_ret_str(self):
        self.assertEqual(str(self.purchase), self.TIME.strftime("%Y-%m-%d %H:%M ")\
            + "Cake $5.99")
    # test method of the Purchase model named process_purchase
    # menu items that are not related to a recipe are not processed    
    def test_process_purchase_constraint(self):
        self.recipe.delete()
        self.assertFalse(self.purchase.process_purchase)
    # a menu item cannot be purchased if ingredients aren't available in inventory
    def test_neg_purchase_inventory_check(self):
        self.recipe.quantity = Decimal('900')
        self.recipe.save(update_fields=['quantity'])
        self.assertFalse(self.purchase.process_purchase, )
    # test inventory check that confirms enough inventory stock is available
    def test_pos_purchase_inventory_check(self):
        self.assertTrue(self.purchase.process_purchase)

    