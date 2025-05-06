"""
Módulo Processador de Pensamento - Implementa o processamento de pensamentos do Alma.
"""

import logging
import random
from typing import Dict, Any, List
from datetime import datetime

class ProcessadorPensamento:
    def __init__(self, persona):
        """Inicializa o processador de pensamento."""
        self.persona = persona
        self.logger = logging.getLogger(__name__)
        self.pensamentos_pendentes = []
        self.ultima_processamento = datetime.now()

    async def processar_pensamento(self, pensamento: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento."""
        try:
            if not isinstance(pensamento, dict):
                raise ValueError("Pensamento deve ser um dicionário")

            # Adiciona timestamp se não existir
            if 'timestamp' not in pensamento:
                pensamento['timestamp'] = datetime.now().isoformat()

            # Processa o pensamento
            resultado = await self._executar_processamento(pensamento)
            
            # Atualiza timestamp
            self.ultima_processamento = datetime.now()
            
            return resultado

        except Exception as e:
            self.logger.error(f"Erro ao processar pensamento: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _executar_processamento(self, pensamento: Dict[str, Any]) -> Dict[str, Any]:
        """Executa o processamento do pensamento."""
        try:
            # Obtém o tipo do pensamento
            tipo = pensamento.get('tipo', 'desconhecido')
            
            # Processa baseado no tipo
            if tipo == 'mensagem':
                return await self._processar_mensagem(pensamento)
            elif tipo == 'aprendizado':
                return await self._processar_aprendizado(pensamento)
            elif tipo == 'reflexao':
                return await self._processar_reflexao(pensamento)
            elif tipo == 'sintese':
                return await self._processar_sintese(pensamento)
            elif tipo == 'metacognicao':
                return await self._processar_metacognicao(pensamento)
            else:
                return await self._processar_generico(pensamento)

        except Exception as e:
            self.logger.error(f"Erro ao executar processamento: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _processar_mensagem(self, pensamento: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma mensagem."""
        try:
            # Adiciona à memória
            memoria = self.persona.memoria.adicionar_memoria(
                conteudo=pensamento['conteudo'],
                tipo='mensagem',
                prioridade=pensamento.get('prioridade', 1)
            )
            
            return {
                'status': 'sucesso',
                'conteudo': f"Processei sua mensagem: {pensamento['conteudo']}",
                'memoria_id': memoria['id'] if memoria else None,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Erro ao processar mensagem: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _processar_aprendizado(self, pensamento: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um aprendizado."""
        try:
            # Adiciona à memória
            memoria = self.persona.memoria.adicionar_memoria(
                conteudo=pensamento['conteudo'],
                tipo='aprendizado',
                prioridade=pensamento.get('prioridade', 2)
            )
            
            return {
                'status': 'sucesso',
                'conteudo': f"Processei o aprendizado: {pensamento['conteudo']}",
                'memoria_id': memoria['id'] if memoria else None,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Erro ao processar aprendizado: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _processar_reflexao(self, pensamento: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento de reflexão."""
        try:
            # Obtem a memória de origem
            memoria_origem_id = pensamento.get('memoria_origem')
            conteudo_reflexao = pensamento['conteudo']
            
            # Cria uma reflexão mais elaborada
            reflexao = f"Reflexão sobre '{conteudo_reflexao}': "
            
            # Adiciona algum conteúdo à reflexão baseado no texto original
            palavras = conteudo_reflexao.split()
            if len(palavras) > 0:
                if '?' in conteudo_reflexao:
                    reflexao += f"Esta é uma pergunta sobre {' '.join(palavras[:3])}..."
                else:
                    reflexao += f"Isso se relaciona com conceitos de {' '.join(palavras[:2])}..."
            
            # Adiciona à memória
            memoria = self.persona.memoria.adicionar_memoria(
                conteudo=reflexao,
                tipo='reflexao',
                prioridade=pensamento.get('prioridade', 2)
            )
            
            return {
                'status': 'sucesso',
                'conteudo': reflexao,
                'memoria_id': memoria['id'] if memoria else None,
                'memoria_origem': memoria_origem_id,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Erro ao processar reflexão: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _processar_sintese(self, pensamento: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento de síntese (combinação de memórias)."""
        try:
            # Obtem as memórias de origem
            memorias_origem = pensamento.get('memorias_origem', [])
            conteudo_sintese = pensamento['conteudo']
            
            # Extrai os conceitos das duas memórias
            partes = conteudo_sintese.split("' com '")
            if len(partes) >= 2:
                conceito1 = partes[0].replace("Combinando: '", "")
                conceito2 = partes[1].replace("'", "")
                
                # Cria uma síntese combinando os conceitos
                conectores = ["relaciona-se com", "pode ser integrado com", "complementa", "expande o conceito de"]
                conector = random.choice(conectores)
                
                sintese = f"Síntese: O conceito '{conceito1}' {conector} '{conceito2}', formando uma nova compreensão."
            else:
                sintese = f"Síntese das memórias: {conteudo_sintese}"
            
            # Adiciona à memória
            memoria = self.persona.memoria.adicionar_memoria(
                conteudo=sintese,
                tipo='sintese',
                prioridade=pensamento.get('prioridade', 3)
            )
            
            return {
                'status': 'sucesso',
                'conteudo': sintese,
                'memoria_id': memoria['id'] if memoria else None,
                'memorias_origem': memorias_origem,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Erro ao processar síntese: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _processar_metacognicao(self, pensamento: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento de metacognição (reflexão sobre o próprio aprendizado)."""
        try:
            # Obtém algumas memórias recentes
            memorias = self.persona.memoria.listar_memorias(5)  # últimas 5 memórias
            
            # Avalia a qualidade/diversidade do aprendizado
            tipos_memoria = set()
            for memoria in memorias:
                tipos_memoria.add(memoria.get('tipo', 'desconhecido'))
            
            # Cria uma avaliação metacognitiva
            metacognicao = "Avaliação do aprendizado recente: "
            
            if len(memorias) < 3:
                metacognicao += "Poucas memórias recentes, preciso adquirir mais experiências."
            elif len(tipos_memoria) < 2:
                metacognicao += "Aprendizado limitado a poucos tipos de informação, preciso diversificar."
            else:
                metacognicao += f"Bom progresso com {len(tipos_memoria)} tipos diferentes de informação."
            
            # Adiciona à memória
            memoria = self.persona.memoria.adicionar_memoria(
                conteudo=metacognicao,
                tipo='metacognicao',
                prioridade=pensamento.get('prioridade', 4)
            )
            
            return {
                'status': 'sucesso',
                'conteudo': metacognicao,
                'memoria_id': memoria['id'] if memoria else None,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Erro ao processar metacognição: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _processar_generico(self, pensamento: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento genérico."""
        try:
            # Adiciona à memória
            memoria = self.persona.memoria.adicionar_memoria(
                conteudo=pensamento['conteudo'],
                tipo=pensamento.get('tipo', 'geral'),
                prioridade=pensamento.get('prioridade', 1)
            )
            
            return {
                'status': 'sucesso',
                'conteudo': f"Processei o pensamento: {pensamento['conteudo']}",
                'memoria_id': memoria['id'] if memoria else None,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Erro ao processar pensamento genérico: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def status(self) -> Dict[str, Any]:
        """Retorna o status do processador."""
        return {
            'pensamentos_pendentes': len(self.pensamentos_pendentes),
            'ultima_processamento': self.ultima_processamento.isoformat()
        } 