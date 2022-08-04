# Generated by Django 4.0.4 on 2022-07-07 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0001_initial'),
        ('user', '0007_remove_employee_name_remove_engineer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='registred_complaints',
            field=models.ManyToManyField(blank=True, to='complaint.complaint'),
        ),
        migrations.AddField(
            model_name='engineer',
            name='assigend_complaints',
            field=models.ManyToManyField(blank=True, related_name='assigned_complaints', to='complaint.complaint'),
        ),
        migrations.AddField(
            model_name='engineer',
            name='complaints_resolved',
            field=models.ManyToManyField(blank=True, related_name='complaints_resolved', to='complaint.complaint'),
        ),
    ]
