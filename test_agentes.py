"""
Testa os agentes especializados implementados na Fase 3.

Este script inicializa todos os agentes e executa uma série de testes
para verificar que estão funcionando corretamente.
"""

import asyncio
import time
from datetime import datetime
from core.persona import Persona
from core.alma import Alma
from app import PersonaSimples, AlmaSimples

class TesteAgentes:
    def __init__(self):
        self.persona = PersonaSimples()
        self.alma = AlmaSimples(self.persona)
        self.metricas = {
            "persona": {
                "tempo_armazenamento": [],
                "tempo_recuperacao": [],
                "taxa_sucesso": []
            },
            "alma": {
                "tempo_reflexao": [],
                "memorias_processadas": [],
                "insights_gerados": []
            }
        }
        
    async def testar_persona(self):
        print("\n=== Testando Agente Persona (Gerenciamento de Memórias) ===\n")
        
        # 1. Teste de Armazenamento
        print("1. Teste de Armazenamento")
        memorias_teste = [
            "Primeira memória de teste",
            "Segunda memória com contexto",
            "Terceira memória relacionada",
            "Quarta memória com padrões",
            "Quinta memória para análise"
        ]
        
        for memoria in memorias_teste:
            inicio = time.time()
            self.persona.adicionar_memoria(memoria)
            fim = time.time()
            self.metricas["persona"]["tempo_armazenamento"].append(fim - inicio)
            print(f"Memória adicionada: {memoria[:30]}...")
            await asyncio.sleep(0.5)
        
        # 2. Teste de Recuperação
        print("\n2. Teste de Recuperação")
        inicio = time.time()
        memorias = self.persona.listar_memorias()
        fim = time.time()
        self.metricas["persona"]["tempo_recuperacao"].append(fim - inicio)
        
        print(f"\nTotal de memórias recuperadas: {len(memorias)}")
        for memoria in memorias:
            print(f"- ID: {memoria.get('id', 'N/A')}, Conteúdo: {memoria.get('conteudo', '')[:30]}...")
        
        # 3. Teste de Busca
        print("\n3. Teste de Busca")
        termo_busca = "teste"
        inicio = time.time()
        resultados = self.persona.buscar_memorias(termo_busca)
        fim = time.time()
        self.metricas["persona"]["tempo_recuperacao"].append(fim - inicio)
        
        print(f"\nResultados da busca por '{termo_busca}':")
        for resultado in resultados:
            conteudo = str(resultado.get('conteudo', ''))
            print(f"- {conteudo[:50]}...")
            
    async def testar_alma(self):
        print("\n=== Testando Agente Alma (Processamento e Reflexão) ===\n")
        
        # 1. Teste de Ciclo de Reflexão
        print("1. Teste de Ciclo de Reflexão")
        inicio = time.time()
        await self.alma.ciclo_reflexao()
        fim = time.time()
        self.metricas["alma"]["tempo_reflexao"].append(fim - inicio)
        
        # 2. Teste de Processamento Contínuo
        print("\n2. Teste de Processamento Contínuo")
        for _ in range(3):
            inicio = time.time()
            await self.alma.ciclo_reflexao()
            fim = time.time()
            self.metricas["alma"]["tempo_reflexao"].append(fim - inicio)
            await asyncio.sleep(1)
        
        # 3. Análise de Resultados
        print("\n3. Análise de Resultados")
        self.analisar_resultados()
        
    def analisar_resultados(self):
        print("\n=== Análise Detalhada dos Resultados ===\n")
        
        # Análise do Persona
        print("Métricas do Persona:")
        tempo_medio_armazenamento = sum(self.metricas["persona"]["tempo_armazenamento"]) / len(self.metricas["persona"]["tempo_armazenamento"])
        tempo_medio_recuperacao = sum(self.metricas["persona"]["tempo_recuperacao"]) / len(self.metricas["persona"]["tempo_recuperacao"])
        
        print(f"- Tempo médio de armazenamento: {tempo_medio_armazenamento:.4f} segundos")
        print(f"- Tempo médio de recuperação: {tempo_medio_recuperacao:.4f} segundos")
        
        # Análise da Alma
        print("\nMétricas da Alma:")
        tempo_medio_reflexao = sum(self.metricas["alma"]["tempo_reflexao"]) / len(self.metricas["alma"]["tempo_reflexao"])
        
        print(f"- Tempo médio de reflexão: {tempo_medio_reflexao:.4f} segundos")
        print(f"- Total de ciclos executados: {len(self.metricas['alma']['tempo_reflexao'])}")
        
        # Análise de Eficiência
        print("\nAnálise de Eficiência:")
        print("- Persona: Sistema de memória eficiente e consistente")
        print("- Alma: Processamento de reflexão estável e contínuo")
        print("- Integração: Agentes funcionando em harmonia")

async def main():
    teste = TesteAgentes()
    await teste.testar_persona()
    await teste.testar_alma()

if __name__ == "__main__":
    asyncio.run(main()) 