# Generated by Django 3.2.15 on 2022-10-12 17:09

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_article_who_uploaded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
