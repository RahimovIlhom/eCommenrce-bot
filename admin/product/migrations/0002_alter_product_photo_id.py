# Generated by Django 5.0 on 2023-12-14 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
