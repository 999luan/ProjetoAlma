"""
Módulo Memoria - Responsável por armazenar e gerenciar memórias.

Este módulo implementa o sistema de armazenamento e gerenciamento de memórias,
incluindo funcionalidades de busca, integração e síntese.
"""

import json
import os
import random
import logging
from datetime import datetime
import asyncio

# Importa o módulo de análise semântica avançada
try:
    from core.nlp_enhancement import analisador_semantico
    ANALISE_SEMANTICA_DISPONIVEL = True
except ImportError:
    ANALISE_SEMANTICA_DISPONIVEL = False

# Configuração de logging
logger = logging.getLogger(__name__)

class Memoria:
    def __init__(self, memoria_path="core/memoria.json"):
        """
        Inicializa o sistema de memória.
        
        Args:
            memoria_path (str): Caminho para o arquivo de memórias
        """
        self.memoria_path = memoria_path
        self._inicializar_memoria()
        self.analise_semantica_ativa = ANALISE_SEMANTICA_DISPONIVEL
        self._analisador_inicializado = False
    
    async def inicializar(self):
        """Inicializa o sistema de memória de forma assíncrona."""
        if self.analise_semantica_ativa and not self._analisador_inicializado:
            try:
                success = await analisador_semantico.inicializar_recursos()
                if success:
                    logger.info("Analisador semântico avançado inicializado com sucesso")
                    self._analisador_inicializado = True
                else:
                    logger.warning("Não foi possível inicializar o analisador semântico avançado")
                    self.analise_semantica_ativa = False
            except Exception as e:
                logger.error(f"Erro ao inicializar analisador semântico: {e}")
                self.analise_semantica_ativa = False
        return self
    
    def _inicializar_memoria(self):
        """Inicializa o arquivo de memória se ele não existir."""
        if not os.path.exists(self.memoria_path):
            diretorio = os.path.dirname(self.memoria_path)
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)
            
            # Cria um arquivo de memória vazio com estrutura básica
            with open(self.memoria_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "memorias": [],
                    "meta": {
                        "criado_em": datetime.now().isoformat(),
                        "versao": "1.0"
                    }
                }, f, ensure_ascii=False, indent=2)
            print(f"Arquivo de memória criado em: {self.memoria_path}")
    
    def _carregar_memorias(self):
        """Carrega as memórias do arquivo JSON.
        
        Returns:
            dict: O conteúdo do arquivo de memórias
        """
        try:
            with open(self.memoria_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar memórias: {e}")
            return {"memorias": [], "meta": {"criado_em": datetime.now().isoformat(), "versao": "1.0"}}
    
    def _salvar_memorias(self, dados):
        """Salva as memórias no arquivo JSON.
        
        Args:
            dados (dict): Os dados a serem salvos
        """
        try:
            with open(self.memoria_path, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar memórias: {e}")
    
    def receber_informacao(self, info):
        """Recebe uma nova informação e inicia o processo de integração.
        
        Args:
            info (str): A informação recebida
            
        Returns:
            bool: True se a informação foi processada com sucesso
        """
        if not info or not isinstance(info, str):
            print("Informação inválida recebida")
            return False
        
        print(f"Recebendo informação: '{info}'")
        return self.integrar_informacao(info)
    
    async def integrar_informacao_avancada(self, info):
        """Versão avançada de integração usando NLP.
        
        Args:
            info (str): A informação a ser integrada
            
        Returns:
            bool: True se a informação foi integrada com sucesso
        """
        # Verifica se a análise semântica está disponível
        if not self.analise_semantica_ativa:
            # Fallback para método padrão
            return self.integrar_informacao(info)
        
        try:
            dados = self._carregar_memorias()
            
            # Extrai palavras-chave da nova informação
            palavras_chave = await analisador_semantico.extrair_palavras_chave(info)
            
            # Analisa o sentimento do texto
            sentimento = await analisador_semantico.analisar_sentimento(info)
            
            # Extrai entidades
            entidades = await analisador_semantico.extrair_entidades(info)
            
            # Busca memórias similares
            memoria_mais_similar = None
            maior_similaridade = 0.0
            
            for memoria in dados["memorias"]:
                similaridade = await analisador_semantico.calcular_similaridade_semantica(
                    info, memoria["conteudo"], metodo="embeddings"
                )
                
                if similaridade > 0.7 and similaridade > maior_similaridade:  # Limiar ajustável
                    maior_similaridade = similaridade
                    memoria_mais_similar = memoria
            
            # Cria a nova memória com enriquecimento semântico
            nova_memoria = {
                "id": len(dados["memorias"]) + 1,
                "conteudo": info,
                "criado_em": datetime.now().isoformat(),
                "versao": 1,
                "origem": "externa",
                "analise_semantica": {
                    "palavras_chave": palavras_chave,
                    "sentimento": sentimento,
                    "entidades": entidades
                }
            }
            
            if memoria_mais_similar:
                # Analisa se há contradições
                contradicoes = await analisador_semantico.encontrar_contradicoes(
                    nova_memoria, memoria_mais_similar
                )
                
                # Adiciona informações de relação e contradição
                nova_memoria["relacionado_a"] = memoria_mais_similar["id"]
                nova_memoria["similaridade"] = maior_similaridade
                nova_memoria["contradicao"] = contradicoes["encontrou_contradicao"]
                nova_memoria["versao"] = memoria_mais_similar["versao"] + 1
                nova_memoria["evolucao"] = "Refinamento semântico de memória anterior"
                
                # Se for uma contradição, registra isso
                if contradicoes["encontrou_contradicao"]:
                    nova_memoria["resolucao_contradicao"] = "A informação mais recente tem precedência"
                    nova_memoria["sentencas_contraditorias"] = contradicoes.get("sentencas_contraditorias", [])
            
            # Armazena a memória enriquecida
            self.armazenar_memoria(nova_memoria, dados)
            logger.info(f"Memória integrada com análise semântica avançada (ID: {nova_memoria['id']})")
            return True
            
        except Exception as e:
            logger.error(f"Erro na integração semântica avançada: {e}")
            # Fallback para método padrão em caso de erro
            return self.integrar_informacao(info)
    
    def integrar_informacao(self, info):
        """Compara com memórias anteriores, ajusta ou cria uma nova memória.
        
        Args:
            info (str): A informação a ser integrada
            
        Returns:
            bool: True se a informação foi integrada com sucesso
        """
        # Se a análise semântica estiver disponível, tenta usar o método avançado
        if self.analise_semantica_ativa:
            asyncio.create_task(self.integrar_informacao_avancada(info))
            return True
        
        # Continua com o método tradicional
        dados = self._carregar_memorias()
        memoria_existente = self._buscar_memoria_similar(dados["memorias"], info)
        
        nova_memoria = {
            "id": len(dados["memorias"]) + 1,
            "conteudo": info,
            "criado_em": datetime.now().isoformat(),
            "versao": 1,
            "origem": "externa"
        }
        
        if memoria_existente:
            # Se encontrou uma memória similar, cria uma versão refinada
            print(f"Memória similar encontrada: '{memoria_existente['conteudo']}'")
            nova_memoria["relacionado_a"] = memoria_existente["id"]
            nova_memoria["versao"] = memoria_existente["versao"] + 1
            nova_memoria["evolucao"] = "Refinamento de memória anterior"
        else:
            print("Nova memória independente criada")
        
        self.armazenar_memoria(nova_memoria, dados)
        return True
    
    def _buscar_memoria_similar(self, memorias, info):
        """Busca uma memória similar à informação fornecida.
        
        Esta é uma implementação simplificada que verifica palavras em comum.
        
        Args:
            memorias (list): Lista de memórias para buscar
            info (str): Informação para comparar
            
        Returns:
            dict: Memória similar ou None se não encontrar
        """
        if not memorias:
            return None
        
        # Extrai palavras significativas (ignorando palavras muito comuns)
        palavras_info = set(w.lower() for w in info.split() if len(w) > 3)
        if not palavras_info:
            return None
        
        melhor_correspondencia = None
        melhor_pontuacao = 0
        
        for memoria in memorias:
            palavras_memoria = set(w.lower() for w in memoria["conteudo"].split() if len(w) > 3)
            
            # Calcular interseção de palavras
            comum = palavras_info.intersection(palavras_memoria)
            if comum:
                pontuacao = len(comum) / max(len(palavras_info), len(palavras_memoria))
                if pontuacao > 0.3 and pontuacao > melhor_pontuacao:  # Limiar de 30% de similaridade
                    melhor_correspondencia = memoria
                    melhor_pontuacao = pontuacao
        
        return melhor_correspondencia
    
    def armazenar_memoria(self, memoria, dados=None):
        """Armazena uma nova memória no sistema.
        
        Args:
            memoria (dict): A memória a ser armazenada
            dados (dict, optional): Dados já carregados ou None para carregar
            
        Returns:
            bool: True se a memória foi armazenada com sucesso
        """
        if dados is None:
            dados = self._carregar_memorias()
        
        dados["memorias"].append(memoria)
        dados["meta"]["ultima_atualizacao"] = datetime.now().isoformat()
        dados["meta"]["total_memorias"] = len(dados["memorias"])
        
        self._salvar_memorias(dados)
        print(f"Memória armazenada com ID: {memoria['id']}")
        return True
    
    async def gerar_sintese_avancada(self):
        """Versão avançada de sintese usando NLP.
        
        Returns:
            str: A síntese gerada ou None se não houver memórias suficientes
        """
        if not self.analise_semantica_ativa:
            # Fallback para método padrão
            return self.gerar_sintese()
        
        try:
            dados = self._carregar_memorias()
            if len(dados["memorias"]) < 2:
                logger.info("Memórias insuficientes para gerar síntese avançada")
                return None
            
            # Escolhe 2-3 memórias que tenham alguma relação semântica
            # Primeiro seleciona uma memória aleatória como ponto de partida
            memoria_base = random.choice(dados["memorias"])
            
            # Encontra memórias relacionadas semanticamente
            memorias_ordenadas = []
            for memoria in dados["memorias"]:
                if memoria["id"] != memoria_base["id"]:
                    similaridade = await analisador_semantico.calcular_similaridade_semantica(
                        memoria_base["conteudo"], memoria["conteudo"]
                    )
                    memorias_ordenadas.append((memoria, similaridade))
            
            # Ordena por similaridade e seleciona as mais próximas
            memorias_ordenadas.sort(key=lambda x: x[1], reverse=True)
            num_memorias = min(len(memorias_ordenadas), random.randint(1, 2))
            
            # Prepara os textos para síntese (inclui a memória base)
            memorias_escolhidas = [memoria_base] + [m[0] for m in memorias_ordenadas[:num_memorias]]
            textos = [memoria["conteudo"] for memoria in memorias_escolhidas]
            
            # Gera uma síntese avançada
            sintese = await analisador_semantico.gerar_sintese_avancada(textos)
            
            # Extrai palavras-chave e sentimento da síntese
            palavras_chave = await analisador_semantico.extrair_palavras_chave(sintese)
            sentimento = await analisador_semantico.analisar_sentimento(sintese)
            
            # Cria e armazena a nova memória sintética com enriquecimento semântico
            nova_memoria = {
                "id": len(dados["memorias"]) + 1,
                "conteudo": sintese,
                "criado_em": datetime.now().isoformat(),
                "versao": 1,
                "origem": "sintese_avancada",
                "baseado_em": [memoria["id"] for memoria in memorias_escolhidas],
                "analise_semantica": {
                    "palavras_chave": palavras_chave,
                    "sentimento": sentimento
                }
            }
            
            self.armazenar_memoria(nova_memoria, dados)
            logger.info(f"Síntese avançada gerada (ID: {nova_memoria['id']})")
            return sintese
            
        except Exception as e:
            logger.error(f"Erro na geração de síntese avançada: {e}")
            # Fallback para método padrão em caso de erro
            return self.gerar_sintese()
    
    def gerar_sintese(self):
        """Durante inatividade, combina memórias antigas para criar novas ideias.
        
        Returns:
            str: A síntese gerada ou None se não houver memórias suficientes
        """
        # Se a análise semântica estiver disponível, tenta usar o método avançado
        if self.analise_semantica_ativa:
            asyncio.create_task(self.gerar_sintese_avancada())
            return None
        
        dados = self._carregar_memorias()
        if len(dados["memorias"]) < 2:
            print("Memórias insuficientes para gerar síntese")
            return None
        
        # Escolhe 2-3 memórias aleatórias
        num_memorias = min(len(dados["memorias"]), random.randint(2, 3))
        memorias_escolhidas = random.sample(dados["memorias"], num_memorias)
        
        # Cria uma síntese simples combinando os conteúdos
        fragmentos = [memoria["conteudo"] for memoria in memorias_escolhidas]
        sintese = f"Combinando os conceitos de: {' e '.join(fragmentos)}"
        
        # Cria e armazena a nova memória sintética
        nova_memoria = {
            "id": len(dados["memorias"]) + 1,
            "conteudo": sintese,
            "criado_em": datetime.now().isoformat(),
            "versao": 1,
            "origem": "sintese_interna",
            "baseado_em": [memoria["id"] for memoria in memorias_escolhidas]
        }
        
        self.armazenar_memoria(nova_memoria, dados)
        return sintese
    
    # Métodos novos para busca semântica de memórias
    
    async def buscar_memorias_semanticamente(self, consulta, limite=5):
        """Busca memórias semanticamente similares à consulta.
        
        Args:
            consulta (str): Texto de consulta
            limite (int): Número máximo de resultados
            
        Returns:
            list: Lista de memórias ordenadas por relevância semântica
        """
        if not self.analise_semantica_ativa:
            # Fallback para busca simples
            return self.buscar_memorias(consulta, limite)
        
        try:
            dados = self._carregar_memorias()
            resultados = []
            
            for memoria in dados["memorias"]:
                similaridade = await analisador_semantico.calcular_similaridade_semantica(
                    consulta, memoria["conteudo"]
                )
                
                # Adiciona à lista se tiver alguma relevância
                if similaridade > 0.2:  # Limiar baixo para não filtrar demais
                    resultados.append((memoria, similaridade))
            
            # Ordena por similaridade e limita resultados
            resultados.sort(key=lambda x: x[1], reverse=True)
            return [memoria for memoria, _ in resultados[:limite]]
            
        except Exception as e:
            logger.error(f"Erro na busca semântica: {e}")
            # Fallback para busca simples em caso de erro
            return self.buscar_memorias(consulta, limite)
    
    def adicionar_memoria(self, conteudo):
        """Adiciona uma nova memória diretamente.
        
        Args:
            conteudo (str): Conteúdo da memória
            
        Returns:
            int: ID da memória adicionada
        """
        dados = self._carregar_memorias()
        nova_memoria = {
            "id": len(dados["memorias"]) + 1,
            "conteudo": conteudo,
            "criado_em": datetime.now().isoformat(),
            "versao": 1,
            "origem": "externa"
        }
        self.armazenar_memoria(nova_memoria, dados)
        return nova_memoria["id"]
    
    def listar_memorias(self, n=5):
        """Lista as últimas n memórias.
        
        Args:
            n (int): Número de memórias a listar
            
        Returns:
            list: Lista das últimas n memórias
        """
        dados = self._carregar_memorias()
        memorias = dados["memorias"]
        
        # Retorna as últimas n memórias (ou todas, se houver menos que n)
        return memorias[-n:] if len(memorias) > n else memorias
    
    def buscar_memorias(self, termo, limite=5):
        """Busca memórias contendo o termo especificado.
        
        Args:
            termo (str): Termo para buscar
            limite (int): Número máximo de resultados
            
        Returns:
            list: Lista de memórias encontradas
        """
        dados = self._carregar_memorias()
        resultados = []
        
        # Busca simples por substring
        termo_lower = termo.lower()
        for memoria in dados["memorias"]:
            if termo_lower in memoria["conteudo"].lower():
                resultados.append(memoria)
                if len(resultados) >= limite:
                    break
        
        return resultados 