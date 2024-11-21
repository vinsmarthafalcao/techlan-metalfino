# Generated by Django 5.0.9 on 2024-11-04 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apontamento', '0001_initial'),
    ]

    operations = [
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
