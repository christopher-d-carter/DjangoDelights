# Generated by Django 5.1.4 on 2025-01-26 10:59

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.CharField(blank=True, max_length=30)),
                ('unit_price', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=5)),
                ('unit_measure', models.CharField(blank=True, max_length=10)),
                ('quantity', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=5)),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('unit_price__gte', Decimal('0.0'))), name='unit_price_gt_0'), models.CheckConstraint(condition=models.Q(('quantity__gte', Decimal('0.0'))), name='ingredient_quantity_gte_0')],
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_item', models.CharField(blank=True, max_length=40)),
                ('item_price', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=5)),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('item_price__gte', Decimal('0.0'))), name='menu_item_price_gte_0')],
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('menu_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.menuitem')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=5)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.ingredient')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.menuitem')),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('quantity__gte', Decimal('0.0'))), name='required_quantity_gte_0')],
            },
        ),
    ]
