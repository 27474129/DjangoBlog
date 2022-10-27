# Generated by Django 3.2.15 on 2022-10-05 15:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20221005_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='is_published',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='publication_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 5, 15, 15, 45, 940378), null=True),
        ),
    ]
