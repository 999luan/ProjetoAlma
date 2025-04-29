# Módulo de Análise Semântica Avançada

Este módulo aprimora as capacidades de compreensão e processamento de texto do sistema, utilizando técnicas avançadas de Processamento de Linguagem Natural (NLP).

## Funcionalidades

### 1. Análise de Similaridade Semântica

Compara textos utilizando diferentes métodos:
- **Embeddings de Sentenças**: Incorporações vetoriais de alta dimensão que capturam o significado das frases
- **TF-IDF**: Análise estatística baseada na frequência de termos
- **Similaridade spaCy**: Comparação contextual usando modelos pré-treinados

### 2. Extração de Entidades

Identifica e classifica entidades no texto como:
- Pessoas
- Organizações
- Locais
- Datas
- Valores numéricos
- Outras categorias relevantes

### 3. Análise de Sentimento

Determina a polaridade emocional do texto:
- Pontuação de positividade (0-1)
- Pontuação de negatividade (0-1)
- Pontuação de neutralidade (0-1)
- Polaridade combinada (-1 a 1)

### 4. Extração de Palavras-chave

Identifica os termos mais relevantes em um texto, descartando palavras comuns (stopwords) e focando em conceitos significativos.

### 5. Síntese Semântica Avançada

Gera sínteses mais coerentes a partir de múltiplos textos:
- Agrupa sentenças semanticamente similares
- Seleciona as mais representativas
- Organiza em texto fluido e não repetitivo

### 6. Detecção de Contradições

Identifica informações contraditórias entre memórias:
- Compara sentenças semanticamente relacionadas
- Detecta afirmações e negações sobre o mesmo tema
- Identifica as sentenças específicas em contradição

## Integração com o Sistema

O módulo está integrado aos seguintes componentes:

1. **Persona**: 
   - Melhor detecção de memórias similares
   - Síntese mais coerente entre memórias
   - Busca semântica avançada

2. **Agente de Consistência**:
   - Identificação mais precisa de contradições
   - Resolução mais detalhada de inconsistências

## Requisitos

- Python 3.8+
- spaCy (com modelo português/multilíngue)
- NLTK (com recursos adicionais)
- scikit-learn
- sentence-transformers

## Uso

### Na linha de comando:

```
python main.py
```

Novos comandos disponíveis:
- `buscar-semantico [consulta]`: Encontra memórias semanticamente relacionadas
- `extrair-entidades [texto]`: Identifica entidades no texto
- `analisar-sentimento [texto]`: Analisa a polaridade emocional do texto
- `palavras-chave [texto]`: Extrai os termos mais significativos

### Opções ao iniciar o sistema:

```
python main.py [--nosemantica] [--modelo-spacy MODELO]
```

- `--nosemantica`: Desativa os recursos de análise semântica avançada
- `--modelo-spacy MODELO`: Especifica o modelo spaCy a ser usado (padrão: pt_core_news_md)

## Teste das Funcionalidades

Para testar todas as funcionalidades do módulo semântico:

```
python test_semantic.py
```

Este script demonstra o uso de todas as capacidades do módulo com exemplos práticos.

## Fallbacks

O módulo possui mecanismos de fallback que garantem o funcionamento do sistema mesmo quando:
- As bibliotecas necessárias não estão instaladas
- Ocorre um erro durante o processamento
- Os modelos não podem ser carregados

Nestes casos, o sistema utilizará os métodos simplificados originais, garantindo a continuidade da operação. 