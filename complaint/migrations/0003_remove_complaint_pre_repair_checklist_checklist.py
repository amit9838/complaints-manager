# Generated by Django 4.0.4 on 2022-08-17 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0002_alter_complaint_category_alter_complaint_model_no_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='pre_repair_checklist',
        ),
        migrations.CreateModel(
            name='CheckList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_list_key', models.CharField(max_length=255)),
                ('c_list_val', models.CharField(max_length=255)),
                ('complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complaint.complaint')),
            ],
        ),
    ]
