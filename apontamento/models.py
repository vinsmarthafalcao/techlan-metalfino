from django.db import models
from app.services.seniorModel import SeniorModel

class Empresas(SeniorModel):

    codemp = models.SmallIntegerField(primary_key=True)

    nomemp = models.CharField(max_length=100, db_collation='Latin1_General_CI_AS')

    class Meta:

        managed = False

        db_table = 'E070EMP'
        

class Origens(SeniorModel):

    codemp = models.SmallIntegerField()

    codori = models.CharField(max_length=3, db_collation='Latin1_General_CI_AS', primary_key=True)

    desori = models.CharField(max_length=40, db_collation='Latin1_General_CI_AS')

    numori = models.SmallIntegerField()

    tippro = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS')

    class Meta:

        managed = False

        db_table = 'E083ORI'

        unique_together = (('codemp', 'codori'),)
        
        
class Produtos(SeniorModel):
    codemp = models.SmallIntegerField()
    codpro = models.CharField(max_length=14, db_collation='Latin1_General_CI_AS',  primary_key=True)
    despro = models.CharField(max_length=100, db_collation='Latin1_General_CI_AS')
    cplpro = models.CharField(max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    tippro = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS')
    codori = models.CharField(max_length=3, db_collation='Latin1_General_CI_AS')
    numori = models.SmallIntegerField()
    sitpro = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS')

    class Meta:

        managed = False

        db_table = 'E075PRO'

        unique_together = (('codemp', 'codpro'),)
        

class OrdensProducao(SeniorModel):
    codemp = models.SmallIntegerField()
    codori = models.CharField(max_length=3, db_collation='Latin1_General_CI_AS')
    numorp = models.IntegerField(primary_key=True)
    codpro = models.CharField(max_length=14, db_collation='Latin1_General_CI_AS')
    sitorp = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS')
    datger = models.DateTimeField()
    qtdprv = models.DecimalField(max_digits=14, decimal_places=5)
    qtdre1 = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    qtdre2 = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    qtdre3 = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    obsorp = models.CharField(max_length=240, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    obsor2 = models.CharField(max_length=240, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    usuger = models.BigIntegerField(blank=True, null=True)
    
    
    class Meta:
        managed = False
        db_table = 'E900COP'
        unique_together = (('codemp', 'codori', 'numorp'),)
 
 
class ComplementoOp(SeniorModel):
    codemp = models.SmallIntegerField()
    codori = models.CharField(max_length=3, db_collation='Latin1_General_CI_AS')
    numorp = models.IntegerField()
    codpro = models.CharField(max_length=14, db_collation='Latin1_General_CI_AS')
    codder = models.CharField(max_length=7, db_collation='Latin1_General_CI_AS', primary_key=True)
    qtdprv = models.DecimalField(max_digits=14, decimal_places=5)
    qtdre1 = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    qtdre2 = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    qtdre3 = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    qtdrfg = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    qtdiql = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    coddep = models.CharField(max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True)  
    
    class Meta:
        managed = False
        db_table = 'E900QDO'
        unique_together = (('codemp', 'codori', 'numorp', 'codpro', 'codder'),)

class RoteirosOP(SeniorModel):
    codemp = models.SmallIntegerField()
    codori = models.CharField(max_length=3, db_collation='Latin1_General_CI_AS')
    numorp = models.IntegerField()
    codetg = models.SmallIntegerField()
    sfxetr = models.SmallIntegerField()
    seqrot = models.SmallIntegerField(primary_key=True)
    sfxseq = models.SmallIntegerField()
    codopr = models.CharField(max_length=6, db_collation='Latin1_General_CI_AS')
    utiopr = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS')
    codcre = models.CharField(max_length=8, db_collation='Latin1_General_CI_AS')
    dtrini = models.DateTimeField(blank=True, null=True)
    dtrfim = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'e900oop'
        unique_together = (('codemp', 'codori', 'numorp', 'codetg', 'sfxetr', 'seqrot', 'sfxseq'),)
        

class ComponentesOP(SeniorModel):
    codemp = models.SmallIntegerField()
    codori = models.CharField(max_length=3, db_collation='Latin1_General_CI_AS')
    numorp = models.IntegerField()
    codetg = models.SmallIntegerField()
    seqcmp = models.SmallIntegerField()
    codcmp = models.CharField(max_length=14, db_collation='Latin1_General_CI_AS')
    codder = models.CharField(max_length=7, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    qtdprv = models.DecimalField(max_digits=14, decimal_places=5)
    qtdres = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    qtduti = models.DecimalField(max_digits=14, decimal_places=5)
    qtdser = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    qtdrts = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    qtdspa = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    qtdreq = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    qtdtrf = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    coddep = models.CharField(max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    codlot = models.CharField(max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    codccu = models.CharField(max_length=9, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    numcad = models.IntegerField(blank=True, null=True)
    cmprep = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    seqrep = models.SmallIntegerField(blank=True, null=True)
   
    class Meta:
        managed = False
        db_table = 'E900CMO'
        unique_together = (('codemp', 'codori', 'numorp', 'codetg', 'seqcmp'),)


class Embalagem(SeniorModel):
    codemp = models.SmallIntegerField(db_column='usu_codemp') 
    numemb = models.BigIntegerField(db_column='usu_numemb')
    veremb = models.SmallIntegerField(primary_key=True, db_column='usu_veremb')
    coddep = models.CharField(max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_coddep')
    sitemb = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_sitemb')
    embdis = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_embdis')
    codpro = models.CharField(max_length=14, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_codpro')
    codlot = models.CharField(max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_codlot')
    qtdemb = models.IntegerField(blank=True, null=True, db_column='usu_qtdemb')
    etgatu = models.SmallIntegerField(blank=True, null=True, db_column='usu_etgatu')
    hisatu = models.SmallIntegerField(blank=True, null=True, db_column='usu_hisatu')
    qtdini = models.IntegerField(blank=True, null=True, db_column='usu_qtdini')
    profim = models.CharField(max_length=14, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_profim')
    datger = models.DateTimeField(db_column='usu_datger')
    horger = models.IntegerField(db_column='usu_horger')
    usuger = models.BigIntegerField(db_column='usu_usuger')


    class Meta:
        managed = False
        db_table = 'USU_TEmbalagem'
        unique_together = (('codemp', 'numemb', 'veremb'),)

class HistoricoEmbalagem(models.Model):
    codemp = models.SmallIntegerField(db_column='usu_codemp') 
    numemb = models.BigIntegerField(db_column='usu_numemb')
    veremb = models.SmallIntegerField(db_column='usu_veremb')
    seqhis = models.SmallIntegerField(primary_key=True, db_column='usu_seqhis')
    codori = models.CharField(max_length=3, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_codori')
    numorp = models.IntegerField(blank=True, null=True, db_column='usu_numorp')
    codetg = models.SmallIntegerField(blank=True, null=True, db_column='usu_codetg')
    seqrot = models.SmallIntegerField(blank=True, null=True, db_column='usu_seqrot')
    codopr = models.CharField(max_length=6, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_codopr')
    seqeoq = models.IntegerField(blank=True, null=True, db_column='usu_seqeoq')
    seqrfg = models.IntegerField(blank=True, null=True, db_column='usu_seqrfg')
    codpro = models.CharField(max_length=14, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_codpro')
    codcre = models.CharField(max_length=8, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_codcre')
    codmol = models.CharField(max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_codmol')
    codlot = models.CharField(max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_codlot')
    qtdhis = models.IntegerField(blank=True, null=True, db_column='usu_qtdhis')
    qtdrfg = models.IntegerField(blank=True, null=True, db_column='usu_qtdrfg')
    tiphis = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_tiphis')
    numcad = models.IntegerField(blank=True, null=True, db_column='usu_numcad')
    turtrb = models.SmallIntegerField(blank=True, null=True, db_column='usu_turtrb')
    depini = models.CharField(max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_depini')
    datger = models.DateField(blank=True, null=True, db_column='usu_datger')
    horger = models.IntegerField(blank=True, null=True, db_column='usu_horger')
    usuger = models.BigIntegerField(blank=True, null=True, db_column='usu_usuger')
    deprec = models.CharField(max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_deprec')
    datrec = models.DateField(blank=True, null=True, db_column='usu_datrec')
    horrec = models.IntegerField(blank=True, null=True, db_column='usu_horrec')
    usurec = models.BigIntegerField(blank=True, null=True, db_column='usu_usurec')
    seqmov = models.IntegerField(blank=True, null=True, db_column='usu_seqmov')
    class Meta:
        managed = False
        db_table = 'USU_THistEmb'
        unique_together = (('codemp', 'numemb', 'veremb', 'seqhis'),)
        

class Deposito(SeniorModel):
    codemp = models.SmallIntegerField()
    coddep = models.CharField(max_length=10, db_collation='Latin1_General_CI_AS', primary_key=True)
    desdep = models.CharField(max_length=30, db_collation='Latin1_General_CI_AS')
    abrdep = models.CharField(max_length=10, db_collation='Latin1_General_CI_AS')
    tipdep = models.SmallIntegerField()
   
    class Meta:
        managed = False
        db_table = 'E205DEP'
        unique_together = (('codemp', 'coddep'),)
   
        
class MoldePro(SeniorModel):
    codemp = models.SmallIntegerField(db_column='usu_codemp')
    codmolde = models.CharField(primary_key=True, max_length=14, db_collation='Latin1_General_CI_AS', db_column='usu_codmolde')
    codpro = models.CharField(max_length=14, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_codpro')
    despro = models.CharField(max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_despro')
    datger = models.DateTimeField(blank=True, null=True, db_column='usu_datger')
    clone = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_clone')
    sitmol = models.CharField(max_length=1, db_collation='Latin1_General_CI_AS', blank=True, null=True, db_column='usu_sitmol')

    class Meta:
        managed = False
        db_table = 'USU_TMOLDEPRO'
        unique_together = (('codemp', 'codmolde', 'codpro'),)