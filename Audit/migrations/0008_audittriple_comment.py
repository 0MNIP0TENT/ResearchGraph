# Generated by Django 4.1 on 2022-10-16 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audit', '0007_dataset_alter_audittriple_dataset_alter_type_dataset'),
    ]

    operations = [
        migrations.AddField(
            model_name='audittriple',
            name='comment',
            field=models.TextField(blank=True, help_text='Enter a optional reason for un verifing', null=True, verbose_name='comments'),
        ),
    ]
