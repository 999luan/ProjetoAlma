# Sistema de Memória Contínua e Reflexão Autônoma

Este projeto implementa um sistema de inteligência artificial com capacidade de memória contínua, reflexão autônoma e aprendizado ao longo da vida (lifelong learning).

## Funcionalidades

- **Memória Persistente**: Armazenamento e recuperação de informações com persistência
- **Reflexão Autônoma**: Ciclos automáticos de análise e reflexão sobre as informações armazenadas
- **Sistema Multi-agentes**: Diferentes agentes especializados para processamento emocional, consistência e identificação de padrões
- **Aprendizado Contínuo**: Mecanismos de aprendizado sem supervisão e otimização automática
- **Experimentação Adaptativa**: Sistema que evolui através de experimentos e auto-avaliação
- **Análise Semântica**: Processamento de linguagem natural avançado para compreensão de textos (opcional)

## Arquitetura

O sistema é dividido em dois módulos principais:

- **Persona**: Interface consciente do sistema, responsável por receber, armazenar e processar informações
- **Alma**: Sistema subconsciente que executa processos de reflexão, metacognição e análise em segundo plano

## Requisitos

- Python 3.7+
- Dependências específicas (instaláveis via `pip install -r requirements.txt`):
  - requests
  - python-dotenv
  - spacy
  - scikit-learn
  - nltk
  - sentence-transformers

## Instalação

1. Clone o repositório
2. Instale as dependências:
```
pip install -r requirements.txt
```
3. Para funcionalidades avançadas de NLP, instale os modelos adicionais:
```
python -m spacy download pt_core_news_md
python -m nltk.downloader punkt wordnet stopwords vader_lexicon
```

## Executando o sistema

Para iniciar o sistema com todas as funcionalidades:
```
python main.py
```

Opções de linha de comando:
- `--noreflexao`: Desativa o ciclo de reflexão automático
- `--noaprendizado`: Desativa o ciclo de aprendizado automático
- `--noadaptacao`: Desativa o ciclo de adaptação automático
- `--nosemantica`: Desativa o módulo de análise semântica avançada
- `--reflexao-intervalo SEGUNDOS`: Define o intervalo entre ciclos de reflexão (padrão: 60s)
- `--aprendizado-intervalo SEGUNDOS`: Define o intervalo entre ciclos de aprendizado (padrão: 300s)
- `--adaptacao-intervalo SEGUNDOS`: Define o intervalo entre ciclos de adaptação (padrão: 600s)
- `--modelo-spacy MODELO`: Define o modelo spaCy a ser utilizado (padrão: pt_core_news_md)

## Comandos disponíveis

O sistema oferece uma interface de linha de comando com diversos comandos:
- `ajuda`: Mostra a lista de comandos disponíveis
- `armazenar [mensagem]`: Armazena uma nova memória
- `listar [n]`: Lista as últimas n memórias (padrão: 5)
- `buscar [termo]`: Busca memórias contendo o termo
- `buscar-semantico [consulta]`: Busca memórias semanticamente similares à consulta
- `extrair-entidades [texto]`: Extrai entidades de um texto
- `analisar-sentimento [texto]`: Analisa o sentimento de um texto
- `palavras-chave [texto]`: Extrai palavras-chave de um texto
- `refletir`: Executa um ciclo de reflexão
- `metacognicao`: Ativa o agente de metacognição
- `emocional`: Ativa o agente emocional
- `consistencia`: Ativa o agente de consistência
- `padroes`: Ativa o agente de identificação de padrões
- `aprendizado`: Informações sobre o aprendizado atual
- `otimizar`: Otimiza o processo de aprendizado
- `estatisticas`: Mostra estatísticas do aprendizado
- `adaptar [intervalo]`: Inicia ciclo adaptativo (intervalo em segundos)
- `experimentos`: Lista experimentos ativos
- `metricas`: Mostra métricas atuais do sistema
- `estrategias`: Lista estratégias efetivas aprendidas
- `sair`: Encerra o programa

## Estrutura de arquivos

- `main.py`: Aplicação principal e ponto de entrada
- `core/`: Diretório dos componentes principais
  - `persona.py`: Implementação da Persona
  - `alma.py`: Implementação da Alma
  - `learning.py`: Sistema de aprendizado contínuo
  - `adaptive_learning.py`: Sistema adaptativo avançado
  - `nlp_enhancement.py`: Módulo de análise semântica
  - `agentes/`: Agentes especializados
- `data/`: Diretório de dados onde as memórias são armazenadas
- `logs/`: Diretório de logs

## Documentação Completa

Para informações mais detalhadas sobre o sistema, consulte o arquivo `documentacao.md`. 