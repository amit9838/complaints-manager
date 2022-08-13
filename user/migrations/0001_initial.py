# Generated by Django 4.0.4 on 2022-08-12 08:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joinDate', models.DateField(auto_now=True)),
                ('expertise', models.CharField(max_length=32)),
                ('mob', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=512, null=True)),
                ('user', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, related_name='engineer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joinDate', models.DateField(auto_now=True)),
                ('mob', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=512, null=True)),
                ('user', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
