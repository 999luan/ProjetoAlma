"""
Sistema de Memória Contínua e Reflexão Autônoma - Fases 1-5

Este sistema implementa:
- Fase 1: Memória e Armazenamento
- Fase 2: Reflexão e Metacognição
- Fase 3: Sistema Multi-agentes
- Fase 4: Ciclo de Pensamento Contínuo e Aprendizado Autônomo
- Fase 5: Adaptação e Experimentação Autônoma

O sistema funciona como uma memória contínua que não apenas armazena
informações, mas também as processa, as sintetiza e evolui seu próprio
funcionamento através de experimentação e adaptação autônoma.
"""

import os
import logging
import asyncio
import argparse
import json
from datetime import datetime
from pathlib import Path
import sys
from rich.console import Console
from rich.panel import Panel

# Importação dos módulos do sistema
from persona.persona import Persona
from core.alma import Alma
from core.learning import GerenciadorAprendizado
from core.adaptive_learning import AprendizadoAdaptativo
from persona.memoria import Memoria
from persona.processador_pensamento import ProcessadorPensamento
from core.chat_interface import ChatInterface

# Inicialização condicional do módulo de análise semântica
MODULO_SEMANTICO_DISPONIVEL = False
try:
    from core.nlp_enhancement import analisador_semantico
    MODULO_SEMANTICO_DISPONIVEL = True
except ImportError:
    print("Aviso: Módulo de análise semântica não disponível. Algumas funcionalidades estarão limitadas.")

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('alma.log')
    ]
)

logger = logging.getLogger(__name__)
console = Console()

async def setup_environment():
    """Configura o ambiente de execução, garantindo que diretórios necessários existam."""
    diretorios = ['data', 'logs', 'data/sinteses', 'data/adaptive_learning', 'data/nlp_models']
    
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)
    
    logger.info("Ambiente configurado com sucesso")

async def processar_comandos(comando, persona, alma, gerenciador_aprendizado=None, adaptativo=None):
    """Processa comandos do usuário."""
    partes = comando.lower().split()
    
    if partes[0] == "ajuda":
        return """
╔════════════════════════════════════════════════════════════════════════════╗
║                           SISTEMA ALMA - COMANDOS                          ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  MEMÓRIA E ARMAZENAMENTO:                                                   ║
║  • armazenar [mensagem]  - Armazena uma nova memória                        ║
║  • listar [n]           - Lista as últimas n memórias (padrão: 5)          ║
║  • buscar [termo]       - Busca memórias contendo o termo                   ║
║                                                                             ║
║  ANÁLISE E REFLEXÃO:                                                        ║
║  • buscar-semantico [consulta] - Busca memórias semanticamente similares    ║
║  • extrair-entidades [texto]   - Extrai entidades de um texto              ║
║  • analisar-sentimento [texto] - Analisa o sentimento de um texto          ║
║  • palavras-chave [texto]      - Extrai palavras-chave de um texto         ║
║                                                                             ║
║  AGENTES E CICLOS:                                                          ║
║  • refletir             - Executa um ciclo de reflexão                     ║
║  • metacognicao         - Ativa o agente de metacognição                   ║
║  • emocional            - Ativa o agente emocional                         ║
║  • consistencia         - Ativa o agente de consistência                   ║
║  • padroes              - Ativa o agente de identificação de padrões       ║
║                                                                             ║
║  APRENDIZADO E ADAPTAÇÃO:                                                   ║
║  • aprendizado          - Informações sobre o aprendizado atual            ║
║  • otimizar             - Otimiza o processo de aprendizado                ║
║  • estatisticas         - Mostra estatísticas do aprendizado              ║
║  • adaptar [intervalo]  - Inicia ciclo adaptativo (intervalo em segundos)  ║
║  • experimentos         - Lista experimentos ativos                        ║
║  • metricas             - Mostra métricas atuais do sistema                ║
║  • estrategias          - Lista estratégias efetivas aprendidas            ║
║                                                                             ║
║  SISTEMA:                                                                   ║
║  • sair                 - Encerra o programa                               ║
║                                                                             ║
╚════════════════════════════════════════════════════════════════════════════╝
        """
    
    elif partes[0] == "buscar-semantico" and len(partes) > 1:
        consulta = " ".join(partes[1:])
        try:
            from core.nlp_enhancement import analisador_semantico
            if not analisador_semantico.inicializado:
                await analisador_semantico.inicializar_recursos()
            
            memorias = await persona.buscar_memorias_semanticamente(consulta)
            resultado = "\n╔════════════════════════════════════════════════════════════════════════════╗"
            resultado += "\n║                        RESULTADO DA BUSCA SEMÂNTICA                        ║"
            resultado += "\n╠════════════════════════════════════════════════════════════════════════════╣"
            
            if memorias:
                for memoria in memorias:
                    resultado += f"\n║ ID {memoria['id']}: {memoria['conteudo']}"
                    resultado += " " * (80 - len(f"║ ID {memoria['id']}: {memoria['conteudo']}")) + "║"
            else:
                resultado += f"\n║ Nenhuma memória semanticamente relacionada com '{consulta}'"
                resultado += " " * (80 - len(f"║ Nenhuma memória semanticamente relacionada com '{consulta}'")) + "║"
            
            resultado += "\n╚════════════════════════════════════════════════════════════════════════════╝"
            return resultado
        except ImportError:
            return """
╔════════════════════════════════════════════════════════════════════════════╗
║                               ERRO                                         ║
╠════════════════════════════════════════════════════════════════════════════╣
║ Funcionalidade de busca semântica não disponível. Verifique se as          ║
║ dependências necessárias estão instaladas.                                 ║
╚════════════════════════════════════════════════════════════════════════════╝
            """
    
    elif partes[0] == "extrair-entidades" and len(partes) > 1:
        texto = " ".join(partes[1:])
        try:
            from core.nlp_enhancement import analisador_semantico
            if not analisador_semantico.inicializado:
                await analisador_semantico.inicializar_recursos()
            
            entidades = await analisador_semantico.extrair_entidades(texto)
            resultado = "Entidades detectadas:\n"
            for categoria, items in entidades.items():
                if not isinstance(entidades, dict) or "error" in entidades:
                    return "Erro ao extrair entidades. Verifique se as bibliotecas de NLP estão instaladas corretamente."
                resultado += f"{categoria}: {', '.join([item['texto'] for item in items])}\n"
            
            return resultado
        except ImportError:
            return "Funcionalidade de extração de entidades não disponível. Verifique se as dependências necessárias estão instaladas."
    
    elif partes[0] == "analisar-sentimento" and len(partes) > 1:
        texto = " ".join(partes[1:])
        try:
            from core.nlp_enhancement import analisador_semantico
            if not analisador_semantico.inicializado:
                await analisador_semantico.inicializar_recursos()
            
            sentimento = await analisador_semantico.analisar_sentimento(texto)
            return f"""
            Análise de sentimento:
            - Polaridade: {sentimento['polaridade']:.4f} (-1=negativo, 1=positivo)
            - Positivo: {sentimento['positivo']:.4f}
            - Negativo: {sentimento['negativo']:.4f}
            - Neutro: {sentimento['neutro']:.4f}
            """
        except ImportError:
            return "Funcionalidade de análise de sentimento não disponível. Verifique se as dependências necessárias estão instaladas."
    
    elif partes[0] == "palavras-chave" and len(partes) > 1:
        texto = " ".join(partes[1:])
        try:
            from core.nlp_enhancement import analisador_semantico
            if not analisador_semantico.inicializado:
                await analisador_semantico.inicializar_recursos()
            
            palavras_chave = await analisador_semantico.extrair_palavras_chave(texto, n=8)
            return f"Palavras-chave: {', '.join(palavras_chave)}"
        except ImportError:
            return "Funcionalidade de extração de palavras-chave não disponível. Verifique se as dependências necessárias estão instaladas."
    
    elif partes[0] == "armazenar" and len(partes) > 1:
        conteudo = " ".join(partes[1:])
        resultado = persona.adicionar_memoria(conteudo)
        return f"Memória armazenada com ID: {resultado}"
    
    elif partes[0] == "listar":
        n = 5  # padrão
        if len(partes) > 1 and partes[1].isdigit():
            n = int(partes[1])
        
        memorias = persona.listar_memorias(n)
        resultado = ""
        for memoria in memorias:
            resultado += f"ID {memoria['id']}: {memoria['conteudo']}\n"
        
        return resultado if resultado else "Nenhuma memória encontrada."
    
    elif partes[0] == "buscar" and len(partes) > 1:
        termo = " ".join(partes[1:])
        memorias = persona.buscar_memorias(termo)
        
        resultado = ""
        for memoria in memorias:
            resultado += f"ID {memoria['id']}: {memoria['conteudo']}\n"
        
        return resultado if resultado else f"Nenhuma memória encontrada com o termo '{termo}'."
    
    elif partes[0] == "refletir":
        await alma.ciclo_reflexao_continuo()
        return "Ciclo de reflexão concluído."
    
    elif partes[0] == "metacognicao":
        await alma.receber_pensamento("duvida", "Ativando agente de metacognição", prioridade=2)
        return "Agente de metacognição ativado."
    
    elif partes[0] == "emocional":
        await alma.receber_pensamento("duvida", "Ativando agente emocional", prioridade=2)
        return "Agente emocional ativado."
    
    elif partes[0] == "consistencia":
        await alma.receber_pensamento("contradicao", "Ativando agente de consistência", prioridade=2)
        return "Agente de consistência ativado."
    
    elif partes[0] == "padroes":
        await alma.receber_pensamento("padrao", "Ativando agente de identificação de padrões", prioridade=2)
        return "Agente de identificação de padrões ativado."
    
    elif partes[0] == "aprendizado" and gerenciador_aprendizado:
        return gerenciador_aprendizado.status_aprendizado()
    
    elif partes[0] == "otimizar" and gerenciador_aprendizado:
        await gerenciador_aprendizado.otimizar_processo()
        return "Processo de aprendizado otimizado."
    
    elif partes[0] == "estatisticas" and gerenciador_aprendizado:
        return gerenciador_aprendizado.mostrar_estatisticas()
    
    elif partes[0] == "adaptar" and adaptativo:
        intervalo = 600  # Padrão: 10 minutos
        if len(partes) > 1 and partes[1].isdigit():
            intervalo = int(partes[1])
        
        # Inicia o ciclo adaptativo em background
        asyncio.create_task(adaptativo.iniciar_ciclo_adaptativo(intervalo))
        return f"Ciclo de adaptação iniciado com intervalo de {intervalo} segundos."
    
    elif partes[0] == "experimentos" and adaptativo:
        if not adaptativo.experimentos_ativos:
            return "Nenhum experimento ativo no momento."
        
        resultado = "Experimentos ativos:\n"
        for exp_id, exp in adaptativo.experimentos_ativos.items():
            resultado += f"- {exp_id}: {exp['descricao']} (ciclo {exp['ciclos_decorridos']}/{exp['ciclos_planejados']})\n"
        return resultado
    
    elif partes[0] == "metricas" and adaptativo:
        # Executa análise sob demanda
        metricas = await adaptativo._analisar_metricas_sistema()
        
        if not metricas:
            return "Nenhuma métrica disponível ainda."
        
        resultado = """
        Métricas atuais do sistema:
        
        Memórias:
        - Total: {n_memorias}
        - Processadas: {n_memorias_processadas}
        - Taxa de processamento: {taxa_processamento:.1%}
        
        Qualidade:
        - Média: {qualidade_media:.2f}
        - Diversidade de temas: {diversidade_temas}
        
        Ciclos:
        - Adaptação: {ciclos_adaptacao}
        - Experimentos ativos: {experimentos_ativos}
        - Estratégias aprendidas: {estrategias_aprendidas}
        
        Eficiência dos agentes:
        """.format(**metricas)
        
        if "eficiencia_agentes" in metricas:
            for agente, valor in metricas["eficiencia_agentes"].items():
                resultado += f"- {agente}: {valor} memórias processadas\n"
        
        return resultado
    
    elif partes[0] == "estrategias" and adaptativo:
        if not adaptativo.estrategias_efetivas:
            return "Nenhuma estratégia efetiva aprendida ainda."
        
        resultado = "Estratégias efetivas aprendidas:\n"
        for i, estrategia in enumerate(adaptativo.estrategias_efetivas, 1):
            resultado += f"{i}. {estrategia}\n"
        return resultado
    
    elif partes[0] == "sair":
        return "sair"
    
    else:
        return "Comando não reconhecido. Digite 'ajuda' para ver os comandos disponíveis."

async def main_async():
    """Função principal assíncrona."""
    try:
        # Inicializa o sistema
        logger.info("Iniciando o sistema...")
        await setup_environment()
        
        # Cria instâncias principais
        alma = Alma()
        chat = ChatInterface(alma)
        
        # Inicia o ciclo de reflexão
        await alma.iniciar_ciclo()
        
        # Inicia a interface de chat
        await chat.iniciar_chat()
        
    except Exception as e:
        logger.error(f"Erro fatal no sistema: {str(e)}")
        console.print(f"[red]Erro: {str(e)}[/red]")
    finally:
        # Encerra o ciclo de reflexão
        await alma.encerrar_ciclo()
        console.print("[green]Sistema finalizado[/green]")

def main():
    """Ponto de entrada principal do programa."""
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\nSistema interrompido pelo usuário.")
    except Exception as e:
        logger.error(f"Erro não tratado: {e}", exc_info=True)

if __name__ == "__main__":
    main() 