# Generated by Django 3.2.16 on 2023-09-29 09:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('receipts', '0003_rename_ingredientreceipt_ingredientinreceipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='image',
            field=models.ImageField(blank=True, upload_to='recipes/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='cooking_time',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Время готовки не менее 1 минуты')], verbose_name='Время приготовления'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='receipts.receipt', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'ordering': ['-id'],
            },
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'receipt'), name='unique_user_receipt_favorite'),
        ),
    ]
