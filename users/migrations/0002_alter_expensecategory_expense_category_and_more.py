# Generated by Django 5.1.5 on 2025-02-04 06:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensecategory',
            name='expense_category',
            field=models.CharField(max_length=60, unique=True),
        ),
        migrations.AlterField(
            model_name='expenseclaim',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empallclaims', to=settings.AUTH_USER_MODEL),
        ),
    ]
