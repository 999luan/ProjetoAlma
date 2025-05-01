# Sistema de Memória Contínua e Reflexão Autônoma

## Visão Geral
O Sistema de Memória Contínua e Reflexão Autônoma é uma aplicação que implementa um mecanismo de armazenamento e processamento de memórias com capacidade de reflexão autônoma. O sistema é composto por dois componentes principais: a Persona (gerenciadora de memórias) e a Alma (processadora de reflexões).

## Arquitetura

### Componentes Principais

#### 1. Persona (PersonaSimples)
- **Responsabilidade**: Gerenciamento de memórias
- **Funcionalidades**:
  - Armazenamento de memórias
  - Listagem de memórias
  - Busca de memórias
  - Persistência de dados em JSON

#### 2. Alma (AlmaSimples)
- **Responsabilidade**: Processamento e reflexão
- **Funcionalidades**:
  - Ciclo de reflexão
  - Ciclo contínuo de reflexão
  - Geração de insights
  - Processamento de memórias não processadas

### API REST

#### Endpoints Disponíveis

1. **Status do Sistema**
   - `GET /`
   - Retorna o status do sistema e informações básicas

2. **Gerenciamento de Memórias**
   - `GET /api/memorias`
   - `POST /api/memorias`
   - `GET /api/memorias/buscar`

3. **Reflexão**
   - `POST /api/reflexao`
   - `GET /api/status`

## Comandos Disponíveis

### Interface de Comandos
- `ajuda`: Lista todos os comandos disponíveis
- `armazenar [mensagem]`: Armazena uma nova memória
- `listar [n]`: Lista as últimas n memórias
- `buscar [termo]`: Busca memórias contendo o termo
- `refletir`: Executa um ciclo de reflexão
- `sair`: Encerra o programa

## Estrutura de Dados

### Memória
```json
{
    "id": 1,
    "conteudo": "texto da memória",
    "timestamp": "2025-04-30T21:26:01.962",
    "processada": false
}
```

### Insight
```json
{
    "id": 1,
    "descricao": "descrição do insight",
    "timestamp": "2025-04-30T21:26:01.962"
}
```

## Configuração do Ambiente

### Requisitos
- Python 3.8+
- Flask
- Requests (para testes)

### Diretórios
- `data/`: Armazena as memórias em JSON
- `logs/`: Armazena logs do sistema

### Instalação
```bash
pip install flask requests
```

## Execução

### Iniciar o Servidor
```bash
python app.py
```

### Executar Testes
```bash
python test_functions.py
```

## Logs e Monitoramento

### Níveis de Log
- INFO: Operações normais
- WARNING: Avisos importantes
- ERROR: Erros críticos

### Arquivos de Log
- `api.log`: Logs da API
- `sistema.log`: Logs do sistema

## Ciclos de Processamento

### Ciclo de Reflexão
1. Identifica memórias não processadas
2. Processa cada memória
3. Gera insights quando necessário
4. Atualiza o estado das memórias

### Ciclo Contínuo
- Executa ciclos de reflexão em intervalos regulares
- Intervalo padrão: 60 segundos
- Pode ser ajustado via parâmetro

## Segurança

### Considerações
- Servidor de desenvolvimento não deve ser usado em produção
- Implementar autenticação para endpoints sensíveis
- Validar entrada de dados
- Sanitizar saída de dados

## Limitações Atuais

1. **Persistência**
   - Armazenamento simples em JSON
   - Sem backup automático

2. **Processamento**
   - Reflexão básica
   - Sem análise semântica avançada

3. **Escalabilidade**
   - Processamento síncrono
   - Sem distribuição de carga

## Próximos Passos

1. **Melhorias Planejadas**
   - Implementar banco de dados
   - Adicionar análise semântica
   - Implementar autenticação
   - Adicionar backup automático

2. **Recursos Futuros**
   - Interface web
   - API GraphQL
   - Processamento distribuído
   - Análise de sentimentos