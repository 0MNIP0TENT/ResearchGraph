# Generated by Django 4.0.4 on 2022-07-28 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_entity_user_relation_user_semantictype_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triple',
            name='entityA',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='entA', to='users.entity'),
        ),
        migrations.AlterField(
            model_name='triple',
            name='entityB',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='entB', to='users.entity'),
        ),
        migrations.AlterField(
            model_name='triple',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='rel', to='users.relation'),
        ),
    ]
