# Generated by Django 3.2.15 on 2022-10-16 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20221016_1656'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mark',
            old_name='article_id',
            new_name='article',
        ),
    ]
