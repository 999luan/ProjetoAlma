"""
Módulo Adaptive Learning - Implementa o aprendizado adaptativo do sistema.
"""

import logging
import asyncio
from typing import Dict, Any
from datetime import datetime

class AprendizadoAdaptativo:
    def __init__(self, gerenciador_aprendizado):
        """Inicializa o sistema de aprendizado adaptativo."""
        self.gerenciador_aprendizado = gerenciador_aprendizado
        self.ciclo_ativo = False
        self.ultima_adaptacao = None
        self.metricas = {
            'total_ciclos': 0,
            'ciclos_sucesso': 0,
            'ultima_otimizacao': None
        }
        self.logger = logging.getLogger(__name__)

    async def iniciar_ciclo_adaptativo(self, intervalo: int = 600):
        """Inicia o ciclo adaptativo."""
        if self.ciclo_ativo:
            self.logger.warning("Ciclo adaptativo já está ativo")
            return

        self.ciclo_ativo = True
        self.logger.info(f"Iniciando ciclo adaptativo (intervalo: {intervalo}s)")

        try:
            while self.ciclo_ativo:
                await self._executar_ciclo_adaptacao()
                await asyncio.sleep(intervalo)
        except asyncio.CancelledError:
            self.logger.info("Ciclo adaptativo interrompido")
            self.ciclo_ativo = False
        except Exception as e:
            self.logger.error(f"Erro no ciclo adaptativo: {str(e)}")
            self.ciclo_ativo = False

    async def _executar_ciclo_adaptacao(self):
        """Executa um ciclo de adaptação."""
        try:
            self.logger.info("Iniciando ciclo de adaptação...")
            self.ultima_adaptacao = datetime.now()
            self.metricas['total_ciclos'] += 1

            # Analisa métricas do sistema
            metricas = await self._analisar_metricas_sistema()
            
            # Ajusta estratégias com base nas métricas
            if metricas['taxa_sucesso'] < 0.7:  # Ajusta se taxa de sucesso < 70%
                await self._ajustar_estrategias(metricas)

            self.metricas['ciclos_sucesso'] += 1
            self.logger.info("Ciclo de adaptação concluído com sucesso")

        except Exception as e:
            self.logger.error(f"Erro ao executar ciclo de adaptação: {str(e)}")

    async def _analisar_metricas_sistema(self) -> Dict[str, Any]:
        """Analisa métricas do sistema."""
        try:
            status = self.gerenciador_aprendizado.status_aprendizado()
            estatisticas = self.gerenciador_aprendizado.mostrar_estatisticas()
            
            return {
                'taxa_sucesso': status['taxa_sucesso'],
                'total_ciclos': status['total_ciclos'],
                'ciclos_sucesso': status['ciclos_sucesso'],
                'memorias_processadas': estatisticas['memorias_processadas']
            }
        except Exception as e:
            self.logger.error(f"Erro ao analisar métricas: {str(e)}")
            return {
                'taxa_sucesso': 0,
                'total_ciclos': 0,
                'ciclos_sucesso': 0,
                'memorias_processadas': 0
            }

    async def _ajustar_estrategias(self, metricas: Dict[str, Any]):
        """Ajusta estratégias com base nas métricas."""
        try:
            self.logger.info("Ajustando estratégias...")
            self.metricas['ultima_otimizacao'] = datetime.now()
            
            # Implementação básica - pode ser expandida
            return {
                'status': 'sucesso',
                'timestamp': datetime.now()
            }
        except Exception as e:
            self.logger.error(f"Erro ao ajustar estratégias: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now()
            }

    def status_adaptacao(self) -> Dict[str, Any]:
        """Retorna o status atual do sistema adaptativo."""
        return {
            'ciclo_ativo': self.ciclo_ativo,
            'ultima_adaptacao': self.ultima_adaptacao,
            'total_ciclos': self.metricas['total_ciclos'],
            'ciclos_sucesso': self.metricas['ciclos_sucesso'],
            'taxa_sucesso': self.metricas['ciclos_sucesso'] / self.metricas['total_ciclos'] if self.metricas['total_ciclos'] > 0 else 0,
            'ultima_otimizacao': self.metricas['ultima_otimizacao']
        } 