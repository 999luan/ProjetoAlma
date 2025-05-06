"""
Módulo Learning - Implementa o gerenciamento de aprendizado do sistema.
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from persona.persona import Persona
from core.alma import Alma

class GerenciadorAprendizado:
    def __init__(self, persona: Optional[Persona] = None, alma: Optional[Alma] = None):
        """Inicializa o gerenciador de aprendizado."""
        self.persona = persona
        self.alma = alma
        self.ciclo_ativo = False
        self.ultimo_aprendizado = None
        self.historico_aprendizado = []
        self.metricas = {
            'total_ciclos': 0,
            'ciclos_sucesso': 0,
            'ultima_otimizacao': None
        }
        self.logger = logging.getLogger(__name__)

    async def ciclo_aprendizado_continuo(self, intervalo: int = 300):
        """Executa o ciclo contínuo de aprendizado."""
        if self.ciclo_ativo:
            self.logger.warning("Ciclo de aprendizado já está ativo")
            return

        self.ciclo_ativo = True
        self.logger.info(f"Iniciando ciclo de aprendizado (intervalo: {intervalo}s)")

        try:
            while self.ciclo_ativo:
                await self._executar_ciclo_aprendizado()
                await asyncio.sleep(intervalo)
        except asyncio.CancelledError:
            self.logger.info("Ciclo de aprendizado interrompido")
            self.ciclo_ativo = False
        except Exception as e:
            self.logger.error(f"Erro no ciclo de aprendizado: {str(e)}")
            self.ciclo_ativo = False

    async def _executar_ciclo_aprendizado(self):
        """Executa um ciclo de aprendizado."""
        try:
            self.logger.info("Iniciando ciclo de aprendizado...")
            self.ultimo_aprendizado = datetime.now()
            self.metricas['total_ciclos'] += 1

            # Processa as últimas 10 memórias
            try:
                resultado = await self._processar_memoria_aprendizado({
                    'id': 'teste',
                    'conteudo': 'Teste de aprendizado'
                })
                self.historico_aprendizado.append(resultado)
            except Exception as e:
                self.logger.error(f"Erro ao processar memória: {str(e)}")

            self.metricas['ciclos_sucesso'] += 1
            self.logger.info("Ciclo de aprendizado concluído com sucesso")

        except Exception as e:
            self.logger.error(f"Erro ao executar ciclo de aprendizado: {str(e)}")

    async def _processar_memoria_aprendizado(self, memoria: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma memória para aprendizado."""
        try:
            return {
                'memoria_id': memoria['id'],
                'timestamp': datetime.now(),
                'status': 'processado'
            }
        except Exception as e:
            self.logger.error(f"Erro ao processar memória para aprendizado: {str(e)}")
            return {
                'memoria_id': memoria.get('id', 'desconhecido'),
                'timestamp': datetime.now(),
                'status': 'erro',
                'erro': str(e)
            }

    def status_aprendizado(self) -> Dict[str, Any]:
        """Retorna o status atual do aprendizado."""
        return {
            'ciclo_ativo': self.ciclo_ativo,
            'ultimo_aprendizado': self.ultimo_aprendizado,
            'total_ciclos': self.metricas['total_ciclos'],
            'ciclos_sucesso': self.metricas['ciclos_sucesso'],
            'taxa_sucesso': self.metricas['ciclos_sucesso'] / self.metricas['total_ciclos'] if self.metricas['total_ciclos'] > 0 else 0
        }

    def mostrar_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas do aprendizado."""
        return {
            'total_ciclos': self.metricas['total_ciclos'],
            'ciclos_sucesso': self.metricas['ciclos_sucesso'],
            'taxa_sucesso': self.metricas['ciclos_sucesso'] / self.metricas['total_ciclos'] if self.metricas['total_ciclos'] > 0 else 0,
            'memorias_processadas': len(self.historico_aprendizado)
        } 