from django.test import TestCase
from django.urls import reverse

class GestaoViewsTest(TestCase):
    
    def test_pagina_alunos_carrega_com_sucesso(self):
        """
        Testa se a rota /alunos/ retorna o status HTTP 200 (OK).
        """
        response = self.client.get('/alunos/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_chamada_carrega_com_sucesso(self):
        """
        Testa se a rota /chamada/ retorna o status HTTP 200 (OK).
        """
        response = self.client.get('/chamada/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_admin_redireciona_para_login(self):
        """
        Testa se a rota /admin/ protege a área e redireciona (status 302).
        """
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)