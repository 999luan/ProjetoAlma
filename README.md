# Sistema de Memória Contínua e Reflexão Autônoma

Sistema capaz de armazenar informações, refletir sobre elas e evoluir seu conhecimento de forma autônoma, com foco na criação de entidades virtuais capazes de metacognição.

## 📖 Visão Geral

Este projeto implementa um sistema de memória contínua que:

- Recebe informações do mundo exterior
- Pensa sozinho em momentos de ociosidade
- Refina seus próprios pensamentos com reflexão autônoma
- Evolui, aprende e corrija suas informações ao longo do tempo

## ⚙️ Requisitos

- Python 3.8+
- PowerShell (Windows) ou terminal Bash (Linux/Mac)

## 🚀 Configuração do Ambiente

### Windows (PowerShell)

1. Clone o repositório ou descompacte os arquivos em uma pasta
2. Abra o PowerShell na pasta do projeto
3. Execute o script de configuração:

```powershell
.\setup.ps1
```

Este script irá:
- Criar um ambiente virtual Python (venv)
- Instalar todas as dependências necessárias
- Configurar os diretórios do sistema

## 🏃‍♂️ Executando o Sistema

Após configurar o ambiente, execute:

```powershell
python main.py
```

## 🧠 Funcionalidades Implementadas (Fase 1)

- **Memória Persistente**: Armazenamento em JSON com detecção de memórias similares
- **Síntese de Conhecimento**: Combinação de memórias existentes para criar novas ideias
- **Ciclo de Reflexão**: Processamento contínuo e autônomo de memórias armazenadas
- **Metacognição**: Avaliação e melhoria de memórias de baixa qualidade
- **Interface de Comandos**: Interação via linha de comando

## 📝 Comandos Disponíveis

No console do sistema:
- `ajuda`       - Mostra a lista de comandos disponíveis
- `sair`        - Encerra o sistema
- `adicionar`   - Adiciona uma nova informação
- `sintese`     - Gera uma síntese de memórias existentes
- `reflexao`    - Força um ciclo de reflexão
- `metacog`     - Força um ciclo de metacognição
- `memorias`    - Lista todas as memórias armazenadas
- `stats`       - Mostra estatísticas do sistema

## 📋 Estrutura do Projeto

```
/
│
├── core/                  # Módulos principais do sistema
│   ├── persona.py        # Recebimento e armazenamento de informações
│   ├── alma.py           # Reflexão e metacognição
│   ├── utils.py          # Funções utilitárias
│   ├── config.py         # Configurações do sistema
│   └── memoria.json      # Arquivo de memórias persistente
│
├── main.py               # Ponto de entrada do sistema
├── requirements.txt      # Dependências do projeto
├── setup.ps1             # Script de configuração para Windows
└── README.md             # Este arquivo
```

## 🔍 Módulos Principais

### Persona

Responsável por:
- Receber informações externas
- Armazenar informações em formato estruturado
- Processar e comparar com memórias existentes
- Gerar sínteses combinando memórias diferentes

### Alma

Responsável por:
- Executar ciclos de reflexão contínuos
- Avaliar a qualidade das memórias (metacognição)
- Refinar e melhorar memórias de baixa qualidade
- Criar conexões e insights entre diferentes memórias

## 🔄 Conceito Central

> "Pensar é lembrar, comparar e criar uma nova versão melhor do que existia."

Esta frase captura a essência do projeto: o sistema constantemente revê suas próprias memórias, as compara, reflete sobre elas e gera novas sínteses, melhorando continuamente seu conhecimento interno.

## 📚 Desenvolvimento

Este projeto segue o plano detalhado em:
- `Plano de Desenvolvimento — Sistema de Memória Contínua e Cognição Adaptativa (V2).md` 