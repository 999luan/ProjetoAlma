"""
Testa o módulo de análise semântica avançada.

Este script demonstra as funcionalidades de análise semântica
implementadas no módulo nlp_enhancement.py.
"""

import asyncio
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def testar_analise_semantica():
    """Testa as funcionalidades de análise semântica."""
    logger.info("=== Teste do Módulo de Análise Semântica Avançada ===")
    
    try:
        # Importa o módulo de análise semântica
        from core.nlp_enhancement import analisador_semantico
        
        # Inicializa recursos
        logger.info("Inicializando recursos de NLP...")
        inicializado = await analisador_semantico.inicializar_recursos()
        
        if not inicializado:
            logger.error("Não foi possível inicializar os recursos de NLP. Verifique se todas as dependências estão instaladas.")
            logger.info("Dica: Execute 'pip install -r requirements.txt' para instalar as dependências necessárias.")
            return
        
        logger.info("Recursos de NLP inicializados com sucesso!")
        
        # Define textos para teste
        textos_teste = [
            "A inteligência artificial é um campo fascinante com muitas aplicações práticas.",
            "IA apresenta diversas possibilidades de uso em problemas do mundo real.",
            "Sistemas de IA não têm emoções ou consciência própria.",
            "Inteligência artificial não possui sentimentos ou autoconsciência.",
            "Algoritmos de aprendizado de máquina exigem grandes quantidades de dados de treinamento.",
            "O Brasil é o maior país da América do Sul em termos de território.",
            "A Argentina não é o maior país da América do Sul."
        ]
        
        # Teste 1: Calcular similaridade semântica
        logger.info("\n=== TESTE 1: Similaridade Semântica ===")
        for i in range(len(textos_teste)):
            for j in range(i+1, len(textos_teste)):
                sim_embeddings = await analisador_semantico.calcular_similaridade_semantica(
                    textos_teste[i], textos_teste[j], metodo="embeddings"
                )
                sim_spacy = await analisador_semantico.calcular_similaridade_semantica(
                    textos_teste[i], textos_teste[j], metodo="spacy"
                )
                
                logger.info(f"Similaridade entre textos {i+1} e {j+1}:")
                logger.info(f"  - Usando embeddings: {sim_embeddings:.4f}")
                logger.info(f"  - Usando spaCy: {sim_spacy:.4f}")
        
        # Teste 2: Extrair entidades
        logger.info("\n=== TESTE 2: Extração de Entidades ===")
        texto_entidades = "A Microsoft e a OpenAI estão trabalhando juntas em projetos de IA. Satya Nadella anunciou novos investimentos em fevereiro de 2023 em São Francisco."
        entidades = await analisador_semantico.extrair_entidades(texto_entidades)
        
        logger.info(f"Texto: {texto_entidades}")
        logger.info("Entidades detectadas:")
        for categoria, items in entidades.items():
            logger.info(f"  {categoria}: {', '.join([item['texto'] for item in items])}")
        
        # Teste 3: Análise de sentimento
        logger.info("\n=== TESTE 3: Análise de Sentimento ===")
        textos_sentimento = [
            "Estou muito feliz com os resultados do novo sistema!",
            "Infelizmente, o aplicativo está cheio de problemas e falhas.",
            "O sistema funciona como esperado, sem grandes surpresas."
        ]
        
        for i, texto in enumerate(textos_sentimento):
            sentimento = await analisador_semantico.analisar_sentimento(texto)
            logger.info(f"Texto {i+1}: {texto}")
            logger.info(f"  Polaridade: {sentimento['polaridade']:.4f} (-1=negativo, 1=positivo)")
            logger.info(f"  Positivo: {sentimento['positivo']:.4f}")
            logger.info(f"  Negativo: {sentimento['negativo']:.4f}")
            logger.info(f"  Neutro: {sentimento['neutro']:.4f}")
        
        # Teste 4: Extração de palavras-chave
        logger.info("\n=== TESTE 4: Extração de Palavras-chave ===")
        texto_longo = """
        Aprendizado de máquina é um subcampo da inteligência artificial que permite aos computadores
        aprender a partir de dados, sem serem explicitamente programados. Os algoritmos de aprendizado
        de máquina analisam padrões em conjuntos de dados e fazem previsões baseadas nesses padrões.
        Deep learning é uma técnica de aprendizado de máquina que utiliza redes neurais com múltiplas
        camadas para processar informações de maneira semelhante ao cérebro humano.
        """
        
        palavras_chave = await analisador_semantico.extrair_palavras_chave(texto_longo, n=8)
        logger.info("Palavras-chave do texto:")
        logger.info(f"  {', '.join(palavras_chave)}")
        
        # Teste 5: Geração de síntese avançada
        logger.info("\n=== TESTE 5: Geração de Síntese Avançada ===")
        textos_para_sintese = [
            "A inteligência artificial está revolucionando diversos setores da economia mundial.",
            "Tecnologias como machine learning e deep learning são fundamentais no desenvolvimento de sistemas inteligentes.",
            "A ética na IA é um tema crucial que precisa ser debatido para garantir um desenvolvimento responsável."
        ]
        
        logger.info("Textos originais:")
        for i, texto in enumerate(textos_para_sintese):
            logger.info(f"  {i+1}: {texto}")
        
        sintese = await analisador_semantico.gerar_sintese_avancada(textos_para_sintese)
        logger.info("\nSíntese gerada:")
        logger.info(f"  {sintese}")
        
        # Teste 6: Detecção de contradições
        logger.info("\n=== TESTE 6: Detecção de Contradições ===")
        memoria1 = {"id": 1, "conteudo": "A Terra é redonda e orbita ao redor do Sol."}
        memoria2 = {"id": 2, "conteudo": "A Terra não é plana e gira em torno do Sol."}
        memoria3 = {"id": 3, "conteudo": "O planeta Terra é achatado nos pólos e tem formato de esferóide."}
        memoria4 = {"id": 4, "conteudo": "A Terra é plana e o Sol gira ao seu redor."}
        
        # Testa pares não contraditórios
        logger.info("Testando memórias sem contradição:")
        resultado1 = await analisador_semantico.encontrar_contradicoes(memoria1, memoria2)
        logger.info(f"  Memórias 1 e 2: Contradição detectada = {resultado1['encontrou_contradicao']}")
        
        resultado2 = await analisador_semantico.encontrar_contradicoes(memoria1, memoria3)
        logger.info(f"  Memórias 1 e 3: Contradição detectada = {resultado2['encontrou_contradicao']}")
        
        # Testa par contraditório
        logger.info("Testando memórias com contradição:")
        resultado3 = await analisador_semantico.encontrar_contradicoes(memoria1, memoria4)
        logger.info(f"  Memórias 1 e 4: Contradição detectada = {resultado3['encontrou_contradicao']}")
        
        if resultado3['encontrou_contradicao'] and 'sentencas_contraditorias' in resultado3:
            logger.info("  Sentenças contraditórias detectadas:")
            for i, sentenca in enumerate(resultado3['sentencas_contraditorias']):
                logger.info(f"    {i+1}: '{sentenca['sentenca1']}' vs '{sentenca['sentenca2']}'")
        
        logger.info("\n=== Testes concluídos com sucesso! ===")
    
    except ImportError:
        logger.error("Módulo de análise semântica não disponível. Verifique se todas as dependências estão instaladas.")
        logger.info("Dica: Execute 'pip install -r requirements.txt' para instalar as dependências necessárias.")
    
    except Exception as e:
        logger.error(f"Erro durante os testes: {e}")

if __name__ == "__main__":
    asyncio.run(testar_analise_semantica()) 