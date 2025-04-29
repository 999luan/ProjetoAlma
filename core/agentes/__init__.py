"""
Pacote de Agentes para o Sistema de Memória Contínua.

Este pacote contém os diversos agentes especializados que trabalham
sobre as memórias do sistema, cada um com uma função específica.
"""

from core.agentes.emotional_agent import AgenteEmocional
from core.agentes.consistency_agent import AgenteConsistencia
from core.agentes.pattern_agent import AgentePadrao

__all__ = [
    'AgenteEmocional',
    'AgenteConsistencia',
    'AgentePadrao'
] 