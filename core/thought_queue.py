"""
Módulo de Fila de Pensamentos - Gerencia o fluxo cognitivo do sistema.

Este módulo implementa a estrutura de dados para armazenar e gerenciar
os pensamentos do sistema, incluindo priorização, emoções e expiração.
"""

import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class Pensamento:
    """Classe que representa um pensamento no sistema."""
    
    def __init__(self, tipo: str, conteudo: str, prioridade: int = 1, 
                 metadata: Dict[str, Any] = None, tags: List[str] = None,
                 emocao: str = None, duracao_segundos: int = 300):
        """
        Inicializa um novo pensamento.
        
        Args:
            tipo: Tipo do pensamento (ex: reflexao, alerta, duvida)
            conteudo: Conteúdo do pensamento
            prioridade: Nível de prioridade (padrão: 1)
            metadata: Dados adicionais (opcional)
            tags: Lista de tags contextuais (opcional)
            emocao: Emoção predominante (opcional)
            duracao_segundos: Tempo até expiração em segundos (padrão: 300)
        """
        self.id = str(uuid.uuid4())
        self.tipo = tipo
        self.conteudo = conteudo
        self.prioridade = prioridade
        self.metadata = metadata or {}
        self.tags = tags or []
        self.emocao = emocao
        self.timestamp = datetime.now()
        self.expira_em = self.timestamp + timedelta(seconds=duracao_segundos)
        self.processado = False
        self.resultado = None
        self.processado_em = None
        self.intensidade_emocional = 1.0  # Escala de 0.0 a 1.0
        self.feedback_count = 0
        self.feedback_score = 0.0  # Média dos feedbacks recebidos
    
    def __lt__(self, other):
        """Compara pensamentos por prioridade (usado para ordenação)."""
        return self.prioridade > other.prioridade
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o pensamento para um dicionário.
        
        Returns:
            Dicionário com os dados do pensamento
        """
        return {
            'id': self.id,
            'tipo': self.tipo,
            'conteudo': self.conteudo,
            'prioridade': self.prioridade,
            'metadata': self.metadata,
            'tags': self.tags,
            'emocao': self.emocao,
            'timestamp': self.timestamp.isoformat(),
            'expira_em': self.expira_em.isoformat(),
            'processado': self.processado,
            'resultado': self.resultado,
            'processado_em': self.processado_em.isoformat() if self.processado_em else None,
            'intensidade_emocional': self.intensidade_emocional,
            'feedback_count': self.feedback_count,
            'feedback_score': self.feedback_score
        }
    
    def esta_expirado(self) -> bool:
        """Verifica se o pensamento expirou."""
        return datetime.now() > self.expira_em
    
    def ajustar_prioridade(self, delta: int):
        """
        Ajusta a prioridade do pensamento.
        
        Args:
            delta: Valor a ser adicionado/subtraído da prioridade
        """
        self.prioridade = max(0, self.prioridade + delta)
    
    def ajustar_intensidade_emocional(self, nova_intensidade: float):
        """
        Ajusta a intensidade emocional do pensamento.
        
        Args:
            nova_intensidade: Nova intensidade (0.0 a 1.0)
        """
        self.intensidade_emocional = max(0.0, min(1.0, nova_intensidade))
    
    def adicionar_feedback(self, score: float):
        """
        Adiciona feedback ao pensamento.
        
        Args:
            score: Pontuação do feedback (0.0 a 1.0)
        """
        self.feedback_count += 1
        self.feedback_score = ((self.feedback_score * (self.feedback_count - 1)) + score) / self.feedback_count
        # Ajusta prioridade baseado no feedback
        if score > 0.7:  # Feedback positivo
            self.ajustar_prioridade(1)
        elif score < 0.3:  # Feedback negativo
            self.ajustar_prioridade(-1)
    
    def marcar_como_processado(self, resultado: Any):
        """
        Marca o pensamento como processado.
        
        Args:
            resultado: Resultado do processamento
        """
        self.processado = True
        self.resultado = resultado
        self.processado_em = datetime.now()
    
    def __repr__(self) -> str:
        """Retorna uma representação string do pensamento."""
        status = "PROCESSADO" if self.processado else "PENDENTE"
        emocao_str = f" | {self.emocao} ({self.intensidade_emocional:.1f})" if self.emocao else ""
        tags_str = f" | tags: {','.join(self.tags)}" if self.tags else ""
        feedback_str = f" | feedback: {self.feedback_score:.1f}" if self.feedback_count > 0 else ""
        return f"<{status} | {self.tipo.upper()} | {self.conteudo[:30]}... | Prio: {self.prioridade}{emocao_str}{tags_str}{feedback_str}>"

class FilaPensamentos:
    """Classe que gerencia a fila de pensamentos."""
    
    def __init__(self):
        """Inicializa a fila de pensamentos."""
        self.fila_ativa = []
        self.historico = []
        self.estatisticas = {
            "total_processados": 0,
            "por_emocao": {},
            "por_tipo": {},
            "media_feedback": 0.0
        }
    
    def adicionar(self, pensamento: Pensamento):
        """
        Adiciona um pensamento à fila.
        
        Args:
            pensamento: Instância de Pensamento
        """
        self.fila_ativa.append(pensamento)
        self._ordenar_fila()
    
    def proximo(self) -> Optional[Pensamento]:
        """
        Retorna o próximo pensamento da fila.
        
        Returns:
            Próximo pensamento ou None se a fila estiver vazia
        """
        self._limpar_expirados()
        if not self.fila_ativa:
            return None
        
        pensamento = self.fila_ativa.pop(0)
        return pensamento
    
    def processar(self, pensamento: Pensamento, resultado: Any):
        """
        Processa um pensamento e o move para o histórico.
        
        Args:
            pensamento: Pensamento a ser processado
            resultado: Resultado do processamento
        """
        pensamento.marcar_como_processado(resultado)
        self.historico.append(pensamento)
        
        # Atualiza estatísticas
        self.estatisticas["total_processados"] += 1
        
        # Atualiza estatísticas por emoção
        if pensamento.emocao:
            if pensamento.emocao not in self.estatisticas["por_emocao"]:
                self.estatisticas["por_emocao"][pensamento.emocao] = 0
            self.estatisticas["por_emocao"][pensamento.emocao] += 1
        
        # Atualiza estatísticas por tipo
        if pensamento.tipo not in self.estatisticas["por_tipo"]:
            self.estatisticas["por_tipo"][pensamento.tipo] = 0
        self.estatisticas["por_tipo"][pensamento.tipo] += 1
        
        # Atualiza média de feedback
        if pensamento.feedback_count > 0:
            total_feedback = self.estatisticas["media_feedback"] * (self.estatisticas["total_processados"] - 1)
            self.estatisticas["media_feedback"] = (total_feedback + pensamento.feedback_score) / self.estatisticas["total_processados"]
    
    def vazia(self) -> bool:
        """
        Verifica se a fila está vazia.
        
        Returns:
            True se a fila estiver vazia
        """
        self._limpar_expirados()
        return len(self.fila_ativa) == 0
    
    def _limpar_expirados(self):
        """Remove pensamentos expirados da fila."""
        expirados = [p for p in self.fila_ativa if p.esta_expirado()]
        for p in expirados:
            p.marcar_como_processado("Expirado")
            self.historico.append(p)
        self.fila_ativa = [p for p in self.fila_ativa if not p.esta_expirado()]
    
    def _ordenar_fila(self):
        """Ordena a fila por prioridade e intensidade emocional."""
        self.fila_ativa.sort(key=lambda p: (p.prioridade * p.intensidade_emocional), reverse=True)
    
    def listar(self) -> List[Pensamento]:
        """
        Lista os pensamentos na fila.
        
        Returns:
            Lista de pensamentos
        """
        return self.fila_ativa.copy()
    
    def listar_fila(self) -> List[str]:
        """
        Lista os pensamentos na fila como strings.
        
        Returns:
            Lista de representações string dos pensamentos
        """
        return [str(p) for p in self.fila_ativa]
    
    def listar_historico(self, n: int = 10) -> List[str]:
        """
        Lista os últimos n pensamentos processados.
        
        Args:
            n: Número de pensamentos a retornar
            
        Returns:
            Lista de representações string dos pensamentos
        """
        return [str(p) for p in self.historico[-n:]]
    
    def listar_processados(self) -> List[Pensamento]:
        """
        Lista os pensamentos processados.
        
        Returns:
            Lista de pensamentos processados
        """
        return [p for p in self.historico if p.processado]
    
    def limpar_processados(self):
        """Limpa a lista de pensamentos processados."""
        self.historico = [p for p in self.historico if not p.processado]
    
    def buscar_por_tipo(self, tipo: str) -> List[Pensamento]:
        """
        Busca pensamentos por tipo.
        
        Args:
            tipo: Tipo a buscar
            
        Returns:
            Lista de pensamentos do tipo especificado
        """
        return [p for p in self.historico if p.tipo == tipo]
    
    def buscar_por_id(self, id_pensamento: str) -> Optional[Pensamento]:
        """
        Busca um pensamento por ID.
        
        Args:
            id_pensamento: ID do pensamento
            
        Returns:
            Pensamento encontrado ou None
        """
        for p in self.historico:
            if p.id == id_pensamento:
                return p
        return None
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """
        Retorna estatísticas sobre os pensamentos processados.
        
        Returns:
            Dicionário com estatísticas
        """
        return self.estatisticas
    
    def buscar_por_emocao(self, emocao: str) -> List[Pensamento]:
        """
        Busca pensamentos por emoção.
        
        Args:
            emocao: Emoção a buscar
            
        Returns:
            Lista de pensamentos com a emoção especificada
        """
        return [p for p in self.historico if p.emocao == emocao]
    
    def buscar_por_tag(self, tag: str) -> List[Pensamento]:
        """
        Busca pensamentos por tag.
        
        Args:
            tag: Tag a buscar
            
        Returns:
            Lista de pensamentos com a tag especificada
        """
        return [p for p in self.historico if tag in p.tags] 