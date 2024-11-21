from django.db import models  
from app.services.seniorModel import SeniorModel  
from apontamento.models import *


class C_Recursos(SeniorModel):
    codemp = models.SmallIntegerField()
    codcre = models.CharField(max_length=8, db_collation='Latin1_General_CI_AS', primary_key=True)
    descre = models.CharField(max_length=40, db_collation='Latin1_General_CI_AS')
    abrcre = models.CharField(max_length=10, db_collation='Latin1_General_CI_AS')
    codetg = models.SmallIntegerField()
    tipcre = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS')
    
    class Meta:
        managed = False
        db_table = 'E725CRE'
        unique_together = (('codemp', 'codcre'),)


class Operacoes(SeniorModel):
    codemp = models.SmallIntegerField()
    codopr = models.CharField(max_length=6, db_collation='Latin1_General_CI_AS', primary_key=True)
    desopr = models.CharField(max_length=40, db_collation='Latin1_General_CI_AS')
    abropr = models.CharField(max_length=10, db_collation='Latin1_General_CI_AS')
    codcre = models.CharField(max_length=8, db_collation='Latin1_General_CI_AS')
    utiopr = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS')
    codetg = models.SmallIntegerField()
    obsopr = models.CharField(max_length=240, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'E720OPR'
        unique_together = (('codemp', 'codopr'),)
        

class Estagios(SeniorModel):
    codemp = models.SmallIntegerField()
    codetg = models.SmallIntegerField(primary_key=True)
    desetg = models.CharField(max_length=30, db_collation='Latin1_General_CI_AS')
    abretg = models.CharField(max_length=10, db_collation='Latin1_General_CI_AS')
    codori = models.CharField(max_length=3, db_collation='Latin1_General_CI_AS')
    tipetg = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS')

    class Meta:
        managed = False
        db_table = 'E093ETG'
        unique_together = (('codemp', 'codetg'),)


class Operadores(SeniorModel):
    codemp = models.SmallIntegerField()
    numcad = models.IntegerField(primary_key=True)
    nomope = models.CharField(max_length=80, db_collation='Latin1_General_CI_AS')
    codgrp = models.CharField(max_length=5, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    turtrb = models.SmallIntegerField(blank=True, null=True)
    sitope = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS')

    class Meta:
        managed = False
        db_table = 'E906OPE'
        unique_together = (('codemp', 'numcad'),)
 
