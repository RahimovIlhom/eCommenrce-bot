# Generated by Django 5.0 on 2023-12-14 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_photo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.BooleanField(default=False),
        ),
    ]
