# Generated by Django 5.0.9 on 2024-11-02 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='C_Recursos',
            fields=[
                ('codemp', models.SmallIntegerField()),
                ('codcre', models.CharField(db_collation='Latin1_General_CI_AS', max_length=8, primary_key=True, serialize=False)),
                ('descre', models.CharField(db_collation='Latin1_General_CI_AS', max_length=40)),
                ('abrcre', models.CharField(db_collation='Latin1_General_CI_AS', max_length=10)),
                ('codetg', models.SmallIntegerField()),
                ('tipcre', models.CharField(db_collation='Latin1_General_CI_AS', max_length=1)),
            ],
            options={
                'db_table': 'E725CRE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ComplementoOp',
            fields=[
                ('codemp', models.SmallIntegerField()),
                ('codori', models.CharField(db_collation='Latin1_General_CI_AS', max_length=3)),
                ('numorp', models.IntegerField()),
                ('codpro', models.CharField(db_collation='Latin1_General_CI_AS', max_length=14)),
                ('codder', models.CharField(db_collation='Latin1_General_CI_AS', max_length=7, primary_key=True, serialize=False)),
                ('qtdprv', models.DecimalField(decimal_places=5, max_digits=14)),
                ('qtdre1', models.DecimalField(blank=True, decimal_places=5, max_digits=14, null=True)),
                ('qtdre2', models.DecimalField(blank=True, decimal_places=5, max_digits=14, null=True)),
                ('qtdre3', models.DecimalField(blank=True, decimal_places=5, max_digits=14, null=True)),
                ('qtdrfg', models.DecimalField(blank=True, decimal_places=5, max_digits=14, null=True)),
                ('qtdiql', models.DecimalField(blank=True, decimal_places=5, max_digits=14, null=True)),
                ('coddep', models.CharField(blank=True, db_collation='Latin1_General_CI_AS', max_length=10, null=True)),
            ],
            options={
                'db_table': 'E900QDO',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('codemp', models.SmallIntegerField()),
                ('coddep', models.CharField(db_collation='Latin1_General_CI_AS', max_length=10, primary_key=True, serialize=False)),
                ('desdep', models.CharField(db_collation='Latin1_General_CI_AS', max_length=30)),
                ('abrdep', models.CharField(db_collation='Latin1_General_CI_AS', max_length=10)),
                ('tipdep', models.SmallIntegerField()),
            ],
            options={
                'db_table': 'E205DEP',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Empresas',
            fields=[
                ('codemp', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('nomemp', models.CharField(db_collation='Latin1_General_CI_AS', max_length=100)),
            ],
            options={
                'db_table': 'E070EMP',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Estagios',
            fields=[
                ('codemp', models.SmallIntegerField()),
                ('codetg', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('desetg', models.CharField(db_collation='Latin1_General_CI_AS', max_length=30)),
                ('abretg', models.CharField(db_collation='Latin1_General_CI_AS', max_length=10)),
                ('codori', models.CharField(db_collation='Latin1_General_CI_AS', max_length=3)),
                ('tipetg', models.CharField(db_collation='Latin1_General_CI_AS', max_length=1)),
            ],
            options={
                'db_table': 'E093ETG',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Operacoes',
            fields=[
                ('codemp', models.SmallIntegerField()),
                ('codopr', models.CharField(db_collation='Latin1_General_CI_AS', max_length=6, primary_key=True, serialize=False)),
                ('desopr', models.CharField(db_collation='Latin1_General_CI_AS', max_length=40)),
                ('abropr', models.CharField(db_collation='Latin1_General_CI_AS', max_length=10)),
                ('codcre', models.CharField(db_collation='Latin1_General_CI_AS', max_length=8)),
                ('utiopr', models.CharField(db_collation='Latin1_General_CI_AS', max_length=1)),
                ('codetg', models.SmallIntegerField()),
                ('obsopr', models.CharField(blank=True, db_collation='Latin1_General_CI_AS', max_length=240, null=True)),
            ],
            options={
                'db_table': 'E720OPR',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Operadores',
            fields=[
                ('codemp', models.SmallIntegerField()),
                ('numcad', models.IntegerField(primary_key=True, serialize=False)),
                ('nomope', models.CharField(db_collation='Latin1_General_CI_AS', max_length=80)),
                ('codgrp', models.CharField(blank=True, db_collation='Latin1_General_CI_AS', max_length=5, null=True)),
                ('turtrb', models.SmallIntegerField(blank=True, null=True)),
                ('sitope', models.CharField(db_collation='Latin1_General_CI_AS', max_length=1)),
            ],
            options={
                'db_table': 'E906OPE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrdensProducao',
            fields=[
                ('codemp', models.SmallIntegerField()),
                ('codori', models.CharField(db_collation='Latin1_General_CI_AS', max_length=3)),
                ('numorp', models.IntegerField(primary_key=True, serialize=False)),
                ('codpro', models.CharField(db_collation='Latin1_General_CI_AS', max_length=14)),
                ('sitorp', models.CharField(db_collation='Latin1_General_CI_AS', max_length=1)),
                ('datger', models.DateTimeField()),
                ('qtdprv', models.DecimalField(decimal_places=5, max_digits=14)),
                ('qtdre1', models.DecimalField(blank=True, decimal_places=5, max_digits=14, null=True)),
                ('qtdre2', models.DecimalField(blank=True, decimal_places=5, max_digits=14, null=True)),
                ('qtdre3', models.DecimalField(blank=True, decimal_places=5, max_digits=14, null=True)),
                ('obsorp', models.CharField(blank=True, db_collation='Latin1_General_CI_AS', max_length=240, null=True)),
                ('obsor2', models.CharField(blank=True, db_collation='Latin1_General_CI_AS', max_length=240, null=True)),
                ('usuger', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'E900COP',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Origens',
            fields=[
                ('codemp', models.SmallIntegerField()),
                ('codori', models.CharField(db_collation='Latin1_General_CI_AS', max_length=3, primary_key=True, serialize=False)),
                ('desori', models.CharField(db_collation='Latin1_General_CI_AS', max_length=40)),
                ('numori', models.SmallIntegerField()),
                ('tippro', models.CharField(db_collation='Latin1_General_CI_AS', max_length=1)),
            ],
            options={
                'db_table': 'E083ORI',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('codemp', models.SmallIntegerField()),
                ('codpro', models.CharField(db_collation='Latin1_General_CI_AS', max_length=14, primary_key=True, serialize=False)),
                ('despro', models.CharField(db_collation='Latin1_General_CI_AS', max_length=100)),
                ('cplpro', models.CharField(blank=True, db_collation='Latin1_General_CI_AS', max_length=50, null=True)),
                ('tippro', models.CharField(db_collation='Latin1_General_CI_AS', max_length=1)),
                ('codori', models.CharField(db_collation='Latin1_General_CI_AS', max_length=3)),
                ('numori', models.SmallIntegerField()),
                ('sitpro', models.CharField(db_collation='Latin1_General_CI_AS', max_length=1)),
            ],
            options={
                'db_table': 'E075PRO',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoteirosOP',
            fields=[
                ('codemp', models.SmallIntegerField()),
                ('codori', models.CharField(db_collation='Latin1_General_CI_AS', max_length=3)),
                ('numorp', models.IntegerField()),
                ('codetg', models.SmallIntegerField()),
                ('sfxetr', models.SmallIntegerField()),
                ('seqrot', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('sfxseq', models.SmallIntegerField()),
                ('codopr', models.CharField(db_collation='Latin1_General_CI_AS', max_length=6)),
                ('utiopr', models.CharField(db_collation='Latin1_General_CI_AS', max_length=1)),
                ('codcre', models.CharField(db_collation='Latin1_General_CI_AS', max_length=8)),
                ('dtrini', models.DateTimeField(blank=True, null=True)),
                ('dtrfim', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'e900oop',
                'managed': False,
            },
        ),
    ]