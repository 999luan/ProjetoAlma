"""
Módulo Alma - Implementa o núcleo do sistema de pensamento e reflexão.
"""

import logging
import asyncio
from typing import Dict, Any, List
from datetime import datetime
from core.persona import Persona
from core.memoria import Memoria
from core.processador_pensamento import ProcessadorPensamento
from core.learning import GerenciadorAprendizado
from core.adaptive_learning import AprendizadoAdaptativo
import random

class Alma:
    def __init__(self):
        """Inicializa o sistema Alma."""
        # Configura o logger primeiro
        self.logger = logging.getLogger(__name__)
        
        try:
            # Inicializa a memória
            self.memoria = Memoria()
            self.logger.info("Memória inicializada")
            
            # Inicializa a persona com a memória
            self.persona = Persona(self.memoria)
            self.logger.info("Persona inicializada")
            
            # Inicializa o processador de pensamento
            self.processador_pensamento = ProcessadorPensamento(self.persona)
            self.logger.info("Processador de pensamento inicializado")
            
            # Conecta o processador à persona (evita referência circular)
            self.persona.inicializar_processador(self.processador_pensamento)
            self.logger.info("Processador conectado à persona")
            
            # Inicializa os componentes de aprendizado
            self.gerenciador_aprendizado = GerenciadorAprendizado(persona=self.persona, alma=self)
            self.aprendizado_adaptativo = AprendizadoAdaptativo(self.gerenciador_aprendizado)
            self.logger.info("Componentes de aprendizado inicializados")
            
            # Inicializa as tasks
            self._ciclo_task = None
            self._ciclo_aprendizado_task = None
            self._ciclo_adaptativo_task = None
            self.logger.info("Tasks inicializadas")
            
            # Executa reflexões iniciais para processar memórias existentes
            # Isso é executado de forma assíncrona através de create_task
            self._reflexoes_iniciais_task = asyncio.create_task(self._executar_reflexoes_iniciais())
            
        except Exception as e:
            self.logger.error(f"Erro na inicialização do sistema: {str(e)}")
            raise

    async def iniciar_ciclo(self):
        """Inicia o ciclo de reflexão contínua."""
        if self._ciclo_task is not None:
            self.logger.warning("Ciclo de reflexão já está ativo")
            return

        self._ciclo_task = asyncio.create_task(self.ciclo_reflexao_continuo())
        self._ciclo_aprendizado_task = asyncio.create_task(self.gerenciador_aprendizado.ciclo_aprendizado_continuo())
        self._ciclo_adaptativo_task = asyncio.create_task(self.aprendizado_adaptativo.iniciar_ciclo_adaptativo())
        
        self.logger.info("Ciclo de reflexão iniciado")

    async def ciclo_reflexao_continuo(self):
        """Executa o ciclo contínuo de reflexão."""
        try:
            while True:
                await self._executar_ciclo_reflexao()
                await asyncio.sleep(1)  # Intervalo entre ciclos
        except asyncio.CancelledError:
            self.logger.info("Ciclo de reflexão interrompido")
        except Exception as e:
            self.logger.error(f"Erro no ciclo de reflexão: {str(e)}")

    async def _executar_ciclo_reflexao(self):
        """Executa um ciclo de reflexão."""
        try:
            pensamentos = await self._obter_pensamentos_pendentes()
            for pensamento in pensamentos:
                resultado = await self.persona.receber_pensamento(pensamento)
                if resultado['status'] == 'sucesso':
                    self.logger.info(f"Pensamento processado com sucesso: {pensamento['tipo']}")
                else:
                    self.logger.error(f"Erro ao processar pensamento: {resultado['erro']}")
        except Exception as e:
            self.logger.error(f"Erro ao executar ciclo de reflexão: {str(e)}")

    async def _obter_pensamentos_pendentes(self) -> List[Dict[str, Any]]:
        """Obtém pensamentos pendentes para processamento."""
        try:
            # Obtém memórias recentes
            todas_memorias = self.memoria.listar_todas_memorias()
            if not todas_memorias:
                return []
            
            # Sempre seleciona algumas memórias para processar (garantindo que pelo menos reflexão ocorra)
            quantidade = min(3, len(todas_memorias))  # No máximo 3 memórias por ciclo
            memorias_selecionadas = random.sample(todas_memorias, quantidade) if len(todas_memorias) > quantidade else todas_memorias
            
            pensamentos = []
            
            # Cria pensamentos de reflexão para cada memória
            for memoria in memorias_selecionadas:
                # Pensamento de reflexão sobre a memória - sempre ocorre
                pensamentos.append({
                    'tipo': 'reflexao',
                    'conteudo': memoria['conteudo'],
                    'memoria_origem': memoria['id'],
                    'timestamp': datetime.now(),
                    'prioridade': 2
                })
                
                # Chance de criar pensamento de síntese (combinando memórias)
                if random.random() < 0.5 and len(todas_memorias) > 1:  # 50% de chance
                    # Pega outra memória aleatória diferente da atual
                    outras_memorias = [m for m in todas_memorias if m['id'] != memoria['id']]
                    if outras_memorias:
                        outra_memoria = random.choice(outras_memorias)
                        
                        # Cria pensamento de síntese
                        pensamentos.append({
                            'tipo': 'sintese',
                            'conteudo': f"Combinando: '{memoria['conteudo']}' com '{outra_memoria['conteudo']}'",
                            'memorias_origem': [memoria['id'], outra_memoria['id']],
                            'timestamp': datetime.now(),
                            'prioridade': 3
                        })
            
            # Chance de criar pensamento de metacognição (avaliação do aprendizado)
            if random.random() < 0.3:  # 30% de chance
                pensamentos.append({
                    'tipo': 'metacognicao',
                    'conteudo': "Avaliando qualidade do aprendizado recente",
                    'timestamp': datetime.now(),
                    'prioridade': 4
                })
            
            # Log dos pensamentos gerados
            if pensamentos:
                self.logger.info(f"Gerados {len(pensamentos)} pensamentos para processamento")
            
            return pensamentos
            
        except Exception as e:
            self.logger.error(f"Erro ao obter pensamentos pendentes: {str(e)}")
            return []

    async def receber_pensamento(self, pensamento: Dict[str, Any]) -> Dict[str, Any]:
        """Recebe e processa um pensamento."""
        try:
            if not isinstance(pensamento, dict):
                raise ValueError("Pensamento deve ser um dicionário")

            resultado = await self.persona.receber_pensamento(pensamento)
            return resultado

        except Exception as e:
            self.logger.error(f"Erro ao receber pensamento: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now()
            }

    async def encerrar_ciclo(self):
        """Encerra o ciclo de reflexão."""
        if self._ciclo_task is None:
            self.logger.warning("Ciclo de reflexão já está encerrado")
            return

        self._ciclo_task.cancel()
        self._ciclo_aprendizado_task.cancel()
        self._ciclo_adaptativo_task.cancel()
        
        self._ciclo_task = None
        self._ciclo_aprendizado_task = None
        self._ciclo_adaptativo_task = None
        
        self.logger.info("Ciclo de reflexão encerrado")

    def status(self) -> Dict[str, Any]:
        """Retorna o status atual do sistema."""
        return {
            'persona': self.persona.status(),
            'aprendizado': self.gerenciador_aprendizado.status_aprendizado(),
            'adaptacao': self.aprendizado_adaptativo.status_adaptacao(),
            'ciclo_ativo': self._ciclo_task is not None
        }

    async def _executar_reflexoes_iniciais(self):
        """Executa reflexões iniciais sobre as memórias existentes."""
        try:
            todas_memorias = self.memoria.listar_todas_memorias()
            if todas_memorias:
                self.logger.info(f"Executando reflexões iniciais sobre {len(todas_memorias)} memórias existentes")
                
                # Seleciona algumas memórias para reflexão inicial
                quantidade = min(5, len(todas_memorias))
                for _ in range(quantidade):
                    await self._executar_ciclo_reflexao()
                    
                self.logger.info("Reflexões iniciais concluídas")
        except Exception as e:
            self.logger.error(f"Erro ao executar reflexões iniciais: {str(e)}") 