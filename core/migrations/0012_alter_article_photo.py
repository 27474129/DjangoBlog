# Generated by Django 3.2.15 on 2022-10-14 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_article_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='photo',
            field=models.ImageField(upload_to='photos/%Y/%m/%d/'),
        ),
    ]
