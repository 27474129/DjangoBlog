# Generated by Django 3.2.15 on 2022-10-06 17:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_article_publication_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='publication_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 6, 17, 5, 13, 851956), null=True),
        ),
    ]
