# Generated by Django 3.1.4 on 2021-01-19 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='dummy-article-img.jpg', upload_to='blog_pics'),
        ),
    ]