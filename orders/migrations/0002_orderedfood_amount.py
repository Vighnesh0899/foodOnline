# Generated by Django 5.0.6 on 2024-07-24 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedfood',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
