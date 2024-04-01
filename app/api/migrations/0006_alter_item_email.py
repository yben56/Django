# Generated by Django 5.0.3 on 2024-03-28 17:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_item_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='email',
            field=models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()]),
        ),
    ]