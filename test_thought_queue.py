"""
Testes para o módulo de fila de pensamentos.
"""

import unittest
import time
from core.thought_queue import Pensamento, FilaPensamentos

class TestPensamento(unittest.TestCase):
    def setUp(self):
        self.pensamento = Pensamento(
            tipo="memoria",
            conteudo="Teste de pensamento",
            prioridade=1
        )

    def test_criacao_pensamento(self):
        """Testa a criação de um pensamento."""
        self.assertEqual(self.pensamento.tipo, "memoria")
        self.assertEqual(self.pensamento.conteudo, "Teste de pensamento")
        self.assertEqual(self.pensamento.prioridade, 1)
        self.assertFalse(self.pensamento.processado)
        self.assertIsNotNone(self.pensamento.id)
        self.assertIsNotNone(self.pensamento.timestamp)

    def test_comparacao_prioridade(self):
        """Testa a comparação de pensamentos por prioridade."""
        pensamento_baixo = Pensamento("memoria", "Baixa prioridade", 0)
        pensamento_alto = Pensamento("memoria", "Alta prioridade", 2)
        
        self.assertTrue(pensamento_alto < pensamento_baixo)  # Maior prioridade vem primeiro
        self.assertFalse(pensamento_baixo < pensamento_alto)

    def test_to_dict(self):
        """Testa a conversão para dicionário."""
        dicionario = self.pensamento.to_dict()
        self.assertEqual(dicionario['tipo'], "memoria")
        self.assertEqual(dicionario['conteudo'], "Teste de pensamento")
        self.assertEqual(dicionario['prioridade'], 1)
        self.assertIn('id', dicionario)
        self.assertIn('timestamp', dicionario)
        self.assertIn('metadata', dicionario)
        self.assertIn('processado', dicionario)

class TestFilaPensamentos(unittest.TestCase):
    def setUp(self):
        """Configuração para cada teste."""
        self.fila = FilaPensamentos()
        self.pensamentos = [
            Pensamento("memoria", "Memória 1", 1),
            Pensamento("duvida", "Dúvida 1", 2),
            Pensamento("contradicao", "Contradição 1", 3)
        ]
    
    def test_adicionar_e_recuperar(self):
        """Testa adicionar e recuperar pensamentos."""
        for pensamento in self.pensamentos:
            self.fila.adicionar(pensamento)
        
        # Verifica se os pensamentos são retornados em ordem de prioridade (maior para menor)
        pensamentos_ordenados = sorted(self.pensamentos, key=lambda p: p.prioridade, reverse=True)
        for pensamento in pensamentos_ordenados:
            proximo = self.fila.proximo()
            self.assertEqual(proximo.tipo, pensamento.tipo)
            self.assertEqual(proximo.conteudo, pensamento.conteudo)
            self.assertEqual(proximo.prioridade, pensamento.prioridade)
        
        # Verifica se a fila está vazia
        self.assertTrue(self.fila.vazia())
        
        # Testa adicionar pensamento com mesma prioridade
        self.fila.adicionar(self.pensamentos[0])
        self.assertEqual(len(self.fila.listar()), 1)
    
    def test_listagem(self):
        """Testa listagem de pensamentos."""
        for pensamento in self.pensamentos:
            self.fila.adicionar(pensamento)
        
        lista = self.fila.listar()
        self.assertEqual(len(lista), 3)
        self.assertTrue(all(isinstance(p, Pensamento) for p in lista))
    
    def test_pensamentos_processados(self):
        """Testa registro de pensamentos processados."""
        for pensamento in self.pensamentos:
            self.fila.adicionar(pensamento)
        
        # Processa os dois primeiros pensamentos
        for i in range(2):
            pensamento = self.fila.proximo()
            self.fila.processar(pensamento, f"Resultado {i}")
        
        processados = self.fila.listar_processados()
        self.assertEqual(len(processados), 2)
        
        # Verifica se o terceiro pensamento ainda está na fila
        self.assertEqual(len(self.fila.listar()), 1)
    
    def test_limpar_processados(self):
        """Testa limpeza de pensamentos processados."""
        for pensamento in self.pensamentos:
            self.fila.adicionar(pensamento)
        
        # Processa todos os pensamentos
        for pensamento in self.pensamentos:
            self.fila.processar(pensamento, "Resultado")
        
        self.assertEqual(len(self.fila.listar_processados()), 3)
        self.fila.limpar_processados()
        self.assertEqual(len(self.fila.listar_processados()), 0)
    
    def test_buscar_por_tipo(self):
        """Testa busca de pensamentos por tipo."""
        for pensamento in self.pensamentos:
            self.fila.adicionar(pensamento)
        
        # Processa todos os pensamentos
        for pensamento in self.pensamentos:
            self.fila.processar(pensamento, "Resultado")
        
        memorias = self.fila.buscar_por_tipo("memoria")
        self.assertEqual(len(memorias), 1)
        self.assertEqual(memorias[0].conteudo, "Memória 1")
    
    def test_buscar_por_id(self):
        """Testa busca de pensamento por ID."""
        pensamento = self.pensamentos[0]
        self.fila.adicionar(pensamento)
        
        # Processa o pensamento
        self.fila.processar(pensamento, "Resultado")
        
        encontrado = self.fila.buscar_por_id(pensamento.id)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.id, pensamento.id)
        
        nao_encontrado = self.fila.buscar_por_id("id_inexistente")
        self.assertIsNone(nao_encontrado)

if __name__ == '__main__':
    unittest.main() 