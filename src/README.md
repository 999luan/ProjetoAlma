# Código-fonte Principal

Esta pasta contém os dois módulos principais do sistema:

## Persona
O módulo Persona é responsável por:
- Receber informações externas
- Armazenar estas informações na memória (curto e longo prazo)
- Processar pensamentos básicos

## Alma
O módulo Alma é responsável por:
- Refinar pensamentos gerados pela Persona
- Executar ciclos contínuos de reflexão
- Gerenciar agentes internos para análise e síntese de informações
- Monitorar e depurar o sistema

## Arquitetura

```
src/
│
├── persona/                # Módulo Persona
│   ├── __init__.py
│   ├── memoria.py          # Gerenciamento de memória
│   └── processador_pensamento.py  # Processamento de pensamentos
│
└── alma/                   # Módulo Alma
    ├── __init__.py
    ├── agente_reflexao.py  # Agente para refinar pensamentos
    └── debug.py            # Sistema de monitoramento e debug
``` 