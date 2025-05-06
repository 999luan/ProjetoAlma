"""
Módulo ProcessadorPensamento - Implementa o processamento de pensamentos do sistema.
"""

import logging
import asyncio
from typing import Dict, Any, List
from datetime import datetime

class ProcessadorPensamento:
    def __init__(self, memoria):
        """Inicializa o processador de pensamentos."""
        self.memoria = memoria
        self.ultimo_processamento = None
        self.historico_processamento = []
        self.logger = logging.getLogger(__name__)
        self.agentes = {
            'reflexao': self._agente_reflexao,
            'metacognicao': self._agente_metacognicao,
            'emocional': self._agente_emocional,
            'consistencia': self._agente_consistencia,
            'padroes': self._agente_padroes
        }

    async def processar_pensamento(self, pensamento: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento baseado em seu tipo e agentes ativos."""
        try:
            if not isinstance(pensamento, dict):
                raise ValueError("Pensamento deve ser um dicionário")

            tipo = pensamento.get('tipo')
            conteudo = pensamento.get('conteudo')
            agentes_ativos = pensamento.get('agentes', {})
            
            if not tipo or not conteudo:
                raise ValueError("Pensamento deve conter tipo e conteúdo")

            self.ultimo_processamento = datetime.now()
            
            # Processa com os agentes ativos
            resultados = {}
            for agente_nome, ativo in agentes_ativos.items():
                if ativo and agente_nome in self.agentes:
                    try:
                        resultado = await self.agentes[agente_nome](conteudo)
                        resultados[agente_nome] = resultado
                    except Exception as e:
                        self.logger.error(f"Erro no agente {agente_nome}: {str(e)}")
                        resultados[agente_nome] = {'erro': str(e)}

            # Processa baseado no tipo
            if tipo == 'reflexao':
                resultado_base = await self._processar_reflexao(conteudo)
            elif tipo == 'memoria':
                resultado_base = await self._processar_memoria(conteudo)
            elif tipo == 'aprendizado':
                resultado_base = await self._processar_aprendizado(conteudo)
            else:
                resultado_base = await self._processar_generico(conteudo)

            # Combina resultados
            resultado_final = {
                'status': 'sucesso',
                'tipo': tipo,
                'resultado_base': resultado_base,
                'resultados_agentes': resultados,
                'timestamp': self.ultimo_processamento
            }

            # Registra no histórico
            self.historico_processamento.append({
                'timestamp': self.ultimo_processamento,
                'tipo': tipo,
                'conteudo': conteudo,
                'resultado': resultado_final
            })

            return resultado_final

        except Exception as e:
            self.logger.error(f"Erro ao processar pensamento: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now()
            }

    async def _agente_reflexao(self, conteudo: str) -> Dict[str, Any]:
        """Agente de reflexão - analisa e reflete sobre o conteúdo."""
        try:
            # Busca memórias relacionadas
            memorias = self.memoria.buscar_memorias(conteudo)
            
            # Analisa o conteúdo
            insights = []
            if memorias:
                insights.append(f"Encontrei {len(memorias)} memórias relacionadas")
            
            return {
                'tipo': 'reflexao',
                'insights': insights,
                'memorias_relacionadas': len(memorias)
            }
        except Exception as e:
            self.logger.error(f"Erro no agente de reflexão: {str(e)}")
            raise

    async def _agente_metacognicao(self, conteudo: str) -> Dict[str, Any]:
        """Agente de metacognição - avalia o próprio processo de pensamento."""
        try:
            # Avalia a qualidade do processamento
            qualidade = {
                'compreensao': True,
                'relevancia': True,
                'novidade': True
            }
            
            return {
                'tipo': 'metacognicao',
                'avaliacao': qualidade
            }
        except Exception as e:
            self.logger.error(f"Erro no agente de metacognição: {str(e)}")
            raise

    async def _agente_emocional(self, conteudo: str) -> Dict[str, Any]:
        """Agente emocional - analisa aspectos emocionais do conteúdo."""
        try:
            # Análise básica de sentimento
            sentimento = {
                'polaridade': 0.0,  # -1 a 1
                'intensidade': 0.5  # 0 a 1
            }
            
            return {
                'tipo': 'emocional',
                'sentimento': sentimento
            }
        except Exception as e:
            self.logger.error(f"Erro no agente emocional: {str(e)}")
            raise

    async def _agente_consistencia(self, conteudo: str) -> Dict[str, Any]:
        """Agente de consistência - verifica consistência com memórias existentes."""
        try:
            # Verifica consistência
            memorias = self.memoria.buscar_memorias(conteudo)
            consistente = True
            
            return {
                'tipo': 'consistencia',
                'consistente': consistente,
                'memorias_verificadas': len(memorias)
            }
        except Exception as e:
            self.logger.error(f"Erro no agente de consistência: {str(e)}")
            raise

    async def _agente_padroes(self, conteudo: str) -> Dict[str, Any]:
        """Agente de padrões - identifica padrões no conteúdo."""
        try:
            # Identifica padrões básicos
            padroes = {
                'repeticao': False,
                'estrutura': 'simples'
            }
            
            return {
                'tipo': 'padroes',
                'padroes_identificados': padroes
            }
        except Exception as e:
            self.logger.error(f"Erro no agente de padrões: {str(e)}")
            raise

    async def _processar_reflexao(self, conteudo: str) -> Dict[str, Any]:
        """Processa um pensamento do tipo reflexão."""
        try:
            return {
                'tipo': 'reflexao',
                'insights': [],
                'conclusoes': []
            }
        except Exception as e:
            self.logger.error(f"Erro ao processar reflexão: {str(e)}")
            raise

    async def _processar_memoria(self, conteudo: str) -> Dict[str, Any]:
        """Processa um pensamento do tipo memória."""
        try:
            return {
                'tipo': 'memoria',
                'memorias_relacionadas': []
            }
        except Exception as e:
            self.logger.error(f"Erro ao processar memória: {str(e)}")
            raise

    async def _processar_aprendizado(self, conteudo: str) -> Dict[str, Any]:
        """Processa um pensamento do tipo aprendizado."""
        try:
            return {
                'tipo': 'aprendizado',
                'novos_conhecimentos': []
            }
        except Exception as e:
            self.logger.error(f"Erro ao processar aprendizado: {str(e)}")
            raise

    async def _processar_generico(self, conteudo: str) -> Dict[str, Any]:
        """Processa um pensamento genérico."""
        try:
            return {
                'tipo': 'generico',
                'processado': True
            }
        except Exception as e:
            self.logger.error(f"Erro ao processar pensamento genérico: {str(e)}")
            raise

    def obter_historico(self, limite: int = 10) -> List[Dict[str, Any]]:
        """Retorna o histórico de processamento."""
        return self.historico_processamento[-limite:] 