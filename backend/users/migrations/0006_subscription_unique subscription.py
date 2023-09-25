# Generated by Django 3.2.16 on 2023-09-24 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_customuser_subscription_list'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique subscription'),
        ),
    ]
