# Generated by Django 4.1 on 2022-09-09 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_entity_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='relation',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
