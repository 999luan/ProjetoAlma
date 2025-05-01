"""
Módulo de Aprendizado Adaptativo - Implementando a Fase 5.

Este módulo amplia o aprendizado do sistema com capacidades avançadas de
auto-otimização, experimentação com estratégias de pensamento e
adaptação autônoma baseada na análise de resultados.
"""

import random
import asyncio
import json
import os
from datetime import datetime
from collections import Counter, defaultdict
import numpy as np
from pathlib import Path

class AprendizadoAdaptativo:
    def __init__(self, persona, alma, gerenciador_aprendizado):
        """Inicializa o aprendizado adaptativo.
        
        Args:
            persona: Instância da classe Persona
            alma: Instância da classe Alma
            gerenciador_aprendizado: Instância do GerenciadorAprendizado
        """
        self.persona = persona
        self.alma = alma
        self.gerenciador = gerenciador_aprendizado
        self.ciclos_adaptacao = 0
        
        # Controle de experimentos
        self.experimentos_ativos = {}
        self.resultados_experimentos = []
        
        # Histórico de métricas para análise de tendências
        self.historico_metricas = {
            "qualidade_media": [],
            "diversidade_temas": [],
            "eficiencia_agentes": {},
            "tempos": []
        }
        
        # Estratégias aprendidas
        self.estrategias_efetivas = []
        
        # Caminho para armazenar dados de aprendizado
        self.data_path = Path("data/adaptive_learning")
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    async def iniciar_ciclo_adaptativo(self, intervalo=600):
        """Inicia o ciclo de aprendizado adaptativo.
        
        Args:
            intervalo (int): Intervalo em segundos entre ciclos
        """
        print(f"Iniciando ciclo de aprendizado adaptativo a cada {intervalo} segundos")
        
        try:
            while True:
                # Aguarda o intervalo entre ciclos
                await asyncio.sleep(intervalo)
                
                # Executa um ciclo de adaptação
                await self.executar_ciclo_adaptacao()
                
                # Salva o estado atual do aprendizado
                self._salvar_estado_aprendizado()
        except asyncio.CancelledError:
            print("Ciclo de aprendizado adaptativo interrompido")
            raise
    
    async def executar_ciclo_adaptacao(self):
        """Executa um ciclo completo de adaptação do sistema de aprendizado."""
        inicio = datetime.now()
        print("\n=== Iniciando Ciclo de Adaptação ===")
        self.ciclos_adaptacao += 1
        
        # Coleta e análise de métricas do sistema
        metricas = await self._analisar_metricas_sistema()
        
        # Identifica tendências e padrões no aprendizado
        tendencias = self._identificar_tendencias(metricas)
        
        # Toma decisões adaptativas baseadas nas tendências
        if tendencias["declinio_qualidade"]:
            await self._intervir_declinio_qualidade()
        
        if tendencias["estagnacao_temas"]:
            await self._estimular_diversidade()
        
        # Gestão de experimentos de aprendizado
        await self._gerenciar_experimentos()
        
        # Aplicação de estratégias aprendidas
        await self._aplicar_estrategias_efetivas()
        
        # Registra tempo de execução
        tempo_execucao = (datetime.now() - inicio).total_seconds()
        self.historico_metricas["tempos"].append(tempo_execucao)
        
        print(f"Ciclo de adaptação #{self.ciclos_adaptacao} concluído em {tempo_execucao:.2f} segundos")
        print(f"Tendências identificadas: {', '.join(t for t, v in tendencias.items() if v)}")
        print("=== Ciclo de Adaptação Concluído ===\n")
        
        return True
    
    async def _analisar_metricas_sistema(self):
        """Analisa métricas do sistema para identificar o estado atual.
        
        Returns:
            dict: Conjunto de métricas relevantes
        """
        # Carrega as memórias
        dados = self.persona._carregar_memorias()
        if not dados["memorias"]:
            return {}
        
        # Calcula qualidade média
        memorias_avaliadas = [m for m in dados["memorias"] if "avaliacao" in m]
        qualidade_media = 0
        if memorias_avaliadas:
            qualidade_media = sum(m["avaliacao"]["qualidade"] for m in memorias_avaliadas) / len(memorias_avaliadas)
            self.historico_metricas["qualidade_media"].append(qualidade_media)
        
        # Calcula diversidade de temas
        temas = Counter()
        for memoria in dados["memorias"]:
            conteudo = memoria.get("conteudo", "").lower()
            palavras = [w for w in conteudo.split() if len(w) > 4 and w not in ["combinando", "conceitos", "sobre"]]
            temas.update(palavras)
        
        n_temas_significativos = len([t for t, c in temas.items() if c >= 3])
        self.historico_metricas["diversidade_temas"].append(n_temas_significativos)
        
        # Eficiência dos agentes
        eficiencia = self.gerenciador.estatisticas["agentes_efetivos"]
        
        # Registra eficiência histórica
        for agente, valor in eficiencia.items():
            if agente not in self.historico_metricas["eficiencia_agentes"]:
                self.historico_metricas["eficiencia_agentes"][agente] = []
            self.historico_metricas["eficiencia_agentes"][agente].append(valor)
        
        # Calcula métricas adicionais
        n_memorias_total = len(dados["memorias"])
        n_memorias_processadas = len([m for m in dados["memorias"] if m.get("processada", False)])
        taxa_processamento = n_memorias_processadas / n_memorias_total if n_memorias_total > 0 else 0
        
        # Retorna métricas coletadas
        return {
            "qualidade_media": qualidade_media,
            "diversidade_temas": n_temas_significativos,
            "n_memorias": n_memorias_total,
            "n_memorias_processadas": n_memorias_processadas,
            "taxa_processamento": taxa_processamento,
            "eficiencia_agentes": eficiencia,
            "ciclos_adaptacao": self.ciclos_adaptacao,
            "experimentos_ativos": len(self.experimentos_ativos),
            "estrategias_aprendidas": len(self.estrategias_efetivas),
            "timestamp": datetime.now().isoformat()
        }
    
    def _identificar_tendencias(self, metricas):
        """Identifica tendências significativas nas métricas.
        
        Args:
            metricas (dict): Métricas atuais do sistema
            
        Returns:
            dict: Tendências identificadas
        """
        tendencias = {
            "declinio_qualidade": False,
            "estagnacao_temas": False,
            "concentracao_agentes": False,
            "crescimento_acelerado": False,
            "processamento_lento": False
        }
        
        # Declínio de qualidade (3 ciclos consecutivos)
        if len(self.historico_metricas["qualidade_media"]) >= 3:
            ultimas_qualidades = self.historico_metricas["qualidade_media"][-3:]
            if all(ultimas_qualidades[i] > ultimas_qualidades[i+1] for i in range(len(ultimas_qualidades)-1)):
                tendencias["declinio_qualidade"] = True
        
        # Estagnação de temas (último valor igual ou menor que média anterior)
        if len(self.historico_metricas["diversidade_temas"]) >= 3:
            ultimos_temas = self.historico_metricas["diversidade_temas"][-3:]
            media_anterior = sum(ultimos_temas[:-1]) / len(ultimos_temas[:-1])
            if ultimos_temas[-1] <= media_anterior:
                tendencias["estagnacao_temas"] = True
        
        # Concentração em poucos agentes
        if metricas.get("eficiencia_agentes"):
            eficiencia = metricas["eficiencia_agentes"]
            total = sum(eficiencia.values())
            if total > 0:
                # Se um único agente é responsável por mais de 70% das memórias
                for agente, valor in eficiencia.items():
                    if valor / total > 0.7:
                        tendencias["concentracao_agentes"] = True
                        break
        
        # Tempos de processamento crescentes
        if len(self.historico_metricas["tempos"]) >= 3:
            ultimos_tempos = self.historico_metricas["tempos"][-3:]
            if all(ultimos_tempos[i] < ultimos_tempos[i+1] for i in range(len(ultimos_tempos)-1)):
                tendencias["processamento_lento"] = True
        
        return tendencias
    
    async def _intervir_declinio_qualidade(self):
        """Intervém quando há declínio de qualidade das memórias."""
        print("Executando intervenção para reverter declínio de qualidade")
        
        # Estratégia 1: Aumenta peso do agente metacognitivo temporariamente
        pesos_originais = self.gerenciador.pesos_agentes.copy()
        if "metacognicao" in self.gerenciador.pesos_agentes:
            # Duplica o peso atual da metacognição
            peso_atual = self.gerenciador.pesos_agentes["metacognicao"]
            self.gerenciador.pesos_agentes["metacognicao"] = min(0.5, peso_atual * 2)
            
            # Normaliza os outros pesos
            soma = sum(self.gerenciador.pesos_agentes.values())
            for agente in self.gerenciador.pesos_agentes:
                self.gerenciador.pesos_agentes[agente] /= soma
            
            print(f"Peso do agente metacognitivo aumentado temporariamente para {self.gerenciador.pesos_agentes['metacognicao']:.2f}")
        
        # Estratégia 2: Executa um ciclo de metacognição agora
        await self.alma.ativar_agente_metacognicao()
        
        # Registra a intervenção como experimento
        self._registrar_experimento(
            "aumentar_metacognicao",
            "Aumentar peso do agente metacognitivo para lidar com declínio de qualidade",
            pesos_originais,
            self.gerenciador.pesos_agentes.copy()
        )
    
    async def _estimular_diversidade(self):
        """Estimula diversidade de temas quando há estagnação."""
        print("Executando estratégia para estimular diversidade de temas")
        
        # Estratégia: Criar algumas memórias sobre temas pouco explorados
        dados = self.persona._carregar_memorias()
        
        # Identifica temas pouco explorados (palavras únicas que aparecem poucas vezes)
        todas_palavras = []
        for memoria in dados["memorias"]:
            conteudo = memoria.get("conteudo", "").lower()
            palavras = [w for w in conteudo.split() if len(w) > 4 and w not in ["combinando", "conceitos", "sobre"]]
            todas_palavras.extend(palavras)
        
        contagem = Counter(todas_palavras)
        
        # Temas raros: aparecem entre 1-2 vezes
        temas_raros = [tema for tema, cont in contagem.items() if 1 <= cont <= 2]
        
        if temas_raros:
            # Escolhe um tema raro para explorar
            tema = random.choice(temas_raros)
            print(f"Estimulando diversidade explorando tema raro: '{tema}'")
            
            # Busca memórias que mencionam este tema
            memorias_relacionadas = [
                m for m in dados["memorias"]
                if tema.lower() in m.get("conteudo", "").lower()
            ]
            
            # Cria uma nova síntese especial aprofundando este tema
            if memorias_relacionadas:
                memoria_base = memorias_relacionadas[0]
                conteudo = f"Exploração de conceito raro '{tema}': {memoria_base['conteudo']}"
                
                # Cria uma nova memória exploratória
                nova_memoria = {
                    "id": len(dados["memorias"]) + 1,
                    "conteudo": conteudo,
                    "criado_em": datetime.now().isoformat(),
                    "versao": 1,
                    "origem": "exploracao_tematica",
                    "baseado_em": [memoria_base["id"]],
                    "tema_explorado": tema
                }
                
                # Armazena a síntese
                self.persona.armazenar_memoria(nova_memoria, dados)
    
    async def _gerenciar_experimentos(self):
        """Gerencia experimentos de aprendizado, avaliando resultados e aplicando estratégias bem-sucedidas."""
        # Verifica experimentos ativos
        experimentos_concluidos = []
        for exp_id, experimento in list(self.experimentos_ativos.items()):
            # Se o experimento já durou o suficiente para avaliação
            if experimento["ciclos_decorridos"] >= experimento["ciclos_planejados"]:
                print(f"Avaliando resultados do experimento: {experimento['descricao']}")
                
                # Avalia resultados
                metricas_atuais = await self._analisar_metricas_sistema()
                avaliacao = self._avaliar_resultado_experimento(experimento, metricas_atuais)
                
                # Registra conclusões
                experimento["resultado"] = avaliacao
                experimento["concluido_em"] = datetime.now().isoformat()
                self.resultados_experimentos.append(experimento)
                
                # Se o experimento foi positivo, adiciona à lista de estratégias efetivas
                if avaliacao["impacto"] > 0:
                    self.estrategias_efetivas.append({
                        "tipo": experimento["tipo"],
                        "descricao": experimento["descricao"],
                        "impacto": avaliacao["impacto"],
                        "configuracao": experimento["configuracao_nova"]
                    })
                    print(f"Experimento {exp_id} concluído com sucesso, adicionado às estratégias efetivas")
                else:
                    # Reverte configurações se o resultado não foi positivo
                    if experimento["tipo"] == "aumentar_metacognicao":
                        self.gerenciador.pesos_agentes = experimento["configuracao_original"]
                        print("Revertendo configurações do experimento não bem-sucedido")
                
                experimentos_concluidos.append(exp_id)
            else:
                # Incrementa o contador de ciclos
                self.experimentos_ativos[exp_id]["ciclos_decorridos"] += 1
        
        # Remove experimentos concluídos
        for exp_id in experimentos_concluidos:
            del self.experimentos_ativos[exp_id]
        
        # Inicia novos experimentos se não houver muitos ativos
        if len(self.experimentos_ativos) < 2 and random.random() < 0.3:  # 30% de chance
            await self._iniciar_novo_experimento()
    
    def _avaliar_resultado_experimento(self, experimento, metricas_atuais):
        """Avalia o resultado de um experimento.
        
        Args:
            experimento (dict): O experimento a avaliar
            metricas_atuais (dict): Métricas atuais do sistema
            
        Returns:
            dict: Avaliação do impacto do experimento
        """
        # Compara métricas antes e depois
        impacto = 0
        
        # Para experimentos de qualidade
        if experimento["tipo"] == "aumentar_metacognicao":
            # Verifica se houve aumento de qualidade
            if len(self.historico_metricas["qualidade_media"]) >= 3:
                antes = self.historico_metricas["qualidade_media"][-experimento["ciclos_decorridos"]-1]
                depois = metricas_atuais["qualidade_media"]
                impacto = depois - antes
        
        # Para experimentos de diversidade
        elif experimento["tipo"] == "estimular_diversidade":
            if len(self.historico_metricas["diversidade_temas"]) >= 3:
                antes = self.historico_metricas["diversidade_temas"][-experimento["ciclos_decorridos"]-1]
                depois = metricas_atuais["diversidade_temas"]
                impacto = (depois - antes) / max(1, antes)  # Impacto relativo
        
        return {
            "impacto": impacto,
            "metricas_iniciais": experimento.get("metricas_iniciais", {}),
            "metricas_finais": metricas_atuais,
            "analise": "Positivo" if impacto > 0 else "Negativo"
        }
    
    async def _iniciar_novo_experimento(self):
        """Inicia um novo experimento de adaptação."""
        # Tipos de experimentos disponíveis
        tipos_experimentos = [
            "ajuste_pesos_agentes",
            "estimular_tema_especifico",
            "revisar_memorias_antigas"
        ]
        
        tipo = random.choice(tipos_experimentos)
        exp_id = f"exp_{self.ciclos_adaptacao}_{tipo}"
        
        metricas_iniciais = await self._analisar_metricas_sistema()
        
        if tipo == "ajuste_pesos_agentes":
            # Experimento: ajustar pesos dos agentes temporariamente
            pesos_originais = self.gerenciador.pesos_agentes.copy()
            
            # Escolhe um agente aleatório para aumentar seu peso
            agente = random.choice(list(pesos_originais.keys()))
            aumento = random.uniform(0.1, 0.3)
            
            novos_pesos = pesos_originais.copy()
            novos_pesos[agente] += aumento
            
            # Normaliza
            soma = sum(novos_pesos.values())
            for a in novos_pesos:
                novos_pesos[a] /= soma
            
            # Aplica modificação
            self.gerenciador.pesos_agentes = novos_pesos
            
            descricao = f"Aumento do peso do agente {agente} em {aumento:.2f}"
            print(f"Iniciando experimento: {descricao}")
            
            self.experimentos_ativos[exp_id] = {
                "tipo": tipo,
                "descricao": descricao,
                "iniciado_em": datetime.now().isoformat(),
                "ciclos_planejados": 3,
                "ciclos_decorridos": 0,
                "configuracao_original": pesos_originais,
                "configuracao_nova": novos_pesos,
                "metricas_iniciais": metricas_iniciais
            }
        
        elif tipo == "estimular_tema_especifico":
            # Experimento: focar em um tema específico por alguns ciclos
            dados = self.persona._carregar_memorias()
            
            # Extrai temas de todas as memórias
            todas_palavras = []
            for memoria in dados["memorias"]:
                conteudo = memoria.get("conteudo", "").lower()
                palavras = [w for w in conteudo.split() if len(w) > 4 and w not in ["combinando", "conceitos", "sobre"]]
                todas_palavras.extend(palavras)
            
            contagem = Counter(todas_palavras)
            
            # Escolhe um tema com frequência média para explorar
            temas_medios = [tema for tema, cont in contagem.items() if 3 <= cont <= 5]
            
            if temas_medios:
                tema = random.choice(temas_medios)
                descricao = f"Explorando tema específico: '{tema}'"
                print(f"Iniciando experimento: {descricao}")
                
                self.experimentos_ativos[exp_id] = {
                    "tipo": tipo,
                    "descricao": descricao,
                    "tema": tema,
                    "iniciado_em": datetime.now().isoformat(),
                    "ciclos_planejados": 3,
                    "ciclos_decorridos": 0,
                    "metricas_iniciais": metricas_iniciais
                }
                
                # Cria uma memória inicial sobre o tema
                await self._criar_memoria_tematica(tema, dados)
        
        elif tipo == "revisar_memorias_antigas":
            # Experimento: revisar memórias mais antigas para atualizá-las
            dados = self.persona._carregar_memorias()
            
            # Ordena memórias por data de criação
            memorias_ordenadas = sorted(
                dados["memorias"], 
                key=lambda m: m.get("criado_em", "2000-01-01")
            )
            
            # Pega as memórias mais antigas (primeiros 20%)
            n_antigas = max(1, int(len(memorias_ordenadas) * 0.2))
            antigas = memorias_ordenadas[:n_antigas]
            
            if antigas:
                # Escolhe uma aleatoriamente
                memoria = random.choice(antigas)
                
                descricao = f"Revisão de memórias antigas (ID #{memoria['id']})"
                print(f"Iniciando experimento: {descricao}")
                
                self.experimentos_ativos[exp_id] = {
                    "tipo": tipo,
                    "descricao": descricao,
                    "memoria_id": memoria["id"],
                    "iniciado_em": datetime.now().isoformat(),
                    "ciclos_planejados": 2,
                    "ciclos_decorridos": 0,
                    "metricas_iniciais": metricas_iniciais
                }
                
                # Atualiza a memória
                await self.alma.atualizar_memoria_especifica(memoria)
    
    async def _criar_memoria_tematica(self, tema, dados):
        """Cria uma nova memória focada em um tema específico.
        
        Args:
            tema (str): O tema a explorar
            dados (dict): Dados de memória
        """
        # Busca memórias relacionadas ao tema
        memorias_relacionadas = [
            m for m in dados["memorias"]
            if tema.lower() in m.get("conteudo", "").lower()
        ]
        
        if memorias_relacionadas:
            # Escolhe 1-2 memórias aleatórias relacionadas
            n_escolher = min(len(memorias_relacionadas), random.randint(1, 2))
            escolhidas = random.sample(memorias_relacionadas, n_escolher)
            
            # Gera conteúdo com foco no tema
            conteudo = f"Exploração aprofundada do conceito '{tema}': "
            conteudo += " ".join([m["conteudo"] for m in escolhidas])
            
            # Cria nova memória
            nova_memoria = {
                "id": len(dados["memorias"]) + 1,
                "conteudo": conteudo,
                "criado_em": datetime.now().isoformat(),
                "versao": 1,
                "origem": "exploracao_experimental",
                "baseado_em": [m["id"] for m in escolhidas],
                "tema_experimental": tema
            }
            
            # Armazena a nova memória
            self.persona.armazenar_memoria(nova_memoria, dados)
    
    async def _aplicar_estrategias_efetivas(self):
        """Aplica estratégias que foram consideradas efetivas em experimentos anteriores."""
        if not self.estrategias_efetivas:
            return
        
        # Escolhe uma estratégia aleatoriamente, dando mais peso às mais efetivas
        pesos = [max(0.1, s["impacto"]) for s in self.estrategias_efetivas]
        estrategia = random.choices(self.estrategias_efetivas, weights=pesos, k=1)[0]
        
        print(f"Aplicando estratégia efetiva: {estrategia['descricao']}")
        
        # Aplica a estratégia de acordo com seu tipo
        if estrategia["tipo"] == "aumentar_metacognicao":
            # Aplica configuração de pesos já testada
            self.gerenciador.pesos_agentes = estrategia["configuracao"].copy()
        
        # Outros tipos de estratégias podem ser implementados aqui
    
    def _registrar_experimento(self, tipo, descricao, config_original, config_nova):
        """Registra um novo experimento.
        
        Args:
            tipo (str): Tipo do experimento
            descricao (str): Descrição do experimento
            config_original (dict): Configuração original
            config_nova (dict): Nova configuração
        """
        exp_id = f"exp_{self.ciclos_adaptacao}_{tipo}"
        
        self.experimentos_ativos[exp_id] = {
            "tipo": tipo,
            "descricao": descricao,
            "iniciado_em": datetime.now().isoformat(),
            "ciclos_planejados": 3,
            "ciclos_decorridos": 0,
            "configuracao_original": config_original,
            "configuracao_nova": config_nova
        }
    
    def _salvar_estado_aprendizado(self):
        """Salva o estado atual do aprendizado adaptativo."""
        estado = {
            "timestamp": datetime.now().isoformat(),
            "ciclos_adaptacao": self.ciclos_adaptacao,
            "historico_metricas": {
                "qualidade_media": self.historico_metricas["qualidade_media"][-10:],
                "diversidade_temas": self.historico_metricas["diversidade_temas"][-10:],
                "tempos": self.historico_metricas["tempos"][-10:]
            },
            "experimentos_ativos": self.experimentos_ativos,
            "resultados_experimentos": self.resultados_experimentos[-20:],
            "estrategias_efetivas": self.estrategias_efetivas
        }
        
        # Salva o arquivo
        caminho = self.data_path / "estado_aprendizado.json"
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(estado, f, ensure_ascii=False, indent=2)
        
        print(f"Estado do aprendizado adaptativo salvo em {caminho}")
    
    def carregar_estado_aprendizado(self):
        """Carrega o estado de aprendizado adaptativo anterior, se existir."""
        caminho = self.data_path / "estado_aprendizado.json"
        
        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    estado = json.load(f)
                
                self.ciclos_adaptacao = estado.get("ciclos_adaptacao", 0)
                
                # Carrega métricas históricas
                for chave in ["qualidade_media", "diversidade_temas", "tempos"]:
                    if chave in estado.get("historico_metricas", {}):
                        self.historico_metricas[chave] = estado["historico_metricas"][chave]
                
                # Carrega experimentos e estratégias
                self.resultados_experimentos = estado.get("resultados_experimentos", [])
                self.estrategias_efetivas = estado.get("estrategias_efetivas", [])
                
                print(f"Estado do aprendizado adaptativo carregado de {caminho}")
                return True
            except Exception as e:
                print(f"Erro ao carregar estado do aprendizado: {e}")
        
        return False 