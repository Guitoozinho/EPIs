from django.db import models

# Create your models here.
class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    #cpf = models.CharField(max_length=14, unique=True)
    #email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    #telefone = models.CharField(max_length=15, blank=True, null=True)
    #data_nascimento = models.DateField(blank=True, null=True)
    #cargo = models.CharField(max_length=50, blank=True, null=True)
    #data_admissao = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nome