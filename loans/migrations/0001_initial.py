# Generated by Django 5.1.3 on 2024-11-08 23:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_date', models.DateTimeField(auto_now_add=True)),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('equipment', models.ManyToManyField(to='equipment.equipment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
