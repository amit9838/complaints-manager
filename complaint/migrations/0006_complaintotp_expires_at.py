# Generated by Django 4.1.3 on 2023-02-07 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0005_complaintotp'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaintotp',
            name='expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
