"""
Módulo Persona - Implementa a personalidade e processamento cognitivo do sistema.
"""

import logging
from typing import Dict, Any
from datetime import datetime

class Persona:
    def __init__(self, memoria):
        """Inicializa a Persona."""
        self.memoria = memoria
        self.logger = logging.getLogger(__name__)
        self.conhecimento = {}
        self.ultima_atualizacao = datetime.now()
        self.processador_pensamento = None  # Será inicializado depois para evitar referência circular

    def inicializar_processador(self, processador):
        """Inicializa o processador de pensamentos."""
        self.processador_pensamento = processador

    async def receber_pensamento(self, pensamento: Dict[str, Any]) -> Dict[str, Any]:
        """Recebe e processa um pensamento."""
        try:
            if not isinstance(pensamento, dict):
                raise ValueError("Pensamento deve ser um dicionário")

            if self.processador_pensamento is None:
                raise ValueError("Processador de pensamentos não inicializado")

            # Processa o pensamento
            resultado = await self.processador_pensamento.processar_pensamento(pensamento)
            
            # Se o processamento foi bem sucedido, atualiza o conhecimento
            if resultado['status'] == 'sucesso':
                self._atualizar_conhecimento(pensamento, resultado)
            
            return resultado

        except Exception as e:
            self.logger.error(f"Erro ao receber pensamento: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now()
            }

    def _atualizar_conhecimento(self, pensamento: Dict[str, Any], resultado: Dict[str, Any]):
        """Atualiza o conhecimento baseado no pensamento processado."""
        try:
            # Obtém conhecimento relevante
            conhecimento = self.obter_conhecimento_relevante(pensamento['conteudo'])
            
            # Atualiza o conhecimento
            self.conhecimento.update(conhecimento)
            self.ultima_atualizacao = datetime.now()
            
        except Exception as e:
            self.logger.error(f"Erro ao atualizar conhecimento: {str(e)}")

    def status(self) -> Dict[str, Any]:
        """Retorna o status da persona."""
        return {
            'conhecimento_atual': len(self.conhecimento),
            'ultima_atualizacao': self.ultima_atualizacao.isoformat(),
            'processador_ativo': self.processador_pensamento is not None,
            'memoria_status': self.memoria.status()
        }

    def obter_conhecimento_relevante(self, contexto: str) -> Dict[str, Any]:
        """Obtém conhecimento relevante para um dado contexto."""
        try:
            # Busca memórias relacionadas ao contexto
            memorias_relacionadas = self.memoria.buscar_memorias(contexto)
            
            # Analisa o contexto das memórias
            contexto_analisado = self._analisar_contexto(memorias_relacionadas)
            
            # Identifica padrões
            padroes = self._identificar_padroes(memorias_relacionadas)
            
            # Gera insights
            insights = self._gerar_insights(memorias_relacionadas, padroes)
            
            # Tira conclusões
            conclusoes = self._tirar_conclusoes(memorias_relacionadas, insights)
            
            # Atualiza o conhecimento
            self.conhecimento = {
                'temas_relacionados': contexto_analisado['temas_relacionados'],
                'frequencia_temas': contexto_analisado['frequencia_temas'],
                'padroes': padroes,
                'insights': insights,
                'conclusoes': conclusoes,
                'total_memorias': len(memorias_relacionadas)
            }
            self.ultima_atualizacao = datetime.now()
            
            return self.conhecimento
            
        except Exception as e:
            self.logger.error(f"Erro ao obter conhecimento relevante: {str(e)}")
            return {
                'temas_relacionados': [],
                'frequencia_temas': {},
                'padroes': [],
                'insights': [],
                'conclusoes': [],
                'total_memorias': 0
            }

    def _analisar_contexto(self, memorias: list) -> Dict[str, Any]:
        """Analisa o contexto das memórias."""
        try:
            # Palavras comuns para ignorar
            palavras_ignorar = {'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'e', 'é', 'de', 'da', 'do', 'das', 'dos', 'em', 'no', 'na', 'nos', 'nas', 'com', 'que', 'quem', 'onde', 'como', 'quando', 'por', 'para', 'porque', 'pois', 'mas', 'se', 'não', 'sim', 'também', 'já', 'ainda', 'só', 'apenas', 'muito', 'pouco', 'mais', 'menos', 'bem', 'mal', 'tudo', 'nada', 'algo', 'alguém', 'ninguém', 'cada', 'qual', 'quais', 'qualquer', 'quaisquer', 'todo', 'toda', 'todos', 'todas', 'este', 'esta', 'estes', 'estas', 'esse', 'essa', 'esses', 'essas', 'aquele', 'aquela', 'aqueles', 'aquelas', 'isto', 'isso', 'aquilo', 'meu', 'minha', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas', 'seu', 'sua', 'seus', 'suas', 'nosso', 'nossa', 'nossos', 'nossas', 'vosso', 'vossa', 'vossos', 'vossas', 'deles', 'delas', 'lhes', 'lhe', 'me', 'te', 'se', 'nos', 'vos', 'o', 'a', 'os', 'as', 'lo', 'la', 'los', 'las', 'no', 'na', 'nos', 'nas', 'lhe', 'lhes', 'se', 'si', 'consigo', 'comigo', 'contigo', 'conosco', 'convosco', 'com', 'sem', 'por', 'para', 'pelo', 'pela', 'pelos', 'pelas', 'ante', 'após', 'até', 'com', 'contra', 'desde', 'entre', 'para', 'perante', 'por', 'sem', 'sob', 'sobre', 'trás', 'durante', 'mediante', 'salvo', 'segundo', 'visto', 'exceto', 'menos', 'fora', 'além', 'aquém', 'através', 'dentro', 'fora', 'longe', 'perto', 'junto', 'além', 'aquém', 'através', 'dentro', 'fora', 'longe', 'perto', 'junto', 'além', 'aquém', 'através', 'dentro', 'fora', 'longe', 'perto', 'junto'}
            
            # Contador de palavras
            contador_palavras = {}
            
            for memoria in memorias:
                # Divide o conteúdo em palavras e remove pontuação
                palavras = memoria['conteudo'].lower().replace('?', '').replace('!', '').replace('.', '').replace(',', '').split()
                
                # Conta palavras significativas
                for palavra in palavras:
                    if palavra not in palavras_ignorar and len(palavra) > 2:
                        contador_palavras[palavra] = contador_palavras.get(palavra, 0) + 1
            
            # Ordena palavras por frequência
            temas_ordenados = sorted(contador_palavras.items(), key=lambda x: x[1], reverse=True)
            
            return {
                'temas_relacionados': [tema for tema, _ in temas_ordenados[:5]],  # Top 5 temas
                'frequencia_temas': dict(temas_ordenados)
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao analisar contexto: {str(e)}")
            return {
                'temas_relacionados': [],
                'frequencia_temas': {}
            }

    def _identificar_padroes(self, memorias: list) -> list:
        """Identifica padrões nas memórias."""
        try:
            padroes = []
            
            # Agrupa memórias por tipo
            memorias_por_tipo = {}
            for memoria in memorias:
                tipo = memoria.get('tipo', 'desconhecido')
                if tipo not in memorias_por_tipo:
                    memorias_por_tipo[tipo] = []
                memorias_por_tipo[tipo].append(memoria)
            
            # Identifica padrões por tipo
            for tipo, mems in memorias_por_tipo.items():
                if len(mems) > 1:
                    padroes.append(f"Padrão identificado: {len(mems)} memórias do tipo '{tipo}'")
            
            return padroes
            
        except Exception as e:
            self.logger.error(f"Erro ao identificar padrões: {str(e)}")
            return []

    def _gerar_insights(self, memorias: list, padroes: list) -> list:
        """Gera insights baseados nas memórias e padrões."""
        try:
            insights = []
            
            # Adiciona insights baseados em padrões
            for padrao in padroes:
                insights.append(f"Insight: {padrao}")
            
            # Adiciona insights baseados em frequência de temas
            contexto = self._analisar_contexto(memorias)
            for tema, freq in contexto['frequencia_temas'].items():
                if freq > 2:
                    insights.append(f"Insight: Tema '{tema}' aparece frequentemente ({freq} vezes)")
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar insights: {str(e)}")
            return []

    def _tirar_conclusoes(self, memorias: list, insights: list) -> list:
        """Tira conclusões baseadas nas memórias e insights."""
        try:
            conclusoes = []
            
            # Adiciona conclusões baseadas em insights
            for insight in insights:
                conclusoes.append(f"Conclusão: {insight}")
            
            # Adiciona conclusões baseadas em quantidade de memórias
            if len(memorias) > 5:
                conclusoes.append(f"Conclusão: Existe um conjunto significativo de {len(memorias)} memórias relacionadas")
            
            return conclusoes
            
        except Exception as e:
            self.logger.error(f"Erro ao tirar conclusões: {str(e)}")
            return []

    def buscar_memorias(self, termo: str) -> list:
        """Busca memórias que contêm o termo especificado.
        
        Args:
            termo: Termo a ser buscado nas memórias
            
        Returns:
            Lista de memórias que contêm o termo
        """
        try:
            todas_memorias = self.memoria.listar_todas_memorias()
            return [m for m in todas_memorias if termo.lower() in m.get('conteudo', '').lower()]
        except Exception as e:
            self.logger.error(f"Erro ao buscar memórias: {str(e)}")
            return []

    def listar_memorias(self, n: int = 5) -> list:
        """Retorna a lista de todas as memórias armazenadas.
        
        Args:
            n: Número de memórias a retornar (opcional, padrão: 5)
            
        Returns:
            Lista de memórias
        """
        try:
            return self.memoria.listar_todas_memorias()[:n] if n > 0 else self.memoria.listar_todas_memorias()
        except Exception as e:
            self.logger.error(f"Erro ao listar memórias: {str(e)}")
            return [] 