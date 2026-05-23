from django.db import models

# Tabela para as Oficinas (Breaking, DJ, Graffiti, etc)
class Oficina(models.Model):
    nome = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Tabela para os Alunos
class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=15)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    oficinas = models.ManyToManyField(Oficina)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    nome_responsavel = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome
    
    @property
    def percentual_frequencia(self):
        # Conta o total de registros de chamada para este aluno
        total_aulas = self.presenca_set.count()
        if total_aulas == 0:
            return 0  # Evita erro de divisão por zero se o aluno for novo
            
        # Conta quantas dessas chamadas ele estava presente
        presencas = self.presenca_set.filter(presente=True).count()
        
        # Calcula a porcentagem e arredonda para número inteiro
        return int((presencas / total_aulas) * 100)


# Tabela para registrar as Faltas e Presenças
class Presenca(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE)
    data = models.DateField()
    presente = models.BooleanField(default=True)

    def __str__(self):
        status = "Presente" if self.presente else "Faltou"
        return f"{self.aluno.nome} - {self.oficina.nome} ({self.data}): {status}"