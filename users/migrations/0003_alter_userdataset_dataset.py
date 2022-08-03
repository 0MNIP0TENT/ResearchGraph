# Generated by Django 4.0.4 on 2022-07-22 02:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userdataset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdataset',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]