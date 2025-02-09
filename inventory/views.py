from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import IngredientForm, MenuItemForm 
from .forms import RecipeRequirementForm, PurchaseForm



class IngredientView(ListView):
    model = Ingredient
    template_name = "r'^ingredients.html$"

class CreateIngredient(CreateView):
    model = Ingredient
    template_name = "r'^add_ingredient.html$"
    form_class = IngredientForm

class UpdateIngredient(UpdateView):
    model = Ingredient
    template_name = "r'^update_ingredient.html$"
    form_class = IngredientForm

class DeleteIngredient(DeleteView):
    model = Ingredient
    template_name = "r'^delete_ingredient.html$"
    form_class = IngredientForm

class MenuItemView(ListView):
    model = MenuItem
    template_name = "r'^menu.html$"

class CreateMenuItem(CreateView):
    model = MenuItem
    template_name = "r'^add_menu_item.html$"
    form_class = MenuItemForm

class UpdateMenuItem(UpdateView):
    model = MenuItem
    template_name = "r'^update_menu_item.html$"
    form_class = MenuItemForm

class DeleteMenuItem(DeleteView):
    model = MenuItem
    template_name = "r'^delete_menu_item.html$"
    form_class = MenuItemForm

class RecipeRequirementView(ListView):
    model = RecipeRequirement
    template_name = "r'^recipe_requirement"

class CreateRecipeRequirement(CreateView):
    model = RecipeRequirement
    template_name = "r'^add_recipe_requirement.html$"
    form_class = RecipeRequirementForm

class UpdateRecipeRequirement(UpdateView):
    model = RecipeRequirement
    template_name = "r'^update_recipe_requirement.html$"
    form_class = RecipeRequirementForm

class DeleteRecipeRequirement(DeleteView):
    model = RecipeRequirement
    template_name = "r'^delete_recipe_requirement.html$"
    form_class = RecipeRequirementForm

class PurchaseView(ListView):
    model = Purchase
    template_name = "r'^puchase.html$"

class CreatePurchase(CreateView):
    model = Purchase
    template_name = "r'^add_purchase$"
    form_class = PurchaseForm

class UpdatePurchase(UpdateView):
    model = Purchase
    template_name = "r'^update_purchase.html$"
    form_class = PurchaseForm

class DeletePurchase(DeleteView):
    model = Purchase
    template_name = "r'^delete_purchase.html$"
    form_class = PurchaseForm