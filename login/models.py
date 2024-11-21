from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models 
from app.services.seniorModel import SeniorModel

class UserManager(BaseUserManager):
    def create_user(self, nomusu, password=None):
        """
        Cria e retorna um usuário com o nomusu.
        """
        if not nomusu:
            raise ValueError("Os usuários devem ter um nomusu.")
        
        user = self.model(nomusu=nomusu)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nomusu, password=None):
        """
        Cria e retorna um superusuário.
        """
        user = self.create_user(nomusu, password)
        return user

class User(AbstractBaseUser):
    codusu = models.BigIntegerField(primary_key=True)
    nomusu = models.CharField(unique=True, max_length=255, db_collation='Latin1_General_CI_AS')
    tipcol = models.CharField(max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    numemp = models.CharField(max_length=255, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    codfil = models.CharField(max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    codloc = models.CharField(max_length=200, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    numcad = models.CharField(max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    numins = models.BigIntegerField(blank=True, null=True)
    
    password = None
    last_login = None

    objects = UserManager()

    USERNAME_FIELD = 'nomusu'

    # Sobrescrevendo para não fazer nada
    def set_password(self, raw_password):
        pass

    def check_password(self, raw_password):
        return True

    @property
    def last_login(self):
        return None

    def __str__(self):
        return self.nomusu

    def get_full_name(self):
        return self.nomusu

    def get_short_name(self):
        return self.nomusu

    class Meta:
        managed = False
        db_table = 'R999USU'
        


class UserComplement(SeniorModel):
    codemp = models.SmallIntegerField()
    codusu = models.BigIntegerField(primary_key=True)
    numemp = models.SmallIntegerField(blank=True, null=True)
    tipcol = models.SmallIntegerField(blank=True, null=True)
    numcad = models.IntegerField(blank=True, null=True)
    codccu = models.CharField(max_length=9, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    nomusu = models.CharField(max_length=255, db_collation='Latin1_General_CI_AS', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'E099USU'
        unique_together = (('codemp', 'codusu'),)