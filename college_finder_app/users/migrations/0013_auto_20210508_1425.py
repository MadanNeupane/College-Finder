# Generated by Django 3.1.4 on 2021-05-08 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210401_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='chance_of_admit',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True),
        ),
    ]
