# Generated by Django 4.1.3 on 2023-02-10 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0007_alter_complaintotp_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='tax',
            field=models.FloatField(default=0),
        ),
    ]
