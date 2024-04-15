# Generated by Django 5.0.2 on 2024-04-15 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_farmerdetails_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmerdetails',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customuser'),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[('Home', 'Home'), ('Office', 'Office'), ('Other', 'Other')], max_length=10)),
                ('name', models.CharField(max_length=25)),
                ('address', models.TextField()),
                ('pincode', models.CharField(max_length=10)),
                ('phoneneumber', models.CharField(max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customuser')),
            ],
        ),
    ]
