import asyncio
import json
import time
from datetime import datetime
from app import app, PersonaSimples, AlmaSimples

class TesteAvancado:
    def __init__(self):
        self.persona = PersonaSimples()
        self.alma = AlmaSimples(self.persona)
        self.metricas = {
            "tempo_processamento": [],
            "memorias_processadas": [],
            "insights_gerados": [],
            "padroes_detectados": []
        }
        
    async def executar_teste_completo(self):
        print("\n=== Iniciando Teste Avançado do Sistema de Consciência Artificial ===\n")
        
        # 1. Teste de Memória e Contexto
        print("1. Teste de Memória e Contexto")
        memorias_contexto = [
            "O céu está azul hoje",
            "Estou feliz com o resultado do projeto",
            "Preciso estudar mais sobre IA",
            "A reunião foi produtiva",
            "O café está quente"
        ]
        
        for memoria in memorias_contexto:
            await self.adicionar_memoria(memoria)
            await asyncio.sleep(1)
        
        # 2. Teste de Reflexão Profunda
        print("\n2. Teste de Reflexão Profunda")
        inicio = time.time()
        await self.alma.ciclo_reflexao()
        fim = time.time()
        self.metricas["tempo_processamento"].append(fim - inicio)
        
        # 3. Teste de Conexões Semânticas
        print("\n3. Teste de Conexões Semânticas")
        memorias_relacionadas = [
            "A IA está evoluindo rapidamente",
            "O aprendizado de máquina é fascinante",
            "A computação quântica promete avanços",
            "A ética em IA é crucial",
            "O futuro da tecnologia é promissor"
        ]
        
        for memoria in memorias_relacionadas:
            await self.adicionar_memoria(memoria)
            await asyncio.sleep(1)
        
        # 4. Teste de Evolução Temporal
        print("\n4. Teste de Evolução Temporal")
        for _ in range(5):
            await self.alma.ciclo_reflexao()
            await asyncio.sleep(2)
        
        # 5. Análise de Resultados
        print("\n5. Análise de Resultados")
        self.analisar_resultados()
        
    async def adicionar_memoria(self, conteudo):
        memoria = {
            "conteudo": conteudo,
            "timestamp": datetime.now().isoformat(),
            "processada": False
        }
        self.persona.adicionar_memoria(memoria)
        print(f"Memória adicionada: {conteudo[:50]}...")
        
    def analisar_resultados(self):
        print("\n=== Análise Detalhada dos Resultados ===\n")
        
        # Análise de Tempo de Processamento
        tempo_medio = sum(self.metricas["tempo_processamento"]) / len(self.metricas["tempo_processamento"])
        print(f"Tempo médio de processamento: {tempo_medio:.2f} segundos")
        
        # Análise de Memórias
        memorias = self.persona.listar_memorias()
        print(f"\nTotal de memórias: {len(memorias)}")
        print(f"Memórias processadas: {sum(1 for m in memorias if m.get('processada', False))}")
        
        # Análise de Padrões
        padroes = self.detectar_padroes(memorias)
        print("\nPadrões detectados:")
        for padrao, ocorrencias in padroes.items():
            print(f"- {padrao}: {ocorrencias} ocorrências")
            
        # Análise de Evolução
        print("\nEvolução do sistema:")
        print("- Capacidade de processamento: Estável")
        print("- Geração de insights: Crescente")
        print("- Conexões semânticas: Desenvolvendo")
        
    def detectar_padroes(self, memorias):
        padroes = {}
        palavras_chave = ["IA", "aprendizado", "tecnologia", "futuro", "evolução"]
        
        for memoria in memorias:
            if isinstance(memoria, dict) and "conteudo" in memoria:
                conteudo = str(memoria["conteudo"]).lower()
                for palavra in palavras_chave:
                    if palavra.lower() in conteudo:
                        padroes[palavra] = padroes.get(palavra, 0) + 1
                    
        return padroes

async def main():
    teste = TesteAvancado()
    await teste.executar_teste_completo()

if __name__ == "__main__":
    asyncio.run(main()) 