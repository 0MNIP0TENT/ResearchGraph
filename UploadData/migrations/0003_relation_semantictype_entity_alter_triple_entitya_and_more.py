# Generated by Django 4.0.4 on 2022-07-25 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UploadData', '0002_verified'),
    ]

    operations = [
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
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('semantic_type', models.ManyToManyField(to='UploadData.semantictype')),
            ],
        ),
        migrations.AlterField(
            model_name='triple',
            name='entityA',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='entA', to='UploadData.entity'),
        ),
        migrations.AlterField(
            model_name='triple',
            name='entityB',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='entB', to='UploadData.entity'),
        ),
        migrations.AlterField(
            model_name='triple',
            name='relation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='rel', to='UploadData.relation'),
        ),
    ]
