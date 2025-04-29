"""
Módulo de Aprendizado Contínuo - Gerencia como o sistema aprende e evolui.

Este módulo implementa mecanismos para permitir que o sistema
aprenda com suas próprias reflexões e otimize seu processo de pensamento.
"""

import random
import asyncio
from datetime import datetime, timedelta
from collections import Counter

class GerenciadorAprendizado:
    def __init__(self, persona, alma):
        """Inicializa o gerenciador de aprendizado.
        
        Args:
            persona: Instância da classe Persona para acesso às memórias
            alma: Instância da classe Alma para acesso aos agentes
        """
        self.persona = persona
        self.alma = alma
        self.ciclos_realizados = 0
        self.estatisticas = {
            "ultima_otimizacao": datetime.now(),
            "agentes_efetivos": {},
            "temas_frequentes": Counter(),
            "qualidade_media": 0,
            "total_avaliacoes": 0
        }
        
        # Pesos iniciais para seleção de agentes
        self.pesos_agentes = {
            "reflexao": 0.5,    # 50% chance
            "metacognicao": 0.2, # 20% chance
            "emocional": 0.1,    # 10% chance
            "consistencia": 0.1, # 10% chance
            "padrao": 0.1        # 10% chance
        }
    
    async def otimizar_processo(self):
        """Avalia e otimiza o processo de pensamento do sistema.
        
        Esta função analisa os resultados produzidos pelos diferentes
        agentes e ajusta suas probabilidades de seleção conforme a eficácia.
        """
        print("\n=== Iniciando Otimização do Processo de Pensamento ===")
        
        # Atualiza estatísticas
        self.ciclos_realizados += 1
        
        # Carrega as memórias
        dados = self.persona._carregar_memorias()
        if not dados["memorias"]:
            print("Sem memórias suficientes para otimização")
            return False
        
        # Coleta estatísticas
        self._coletar_estatisticas(dados["memorias"])
        
        # Ajusta pesos dos agentes
        ajustes_realizados = self._ajustar_pesos_agentes()
        
        # Identifica áreas de foco
        areas_foco = self._identificar_areas_foco()
        
        print(f"Otimização concluída - Ciclo #{self.ciclos_realizados}")
        print(f"Pesos atualizados dos agentes: {self.pesos_agentes}")
        if areas_foco:
            print(f"Áreas de foco identificadas: {', '.join(areas_foco)}")
        
        print("=== Otimização do Processo Concluída ===\n")
        
        return True
    
    async def ciclo_aprendizado_continuo(self, intervalo=300):
        """Executa o ciclo de aprendizado contínuo.
        
        Args:
            intervalo (int): Intervalo em segundos entre otimizações
        """
        print(f"Iniciando ciclo de aprendizado contínuo a cada {intervalo} segundos")
        
        try:
            while True:
                # Aguarda acúmulo de experiência
                await asyncio.sleep(intervalo)
                
                # Executa otimização do processo
                await self.otimizar_processo()
                
                # Executa estratégias de aprendizado específicas
                await self._aplicar_estrategias_aprendizado()
        
        except asyncio.CancelledError:
            print("Ciclo de aprendizado contínuo interrompido")
            raise
    
    def _coletar_estatisticas(self, memorias):
        """Coleta estatísticas sobre as memórias e seu processamento.
        
        Args:
            memorias (list): Lista de memórias para análise
        """
        # Coleta temas frequentes
        for memoria in memorias:
            # Extrai palavras-chave do conteúdo
            conteudo = memoria.get("conteudo", "").lower()
            palavras = [p for p in conteudo.split() if len(p) > 4 and p not in ["combinando", "conceitos"]]
            for palavra in palavras:
                self.estatisticas["temas_frequentes"][palavra] += 1
        
        # Calcula qualidade média das memórias avaliadas
        memorias_avaliadas = [m for m in memorias if "avaliacao" in m]
        if memorias_avaliadas:
            total_qualidade = sum(m["avaliacao"]["qualidade"] for m in memorias_avaliadas)
            nova_media = total_qualidade / len(memorias_avaliadas)
            
            # Atualiza média ponderada
            if self.estatisticas["total_avaliacoes"] > 0:
                self.estatisticas["qualidade_media"] = (
                    (self.estatisticas["qualidade_media"] * self.estatisticas["total_avaliacoes"] + 
                     nova_media * len(memorias_avaliadas)) / 
                    (self.estatisticas["total_avaliacoes"] + len(memorias_avaliadas))
                )
            else:
                self.estatisticas["qualidade_media"] = nova_media
            
            self.estatisticas["total_avaliacoes"] += len(memorias_avaliadas)
        
        # Avalia eficácia dos diferentes agentes
        # (simplificado - na prática, precisaria de métricas mais complexas)
        self.estatisticas["agentes_efetivos"] = {
            "reflexao": sum(1 for m in memorias if m.get("origem") == "sintese_interna"),
            "emocional": sum(1 for m in memorias if "contexto_emocional" in m),
            "consistencia": sum(1 for m in memorias if "consistencia" in m),
            "padrao": sum(1 for m in memorias if "padroes" in m),
            "metacognicao": sum(1 for m in memorias if "avaliacao" in m)
        }
    
    def _ajustar_pesos_agentes(self):
        """Ajusta os pesos dos agentes com base na eficácia observada.
        
        Returns:
            bool: True se ajustes foram realizados
        """
        # Obtém contagens de eficácia
        efetividade = self.estatisticas["agentes_efetivos"]
        
        # Soma total para normalização
        total = sum(efetividade.values())
        
        if total == 0:
            return False
        
        # Calcula novos pesos (mistura com os pesos anteriores para suavizar mudanças)
        novos_pesos = {}
        for agente, contagem in efetividade.items():
            # 70% peso anterior + 30% nova efetividade
            novos_pesos[agente] = 0.7 * self.pesos_agentes.get(agente, 0.1) + 0.3 * (contagem / total)
        
        # Normaliza para garantir soma = 1
        soma_pesos = sum(novos_pesos.values())
        for agente in novos_pesos:
            novos_pesos[agente] /= soma_pesos
        
        # Atualiza pesos
        self.pesos_agentes = novos_pesos
        
        # Registra momento da otimização
        self.estatisticas["ultima_otimizacao"] = datetime.now()
        
        return True
    
    def _identificar_areas_foco(self):
        """Identifica áreas temáticas para focar o aprendizado.
        
        Returns:
            list: Lista de temas prioritários
        """
        # Obtém os temas mais frequentes (top 5)
        temas_comuns = [tema for tema, _ in self.estatisticas["temas_frequentes"].most_common(5)]
        
        return temas_comuns
    
    async def _aplicar_estrategias_aprendizado(self):
        """Aplica estratégias específicas de aprendizado após otimização.
        
        Esta função implementa abordagens específicas para melhorar o aprendizado,
        como revisão de memórias de baixa qualidade.
        """
        # Carrega memórias
        dados = self.persona._carregar_memorias()
        
        # Estratégia 1: Revisar memórias de baixa qualidade
        memorias_baixa_qualidade = [
            m for m in dados["memorias"] 
            if "avaliacao" in m and m["avaliacao"]["qualidade"] < 4
        ]
        
        if memorias_baixa_qualidade:
            print(f"Aplicando estratégia de revisão para {len(memorias_baixa_qualidade)} memórias de baixa qualidade")
            # Escolhe uma memória aleatória para revisar
            memoria = random.choice(memorias_baixa_qualidade)
            await self.alma.atualizar_memoria_especifica(memoria)
        
        # Estratégia 2: Reforçar aprendizado sobre temas frequentes
        areas_foco = self._identificar_areas_foco()
        if areas_foco:
            tema = random.choice(areas_foco)
            print(f"Reforçando aprendizado sobre tema frequente: {tema}")
            
            # Busca memórias relacionadas ao tema
            memorias_relacionadas = [
                m for m in dados["memorias"]
                if tema.lower() in m.get("conteudo", "").lower()
            ]
            
            # Se encontrou memórias suficientes, gera uma síntese especial
            if len(memorias_relacionadas) >= 2:
                memorias_escolhidas = random.sample(memorias_relacionadas, min(3, len(memorias_relacionadas)))
                conteudos = [m["conteudo"] for m in memorias_escolhidas]
                
                # Gera uma síntese aprofundada
                sintese = f"Aprofundamento sobre '{tema}': Integrando conceitos de: {' e '.join(conteudos)}"
                
                # Cria nova memória com a síntese
                nova_memoria = {
                    "id": len(dados["memorias"]) + 1,
                    "conteudo": sintese,
                    "criado_em": datetime.now().isoformat(),
                    "versao": 1,
                    "origem": "aprofundamento_tematico",
                    "baseado_em": [m["id"] for m in memorias_escolhidas],
                    "tema_aprofundado": tema
                }
                
                # Armazena a síntese
                self.persona.armazenar_memoria(nova_memoria, dados)
    
    def selecionar_agente(self):
        """Seleciona um agente com base nos pesos otimizados.
        
        Returns:
            str: Nome do agente selecionado
        """
        # Separar nomes e pesos
        agentes = list(self.pesos_agentes.keys())
        pesos = list(self.pesos_agentes.values())
        
        # Selecionar usando distribuição de probabilidade
        return random.choices(agentes, weights=pesos, k=1)[0] 