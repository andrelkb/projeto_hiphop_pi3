from django.test import TestCase
from django.urls import reverse

class GestaoViewsTest(TestCase):
    
    def test_pagina_alunos_carrega_com_sucesso(self):
        """
        Testa se a rota /alunos/ retorna o status HTTP 200 (OK).
        """
        response = self.client.get('/alunos/')
        self.assertEqual(response.status_code, 200)