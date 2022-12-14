# Generated by Django 3.2.15 on 2022-10-05 11:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('photo', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('who_uploaded', models.CharField(max_length=105)),
                ('is_published', models.BooleanField()),
                ('publication_time', models.DateTimeField(default=datetime.datetime(2022, 10, 5, 11, 45, 17, 156556))),
            ],
        ),
    ]
