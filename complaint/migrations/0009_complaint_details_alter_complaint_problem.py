# Generated by Django 4.1.7 on 2023-02-24 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0008_item_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='details',
            field=models.CharField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='problem',
            field=models.CharField(blank=True, max_length=5000),
        ),
    ]
