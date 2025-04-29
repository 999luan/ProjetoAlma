"""
Sistema de Memória Contínua e Reflexão Autônoma

Arquivo principal para iniciar o sistema, implementando a Fase 4
do projeto com ciclo de pensamento contínuo e aprendizado autônomo.
"""
import os
import sys
import asyncio
import logging
import signal
from datetime import datetime

# Configuração de logging
from core.config import LOG_CONFIG

logging.basicConfig(
    level=getattr(logging, LOG_CONFIG["nivel"]),
    format=LOG_CONFIG["formato"],
    handlers=[
        logging.FileHandler(LOG_CONFIG["arquivo"]),
        logging.StreamHandler() if LOG_CONFIG["console"] else logging.NullHandler()
    ]
)

logger = logging.getLogger("sistema_memoria")

# Importa os módulos principais
from core.persona import Persona
from core.alma import Alma
from core.learning import GerenciadorAprendizado
from core.config import ALMA_CONFIG

def setup_environment():
    """Configura o ambiente para a execução do sistema."""
    # Adiciona diretórios ao path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    logger.info(f"Adicionado ao path: {current_dir}")
    
    # Assegura que o diretório core existe
    os.makedirs("core", exist_ok=True)
    os.makedirs("core/agentes", exist_ok=True)
    logger.info("Estrutura de diretórios verificada")

async def processar_comandos(persona, alma, gerenciador_aprendizado):
    """Processa comandos do usuário.
    
    Args:
        persona: Instância da classe Persona
        alma: Instância da classe Alma
        gerenciador_aprendizado: Instância do GerenciadorAprendizado
    """
    while True:
        try:
            comando = await asyncio.to_thread(
                input, "\nComando (digite 'ajuda' para ver os comandos disponíveis): "
            )
            
            match comando.lower().strip():
                case 'ajuda':
                    print("\nComandos disponíveis:")
                    print("  ajuda       - Mostra esta mensagem")
                    print("  sair        - Encerra o sistema")
                    print("  adicionar   - Adiciona uma nova informação")
                    print("  sintese     - Gera uma síntese de memórias existentes")
                    print("  reflexao    - Força um ciclo de reflexão")
                    print("  metacog     - Força um ciclo de metacognição")
                    print("  emocional   - Ativa o agente emocional")
                    print("  consistencia- Ativa o agente de consistência")
                    print("  padroes     - Ativa o agente de padrões")
                    print("  otimizar    - Força um ciclo de otimização de aprendizado")
                    print("  memorias    - Lista todas as memórias armazenadas")
                    print("  stats       - Mostra estatísticas do sistema")
                    
                case 'sair':
                    logger.info("Comando de saída recebido")
                    return
                    
                case 'adicionar':
                    info = await asyncio.to_thread(
                        input, "Digite a nova informação: "
                    )
                    persona.receber_informacao(info)
                    
                case 'sintese':
                    sintese = persona.gerar_sintese()
                    if sintese:
                        print(f"Síntese gerada: {sintese}")
                    else:
                        print("Não foi possível gerar uma síntese")
                        
                case 'reflexao':
                    await alma.ativar_agente_reflexao()
                    
                case 'metacog':
                    await alma.ativar_agente_metacognicao()
                    
                case 'emocional':
                    await alma.ativar_agente_emocional()
                    
                case 'consistencia':
                    await alma.ativar_agente_consistencia()
                    
                case 'padroes':
                    await alma.ativar_agente_padrao()
                    
                case 'otimizar':
                    await gerenciador_aprendizado.otimizar_processo()
                    
                case 'memorias':
                    dados = persona._carregar_memorias()
                    print("\nMemórias armazenadas:")
                    
                    if not dados["memorias"]:
                        print("  Nenhuma memória encontrada")
                    else:
                        for memoria in dados["memorias"]:
                            print(f"  #{memoria['id']} ({memoria.get('origem', 'desconhecida')}): {memoria['conteudo']}")
                            
                            # Mostra avaliação se existir
                            if 'avaliacao' in memoria:
                                print(f"    Qualidade: {memoria['avaliacao']['qualidade']}/10")
                                
                            # Mostra contexto emocional se existir
                            if 'contexto_emocional' in memoria:
                                print(f"    Emoção: {memoria['contexto_emocional']['emocao']} (intensidade: {memoria['contexto_emocional']['intensidade']})")
                                
                            # Mostra consistência se existir
                            if 'consistencia' in memoria:
                                print(f"    Inconsistente com: {memoria['consistencia']['inconsistente_com']}")
                                
                            # Mostra padrões se existirem
                            if 'padroes' in memoria:
                                print(f"    Temas: {', '.join(memoria['padroes']['temas_detectados'])}")
                    
                case 'stats':
                    dados = persona._carregar_memorias()
                    print("\n=== Estatísticas do Sistema ===")
                    print(f"Total de memórias: {len(dados['memorias'])}")
                    print(f"Reflexões realizadas: {alma.reflexoes_realizadas}")
                    print(f"Metacognições realizadas: {alma.metacognicoes_realizadas}")
                    
                    # Estatísticas dos agentes especializados
                    print(f"Processamentos emocionais: {alma.agente_emocional.processamentos}")
                    print(f"Inconsistências detectadas: {alma.agente_consistencia.inconsistencias_detectadas}")
                    print(f"Padrões identificados: {len(alma.agente_padrao.padroes_detectados)}")
                    
                    # Estatísticas de aprendizado
                    print(f"Ciclos de otimização: {gerenciador_aprendizado.ciclos_realizados}")
                    if gerenciador_aprendizado.estatisticas["total_avaliacoes"] > 0:
                        print(f"Qualidade média das memórias: {gerenciador_aprendizado.estatisticas['qualidade_media']:.2f}/10")
                    
                    print(f"Pesos dos agentes: {gerenciador_aprendizado.pesos_agentes}")
                    
                    # Conta tipos de origem
                    origens = {}
                    for memoria in dados["memorias"]:
                        origem = memoria.get("origem", "desconhecida")
                        origens[origem] = origens.get(origem, 0) + 1
                    
                    print("\nTipos de memória:")
                    for origem, contagem in origens.items():
                        print(f"  {origem}: {contagem}")
                        
                    # Conta memórias com cada tipo de processamento
                    emocional = sum(1 for m in dados["memorias"] if "contexto_emocional" in m)
                    consistencia = sum(1 for m in dados["memorias"] if "consistencia" in m)
                    padroes = sum(1 for m in dados["memorias"] if "padroes" in m)
                    
                    print("\nMemórias processadas:")
                    print(f"  Com contexto emocional: {emocional}")
                    print(f"  Com análise de consistência: {consistencia}")
                    print(f"  Com padrões detectados: {padroes}")
                    
                    # Áreas de foco atuais
                    areas_foco = gerenciador_aprendizado._identificar_areas_foco()
                    if areas_foco:
                        print("\nÁreas de foco atuais:")
                        for area in areas_foco:
                            print(f"  {area}")
                    
                    print("============================\n")
                    
                case _:
                    if comando.strip():
                        print(f"Comando desconhecido: '{comando}'")
            
        except asyncio.CancelledError:
            logger.info("Processamento de comandos interrompido")
            break
        except Exception as e:
            logger.error(f"Erro ao processar comando: {str(e)}")

async def main_async():
    """Função principal assíncrona do sistema."""
    try:
        print("Iniciando Sistema de Memória Contínua e Reflexão Autônoma")
        setup_environment()
        
        # Inicializa os componentes do sistema
        persona = Persona()
        alma = Alma(persona)
        gerenciador_aprendizado = GerenciadorAprendizado(persona, alma)
        
        # Configura referência circular
        alma.configurar_gerenciador_aprendizado(gerenciador_aprendizado)
        
        # Carregar algumas informações iniciais
        exemplos = [
            "Sistemas de memória contínua são fundamentais para o aprendizado profundo.",
            "A cognição adaptativa permite evolução constante do conhecimento.",
            "Reflexão e metacognição são processos que melhoram o aprendizado."
        ]
        
        print("\nCarregando informações iniciais...")
        for exemplo in exemplos:
            persona.receber_informacao(exemplo)
            await asyncio.sleep(0.5)
        
        print("\nIniciando ciclos de processamento contínuos...")
        print("Use Ctrl+C para interromper ou digite 'sair'")
        
        # Inicia os ciclos em tasks separadas
        tasks = [
            # Ciclo de reflexão - a cada 30 segundos
            asyncio.create_task(
                alma.iniciar_ciclo_reflexao(intervalo=ALMA_CONFIG["intervalo_reflexao"])
            ),
            
            # Ciclo de aprendizado - a cada 5 minutos (300 segundos)
            asyncio.create_task(
                gerenciador_aprendizado.ciclo_aprendizado_continuo(intervalo=300)
            )
        ]
        
        # Inicia o processamento de comandos
        comando_task = asyncio.create_task(processar_comandos(persona, alma, gerenciador_aprendizado))
        
        # Espera até que o processamento de comandos termine
        await comando_task
        
        # Cancela os ciclos
        for task in tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
    
    except KeyboardInterrupt:
        logger.info("Interrupção de teclado detectada")
    except Exception as e:
        logger.error(f"Erro não tratado: {str(e)}")
    finally:
        logger.info("Finalizando sistema")
    
    print("Sistema encerrado.")

def main():
    """Função principal do sistema."""
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
    except Exception as e:
        print(f"\nErro: {str(e)}")
        logger.error(f"Erro fatal: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main() 