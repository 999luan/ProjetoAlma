"""
Módulo Persona - Implementa a personalidade e comportamento do sistema.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
from persona.memoria import Memoria
from persona.processador_pensamento import ProcessadorPensamento

class Persona:
    def __init__(self):
        """Inicializa a persona do sistema."""
        self.memoria = Memoria()
        self.processador_pensamento = ProcessadorPensamento(self.memoria)
        self.logger = logging.getLogger(__name__)
        self.ultima_interacao = None
        self.historico_interacoes = []

    async def receber_pensamento(self, pensamento: Dict[str, Any]) -> Dict[str, Any]:
        """Recebe e processa um pensamento."""
        try:
            if not isinstance(pensamento, dict):
                raise ValueError("Pensamento deve ser um dicionário")

            self.ultima_interacao = datetime.now()
            
            # Processa o pensamento
            resultado = await self.processador_pensamento.processar_pensamento(pensamento)
            
            # Registra a interação
            self.historico_interacoes.append({
                'timestamp': self.ultima_interacao,
                'pensamento': pensamento,
                'resultado': resultado
            })

            return resultado

        except Exception as e:
            self.logger.error(f"Erro ao receber pensamento: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now()
            }

    def obter_historico(self, limite: int = 10) -> List[Dict[str, Any]]:
        """Retorna o histórico de interações."""
        return self.historico_interacoes[-limite:]

    def status(self) -> Dict[str, Any]:
        """Retorna o status atual da persona."""
        return {
            'ultima_interacao': self.ultima_interacao,
            'total_interacoes': len(self.historico_interacoes),
            'memoria': self.memoria.status(),
            'processador': {
                'ultimo_processamento': self.processador_pensamento.ultimo_processamento,
                'total_processados': len(self.processador_pensamento.historico_processamento)
            }
        }

    def _carregar_memorias(self):
        """
        Carrega as memórias do sistema.
        
        Returns:
            dict: O conteúdo do arquivo de memórias
        """
        return self.memoria._carregar_memorias()
        
    def adicionar_memoria(self, conteudo: str) -> str:
        """
        Adiciona uma nova memória ao sistema.
        
        Args:
            conteudo: Conteúdo da memória a ser armazenada
            
        Returns:
            ID da memória armazenada
        """
        return self.memoria.adicionar_memoria(conteudo)
    
    def listar_memorias(self, n: int = 5) -> list:
        """
        Lista as últimas n memórias.
        
        Args:
            n: Número de memórias a retornar
            
        Returns:
            Lista de memórias
        """
        return self.memoria.listar_memorias(n)
    
    def buscar_memorias(self, termo: str) -> list:
        """
        Busca memórias contendo o termo especificado.
        
        Args:
            termo: Termo a ser buscado
            
        Returns:
            Lista de memórias encontradas
        """
        return self.memoria.buscar_memorias(termo)
    
    def buscar_memorias_semanticamente(self, consulta: str) -> list:
        """
        Busca memórias semanticamente relacionadas à consulta.
        
        Args:
            consulta: Texto para busca semântica
            
        Returns:
            Lista de memórias semanticamente relacionadas
        """
        # Implementação básica - retorna busca textual normal
        return self.buscar_memorias(consulta) 