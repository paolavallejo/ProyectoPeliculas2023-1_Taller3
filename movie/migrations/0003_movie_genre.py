# Generated by Django 5.0.1 on 2024-02-15 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
