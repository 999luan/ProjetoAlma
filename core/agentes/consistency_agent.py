"""
Agente de Consistência - Detecta e resolve contradições entre memórias.

Este agente analisa memórias existentes buscando inconsistências
e propõe resoluções para manter a base de conhecimento coerente.
"""

import re
from datetime import datetime
from core.utils import calcular_similaridade_texto

class AgenteConsistencia:
    def __init__(self, persona):
        """Inicializa o agente de consistência.
        
        Args:
            persona: Referência à instância da Persona para acessar memórias
        """
        self.persona = persona
        self.processamentos = 0
        self.inconsistencias_detectadas = 0
        self.resolucoes_aplicadas = 0
    
    async def processar(self, memoria):
        """Processa uma memória verificando inconsistências com outras memórias.
        
        Args:
            memoria (dict): A memória a ser analisada
            
        Returns:
            dict: A memória possivelmente atualizada para resolver inconsistências
        """
        self.processamentos += 1
        print(f"Agente de Consistência analisando memória #{memoria['id']}")
        
        # Busca memórias potencialmente inconsistentes
        inconsistencias = self._buscar_inconsistencias(memoria)
        
        # Se não encontrou inconsistências, retorna a memória original
        if not inconsistencias:
            print("Nenhuma inconsistência detectada")
            return memoria
        
        # Encontrou inconsistências, tenta resolver
        self.inconsistencias_detectadas += 1
        print(f"Inconsistência detectada entre memória #{memoria['id']} e #{inconsistencias[0]['id']}")
        
        # Resolve a inconsistência
        memoria_atualizada = self._resolver_inconsistencia(memoria, inconsistencias[0])
        self.resolucoes_aplicadas += 1
        
        return memoria_atualizada
    
    def _buscar_inconsistencias(self, memoria):
        """Busca memórias que podem ser inconsistentes com a memória atual.
        
        Args:
            memoria (dict): A memória a ser comparada
            
        Returns:
            list: Lista de memórias potencialmente inconsistentes
        """
        resultado = []
        
        # Carrega todas as memórias
        dados = self.persona._carregar_memorias()
        if not dados["memorias"]:
            return resultado
        
        # Analisa o conteúdo da memória atual
        conteudo = memoria["conteudo"].lower()
        
        # Padrões de inconsistência (simplificados)
        # Buscando por "não", "nunca", "impossível" em conteúdos similares
        for outra_memoria in dados["memorias"]:
            # Não compara com ela mesma
            if outra_memoria["id"] == memoria["id"]:
                continue
            
            # Verifica se são similares o suficiente para analisar
            similaridade = calcular_similaridade_texto(memoria["conteudo"], outra_memoria["conteudo"])
            
            if similaridade > 0.3:  # Limiar de similaridade para considerar comparação
                # Busca padrões de contradição entre as duas memórias
                conteudo_outra = outra_memoria["conteudo"].lower()
                
                # Exemplo simples: uma afirma algo, outra nega
                padrao_positivo = r"(é|são|deve|devem|tem|têm|existe|existem|permite)"
                padrao_negativo = r"(não é|não são|não deve|não devem|não tem|não têm|não existe|não existem|não permite)"
                
                positivo_atual = bool(re.search(padrao_positivo, conteudo))
                negativo_atual = bool(re.search(padrao_negativo, conteudo))
                
                positivo_outra = bool(re.search(padrao_positivo, conteudo_outra))
                negativo_outra = bool(re.search(padrao_negativo, conteudo_outra))
                
                # Se uma afirma e outra nega sobre o mesmo tema
                if (positivo_atual and negativo_outra) or (negativo_atual and positivo_outra):
                    resultado.append(outra_memoria)
                    break  # Encontrou uma inconsistência, suficiente para este ciclo
        
        return resultado
    
    def _resolver_inconsistencia(self, memoria, memoria_inconsistente):
        """Resolve a inconsistência entre duas memórias.
        
        Esta é uma implementação simplificada que favorece a memória mais recente
        e marca a inconsistência.
        
        Args:
            memoria (dict): A memória atual
            memoria_inconsistente (dict): A memória inconsistente
            
        Returns:
            dict: A memória atualizada com marcação de inconsistência
        """
        memoria_atualizada = memoria.copy()
        
        # Adiciona ou atualiza o campo de consistência
        if "consistencia" not in memoria_atualizada:
            memoria_atualizada["consistencia"] = {
                "inconsistente_com": [memoria_inconsistente["id"]],
                "resolvido_em": datetime.now().isoformat(),
                "resolucao": "Memória atual considerada mais precisa devido à recenticidade."
            }
        else:
            # Atualiza o campo existente
            inconsistentes = memoria_atualizada["consistencia"].get("inconsistente_com", [])
            if memoria_inconsistente["id"] not in inconsistentes:
                inconsistentes.append(memoria_inconsistente["id"])
            
            memoria_atualizada["consistencia"] = {
                "inconsistente_com": inconsistentes,
                "atualizado_em": datetime.now().isoformat(),
                "resolucao": "Memória atual considerada mais precisa devido à recenticidade."
            }
        
        print(f"Inconsistência resolvida, favorecendo memória #{memoria['id']}")
        return memoria_atualizada 