# Projeto Alma - Sistema de Memória Contínua e Reflexão Autônoma

## Visão Geral
O Projeto Alma é um sistema avançado de memória contínua e reflexão autônoma que implementa um ciclo contínuo de aprendizado e adaptação. O sistema é composto por cinco fases principais:

1. **Memória e Armazenamento**: Sistema robusto de armazenamento e recuperação de memórias
2. **Reflexão e Metacognição**: Processamento contínuo de pensamentos e reflexões
3. **Sistema Multi-agentes**: Agentes especializados para diferentes aspectos do processamento
4. **Ciclo de Pensamento Contínuo**: Aprendizado autônomo baseado em experiências
5. **Adaptação e Experimentação**: Evolução contínua do sistema através de experimentação

## Estrutura do Projeto

```
ProjetoAlma/
├── core/
│   ├── alma.py                 # Controlador principal do sistema
│   ├── learning.py             # Gerenciador de aprendizado
│   ├── adaptive_learning.py    # Sistema de aprendizado adaptativo
│   └── nlp_enhancement.py      # Melhorias de processamento de linguagem natural
├── persona/
│   ├── persona.py              # Interface do sistema Persona
│   ├── memoria.py              # Sistema de memória
│   └── processador_pensamento.py # Processador de pensamentos
├── data/
│   ├── memoria.json           # Armazenamento de memórias
│   ├── sinteses/              # Diretório para sínteses geradas
│   └── adaptive_learning/     # Dados de aprendizado adaptativo
├── logs/                      # Logs do sistema
└── main.py                    # Ponto de entrada do sistema
```

## Funcionalidades Principais

### Sistema de Memória
- Armazenamento persistente de memórias
- Busca semântica avançada
- Integração de novas informações
- Geração de sínteses
- Análise de sentimentos e entidades

### Processamento de Pensamentos
- Ciclo contínuo de reflexão
- Processamento assíncrono
- Integração com memória
- Histórico de processamento

### Aprendizado Adaptativo
- Ciclos de aprendizado contínuos
- Análise de métricas do sistema
- Ajuste automático de estratégias
- Experimentação autônoma

## Requisitos

- Python 3.8+
- Dependências principais:
  - asyncio
  - logging
  - json
  - datetime
  - (Opcional) spaCy para análise semântica avançada

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/999luan/ProjetoAlma.git
cd ProjetoAlma
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. (Opcional) Para análise semântica avançada:
```bash
python -m spacy download pt_core_news_md
```

## Uso

Execute o sistema com:
```bash
python main.py
```

### Comandos Disponíveis

- **Memória e Armazenamento**:
  - `armazenar [mensagem]` - Armazena nova memória
  - `listar [n]` - Lista últimas n memórias
  - `buscar [termo]` - Busca memórias por termo

- **Análise e Reflexão**:
  - `buscar-semantico [consulta]` - Busca semântica
  - `extrair-entidades [texto]` - Extrai entidades
  - `analisar-sentimento [texto]` - Analisa sentimento
  - `palavras-chave [texto]` - Extrai palavras-chave

- **Agentes e Ciclos**:
  - `refletir` - Executa ciclo de reflexão
  - `metacognicao` - Ativa agente metacognitivo
  - `emocional` - Ativa agente emocional
  - `consistencia` - Ativa agente de consistência
  - `padroes` - Ativa agente de padrões

- **Aprendizado e Adaptação**:
  - `aprendizado` - Status do aprendizado
  - `otimizar` - Otimiza processo
  - `estatisticas` - Mostra estatísticas
  - `adaptar [intervalo]` - Inicia ciclo adaptativo
  - `experimentos` - Lista experimentos ativos
  - `metricas` - Mostra métricas do sistema
  - `estrategias` - Lista estratégias efetivas

## Opções de Execução

O sistema pode ser executado com várias opções:

```bash
python main.py [opções]

Opções:
  --noreflexao              Desabilita ciclo de reflexão automático
  --noaprendizado           Desabilita ciclo de aprendizado automático
  --noadaptacao             Desabilita ciclo de adaptação automático
  --nosemantica             Desabilita módulo de análise semântica
  --reflexao-intervalo N    Intervalo entre ciclos de reflexão (segundos)
  --aprendizado-intervalo N Intervalo entre ciclos de aprendizado (segundos)
  --adaptacao-intervalo N   Intervalo entre ciclos de adaptação (segundos)
  --modelo-spacy MODELO     Modelo spaCy para análise semântica
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Para questões e sugestões, abra uma issue no repositório. 