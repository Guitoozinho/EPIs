from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)  # formato: 000.000.000-00 (validação opcional)
    matricula = models.CharField(max_length=50, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True)
    setor = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    tamanho = models.CharField("Tamanho (uniforme / EPI)", max_length=20, blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"


class EPIEntrega(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='entregas')
    nome_epi = models.CharField("Nome do EPI", max_length=200)
    codigo_epi = models.CharField("Código do EPI", max_length=100, blank=True)
    data_entrega = models.DateField()
    validade = models.DateField(blank=True, null=True)
    quantidade = models.PositiveIntegerField(default=1)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Entrega de EPI"
        verbose_name_plural = "Entregas de EPIs"
        ordering = ['-data_entrega', '-criado_em']

    def __str__(self):
        return f"{self.nome_epi} → {self.colaborador.nome} ({self.data_entrega})"
