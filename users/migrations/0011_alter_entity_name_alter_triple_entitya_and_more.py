# Generated by Django 4.0.6 on 2022-08-03 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_semantictype_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='triple',
            name='entityA',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entA', to='users.entity'),
        ),
        migrations.AlterField(
            model_name='triple',
            name='entityB',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entB', to='users.entity'),
        ),
        migrations.AlterField(
            model_name='triple',
            name='relation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rel', to='users.relation'),
        ),
    ]
