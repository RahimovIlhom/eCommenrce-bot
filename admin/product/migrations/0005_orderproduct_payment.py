# Generated by Django 5.0 on 2024-01-04 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='payment',
            field=models.BooleanField(default=False),
        ),
    ]