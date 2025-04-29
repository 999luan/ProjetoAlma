"""
Módulo Alma - Responsável por processos internos de reflexão e metacognição.

Este módulo implementa a parte "subconsciente" do sistema, que trabalha continuamente
em segundo plano para refinar, analisar e evoluir o conhecimento armazenado.
"""

import random
import asyncio
import time
from datetime import datetime
from core.agentes import AgenteEmocional, AgenteConsistencia, AgentePadrao

class Alma:
    def __init__(self, persona):
        """
        Inicializa a Alma com referência à Persona.
        
        Args:
            persona: Instância da classe Persona
        """
        self.persona = persona
        self.ciclo_ativo = False
        self.reflexoes_realizadas = 0
        self.metacognicoes_realizadas = 0
        
        # Inicializa os agentes especializados
        self.agente_emocional = AgenteEmocional()
        self.agente_consistencia = AgenteConsistencia(persona)
        self.agente_padrao = AgentePadrao(persona)
        
        # O gerenciador de aprendizado será inicializado posteriormente
        # quando tivermos acesso a esta instância de Alma
        self.gerenciador_aprendizado = None
    
    def configurar_gerenciador_aprendizado(self, gerenciador):
        """Configura o gerenciador de aprendizado.
        
        Args:
            gerenciador: Instância do GerenciadorAprendizado
        """
        self.gerenciador_aprendizado = gerenciador
    
    async def iniciar_ciclo_reflexao(self, intervalo=60):
        """Inicia o ciclo contínuo de reflexão.
        
        Args:
            intervalo (int): Intervalo em segundos entre reflexões
        """
        self.ciclo_ativo = True
        print(f"Iniciando ciclo de reflexão a cada {intervalo} segundos")
        
        try:
            while self.ciclo_ativo:
                await self.ciclo_de_reflexao()
                await asyncio.sleep(intervalo)
        except asyncio.CancelledError:
            self.ciclo_ativo = False
            print("Ciclo de reflexão interrompido")
            raise
    
    async def ciclo_de_reflexao(self):
        """Executa um ciclo de reflexão sobre as memórias existentes."""
        print("\n=== Iniciando Ciclo de Reflexão ===")
        
        # Determina qual agente ativar
        if self.gerenciador_aprendizado:
            # Usa pesos otimizados para seleção do agente
            agente = self.gerenciador_aprendizado.selecionar_agente()
            print(f"Seleção otimizada: agente '{agente}' escolhido")
            
            match agente:
                case "reflexao":
                    await self.ativar_agente_reflexao()
                case "metacognicao":
                    await self.ativar_agente_metacognicao()
                case "emocional":
                    await self.ativar_agente_emocional()
                case "consistencia":
                    await self.ativar_agente_consistencia()
                case "padrao":
                    await self.ativar_agente_padrao()
        else:
            # Escolha aleatória padrão
            escolha = random.random()
            
            if escolha < 0.5:  # 50% chance para reflexão
                await self.ativar_agente_reflexao()
            elif escolha < 0.7:  # 20% chance para metacognição
                await self.ativar_agente_metacognicao()
            elif escolha < 0.8:  # 10% chance para agente emocional
                await self.ativar_agente_emocional()
            elif escolha < 0.9:  # 10% chance para agente de consistência
                await self.ativar_agente_consistencia()
            else:  # 10% chance para agente de padrões
                await self.ativar_agente_padrao()
        
        print("=== Ciclo de Reflexão Concluído ===\n")
    
    async def ativar_agente_reflexao(self):
        """Ativa o agente de reflexão para criar novas sínteses.
        
        Este agente pega memórias existentes e cria conexões entre elas.
        """
        print("Ativando Agente de Reflexão")
        self.reflexoes_realizadas += 1
        
        # Gera uma síntese usando o método da Persona
        sintese = self.persona.gerar_sintese()
        
        if sintese:
            print(f"Reflexão #{self.reflexoes_realizadas}: {sintese}")
            # Simula tempo de processamento
            await asyncio.sleep(1)
            return sintese
        else:
            print("Não foi possível gerar uma reflexão")
            return None
    
    async def ativar_agente_metacognicao(self):
        """Ativa o agente de metacognição para avaliar a qualidade das memórias.
        
        Este agente analisa as memórias existentes e avalia seu valor.
        """
        print("Ativando Agente de Metacognição")
        self.metacognicoes_realizadas += 1
        
        # Carrega as memórias
        dados = self.persona._carregar_memorias()
        if not dados["memorias"]:
            print("Não há memórias para avaliar")
            return None
        
        # Escolhe uma memória aleatória para avaliar
        memoria = random.choice(dados["memorias"])
        
        # Avalia a qualidade da memória (implementação simples)
        qualidade = self._avaliar_qualidade_memoria(memoria)
        
        # Registra a avaliação na própria memória
        self._registrar_avaliacao(memoria, qualidade, dados)
        
        print(f"Metacognição #{self.metacognicoes_realizadas}: Memória #{memoria['id']} avaliada com qualidade {qualidade}/10")
        
        # Simula tempo de processamento
        await asyncio.sleep(1)
        
        return qualidade
    
    async def ativar_agente_emocional(self):
        """Ativa o agente emocional para adicionar contexto emocional às memórias.
        
        Este agente analisa o conteúdo das memórias e atribui emoções relacionadas.
        """
        print("Ativando Agente Emocional")
        
        # Carrega as memórias
        dados = self.persona._carregar_memorias()
        if not dados["memorias"]:
            print("Não há memórias para processar emocionalmente")
            return None
        
        # Escolhe uma memória aleatória para processar
        memoria = random.choice(dados["memorias"])
        
        # Processa a memória com o agente emocional
        memoria_processada = await self.agente_emocional.processar(memoria)
        
        # Se a memória foi alterada, atualiza no armazenamento
        if memoria_processada != memoria:
            for idx, mem in enumerate(dados["memorias"]):
                if mem["id"] == memoria["id"]:
                    dados["memorias"][idx] = memoria_processada
                    self.persona._salvar_memorias(dados)
                    break
        
        # Simula tempo de processamento
        await asyncio.sleep(1)
        
        return memoria_processada

    async def ativar_agente_consistencia(self):
        """Ativa o agente de consistência para detectar e resolver inconsistências.
        
        Este agente compara memórias buscando contradições e propõe resoluções.
        """
        print("Ativando Agente de Consistência")
        
        # Carrega as memórias
        dados = self.persona._carregar_memorias()
        if not dados["memorias"]:
            print("Não há memórias para verificar consistência")
            return None
        
        # Escolhe uma memória aleatória para processar
        memoria = random.choice(dados["memorias"])
        
        # Processa a memória com o agente de consistência
        memoria_processada = await self.agente_consistencia.processar(memoria)
        
        # Se a memória foi alterada, atualiza no armazenamento
        if memoria_processada != memoria:
            for idx, mem in enumerate(dados["memorias"]):
                if mem["id"] == memoria["id"]:
                    dados["memorias"][idx] = memoria_processada
                    self.persona._salvar_memorias(dados)
                    break
        
        # Simula tempo de processamento
        await asyncio.sleep(1)
        
        return memoria_processada

    async def ativar_agente_padrao(self):
        """Ativa o agente de padrões para detectar tendências nas memórias.
        
        Este agente analisa o conjunto de memórias buscando padrões recorrentes.
        """
        print("Ativando Agente de Padrões")
        
        # Carrega as memórias
        dados = self.persona._carregar_memorias()
        if not dados["memorias"]:
            print("Não há memórias para detectar padrões")
            return None
        
        # Escolhe uma memória aleatória para processar
        memoria = random.choice(dados["memorias"])
        
        # Processa a memória com o agente de padrões
        memoria_processada = await self.agente_padrao.processar(memoria)
        
        # Se a memória foi alterada, atualiza no armazenamento
        if memoria_processada != memoria:
            for idx, mem in enumerate(dados["memorias"]):
                if mem["id"] == memoria["id"]:
                    dados["memorias"][idx] = memoria_processada
                    self.persona._salvar_memorias(dados)
                    break
        
        # Simula tempo de processamento
        await asyncio.sleep(1)
        
        return memoria_processada
    
    async def atualizar_memoria_especifica(self, memoria):
        """Atualiza uma memória específica, refinando seu conteúdo.
        
        Args:
            memoria (dict): A memória a ser atualizada
            
        Returns:
            dict: A nova memória criada ou None
        """
        dados = self.persona._carregar_memorias()
        
        print(f"Atualizando memória específica: #{memoria['id']}")
        
        # Gera um conteúdo refinado para a memória
        # Em uma implementação mais avançada, isso poderia usar técnicas de NLP
        # ou combinar com outras memórias relacionadas
        conteudo_refinado = f"Versão melhorada e aprofundada: {memoria['conteudo']}"
        
        # Cria uma nova versão refinada
        nova_memoria = {
            "id": len(dados["memorias"]) + 1,
            "conteudo": conteudo_refinado,
            "criado_em": datetime.now().isoformat(),
            "versao": memoria.get("versao", 1) + 1,
            "origem": "refinamento_inteligente",
            "baseado_em": [memoria["id"]]
        }
        
        # Copia atributos relevantes da memória original
        if "contexto_emocional" in memoria:
            nova_memoria["contexto_emocional"] = memoria["contexto_emocional"].copy()
        
        if "padroes" in memoria:
            nova_memoria["padroes"] = memoria["padroes"].copy()
        
        # Armazena a nova versão
        self.persona.armazenar_memoria(nova_memoria, dados)
        
        return nova_memoria
    
    def _avaliar_qualidade_memoria(self, memoria):
        """Avalia a qualidade de uma memória específica.
        
        Esta é uma implementação simplificada que considera:
        - Comprimento do conteúdo
        - Origem da memória (sinteses internas são valorizadas)
        - Versão (memórias refinadas são mais valorizadas)
        
        Args:
            memoria (dict): A memória a ser avaliada
            
        Returns:
            int: Pontuação de qualidade (1-10)
        """
        pontuacao = 5  # Pontuação base
        
        # Avalia comprimento (maior conteúdo = mais informação)
        tamanho = len(memoria["conteudo"])
        if tamanho > 100:
            pontuacao += 2
        elif tamanho > 50:
            pontuacao += 1
        
        # Avalia origem
        origem = memoria.get("origem", "")
        if origem == "sintese_interna":
            pontuacao += 1
        elif origem == "refinamento_inteligente":
            pontuacao += 2
        elif origem == "aprofundamento_tematico":
            pontuacao += 3
        
        # Avalia versão
        versao = memoria.get("versao", 1)
        if versao > 1:
            pontuacao += versao - 1  # Adiciona pontos por cada refinamento
        
        # Avalia diversidade de processamento
        processamentos = 0
        if "contexto_emocional" in memoria:
            processamentos += 1
        if "consistencia" in memoria:
            processamentos += 1
        if "padroes" in memoria:
            processamentos += 1
        
        pontuacao += processamentos / 2  # Adiciona até 1.5 pontos por processamentos diversos
        
        # Garante que a pontuação está no intervalo 1-10
        return max(1, min(10, pontuacao))
    
    def _registrar_avaliacao(self, memoria, qualidade, dados):
        """Registra a avaliação de qualidade na memória.
        
        Args:
            memoria (dict): A memória avaliada
            qualidade (int): A pontuação de qualidade
            dados (dict): Os dados completos de memória
        """
        # Encontra a memória no conjunto de dados
        for idx, mem in enumerate(dados["memorias"]):
            if mem["id"] == memoria["id"]:
                # Adiciona ou atualiza o campo de avaliação
                dados["memorias"][idx]["avaliacao"] = {
                    "qualidade": qualidade,
                    "avaliado_em": datetime.now().isoformat(),
                    "revisao": self.metacognicoes_realizadas
                }
                
                # Se for de baixa qualidade, marca para revisão futura
                if qualidade < 4:
                    dados["memorias"][idx]["precisa_revisao"] = True
                
                # Salva as alterações
                self.persona._salvar_memorias(dados)
                break
    
    def atualizar_memorias(self):
        """Atualiza memórias baseado nas avaliações de metacognição.
        
        Este método revisa memórias que foram marcadas como de baixa qualidade
        e tenta refiná-las.
        """
        dados = self.persona._carregar_memorias()
        
        # Encontra memórias que precisam de revisão
        for memoria in dados["memorias"]:
            if memoria.get("precisa_revisao"):
                print(f"Atualizando memória de baixa qualidade: #{memoria['id']}")
                
                # Tenta refinar a memória
                conteudo_refinado = f"Versão melhorada de: {memoria['conteudo']}"
                
                # Cria uma nova versão refinada
                nova_memoria = {
                    "id": len(dados["memorias"]) + 1,
                    "conteudo": conteudo_refinado,
                    "criado_em": datetime.now().isoformat(),
                    "versao": memoria.get("versao", 1) + 1,
                    "origem": "refinamento_metacognitivo",
                    "baseado_em": [memoria["id"]]
                }
                
                # Armazena a nova versão
                self.persona.armazenar_memoria(nova_memoria, dados)
                
                # Remove a marcação de necessidade de revisão
                for idx, mem in enumerate(dados["memorias"]):
                    if mem["id"] == memoria["id"]:
                        dados["memorias"][idx]["precisa_revisao"] = False
                        self.persona._salvar_memorias(dados)
                        break 