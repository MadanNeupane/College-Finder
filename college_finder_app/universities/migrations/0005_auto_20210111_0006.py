# Generated by Django 3.1.4 on 2021-01-10 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0004_auto_20210110_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universities',
            name='rank',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='universities',
            name='record_type',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='universities',
            name='stats_pc_intl_students',
            field=models.CharField(max_length=16),
        ),
    ]