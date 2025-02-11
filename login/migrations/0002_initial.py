# Generated by Django 5.0.9 on 2024-10-23 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='R999Usu',
            fields=[
                ('codusu', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nomusu', models.CharField(db_collation='Latin1_General_CI_AS', max_length=255, unique=True)),
                ('tipcol', models.CharField(blank=True, db_collation='Latin1_General_CI_AS', max_length=10, null=True)),
                ('numemp', models.CharField(blank=True, db_collation='Latin1_General_CI_AS', max_length=255, null=True)),
                ('codfil', models.CharField(blank=True, db_collation='Latin1_General_CI_AS', max_length=50, null=True)),
                ('codloc', models.CharField(blank=True, db_collation='Latin1_General_CI_AS', max_length=200, null=True)),
                ('numcad', models.CharField(blank=True, db_collation='Latin1_General_CI_AS', max_length=50, null=True)),
                ('numins', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'R999USU',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Secappweb',
            fields=[
                ('session_key', models.CharField(db_collation='Latin1_General_CI_AS', db_column='usu_chavesec', max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField(db_collation='Latin1_General_CI_AS', db_column='usu_dadossec')),
                ('expire_date', models.DateTimeField(db_column='usu_datexp')),
            ],
            options={
                'db_table': 'USU_TSecAppWeb',
                'managed': False,
            },
        ),
    ]
