# Generated by Django 3.2.15 on 2022-10-20 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0016_alter_mark_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.JSONField()),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.article')),
            ],
        ),
    ]
