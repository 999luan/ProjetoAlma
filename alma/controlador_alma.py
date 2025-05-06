"""
Módulo principal do sistema Alma.
Implementa o processamento e reflexão do sistema.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from .thought_queue import FilaPensamentos, Pensamento
import random

logger = logging.getLogger(__name__)

class Alma:
    """Classe principal do sistema Alma."""
    
    def __init__(self, persona):
        """
        Inicializa o sistema Alma.
        
        Args:
            persona: Instância do sistema Persona para gerenciamento de memórias
        """
        self.persona = persona
        self.fila_pensamentos = FilaPensamentos()
        self.ciclos_reflexao = 0
        self.insights = []
        
        # Registra os processadores de pensamentos
        self.processadores = {
            "reflexao": self._processar_reflexao,
            "metacognicao": self._processar_metacognicao,
            "insight": self._processar_insight,
            "memoria": self._processar_memoria,
            "duvida": self._processar_duvida,
            "contradicao": self._processar_contradicao,
            "padrao": self._processar_padrao
        }
        
        logger.info("Alma inicializada")

    async def receber_pensamento(self, tipo: str, conteudo: str, prioridade: int = 0, 
                          metadata: Dict[str, Any] = None, tags: List[str] = None,
                          emocao: str = None, duracao_segundos: int = 300) -> str:
        """
        Recebe um novo pensamento para processamento.
        
        Args:
            tipo: Tipo do pensamento
            conteudo: Conteúdo do pensamento
            prioridade: Nível de prioridade
            metadata: Dados adicionais
            tags: Lista de tags contextuais
            emocao: Emoção predominante
            duracao_segundos: Tempo até expiração em segundos
            
        Returns:
            ID do pensamento
        """
        # Ajusta prioridade baseado na emoção
        if emocao:
            prioridade = self._ajustar_prioridade_por_emocao(prioridade, emocao)
        
        pensamento = Pensamento(tipo, conteudo, prioridade, metadata, tags, emocao, duracao_segundos)
        self.fila_pensamentos.adicionar(pensamento)
        logger.info(f"Novo pensamento recebido: {tipo} | {conteudo[:30]}... | Emoção: {emocao}")
        return pensamento.id

    def _ajustar_prioridade_por_emocao(self, prioridade: int, emocao: str) -> int:
        """
        Ajusta a prioridade do pensamento baseado na emoção.
        
        Args:
            prioridade: Prioridade original
            emocao: Emoção do pensamento
            
        Returns:
            Prioridade ajustada
        """
        # Emoções que aumentam prioridade
        emocoes_urgentes = ["medo", "raiva", "alerta", "ansiedade"]
        # Emoções que diminuem prioridade
        emocoes_calmas = ["tranquilidade", "satisfacao", "gratidao"]
        
        if emocao.lower() in emocoes_urgentes:
            return prioridade + 2
        elif emocao.lower() in emocoes_calmas:
            return max(0, prioridade - 1)
        return prioridade

    async def ciclo_cognitivo(self) -> Optional[Dict[str, Any]]:
        """
        Executa um ciclo de processamento cognitivo.
        
        Returns:
            Resultado do processamento ou None se não houver pensamentos
        """
        logger.info("[Alma] Iniciando ciclo cognitivo...")
        
        if self.fila_pensamentos.vazia():
            logger.info("[Alma] Nenhum pensamento na fila.")
            return None

        pensamento = self.fila_pensamentos.proximo()
        logger.info(f"[Alma] Processando pensamento: {pensamento.tipo} | {pensamento.conteudo[:30]}...")

        # Processa o pensamento com base no tipo
        processador = self.processadores.get(pensamento.tipo)
        if processador:
            resultado = await processador(pensamento.conteudo, pensamento.metadata)
            
            # Avalia o resultado e adiciona feedback
            feedback = self._avaliar_resultado(resultado, pensamento)
            pensamento.adicionar_feedback(feedback)
            
            # Registra o resultado no histórico
            self.fila_pensamentos.processar(pensamento, resultado)
            
            # Atualiza estatísticas
            estatisticas = self.fila_pensamentos.obter_estatisticas()
            logger.info(f"[Alma] Estatísticas atualizadas: {estatisticas}")
            
            return {
                "pensamento_id": pensamento.id,
                "tipo": pensamento.tipo,
                "resultado": resultado,
                "emocao": pensamento.emocao,
                "tags": pensamento.tags,
                "feedback": feedback,
                "estatisticas": estatisticas
            }
        
        return None

    def _avaliar_resultado(self, resultado: Any, pensamento: Pensamento) -> float:
        """
        Avalia a qualidade do resultado do processamento.
        
        Args:
            resultado: Resultado do processamento
            pensamento: Pensamento processado
            
        Returns:
            Score de feedback (0.0 a 1.0)
        """
        # Implementação básica - pode ser expandida com análise mais sofisticada
        if isinstance(resultado, dict) and "resultado" in resultado:
            # Avalia baseado no tipo de pensamento
            if pensamento.tipo == "reflexao":
                return 0.8 if len(resultado["resultado"]) > 50 else 0.5
            elif pensamento.tipo == "alerta":
                return 0.9 if "importante" in resultado["resultado"].lower() else 0.6
            elif pensamento.tipo == "duvida":
                return 0.7 if "?" in resultado["resultado"] else 0.4
        return 0.5  # Score padrão

    async def _processar_reflexao(self, conteudo: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento do tipo reflexão."""
        logger.info(f"[Alma] Processando reflexão: {conteudo[:50]}...")
        # Simula processamento reflexivo
        await asyncio.sleep(0.5)
        return {
            "tipo": "reflexao",
            "resultado": "Reflexão processada com sucesso",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _processar_metacognicao(self, conteudo: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento do tipo metacognição."""
        logger.info(f"[Alma] Processando metacognição: {conteudo[:50]}...")
        # Simula análise metacognitiva
        await asyncio.sleep(0.5)
        return {
            "tipo": "metacognicao",
            "resultado": "Análise metacognitiva concluída",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _processar_insight(self, conteudo: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento do tipo insight."""
        logger.info(f"[Alma] Processando insight: {conteudo[:50]}...")
        # Registra o insight
        insight = {
            "id": len(self.insights) + 1,
            "descricao": conteudo,
            "timestamp": datetime.now().isoformat()
        }
        self.insights.append(insight)
        return {
            "tipo": "insight",
            "resultado": "Insight registrado com sucesso",
            "insight_id": insight["id"],
            "timestamp": datetime.now().isoformat()
        }
    
    async def _processar_memoria(self, conteudo: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento do tipo memória."""
        logger.info(f"[Alma] Processando memória: {conteudo[:50]}...")
        # Simula processamento de memória
        await asyncio.sleep(0.5)
        return {
            "tipo": "memoria",
            "resultado": "Memória processada com sucesso",
            "memoria_id": metadata.get("memoria_id"),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _processar_duvida(self, conteudo: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento do tipo dúvida."""
        logger.info(f"[Alma] Processando dúvida: {conteudo[:50]}...")
        # Simula análise de dúvida
        await asyncio.sleep(0.5)
        return {
            "tipo": "duvida",
            "resultado": "Dúvida analisada",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _processar_contradicao(self, conteudo: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento do tipo contradição."""
        logger.info(f"[Alma] Processando contradição: {conteudo[:50]}...")
        # Simula análise de contradição
        await asyncio.sleep(0.5)
        return {
            "tipo": "contradicao",
            "resultado": "Contradição analisada",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _processar_padrao(self, conteudo: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pensamento do tipo padrão."""
        logger.info(f"[Alma] Processando padrão: {conteudo[:50]}...")
        # Simula identificação de padrão
        await asyncio.sleep(0.5)
        return {
            "tipo": "padrao",
            "resultado": "Padrão identificado e analisado",
            "timestamp": datetime.now().isoformat()
        }

    async def ciclo_reflexao(self, num_memorias: int = None) -> None:
        """
        Executa um ciclo de reflexão sobre as memórias e pensamentos.
        
        Args:
            num_memorias: Número de memórias recentes a processar (opcional)
        """
        logger.info("[Alma] Iniciando ciclo de reflexão...")
        
        # Gera pensamentos reflexivos sobre memórias recentes
        dados = self.persona._carregar_memorias()
        if dados["memorias"]:
            # Pega as últimas n memórias
            if num_memorias is None:
                num_memorias = 5  # Padrão
            memorias_recentes = dados["memorias"][-num_memorias:]
            
            for memoria in memorias_recentes:
                # Gera reflexão com emoção e tags apropriadas
                emocao = self._inferir_emocao(memoria["conteudo"])
                tags = self._extrair_tags(memoria["conteudo"])
                
                await self.receber_pensamento(
                    "reflexao",
                    f"Refletindo sobre: {memoria['conteudo']}",
                    prioridade=2,
                    metadata={"memoria_id": memoria["id"]},
                    emocao=emocao,
                    tags=tags
                )
        
        # Processa pensamentos pendentes
        while not self.fila_pensamentos.vazia():
            await self.ciclo_cognitivo()
            await asyncio.sleep(0.1)  # Pequena pausa entre processamentos
    
    def _inferir_emocao(self, texto: str) -> Optional[str]:
        """
        Infere a emoção predominante de um texto.
        
        Args:
            texto: Texto para análise
            
        Returns:
            Nome da emoção ou None
        """
        # Mapeamento simples de palavras-chave para emoções
        mapa_emocoes = {
            "feliz": "alegria",
            "triste": "tristeza",
            "raiva": "raiva",
            "medo": "medo",
            "surpresa": "surpresa",
            "dúvida": "curiosidade",
            "curioso": "curiosidade",
            "preocupa": "preocupação"
        }
        
        texto = texto.lower()
        for palavra, emocao in mapa_emocoes.items():
            if palavra in texto:
                return emocao
        
        return None
    
    def _extrair_tags(self, texto: str) -> List[str]:
        """
        Extrai tags relevantes de um texto.
        
        Args:
            texto: Texto para análise
            
        Returns:
            Lista de tags
        """
        # Lista de palavras-chave para tags
        palavras_chave = {
            "memória": "memoria",
            "aprendizado": "aprendizado",
            "emoção": "emocional",
            "padrão": "padrao",
            "dúvida": "duvida",
            "reflexão": "reflexao",
            "missão": "missao",
            "objetivo": "objetivo",
            "relação": "relacional"
        }
        
        tags = set()
        texto = texto.lower()
        
        for palavra, tag in palavras_chave.items():
            if palavra in texto:
                tags.add(tag)
        
        return list(tags)

    async def ciclo_reflexao_continuo(self, intervalo: int = 60) -> None:
        """
        Executa ciclos de reflexão continuamente com o intervalo especificado.
        
        Args:
            intervalo: Tempo em segundos entre os ciclos
        """
        logger.info(f"[Alma] Iniciando ciclo de reflexão contínuo (intervalo: {intervalo}s)")
        
        while True:
            try:
                # Executa um ciclo de reflexão
                await self.ciclo_reflexao()
                
                # Gera pensamento sobre o ciclo
                await self.receber_pensamento(
                    "reflexao",
                    "Avaliando resultados do último ciclo de reflexão",
                    prioridade=1,
                    tags=["reflexao", "ciclo"],
                    emocao="curiosidade",
                    duracao_segundos=intervalo
                )
                
                # Limpa pensamentos antigos antes de dormir
                self.fila_pensamentos._limpar_expirados()
                
                # Aguarda o próximo ciclo
                await asyncio.sleep(intervalo)
            
            except asyncio.CancelledError:
                logger.info("[Alma] Ciclo de reflexão contínuo cancelado")
                break
            except Exception as e:
                logger.error(f"[Alma] Erro no ciclo de reflexão: {e}")
                await asyncio.sleep(intervalo)  # Aguarda antes de tentar novamente

    def configurar_gerenciador_aprendizado(self, gerenciador):
        """
        Configura o gerenciador de aprendizado.
        
        Args:
            gerenciador: Instância do GerenciadorAprendizado
        """
        self.gerenciador_aprendizado = gerenciador
        logger.info("Gerenciador de aprendizado configurado")

    def listar_historico_pensamentos(self, n: int = 10) -> List[str]:
        """
        Lista os últimos n pensamentos processados.
        
        Args:
            n: Número de pensamentos a retornar
            
        Returns:
            Lista de representações string dos pensamentos
        """
        return self.fila_pensamentos.listar_historico(n)

    def listar_fila_pensamentos(self) -> List[str]:
        """
        Lista os pensamentos atualmente na fila.
        
        Returns:
            Lista de representações string dos pensamentos
        """
        return self.fila_pensamentos.listar_fila()

    async def ativar_agente_metacognicao(self) -> None:
        """Ativa o agente de metacognição para avaliar o estado do sistema."""
        logger.info("[Alma] Ativando agente de metacognição...")
        
        # Analisa o histórico recente de pensamentos
        historico = self.fila_pensamentos.listar_historico(5)
        if historico:
            # Gera pensamento metacognitivo sobre o histórico
            await self.receber_pensamento(
                "metacognicao",
                "Analisando padrões nos últimos pensamentos processados",
                prioridade=3,
                tags=["metacognicao", "analise"],
                emocao="curiosidade"
            )
        
        # Avalia a fila atual
        fila_atual = self.fila_pensamentos.listar_fila()
        if fila_atual:
            # Gera pensamento sobre a fila atual
            await self.receber_pensamento(
                "metacognicao",
                "Avaliando prioridades da fila de pensamentos",
                prioridade=3,
                tags=["metacognicao", "prioridade"],
                emocao="concentracao"
            )
        
        # Gera insight metacognitivo
        await self.receber_pensamento(
            "insight",
            "Reflexão sobre o estado atual do sistema",
            prioridade=4,
            tags=["metacognicao", "insight"],
            emocao="curiosidade"
        )

class ControladorAlma:
    def __init__(self, memoria):
        self.memoria = memoria
        self.agentes = []
        self.ciclo_ativo = False

    async def ciclo_ativo(self):
        """Loop assíncrono contínuo que aciona o processo de refinamento das memórias."""
        self.ciclo_ativo = True
        while self.ciclo_ativo:
            try:
                # Escolhe uma memória aleatória para processar
                memorias = self.memoria.buscar_memoria('longo_prazo')
                if memorias:
                    memoria_escolhida = random.choice(memorias)
                    # Processa a memória através dos agentes
                    memoria_refinada = await self.acionar_agentes(memoria_escolhida)
                    if memoria_refinada:
                        # Atualiza a memória com a versão refinada
                        self.memoria.atualizar_memoria(memoria_escolhida, memoria_refinada)
                
                # Aguarda um intervalo antes do próximo ciclo
                await asyncio.sleep(60)  # 1 minuto entre ciclos
            except Exception as e:
                print(f"Erro no ciclo da Alma: {str(e)}")
                await asyncio.sleep(5)  # Espera um pouco em caso de erro

    async def acionar_agentes(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """Encaminha a informação pelos agentes, um após o outro."""
        resultado = info.copy()
        
        # Processa através de cada agente
        for agente in self.agentes:
            try:
                resultado = await agente.processar(resultado)
            except Exception as e:
                print(f"Erro no agente {agente.__class__.__name__}: {str(e)}")
                continue
        
        return resultado

    def adicionar_agente(self, agente):
        """Adiciona um novo agente à lista de agentes."""
        self.agentes.append(agente)

    def remover_agente(self, agente):
        """Remove um agente da lista de agentes."""
        if agente in self.agentes:
            self.agentes.remove(agente)

    def parar_ciclo(self):
        """Para o ciclo de processamento da Alma."""
        self.ciclo_ativo = False 