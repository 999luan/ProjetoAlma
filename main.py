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

# Importação dos módulos do sistema
from core.persona import Persona
from core.alma import Alma
from core.learning import GerenciadorAprendizado
from core.adaptive_learning import AprendizadoAdaptativo

# Inicialização condicional do módulo de análise semântica
try:
    from core.nlp_enhancement import analisador_semantico
    MODULO_SEMANTICO_DISPONIVEL = True
except ImportError:
    MODULO_SEMANTICO_DISPONIVEL = False

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sistema.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def setup_environment():
    """Configura o ambiente de execução, garantindo que diretórios necessários existam."""
    diretorios = ['data', 'logs', 'data/sinteses', 'data/adaptive_learning', 'data/nlp_models']
    
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)
    
    logger.info("Ambiente configurado com sucesso")

async def processar_comandos(comando, persona, alma, gerenciador_aprendizado=None, adaptativo=None):
    """Processa comandos do usuário.
    
    Args:
        comando: Comando a ser processado
        persona: Instância da classe Persona
        alma: Instância da classe Alma
        gerenciador_aprendizado: Instância de GerenciadorAprendizado (opcional)
        adaptativo: Instância de AprendizadoAdaptativo (opcional)
        
    Returns:
        str: Resposta ao comando
    """
    partes = comando.lower().split()
    
    if partes[0] == "ajuda":
        return """
        Comandos disponíveis:
        - ajuda: Mostra esta mensagem
        - armazenar [mensagem]: Armazena uma nova memória
        - listar [n]: Lista as últimas n memórias (padrão: 5)
        - buscar [termo]: Busca memórias contendo o termo
        - buscar-semantico [consulta]: Busca memórias semanticamente similares à consulta
        - extrair-entidades [texto]: Extrai entidades de um texto
        - analisar-sentimento [texto]: Analisa o sentimento de um texto
        - palavras-chave [texto]: Extrai palavras-chave de um texto
        - refletir: Executa um ciclo de reflexão
        - metacognicao: Ativa o agente de metacognição
        - emocional: Ativa o agente emocional
        - consistencia: Ativa o agente de consistência
        - padroes: Ativa o agente de identificação de padrões
        - aprendizado: Informações sobre o aprendizado atual
        - otimizar: Otimiza o processo de aprendizado
        - estatisticas: Mostra estatísticas do aprendizado
        - adaptar [intervalo]: Inicia ciclo adaptativo (intervalo em segundos)
        - experimentos: Lista experimentos ativos
        - metricas: Mostra métricas atuais do sistema
        - estrategias: Lista estratégias efetivas aprendidas
        - sair: Encerra o programa
        """
    
    elif partes[0] == "buscar-semantico" and len(partes) > 1:
        consulta = " ".join(partes[1:])
        try:
            # Importa o módulo de análise semântica
            from core.nlp_enhancement import analisador_semantico
            if not analisador_semantico.inicializado:
                await analisador_semantico.inicializar_recursos()
            
            memorias = await persona.buscar_memorias_semanticamente(consulta)
            resultado = "Resultado da busca semântica:\n"
            for memoria in memorias:
                resultado += f"ID {memoria['id']}: {memoria['conteudo']}\n"
            
            return resultado if resultado else f"Nenhuma memória semanticamente relacionada com '{consulta}'."
        except ImportError:
            return "Funcionalidade de busca semântica não disponível. Verifique se as dependências necessárias estão instaladas."
    
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
        await alma.ciclo_de_reflexao()
        return "Ciclo de reflexão concluído."
    
    elif partes[0] == "metacognicao":
        await alma.ativar_agente_metacognicao()
        return "Agente de metacognição ativado."
    
    elif partes[0] == "emocional":
        await alma.ativar_agente_emocional()
        return "Agente emocional ativado."
    
    elif partes[0] == "consistencia":
        await alma.ativar_agente_consistencia()
        return "Agente de consistência ativado."
    
    elif partes[0] == "padroes":
        await alma.ativar_agente_padroes()
        return "Agente de identificação de padrões ativado."
    
    elif partes[0] == "aprendizado" and gerenciador_aprendizado:
        return gerenciador_aprendizado.status_aprendizado()
    
    elif partes[0] == "otimizar" and gerenciador_aprendizado:
        await gerenciador_aprendizado.otimizar_aprendizado()
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
        
        resultado = "Métricas atuais do sistema:\n"
        for chave, valor in metricas.items():
            if chave != "timestamp" and chave != "eficiencia_agentes":
                resultado += f"- {chave}: {valor}\n"
        
        if "eficiencia_agentes" in metricas:
            resultado += "\nEficiência dos agentes:\n"
            for agente, valor in metricas["eficiencia_agentes"].items():
                resultado += f"- {agente}: {valor}\n"
        
        return resultado
    
    elif partes[0] == "sair":
        return "sair"
    
    else:
        return "Comando não reconhecido. Digite 'ajuda' para ver os comandos disponíveis."

async def main_async():
    """Função principal do sistema, executada de forma assíncrona."""
    parser = argparse.ArgumentParser(description='Sistema de Memória Contínua e Reflexão Autônoma')
    parser.add_argument('--noreflexao', action='store_true', help='Desabilita o ciclo de reflexão automático')
    parser.add_argument('--noaprendizado', action='store_true', help='Desabilita o ciclo de aprendizado automático')
    parser.add_argument('--noadaptacao', action='store_true', help='Desabilita o ciclo de adaptação automático')
    parser.add_argument('--nosemantica', action='store_true', help='Desabilita o módulo de análise semântica avançada')
    parser.add_argument('--reflexao-intervalo', type=int, default=60, help='Intervalo entre ciclos de reflexão em segundos')
    parser.add_argument('--aprendizado-intervalo', type=int, default=300, help='Intervalo entre ciclos de aprendizado em segundos')
    parser.add_argument('--adaptacao-intervalo', type=int, default=600, help='Intervalo entre ciclos de adaptação em segundos')
    parser.add_argument('--modelo-spacy', type=str, default='pt_core_news_md', help='Modelo spaCy a ser utilizado para análise semântica')
    
    args = parser.parse_args()
    
    logger.info("Iniciando o sistema...")
    
    # Configuração inicial do ambiente
    await setup_environment()
    
    # Inicialização dos componentes do sistema
    persona = Persona()
    alma = Alma(persona)
    
    # Inicialização do gerenciador de aprendizado (Fase 4)
    gerenciador_aprendizado = GerenciadorAprendizado(persona, alma)
    alma.configurar_gerenciador_aprendizado(gerenciador_aprendizado)
    
    # Inicialização do sistema adaptativo (Fase 5)
    adaptativo = AprendizadoAdaptativo(persona, alma, gerenciador_aprendizado)
    
    # Carrega estado adaptativo anterior, se existir
    adaptativo.carregar_estado_aprendizado()
    
    # Inicialização do módulo semântico avançado, se disponível
    if MODULO_SEMANTICO_DISPONIVEL and not args.nosemantica:
        logger.info(f"Inicializando módulo de análise semântica avançada (modelo: {args.modelo_spacy})...")
        analisador_semantico.caminho_modelo = args.modelo_spacy
        
        # Inicializa recursos em background para não bloquear a inicialização
        asyncio.create_task(analisador_semantico.inicializar_recursos())
    
    # Iniciar tarefas assíncronas
    tarefas = []
    
    # Tarefa para o ciclo de reflexão
    if not args.noreflexao:
        logger.info(f"Iniciando ciclo de reflexão (intervalo: {args.reflexao_intervalo}s)")
        tarefa_reflexao = asyncio.create_task(alma.iniciar_ciclo_reflexao(intervalo=args.reflexao_intervalo))
        tarefas.append(tarefa_reflexao)
    
    # Tarefa para o ciclo de aprendizado
    if not args.noaprendizado:
        logger.info(f"Iniciando ciclo de aprendizado (intervalo: {args.aprendizado_intervalo}s)")
        tarefa_aprendizado = asyncio.create_task(gerenciador_aprendizado.ciclo_aprendizado_continuo(intervalo=args.aprendizado_intervalo))
        tarefas.append(tarefa_aprendizado)
    
    # Tarefa para o ciclo adaptativo
    if not args.noadaptacao:
        logger.info(f"Iniciando ciclo adaptativo (intervalo: {args.adaptacao_intervalo}s)")
        tarefa_adaptacao = asyncio.create_task(adaptativo.iniciar_ciclo_adaptativo(intervalo=args.adaptacao_intervalo))
        tarefas.append(tarefa_adaptacao)
    
    logger.info("Sistema inicializado. Digite 'ajuda' para ver os comandos disponíveis ou 'sair' para encerrar.")
    
    # Loop principal de interação com o usuário
    while True:
        try:
            comando = input("\n> ")
            resposta = await processar_comandos(comando, persona, alma, gerenciador_aprendizado, adaptativo)
            
            if resposta == "sair":
                logger.info("Encerrando o sistema...")
                break
            
            print(resposta)
        except Exception as e:
            logger.error(f"Erro ao processar comando: {e}")
            print(f"Ocorreu um erro: {e}")
    
    # Cancela as tarefas em andamento
    for tarefa in tarefas:
        tarefa.cancel()
    
    # Aguarda a conclusão das tarefas
    for tarefa in tarefas:
        try:
            await tarefa
        except asyncio.CancelledError:
            pass
    
    logger.info("Sistema encerrado.")

def main():
    """Ponto de entrada principal do programa."""
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("Sistema interrompido pelo usuário.")
    except Exception as e:
        logger.error(f"Erro não tratado: {e}", exc_info=True)

if __name__ == "__main__":
    main() 