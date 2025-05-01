"""
Testes para o sistema Alma com integração de fila de pensamentos.
"""

import unittest
import asyncio
from datetime import datetime
from core.alma import Alma
from core.persona import Persona
from core.thought_queue import FilaPensamentos

class TestAlmaThoughts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuração inicial para todos os testes."""
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)

    def setUp(self):
        """Configuração para cada teste."""
        self.persona = Persona()
        # Inicializa a Persona de forma assíncrona
        self.loop.run_until_complete(self.persona.inicializar())
        self.alma = Alma(self.persona)
        # Limpa a fila de pensamentos
        self.alma.fila_pensamentos = FilaPensamentos()

    def test_receber_pensamento(self):
        """Testa o recebimento de pensamentos."""
        # Testa pensamento básico
        id_pensamento = self.loop.run_until_complete(self.alma.receber_pensamento(
            tipo="memoria",
            conteudo="Teste de pensamento",
            prioridade=1
        ))
        self.assertIsNotNone(id_pensamento)
        self.assertEqual(len(self.alma.fila_pensamentos.listar()), 1)

        # Testa pensamento com metadados
        id_pensamento2 = self.loop.run_until_complete(self.alma.receber_pensamento(
            tipo="duvida",
            conteudo="Por que isso acontece?",
            prioridade=2,
            metadata={"contexto": "teste"}
        ))
        self.assertIsNotNone(id_pensamento2)
        self.assertEqual(len(self.alma.fila_pensamentos.listar()), 2)

    def test_ciclo_cognitivo(self):
        """Testa o ciclo cognitivo de processamento."""
        # Adiciona pensamentos para processar
        self.loop.run_until_complete(self.alma.receber_pensamento("memoria", "Memória de teste", 1))
        self.loop.run_until_complete(self.alma.receber_pensamento("duvida", "Dúvida de teste", 2))
        self.loop.run_until_complete(self.alma.receber_pensamento("contradicao", "Contradição de teste", 3))

        # Processa os pensamentos
        resultado1 = self.loop.run_until_complete(self.alma.ciclo_cognitivo())
        self.assertIsNotNone(resultado1)
        self.assertEqual(resultado1["tipo"], "contradicao")

        resultado2 = self.loop.run_until_complete(self.alma.ciclo_cognitivo())
        self.assertIsNotNone(resultado2)
        self.assertEqual(resultado2["tipo"], "duvida")

        resultado3 = self.loop.run_until_complete(self.alma.ciclo_cognitivo())
        self.assertIsNotNone(resultado3)
        self.assertEqual(resultado3["tipo"], "memoria")

        # Verifica se a fila está vazia
        self.assertTrue(self.alma.fila_pensamentos.vazia())

    def test_ciclo_reflexao(self):
        """Testa o ciclo de reflexão."""
        # Limpa memórias existentes
        self.persona._memorias = {"memorias": []}
        
        # Adiciona algumas memórias
        self.persona.adicionar_memoria("Memória 1")
        self.persona.adicionar_memoria("Memória 2")
        self.persona.adicionar_memoria("Memória 3")

        # Executa ciclo de reflexão com exatamente 3 memórias
        self.loop.run_until_complete(self.alma.ciclo_reflexao(num_memorias=3))
        
        # Verifica se as memórias foram processadas
        self.assertEqual(len(self.alma.fila_pensamentos.listar_processados()), 3)

    def test_processadores(self):
        """Testa os processadores de diferentes tipos de pensamento."""
        # Verifica se todos os processadores estão registrados
        tipos_esperados = ["memoria", "duvida", "contradicao", "padrao", "insight"]
        for tipo in tipos_esperados:
            self.assertIn(tipo, self.alma.processadores)

    def test_processamento_continuo(self):
        """Testa o processamento contínuo de pensamentos."""
        # Adiciona vários pensamentos
        for i in range(5):
            self.loop.run_until_complete(self.alma.receber_pensamento(
                tipo="memoria",
                conteudo=f"Memória contínua {i}",
                prioridade=i
            ))

        # Processa todos os pensamentos
        for _ in range(5):
            resultado = self.loop.run_until_complete(self.alma.ciclo_cognitivo())
            self.assertIsNotNone(resultado)
            self.assertEqual(resultado["tipo"], "memoria")

        # Verifica se todos foram processados
        self.assertTrue(self.alma.fila_pensamentos.vazia())
        self.assertEqual(len(self.alma.fila_pensamentos.listar_processados()), 5)

    @classmethod
    def tearDownClass(cls):
        """Limpeza após todos os testes."""
        cls.loop.close()

if __name__ == '__main__':
    unittest.main() 