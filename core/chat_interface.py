"""
Módulo Chat Interface - Implementa a interface de chat do sistema.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

class ChatInterface:
    def __init__(self, alma):
        """Inicializa a interface de chat."""
        self.alma = alma
        self.console = Console()
        self.logger = logging.getLogger(__name__)
        self.historico_chat = []
        self.ultima_interacao = None
        self.agentes_ativos = {
            'reflexao': True,
            'metacognicao': True,
            'emocional': True,
            'consistencia': True,
            'padroes': True
        }

    async def iniciar_chat(self):
        """Inicia a interface de chat."""
        self.console.print(Panel.fit(
            "Sistema Alma - Chat Interface\n"
            "Digite 'ajuda' para ver os comandos disponíveis\n"
            "Digite 'sair' para encerrar",
            style="bold green"
        ))

        # Inicia os ciclos de processamento
        await self.alma.iniciar_ciclo()

        while True:
            try:
                # Recebe input do usuário
                mensagem = input("\nVocê: ").strip()
                
                if not mensagem:
                    continue
                
                if mensagem.lower() == "sair":
                    self.console.print("[yellow]Encerrando chat...[/yellow]")
                    break
                
                if mensagem.lower() == "ajuda":
                    self.exibir_ajuda()
                    continue
                
                # Processa a mensagem
                resposta = await self.processar_mensagem(mensagem)
                
                # Exibe a resposta
                self.exibir_resposta(resposta)
                
                # Atualiza histórico
                self.atualizar_historico(mensagem, resposta)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Chat interrompido pelo usuário[/yellow]")
                break
            except Exception as e:
                self.logger.error(f"Erro no chat: {str(e)}")
                self.console.print(f"[red]Erro: {str(e)}[/red]")
        
        # Encerra os ciclos de processamento
        await self.alma.encerrar_ciclo()

    def exibir_ajuda(self):
        """Exibe a ajuda do sistema."""
        ajuda = """
╔════════════════════════════════════════════════════════════════════════════╗
║                           SISTEMA ALMA - COMANDOS                          ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  AGENTES:                                                                   ║
║  • ativar [agente]     - Ativa um agente específico                         ║
║  • desativar [agente]  - Desativa um agentes específico                     ║
║  • agentes            - Lista os agentes e seus status                      ║
║                                                                             ║
║  MEMÓRIA:                                                                   ║
║  • memorias [n]       - Lista as últimas n memórias (padrão: 5)            ║
║  • buscar [termo]     - Busca memórias contendo o termo                     ║
║                                                                             ║
║  SISTEMA:                                                                   ║
║  • status             - Mostra o status atual do sistema                    ║
║  • ajuda              - Mostra esta mensagem de ajuda                       ║
║  • sair               - Encerra o programa                                  ║
║                                                                             ║
╚════════════════════════════════════════════════════════════════════════════╝
        """
        self.console.print(ajuda)

    async def processar_mensagem(self, mensagem: str) -> Dict[str, Any]:
        """Processa uma mensagem do usuário."""
        try:
            # Processa comandos do sistema
            cmd = mensagem.lower().split()[0] if mensagem else ""
            comandos_validos = {
                'memoria': 'memorias',
                'memorias': 'memorias',
                'buscar': 'buscar',
                'status': 'status',
                'agentes': 'agentes',
                'ativar': 'ativar',
                'desativar': 'desativar',
                'ajuda': 'ajuda'
            }
            
            if cmd in comandos_validos:
                return await self.processar_comando(mensagem)

            # Cria um pensamento a partir da mensagem
            pensamento = {
                'tipo': 'mensagem',
                'conteudo': mensagem,
                'timestamp': datetime.now(),
                'prioridade': 1,
                'agentes': self.agentes_ativos
            }
            
            # Envia para o sistema processar
            resultado = await self.alma.receber_pensamento(pensamento)
            
            # Processa o aprendizado interno
            if resultado['status'] == 'sucesso':
                # Obtém o conhecimento refinado do sistema
                conhecimento = self.alma.persona.obter_conhecimento_relevante(mensagem)
                
                # Verifica se há contexto suficiente para reprocessamento
                if self._verificar_contexto_suficiente(conhecimento):
                    # Cria um pensamento interno para reprocessamento
                    pensamento_interno = {
                        'tipo': 'aprendizado',
                        'conteudo': self._gerar_pensamento_interno(conhecimento),
                        'timestamp': datetime.now(),
                        'prioridade': 2,
                        'agentes': self.agentes_ativos
                    }
                    # Envia o pensamento interno para processamento
                    await self.alma.receber_pensamento(pensamento_interno)
                
                # Gera uma resposta contextual usando o conhecimento refinado
                resposta = self.gerar_resposta_contextual(mensagem, conhecimento, resultado)
                
                return {
                    'status': 'sucesso',
                    'resposta': resposta,
                    'timestamp': datetime.now()
                }
            else:
                return {
                    'status': 'erro',
                    'erro': resultado.get('erro', 'Erro desconhecido'),
                    'timestamp': datetime.now()
                }
                
        except Exception as e:
            self.logger.error(f"Erro ao processar mensagem: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now()
            }

    async def processar_comando(self, comando: str) -> Dict[str, Any]:
        """Processa comandos do sistema."""
        try:
            partes = comando.lower().split()
            cmd = partes[0]

            # Normaliza o comando (singular/plural)
            if cmd == 'memoria':
                cmd = 'memorias'

            if cmd == 'memorias':
                n = 5  # padrão
                if len(partes) > 1 and partes[1].isdigit():
                    n = int(partes[1])
                memorias = self.alma.persona.listar_memorias(n)
                resposta = "Últimas memórias:\n\n"
                if memorias:
                    for memoria in memorias:
                        tipo = memoria.get('tipo', 'desconhecido')
                        resposta += f"ID {memoria['id']} [{tipo}]: {memoria['conteudo']}\n"
                else:
                    resposta += "Nenhuma memória encontrada."
                return {
                    'status': 'sucesso',
                    'resposta': resposta,
                    'timestamp': datetime.now()
                }

            elif cmd == 'buscar' and len(partes) > 1:
                termo = ' '.join(partes[1:])
                memorias = self.alma.persona.buscar_memorias(termo)
                resposta = f"Memórias encontradas para '{termo}':\n\n"
                if memorias:
                    for memoria in memorias:
                        tipo = memoria.get('tipo', 'desconhecido')
                        resposta += f"ID {memoria['id']} [{tipo}]: {memoria['conteudo']}\n"
                else:
                    resposta += "Nenhuma memória encontrada."
                return {
                    'status': 'sucesso',
                    'resposta': resposta,
                    'timestamp': datetime.now()
                }

            elif cmd == 'status':
                status = self.alma.status()
                resposta = "Status do Sistema:\n\n"
                resposta += f"Persona: {status['persona']}\n"
                resposta += f"Aprendizado: {status['aprendizado']}\n"
                resposta += f"Adaptação: {status['adaptacao']}\n"
                resposta += f"Ciclo Ativo: {'Sim' if status['ciclo_ativo'] else 'Não'}\n"
                return {
                    'status': 'sucesso',
                    'resposta': resposta,
                    'timestamp': datetime.now()
                }

            elif cmd == 'agentes':
                resposta = "Status dos Agentes:\n\n"
                for agente, ativo in self.agentes_ativos.items():
                    resposta += f"{agente}: {'Ativo' if ativo else 'Inativo'}\n"
                return {
                    'status': 'sucesso',
                    'resposta': resposta,
                    'timestamp': datetime.now()
                }

            elif cmd == 'ativar' and len(partes) > 1:
                agente = partes[1]
                if agente in self.agentes_ativos:
                    self.agentes_ativos[agente] = True
                    return {
                        'status': 'sucesso',
                        'resposta': f"Agente {agente} ativado com sucesso.",
                        'timestamp': datetime.now()
                    }
                else:
                    return {
                        'status': 'erro',
                        'erro': f"Agente {agente} não encontrado.",
                        'timestamp': datetime.now()
                    }

            elif cmd == 'desativar' and len(partes) > 1:
                agente = partes[1]
                if agente in self.agentes_ativos:
                    self.agentes_ativos[agente] = False
                    return {
                        'status': 'sucesso',
                        'resposta': f"Agente {agente} desativado com sucesso.",
                        'timestamp': datetime.now()
                    }
                else:
                    return {
                        'status': 'erro',
                        'erro': f"Agente {agente} não encontrado.",
                        'timestamp': datetime.now()
                    }

            else:
                return {
                    'status': 'erro',
                    'erro': "Comando não reconhecido. Digite 'ajuda' para ver os comandos disponíveis.",
                    'timestamp': datetime.now()
                }

        except Exception as e:
            self.logger.error(f"Erro ao processar comando: {str(e)}")
            return {
                'status': 'erro',
                'erro': str(e),
                'timestamp': datetime.now()
            }

    def gerar_resposta_contextual(self, mensagem: str, conhecimento: Dict[str, Any], resultado: Dict[str, Any]) -> str:
        """Gera uma resposta contextual usando o conhecimento refinado."""
        try:
            resposta = ""
            
            # Analisa o contexto da mensagem
            contexto = self._analisar_contexto([{'conteudo': mensagem}])
            
            # Gera uma resposta baseada no conhecimento refinado
            if conhecimento and conhecimento.get('temas_relacionados'):
                temas = conhecimento['temas_relacionados']
                resposta += f"Baseado no que aprendi sobre {', '.join(temas)}, "
            
            # Adiciona a resposta principal
            if resultado.get('conteudo'):
                resposta += resultado['conteudo']
            else:
                # Resposta padrão baseada no tipo de mensagem
                if '?' in mensagem:
                    resposta += "Vou refletir sobre isso e te dar uma resposta mais elaborada em breve."
                else:
                    resposta += "Entendi o que você disse. Estou processando essa informação e aprendendo com ela."
            
            # Adiciona informações do sistema de forma sutil
            if self.alma.persona.memoria.status()['total_memorias'] > 0:
                resposta += "\n\n[Status do Sistema: Aprendendo e refinando conhecimento...]"
            
            return resposta
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar resposta contextual: {str(e)}")
            return "Desculpe, tive um problema ao processar sua mensagem."

    def _analisar_contexto(self, memorias: list) -> Dict[str, Any]:
        """Analisa o contexto das memórias recentes."""
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
                'total_memorias': len(memorias),
                'frequencia_temas': dict(temas_ordenados)
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao analisar contexto: {str(e)}")
            return {
                'temas_relacionados': [],
                'total_memorias': 0,
                'frequencia_temas': {}
            }

    def exibir_resposta(self, resposta: Dict[str, Any]):
        """Exibe a resposta do sistema."""
        if resposta['status'] == 'sucesso':
            # Formata a resposta em seções
            conteudo = resposta['resposta']
            self.console.print(Panel(
                Markdown(conteudo),
                title="Alma",
                style="bold blue",
                border_style="blue"
            ))
        else:
            self.console.print(f"[red]Erro: {resposta['erro']}[/red]")

    def atualizar_historico(self, mensagem: str, resposta: Dict[str, Any]):
        """Atualiza o histórico de chat."""
        self.historico_chat.append({
            'mensagem': mensagem,
            'resposta': resposta,
            'timestamp': datetime.now()
        })
        self.ultima_interacao = datetime.now()

    def obter_historico(self, limite: int = 10) -> list:
        """Retorna o histórico de chat."""
        return self.historico_chat[-limite:]

    def _verificar_contexto_suficiente(self, conhecimento: Dict[str, Any]) -> bool:
        """Verifica se há contexto suficiente para reprocessamento."""
        try:
            if not conhecimento or not conhecimento.get('temas_relacionados'):
                return False
                
            # Obtém a frequência dos temas
            frequencia = conhecimento.get('frequencia_temas', {})
            
            # Verifica se algum tema tem frequência significativa (mais de 3 ocorrências)
            return any(freq > 3 for freq in frequencia.values())
            
        except Exception as e:
            self.logger.error(f"Erro ao verificar contexto: {str(e)}")
            return False

    def _gerar_pensamento_interno(self, conhecimento: Dict[str, Any]) -> str:
        """Gera um pensamento interno baseado no conhecimento refinado."""
        try:
            pensamento = "Reflexão interna sobre aprendizado:\n\n"
            
            # Adiciona temas principais
            if conhecimento.get('temas_relacionados'):
                temas = conhecimento['temas_relacionados']
                pensamento += f"Temas principais identificados: {', '.join(temas)}\n"
            
            # Adiciona padrões identificados
            if conhecimento.get('padroes'):
                pensamento += "\nPadrões identificados:\n"
                for padrao in conhecimento['padroes']:
                    pensamento += f"• {padrao}\n"
            
            # Adiciona insights
            if conhecimento.get('insights'):
                pensamento += "\nInsights:\n"
                for insight in conhecimento['insights']:
                    pensamento += f"• {insight}\n"
            
            # Adiciona conclusões
            if conhecimento.get('conclusoes'):
                pensamento += "\nConclusões:\n"
                for conclusao in conhecimento['conclusoes']:
                    pensamento += f"• {conclusao}\n"
            
            return pensamento
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar pensamento interno: {str(e)}")
            return "Erro ao gerar reflexão interna." 