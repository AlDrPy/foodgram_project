# Generated by Django 3.2.16 on 2023-09-30 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0008_auto_20230930_1554'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientinreceipt',
            old_name='ingr_amount',
            new_name='amount',
        ),
    ]
