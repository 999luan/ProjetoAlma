"""
Agente de Padrões - Detecta padrões recorrentes nas memórias.

Este agente analisa o conjunto de memórias buscando identificar
padrões, temas recorrentes e tendências de pensamento.
"""

import re
from collections import Counter
from datetime import datetime

class AgentePadrao:
    def __init__(self, persona):
        """Inicializa o agente de padrões.
        
        Args:
            persona: Referência à instância da Persona para acessar memórias
        """
        self.persona = persona
        self.processamentos = 0
        self.padroes_detectados = []
    
    async def processar(self, memoria):
        """Processa uma memória buscando padrões relacionados.
        
        Args:
            memoria (dict): A memória a ser analisada
            
        Returns:
            dict: A memória atualizada com informações sobre padrões detectados
        """
        self.processamentos += 1
        print(f"Agente de Padrões analisando memória #{memoria['id']}")
        
        # Busca padrões relacionados a esta memória
        padroes = self._detectar_padroes(memoria)
        
        if not padroes:
            print("Nenhum padrão significativo detectado")
            return memoria
        
        # Encontrou padrões, atualiza a memória
        memoria_atualizada = memoria.copy()
        
        if "padroes" not in memoria_atualizada:
            memoria_atualizada["padroes"] = {
                "temas_detectados": padroes,
                "detectado_em": datetime.now().isoformat(),
                "versao_padrao": 1
            }
        else:
            # Atualiza informações de padrões existentes
            memoria_atualizada["padroes"]["temas_detectados"] = padroes
            memoria_atualizada["padroes"]["atualizado_em"] = datetime.now().isoformat()
            memoria_atualizada["padroes"]["versao_padrao"] = memoria_atualizada["padroes"].get("versao_padrao", 1) + 1
        
        # Registra globalmente os padrões detectados
        for padrao in padroes:
            if padrao not in [p["tema"] for p in self.padroes_detectados]:
                self.padroes_detectados.append({
                    "tema": padrao,
                    "detectado_em": datetime.now().isoformat(),
                    "memorias_relacionadas": [memoria["id"]]
                })
            else:
                # Atualiza padrão existente
                for p in self.padroes_detectados:
                    if p["tema"] == padrao and memoria["id"] not in p["memorias_relacionadas"]:
                        p["memorias_relacionadas"].append(memoria["id"])
        
        print(f"Padrões detectados: {', '.join(padroes)}")
        return memoria_atualizada
    
    def _detectar_padroes(self, memoria):
        """Detecta padrões relacionados a uma memória.
        
        Args:
            memoria (dict): A memória a ser analisada
            
        Returns:
            list: Lista de padrões detectados
        """
        # Carrega todas as memórias
        dados = self.persona._carregar_memorias()
        if not dados["memorias"]:
            return []
        
        # Extrai palavras-chave da memória atual
        palavras_chave = self._extrair_palavras_chave(memoria["conteudo"])
        
        if not palavras_chave:
            return []
        
        # Busca essas palavras-chave em outras memórias
        temas_recorrentes = Counter()
        
        for outra_memoria in dados["memorias"]:
            # Não considera a própria memória
            if outra_memoria["id"] == memoria["id"]:
                continue
            
            outras_palavras = self._extrair_palavras_chave(outra_memoria["conteudo"])
            
            # Intersecção de palavras-chave
            intersecao = set(palavras_chave).intersection(set(outras_palavras))
            
            for palavra in intersecao:
                temas_recorrentes[palavra] += 1
        
        # Seleciona os temas mais recorrentes (pelo menos 2 ocorrências)
        padroes = [tema for tema, contagem in temas_recorrentes.items() if contagem >= 2]
        
        return padroes[:5]  # Limita a 5 padrões para não sobrecarregar
    
    def _extrair_palavras_chave(self, texto):
        """Extrai palavras-chave de um texto.
        
        Args:
            texto (str): O texto a ser analisado
            
        Returns:
            list: Lista de palavras-chave
        """
        # Converte para minúsculas
        texto = texto.lower()
        
        # Remove pontuação comum
        texto = re.sub(r'[,.;:!?"\']', '', texto)
        
        # Divide em palavras
        palavras = texto.split()
        
        # Remove palavras muito comuns (stopwords simplificadas)
        stopwords = {
            'a', 'o', 'e', 'de', 'da', 'do', 'em', 'no', 'na', 'para', 'por',
            'que', 'se', 'um', 'uma', 'os', 'as', 'dos', 'das', 'com', 'é',
            'são', 'ao', 'ou', 'seu', 'sua'
        }
        
        palavras = [p for p in palavras if p not in stopwords and len(p) > 3]
        
        # Retorna palavras únicas
        return list(set(palavras)) 