# Generated by Django 5.1.6 on 2025-02-27 01:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seguidores', models.IntegerField(default=0)),
                ('seguidos', models.IntegerField(default=0)),
                ('fecha_creacion', models.CharField(default='0', max_length=10)),
                ('promedio_hashtags_por_publicacion', models.FloatField(default=0)),
                ('promedio_publicaciones_por_dia', models.FloatField(default=0)),
                ('promedio_comentarios_por_dia', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'cuentas',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('etiqueta', models.CharField(default='normal', max_length=20)),
            ],
            options={
                'db_table': 'usuarios',
            },
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('texto', models.TextField()),
                ('fecha_publicacion', models.DateField()),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publicaciones', to='backpropagation.cuenta')),
            ],
            options={
                'db_table': 'publicaciones',
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=50)),
                ('texto_comentario', models.TextField()),
                ('fecha_comentario', models.DateField()),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='backpropagation.publicacion')),
            ],
            options={
                'db_table': 'comentarios',
            },
        ),
        migrations.AddField(
            model_name='cuenta',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cuenta', to='backpropagation.usuario'),
        ),
    ]
