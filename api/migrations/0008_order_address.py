# Generated by Django 5.0.2 on 2024-04-15 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_phoneneumber_address_phonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.address'),
            preserve_default=False,
        ),
    ]
