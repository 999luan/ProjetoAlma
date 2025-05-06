"""
Módulo de Aprimoramento Semântico - Implementa técnicas avançadas de NLP.

Este módulo melhora a análise semântica do sistema, oferecendo ferramentas para:
- Comparação semântica avançada entre memórias
- Extração de entidades e conceitos relevantes
- Análise de sentimento e contexto emocional
- Agrupamento temático de memórias relacionadas
- Geração de sínteses mais coerentes
"""

import os
import re
import json
import pickle
import logging
import asyncio
from datetime import datetime
from collections import Counter
from pathlib import Path

# Importações condicionais para evitar erros se as bibliotecas não estiverem instaladas
try:
    import spacy
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import WordNetLemmatizer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sentence_transformers import SentenceTransformer
    BIBLIOTECAS_NLP_DISPONIVEIS = True
except ImportError:
    BIBLIOTECAS_NLP_DISPONIVEIS = False

# Configuração de logging
logger = logging.getLogger(__name__)

class AnalisadorSemantico:
    """Classe principal para análise semântica avançada."""
    
    def __init__(self, caminho_modelo="pt_core_news_md", modelos_path="data/nlp_models"):
        """
        Inicializa o analisador semântico.
        
        Args:
            caminho_modelo (str): Modelo spaCy a ser utilizado
            modelos_path (str): Caminho para armazenar modelos baixados
        """
        self.inicializado = False
        self.modelos_path = Path(modelos_path)
        self.caminho_modelo = caminho_modelo
        
        # Estes atributos serão inicializados posteriormente
        self.nlp = None
        self.modelo_embeddings = None
        self.lemmatizer = None
        self.stop_words = set()
        self.vetorizador = None
        
        # Cria o diretório para modelos se não existir
        os.makedirs(self.modelos_path, exist_ok=True)
    
    async def inicializar_recursos(self):
        """Inicializa os recursos de NLP de forma assíncrona para não bloquear o sistema."""
        if not BIBLIOTECAS_NLP_DISPONIVEIS:
            logger.warning("Bibliotecas de NLP não disponíveis. Funcionalidades avançadas desabilitadas.")
            return False
        
        if self.inicializado:
            return True
        
        try:
            logger.info("Inicializando recursos de NLP avançados...")
            
            # Inicializa o modelo spaCy
            try:
                self.nlp = spacy.load(self.caminho_modelo)
                logger.info(f"Modelo spaCy '{self.caminho_modelo}' carregado com sucesso.")
            except OSError:
                logger.info(f"Baixando modelo spaCy '{self.caminho_modelo}'...")
                os.system(f"python -m spacy download {self.caminho_modelo}")
                self.nlp = spacy.load(self.caminho_modelo)
            
            # Inicializa recursos NLTK
            nltk_recursos = ['punkt', 'wordnet', 'stopwords', 'vader_lexicon']
            for recurso in nltk_recursos:
                try:
                    nltk.data.find(f'tokenizers/{recurso}')
                except LookupError:
                    logger.info(f"Baixando recurso NLTK: {recurso}")
                    nltk.download(recurso)
            
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('portuguese') + stopwords.words('english'))
            
            # Inicializa o modelo de embeddings
            modelo_embeddings_path = self.modelos_path / "sentence-transformer"
            if modelo_embeddings_path.exists():
                self.modelo_embeddings = SentenceTransformer(str(modelo_embeddings_path))
                logger.info("Modelo de embeddings carregado do cache local.")
            else:
                logger.info("Inicializando modelo de embeddings...")
                self.modelo_embeddings = SentenceTransformer('distiluse-base-multilingual-cased-v1')
                # Salva o modelo para uso futuro
                os.makedirs(modelo_embeddings_path, exist_ok=True)
                self.modelo_embeddings.save(str(modelo_embeddings_path))
            
            # Inicializa o vetorizador TF-IDF
            self.vetorizador = TfidfVectorizer(
                min_df=2, max_df=0.95, 
                stop_words=list(self.stop_words),
                ngram_range=(1, 2)
            )
            
            self.inicializado = True
            logger.info("Recursos de NLP inicializados com sucesso.")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar recursos de NLP: {e}")
            self.inicializado = False
            return False
    
    async def calcular_similaridade_semantica(self, texto1, texto2, metodo="embeddings"):
        """
        Calcula a similaridade semântica entre dois textos usando diferentes métodos.
        
        Args:
            texto1 (str): Primeiro texto
            texto2 (str): Segundo texto
            metodo (str): Método a utilizar ('embeddings', 'tfidf', 'spacy')
            
        Returns:
            float: Score de similaridade entre 0 e 1
        """
        if not self.inicializado:
            await self.inicializar_recursos()
            if not self.inicializado:
                # Fallback para método simples se NLP não estiver disponível
                from core.utils import calcular_similaridade_texto
                return calcular_similaridade_texto(texto1, texto2)
        
        if not texto1 or not texto2:
            return 0.0
        
        try:
            if metodo == "embeddings":
                # Uso de embeddings semânticos (mais preciso)
                embedding1 = self.modelo_embeddings.encode([texto1])[0]
                embedding2 = self.modelo_embeddings.encode([texto2])[0]
                # Calcula similaridade de cosseno
                similarity = cosine_similarity([embedding1], [embedding2])[0][0]
                return float(similarity)
            
            elif metodo == "tfidf":
                # Vetorização TF-IDF
                vetores = self.vetorizador.fit_transform([texto1, texto2])
                similarity = cosine_similarity(vetores[0:1], vetores[1:2])[0][0]
                return float(similarity)
            
            elif metodo == "spacy":
                # Uso de spaCy para similaridade
                doc1 = self.nlp(texto1)
                doc2 = self.nlp(texto2)
                return doc1.similarity(doc2)
            
            else:
                logger.warning(f"Método de similaridade '{metodo}' não reconhecido.")
                # Fallback para método padrão
                doc1 = self.nlp(texto1)
                doc2 = self.nlp(texto2)
                return doc1.similarity(doc2)
                
        except Exception as e:
            logger.error(f"Erro ao calcular similaridade semântica: {e}")
            # Fallback para método simples em caso de erro
            from core.utils import calcular_similaridade_texto
            return calcular_similaridade_texto(texto1, texto2)
    
    async def extrair_entidades(self, texto):
        """
        Extrai entidades relevantes de um texto.
        
        Args:
            texto (str): Texto para análise
            
        Returns:
            dict: Dicionário de entidades por categoria
        """
        if not self.inicializado:
            await self.inicializar_recursos()
            if not self.inicializado:
                return {"error": "Recursos NLP não disponíveis"}
        
        try:
            doc = self.nlp(texto)
            entidades = {}
            
            for ent in doc.ents:
                categoria = ent.label_
                if categoria not in entidades:
                    entidades[categoria] = []
                entidades[categoria].append({
                    "texto": ent.text,
                    "posicao_inicio": ent.start_char,
                    "posicao_fim": ent.end_char
                })
            
            return entidades
        
        except Exception as e:
            logger.error(f"Erro ao extrair entidades: {e}")
            return {"error": str(e)}
    
    async def analisar_sentimento(self, texto):
        """
        Analisa o sentimento de um texto.
        
        Args:
            texto (str): Texto para análise
            
        Returns:
            dict: Informações de sentimento (polaridade, subjetividade)
        """
        if not self.inicializado:
            await self.inicializar_recursos()
            if not self.inicializado:
                return {"polaridade": 0, "subjetividade": 0.5}
        
        try:
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
            
            # Análise com VADER (para inglês)
            sid = SentimentIntensityAnalyzer()
            scores = sid.polarity_scores(texto)
            
            # Para português, podemos usar uma heurística baseada em palavras-chave
            # ou um modelo específico para português (não implementado aqui)
            
            return {
                "polaridade": scores["compound"],  # Entre -1 (negativo) e 1 (positivo)
                "positivo": scores["pos"],
                "negativo": scores["neg"],
                "neutro": scores["neu"]
            }
            
        except Exception as e:
            logger.error(f"Erro ao analisar sentimento: {e}")
            return {"polaridade": 0, "positivo": 0.33, "negativo": 0.33, "neutro": 0.34}
    
    async def extrair_palavras_chave(self, texto, n=5):
        """
        Extrai as principais palavras-chave de um texto.
        
        Args:
            texto (str): Texto para análise
            n (int): Número de palavras-chave a retornar
            
        Returns:
            list: Lista das principais palavras-chave
        """
        if not self.inicializado:
            await self.inicializar_recursos()
            if not self.inicializado:
                # Fallback simples
                palavras = texto.lower().split()
                contador = Counter(palavras)
                return [palavra for palavra, _ in contador.most_common(n)]
        
        try:
            # Remove stopwords e faz lematização
            tokens = [token.lemma_ for token in self.nlp(texto) 
                     if not token.is_stop and not token.is_punct and len(token.text) > 3]
            
            # Conta frequência
            contador = Counter(tokens)
            
            # Retorna as mais comuns
            return [palavra for palavra, _ in contador.most_common(n)]
            
        except Exception as e:
            logger.error(f"Erro ao extrair palavras-chave: {e}")
            # Fallback simples
            palavras = texto.lower().split()
            contador = Counter(palavras)
            return [palavra for palavra, _ in contador.most_common(n)]
    
    async def gerar_sintese_avancada(self, textos):
        """
        Gera uma síntese avançada a partir de múltiplos textos.
        
        Args:
            textos (list): Lista de textos para sintetizar
            
        Returns:
            str: Síntese gerada
        """
        if not textos:
            return ""
        
        if len(textos) == 1:
            return textos[0]
        
        if not self.inicializado:
            await self.inicializar_recursos()
            if not self.inicializado:
                # Fallback para método simples
                from core.utils import combinar_textos
                return combinar_textos(textos, "intercalar")
        
        try:
            # Extrai sentenças de todos os textos
            todas_sentencas = []
            for texto in textos:
                sentencas = sent_tokenize(texto)
                todas_sentencas.extend(sentencas)
            
            # Calcula embeddings para todas as sentenças
            embeddings = self.modelo_embeddings.encode(todas_sentencas)
            
            # Agrupa sentencas semelhantes
            grupos = self._agrupar_sentencas(todas_sentencas, embeddings)
            
            # Seleciona uma sentença representativa de cada grupo
            sentencas_selecionadas = []
            for grupo in grupos:
                if grupo:  # Certifica-se de que o grupo não está vazio
                    sentencas_selecionadas.append(grupo[0])
            
            # Ordena as sentenças para formar um texto coerente
            # (neste caso, uma ordenação simples baseada na ordem original)
            resultado = " ".join(sentencas_selecionadas)
            
            return resultado
            
        except Exception as e:
            logger.error(f"Erro ao gerar síntese avançada: {e}")
            # Fallback para método simples
            from core.utils import combinar_textos
            return combinar_textos(textos, "intercalar")
    
    def _agrupar_sentencas(self, sentencas, embeddings, limiar=0.7):
        """
        Agrupa sentenças semelhantes com base em seus embeddings.
        
        Args:
            sentencas (list): Lista de sentenças
            embeddings (list): Embeddings correspondentes
            limiar (float): Limiar de similaridade para agrupar
            
        Returns:
            list: Lista de grupos de sentenças
        """
        grupos = []
        sentencas_processadas = set()
        
        for i, (sentenca, embedding) in enumerate(zip(sentencas, embeddings)):
            if i in sentencas_processadas:
                continue
                
            grupo_atual = [sentenca]
            sentencas_processadas.add(i)
            
            for j, outro_embedding in enumerate(embeddings):
                if j != i and j not in sentencas_processadas:
                    # Calcula similaridade
                    sim = cosine_similarity([embedding], [outro_embedding])[0][0]
                    if sim > limiar:
                        grupo_atual.append(sentencas[j])
                        sentencas_processadas.add(j)
            
            grupos.append(grupo_atual)
        
        return grupos
    
    async def encontrar_contradicoes(self, memoria1, memoria2):
        """
        Tenta identificar contradições entre duas memórias.
        
        Args:
            memoria1 (dict): Primeira memória
            memoria2 (dict): Segunda memória
            
        Returns:
            dict: Informações sobre contradições encontradas
        """
        if not self.inicializado:
            await self.inicializar_recursos()
            if not self.inicializado:
                return {"encontrou_contradicao": False}
        
        try:
            texto1 = memoria1["conteudo"]
            texto2 = memoria2["conteudo"]
            
            # Extrai entidades para comparação
            entidades1 = await self.extrair_entidades(texto1)
            entidades2 = await self.extrair_entidades(texto2)
            
            # Procura negações que possam indicar contradições
            negacoes1 = self._detectar_negacoes(texto1)
            negacoes2 = self._detectar_negacoes(texto2)
            
            # Analisa se há afirmações contraditórias
            doc1 = self.nlp(texto1)
            doc2 = self.nlp(texto2)
            
            # Encontra sentenças semelhantes para comparar
            sentencas_contraditorias = []
            
            for sent1 in doc1.sents:
                for sent2 in doc2.sents:
                    # Verifica similaridade entre as sentenças
                    similaridade = sent1.similarity(sent2)
                    
                    if similaridade > 0.6:  # Sentenças bastante similares
                        # Verifica se uma contém negação e a outra não
                        tem_negacao1 = any(negacao in sent1.text.lower() for negacao in negacoes1)
                        tem_negacao2 = any(negacao in sent2.text.lower() for negacao in negacoes2)
                        
                        if tem_negacao1 != tem_negacao2:
                            sentencas_contraditorias.append({
                                "sentenca1": sent1.text,
                                "sentenca2": sent2.text,
                                "similaridade": similaridade
                            })
            
            # Retorna resultado
            return {
                "encontrou_contradicao": len(sentencas_contraditorias) > 0,
                "sentencas_contraditorias": sentencas_contraditorias,
                "similaridade_geral": doc1.similarity(doc2)
            }
            
        except Exception as e:
            logger.error(f"Erro ao buscar contradições: {e}")
            return {"encontrou_contradicao": False, "erro": str(e)}
    
    def _detectar_negacoes(self, texto):
        """
        Detecta palavras e expressões de negação em um texto.
        
        Args:
            texto (str): Texto para análise
            
        Returns:
            list: Lista de negações encontradas
        """
        negacoes_pt = ['não', 'nunca', 'jamais', 'nem', 'nenhum', 'nada']
        negacoes_en = ['not', 'never', 'no', 'none', 'nothing']
        
        # Converte para minúsculas para facilitar a comparação
        texto_lower = texto.lower()
        
        # Procura negações no texto
        negacoes_encontradas = []
        for negacao in negacoes_pt + negacoes_en:
            if negacao in texto_lower:
                negacoes_encontradas.append(negacao)
        
        return negacoes_encontradas

# Instância global para uso em todo o sistema
analisador_semantico = AnalisadorSemantico() 