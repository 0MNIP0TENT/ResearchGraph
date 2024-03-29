# Generated by Django 4.0.4 on 2022-07-29 00:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_triple_entitya_alter_triple_entityb_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='relation',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='semantictype',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
