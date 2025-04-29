"""
Módulo Persona - Responsável por receber informações, armazenar, aprender e sintetizar.

Este módulo implementa a parte consciente do sistema, que lida com o recebimento
de informações externas, sua integração com o conhecimento existente e o armazenamento.
"""

import json
import os
import random
from datetime import datetime

class Persona:
    def __init__(self, memoria_path="core/memoria.json"):
        """
        Inicializa a Persona com referência ao arquivo de memórias.
        
        Args:
            memoria_path (str): Caminho para o arquivo de memórias
        """
        self.memoria_path = memoria_path
        self._inicializar_memoria()
    
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
    
    def integrar_informacao(self, info):
        """Compara com memórias anteriores, ajusta ou cria uma nova memória.
        
        Args:
            info (str): A informação a ser integrada
            
        Returns:
            bool: True se a informação foi integrada com sucesso
        """
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
        
        # Extrair palavras significativas (ignorando palavras muito comuns)
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
    
    def gerar_sintese(self):
        """Durante inatividade, combina memórias antigas para criar novas ideias.
        
        Returns:
            str: A síntese gerada ou None se não houver memórias suficientes
        """
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