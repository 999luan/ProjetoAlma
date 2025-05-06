"""
Agente Emocional - Adiciona contexto emocional às informações processadas.

Este agente analisa conteúdos e atribui tonalidades emocionais, 
enriquecendo as memórias com uma camada afetiva.
"""

import random
from datetime import datetime

class AgenteEmocional:
    def __init__(self):
        """Inicializa o agente emocional com emoções predefinidas."""
        self.emocoes_positivas = [
            "alegria", "entusiasmo", "curiosidade", "admiração", 
            "satisfação", "otimismo", "confiança", "inspiração"
        ]
        
        self.emocoes_negativas = [
            "preocupação", "confusão", "frustração", "ansiedade",
            "desconfiança", "ceticismo", "dúvida", "insegurança"
        ]
        
        self.emocoes_neutras = [
            "neutralidade", "contemplação", "ponderação", "análise",
            "consideração", "reflexão", "imparcialidade", "equilíbrio"
        ]
        
        self.processamentos = 0
    
    async def processar(self, memoria):
        """Processa uma memória adicionando contexto emocional.
        
        Args:
            memoria (dict): A memória a ser processada
            
        Returns:
            dict: A memória com contexto emocional adicionado
        """
        self.processamentos += 1
        print(f"Agente Emocional analisando memória #{memoria['id']}")
        
        # Determina o tipo de emoção com base no conteúdo
        emocao = self._analisar_conteudo(memoria["conteudo"])
        
        # Adiciona o contexto emocional à memória
        memoria_processada = memoria.copy()
        
        if "contexto_emocional" not in memoria:
            memoria_processada["contexto_emocional"] = {
                "emocao": emocao,
                "intensidade": round(random.uniform(0.3, 0.9), 2),
                "adicionado_em": datetime.now().isoformat(),
                "versao_emocional": 1
            }
        else:
            # Atualiza o contexto emocional existente
            contexto_atual = memoria["contexto_emocional"].copy()
            contexto_atual["emocao"] = emocao
            contexto_atual["intensidade"] = round(random.uniform(0.3, 0.9), 2)
            contexto_atual["atualizado_em"] = datetime.now().isoformat()
            contexto_atual["versao_emocional"] = contexto_atual.get("versao_emocional", 1) + 1
            memoria_processada["contexto_emocional"] = contexto_atual
        
        print(f"Emoção atribuída: {emocao}")
        return memoria_processada
    
    def _analisar_conteudo(self, conteudo):
        """Analisa o conteúdo da memória para determinar a emoção apropriada.
        
        Implementação simples baseada em palavras-chave.
        
        Args:
            conteudo (str): O conteúdo da memória
            
        Returns:
            str: A emoção determinada
        """
        conteudo_lower = conteudo.lower()
        
        # Palavras associadas a emoções positivas
        palavras_positivas = [
            "bom", "excelente", "ótimo", "maravilhoso", "feliz", "alegr", 
            "positiv", "fundamental", "evolução", "aprend", "melhor"
        ]
        
        # Palavras associadas a emoções negativas
        palavras_negativas = [
            "ruim", "mau", "péssimo", "triste", "infeliz", "negativ", "problema",
            "dificuldade", "erro", "falha", "preocup"
        ]
        
        # Conta ocorrências de cada tipo
        pontos_positivos = sum(1 for palavra in palavras_positivas if palavra in conteudo_lower)
        pontos_negativos = sum(1 for palavra in palavras_negativas if palavra in conteudo_lower)
        
        # Decide a categoria da emoção
        if pontos_positivos > pontos_negativos + 1:
            return random.choice(self.emocoes_positivas)
        elif pontos_negativos > pontos_positivos + 1:
            return random.choice(self.emocoes_negativas)
        else:
            return random.choice(self.emocoes_neutras) 