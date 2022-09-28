# Generated by Django 4.1 on 2022-09-21 22:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Audit', '0002_alter_audittriple_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audittriple',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='type',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]