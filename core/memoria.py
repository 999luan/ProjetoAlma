"""
Módulo Memória - Implementa o sistema de memória do Alma.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import json
import os

class Memoria:
    def __init__(self):
        """Inicializa o sistema de memória."""
        self.logger = logging.getLogger(__name__)
        self.memorias = []
        self.ultima_atualizacao = datetime.now()
        
        # Cria diretório de memória se não existir
        self.diretorio_memoria = "memoria"
        if not os.path.exists(self.diretorio_memoria):
            os.makedirs(self.diretorio_memoria)
        
        # Carrega memórias existentes
        self._carregar_memorias()

    def _carregar_memorias(self):
        """Carrega memórias do arquivo."""
        try:
            arquivo_memoria = os.path.join(self.diretorio_memoria, "memorias.json")
            if os.path.exists(arquivo_memoria):
                with open(arquivo_memoria, 'r', encoding='utf-8') as f:
                    self.memorias = json.load(f)
                self.logger.info(f"Memórias carregadas: {len(self.memorias)}")
        except Exception as e:
            self.logger.error(f"Erro ao carregar memórias: {str(e)}")
            self.memorias = []

    def _salvar_memorias(self):
        """Salva memórias no arquivo."""
        try:
            arquivo_memoria = os.path.join(self.diretorio_memoria, "memorias.json")
            with open(arquivo_memoria, 'w', encoding='utf-8') as f:
                json.dump(self.memorias, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Memórias salvas: {len(self.memorias)}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar memórias: {str(e)}")

    def adicionar_memoria(self, conteudo: str, tipo: str = "geral", prioridade: int = 1) -> Dict[str, Any]:
        """Adiciona uma nova memória."""
        try:
            memoria = {
                'id': len(self.memorias) + 1,
                'conteudo': conteudo,
                'tipo': tipo,
                'prioridade': prioridade,
                'timestamp': datetime.now().isoformat()
            }
            
            self.memorias.append(memoria)
            self._salvar_memorias()
            self.ultima_atualizacao = datetime.now()
            
            return memoria
            
        except Exception as e:
            self.logger.error(f"Erro ao adicionar memória: {str(e)}")
            return None

    def buscar_memorias(self, termo: str) -> List[Dict[str, Any]]:
        """Busca memórias contendo o termo."""
        try:
            termo = termo.lower()
            return [
                memoria for memoria in self.memorias
                if termo in memoria['conteudo'].lower()
            ]
        except Exception as e:
            self.logger.error(f"Erro ao buscar memórias: {str(e)}")
            return []

    def listar_memorias(self, limite: int = 5) -> List[Dict[str, Any]]:
        """Lista as últimas memórias."""
        try:
            return sorted(
                self.memorias,
                key=lambda x: x['timestamp'],
                reverse=True
            )[:limite]
        except Exception as e:
            self.logger.error(f"Erro ao listar memórias: {str(e)}")
            return []

    def listar_todas_memorias(self) -> List[Dict[str, Any]]:
        """Retorna todas as memórias armazenadas sem limite."""
        try:
            return sorted(
                self.memorias,
                key=lambda x: x['timestamp'],
                reverse=True
            )
        except Exception as e:
            self.logger.error(f"Erro ao listar todas as memórias: {str(e)}")
            return []

    def status(self) -> Dict[str, Any]:
        """Retorna o status da memória."""
        return {
            'total_memorias': len(self.memorias),
            'ultima_atualizacao': self.ultima_atualizacao.isoformat(),
            'tipos_memoria': list(set(m['tipo'] for m in self.memorias))
        } 