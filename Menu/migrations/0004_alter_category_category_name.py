# Generated by Django 5.0.6 on 2024-07-16 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Menu', '0003_alter_fooditem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=50),
        ),
    ]
