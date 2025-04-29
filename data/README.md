# Dados do Sistema

Esta pasta contém os dados persistentes gerados e utilizados pelo sistema:

## Estrutura

```
data/
│
├── memoria/       # Armazenamento de memórias geradas pelo sistema
│
├── conhecimento/  # Base de conhecimento e informações estruturadas
│
└── perfis/        # Perfis de personalidade
```

## Descrição

### Memória

Contém arquivos que representam as memórias de longo prazo do sistema. O armazenamento pode ser em formatos como:
- JSON: para estruturas simples
- SQLite: para memórias mais complexas com necessidade de consultas
- Texto: para memórias em formato não estruturado

### Conhecimento

Armazena a base de conhecimento do sistema, incluindo:
- Fatos aprendidos
- Regras e padrões descobertos
- Metadados sobre informações processadas

### Perfis

Contém perfis que determinam como o sistema processa e reage a informações:
- Configurações de personalidade
- Histórico de evolução cognitiva
- Preferências e tendências do sistema

## Notas de Uso

- Os diretórios são criados automaticamente durante a execução do sistema
- Os dados são persistidos entre sessões para manter a continuidade da "memória"
- Backups periódicos são recomendados para evitar perdas de dados 