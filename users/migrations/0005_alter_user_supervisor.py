# Generated by Django 5.1.5 on 2025-02-10 03:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_expensecategory_expense_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='supervisor',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'manager'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subordinates', to=settings.AUTH_USER_MODEL),
        ),
    ]
