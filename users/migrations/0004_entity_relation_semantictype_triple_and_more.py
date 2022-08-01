# Generated by Django 4.0.4 on 2022-07-25 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_userdataset_dataset'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SemanticType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Triple',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entityA', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='entA', to='users.entity')),
                ('entityB', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='entB', to='users.entity')),
                ('relation', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='rel', to='users.relation')),
            ],
        ),
        migrations.AddField(
            model_name='entity',
            name='semantic_type',
            field=models.ManyToManyField(to='users.semantictype'),
        ),
    ]
