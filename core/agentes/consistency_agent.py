"""
Agente de Consistência - Detecta e resolve contradições entre memórias.

Este agente analisa memórias existentes buscando inconsistências
e propõe resoluções para manter a base de conhecimento coerente.
"""

import re
import logging
from datetime import datetime
from core.utils import calcular_similaridade_texto

# Importação condicional do módulo de análise semântica
try:
    from core.nlp_enhancement import analisador_semantico
    ANALISE_SEMANTICA_DISPONIVEL = True
except ImportError:
    ANALISE_SEMANTICA_DISPONIVEL = False

# Configuração de logging
logger = logging.getLogger(__name__)

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
        self.analise_semantica_ativa = ANALISE_SEMANTICA_DISPONIVEL
    
    async def processar(self, memoria):
        """Processa uma memória verificando inconsistências com outras memórias.
        
        Args:
            memoria (dict): A memória a ser analisada
            
        Returns:
            dict: A memória possivelmente atualizada para resolver inconsistências
        """
        self.processamentos += 1
        print(f"Agente de Consistência analisando memória #{memoria['id']}")
        
        # Verifica se pode usar análise semântica avançada
        if self.analise_semantica_ativa:
            try:
                # Busca inconsistências com análise semântica avançada
                inconsistencias = await self._buscar_inconsistencias_avancadas(memoria)
                # Se não encontrou com o método avançado, tenta o método tradicional
                if not inconsistencias:
                    inconsistencias = self._buscar_inconsistencias(memoria)
            except Exception as e:
                logger.error(f"Erro na análise semântica de inconsistências: {e}")
                # Fallback para método tradicional
                inconsistencias = self._buscar_inconsistencias(memoria)
        else:
            # Usa o método tradicional
            inconsistencias = self._buscar_inconsistencias(memoria)
        
        # Se não encontrou inconsistências, retorna a memória original
        if not inconsistencias:
            print("Nenhuma inconsistência detectada")
            return memoria
        
        # Encontrou inconsistências, tenta resolver
        self.inconsistencias_detectadas += 1
        print(f"Inconsistência detectada entre memória #{memoria['id']} e #{inconsistencias[0]['id']}")
        
        # Resolve a inconsistência
        memoria_atualizada = await self._resolver_inconsistencia(memoria, inconsistencias[0])
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
    
    async def _buscar_inconsistencias_avancadas(self, memoria):
        """Busca inconsistências usando análise semântica avançada.
        
        Args:
            memoria (dict): A memória a ser analisada
            
        Returns:
            list: Lista de memórias inconsistentes
        """
        resultado = []
        
        # Carrega todas as memórias
        dados = self.persona._carregar_memorias()
        if not dados["memorias"]:
            return resultado
        
        # Apenas inicializa o analisador se ainda não tiver sido feito
        if not analisador_semantico.inicializado:
            await analisador_semantico.inicializar_recursos()
            if not analisador_semantico.inicializado:
                logger.warning("Não foi possível inicializar análise semântica para busca de inconsistências")
                return resultado
        
        for outra_memoria in dados["memorias"]:
            # Não compara com ela mesma
            if outra_memoria["id"] == memoria["id"]:
                continue
            
            # Primeiro verifica se são similares o suficiente para comparar
            similaridade = await analisador_semantico.calcular_similaridade_semantica(
                memoria["conteudo"], outra_memoria["conteudo"], metodo="embeddings"
            )
            
            # Se forem similares, analisa possíveis contradições
            if similaridade > 0.5:  # Limiar mais alto para o método semântico
                resultado_contradicao = await analisador_semantico.encontrar_contradicoes(
                    memoria, outra_memoria
                )
                
                if resultado_contradicao["encontrou_contradicao"]:
                    # Adiciona dados de contradição à memória
                    outra_memoria_copia = outra_memoria.copy()
                    outra_memoria_copia["detalhes_contradicao"] = {
                        "sentencas_contraditorias": resultado_contradicao.get("sentencas_contraditorias", []),
                        "similaridade_geral": resultado_contradicao.get("similaridade_geral", 0.0)
                    }
                    resultado.append(outra_memoria_copia)
                    
                    logger.info(f"Contradição semântica detectada entre memórias #{memoria['id']} e #{outra_memoria['id']}")
                    break  # Uma contradição é suficiente para este ciclo
        
        return resultado
    
    async def _resolver_inconsistencia(self, memoria, memoria_inconsistente):
        """Resolve a inconsistência entre duas memórias.
        
        Esta é uma implementação que favorece a memória mais recente
        e marca a inconsistência com detalhes quando disponíveis.
        
        Args:
            memoria (dict): A memória atual
            memoria_inconsistente (dict): A memória inconsistente
            
        Returns:
            dict: A memória atualizada com marcação de inconsistência
        """
        memoria_atualizada = memoria.copy()
        
        # Informações básicas de resolução
        resolucao_info = {
            "inconsistente_com": [memoria_inconsistente["id"]],
            "resolvido_em": datetime.now().isoformat(),
            "resolucao": "Memória atual considerada mais precisa devido à recenticidade."
        }
        
        # Adiciona detalhes semânticos se disponíveis
        if self.analise_semantica_ativa and "detalhes_contradicao" in memoria_inconsistente:
            resolucao_info["tipo_contradicao"] = "semântica"
            
            # Adiciona as sentenças contraditórias se existirem
            if "sentencas_contraditorias" in memoria_inconsistente["detalhes_contradicao"]:
                resolucao_info["sentencas_contraditorias"] = memoria_inconsistente["detalhes_contradicao"]["sentencas_contraditorias"]
            
            # Adiciona o nível de similaridade geral
            if "similaridade_geral" in memoria_inconsistente["detalhes_contradicao"]:
                resolucao_info["similaridade"] = memoria_inconsistente["detalhes_contradicao"]["similaridade_geral"]
            
            # Adiciona explicação mais detalhada
            resolucao_info["resolucao"] = "Contradição semântica identificada. " + resolucao_info["resolucao"]
        else:
            resolucao_info["tipo_contradicao"] = "sintática"
        
        # Atualiza ou cria o campo de consistência
        if "consistencia" not in memoria_atualizada:
            memoria_atualizada["consistencia"] = resolucao_info
        else:
            # Atualiza o campo existente
            inconsistentes = memoria_atualizada["consistencia"].get("inconsistente_com", [])
            if memoria_inconsistente["id"] not in inconsistentes:
                inconsistentes.append(memoria_inconsistente["id"])
            
            resolucao_info["inconsistente_com"] = inconsistentes
            resolucao_info["atualizado_em"] = datetime.now().isoformat()
            
            memoria_atualizada["consistencia"] = resolucao_info
        
        print(f"Inconsistência resolvida, favorecendo memória #{memoria['id']}")
        return memoria_atualizada 