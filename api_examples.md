# Exemplos de Uso da API

Este documento contém exemplos de uso da API do Sistema de Memória Contínua utilizando PowerShell e cURL.

## PowerShell

### Verificar o Status do Sistema

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/status" -Method GET -ContentType "application/json"
```

### Adicionar uma Nova Memória

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/memorias" -Method POST -Body '{"conteudo": "Esta é uma memória de teste."}' -ContentType "application/json"
```

### Listar todas as Memórias

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/memorias" -Method GET -ContentType "application/json"
```

### Buscar Memórias por Termo

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/memorias/buscar?termo=teste" -Method GET -ContentType "application/json"
```

### Executar um Ciclo de Reflexão

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/reflexao" -Method POST -ContentType "application/json"
```

### Processar Comandos

```powershell
# Ajuda
Invoke-RestMethod -Uri "http://localhost:5000/api/comando" -Method POST -Body '{"comando": "ajuda"}' -ContentType "application/json"

# Listar memórias
Invoke-RestMethod -Uri "http://localhost:5000/api/comando" -Method POST -Body '{"comando": "listar"}' -ContentType "application/json"

# Armazenar uma nova memória
Invoke-RestMethod -Uri "http://localhost:5000/api/comando" -Method POST -Body '{"comando": "armazenar Esta é uma memória criada via comando"}' -ContentType "application/json"

# Buscar memórias
Invoke-RestMethod -Uri "http://localhost:5000/api/comando" -Method POST -Body '{"comando": "buscar memória"}' -ContentType "application/json"
```

## cURL (Linux/Mac/Windows com Git Bash)

### Verificar o Status do Sistema

```bash
curl -X GET "http://localhost:5000/api/status" -H "Content-Type: application/json"
```

### Adicionar uma Nova Memória

```bash
curl -X POST "http://localhost:5000/api/memorias" -H "Content-Type: application/json" -d '{"conteudo": "Esta é uma memória de teste."}'
```

### Listar todas as Memórias

```bash
curl -X GET "http://localhost:5000/api/memorias" -H "Content-Type: application/json"
```

### Buscar Memórias por Termo

```bash
curl -X GET "http://localhost:5000/api/memorias/buscar?termo=teste" -H "Content-Type: application/json"
```

### Executar um Ciclo de Reflexão

```bash
curl -X POST "http://localhost:5000/api/reflexao" -H "Content-Type: application/json"
```

### Processar Comandos

```bash
# Ajuda
curl -X POST "http://localhost:5000/api/comando" -H "Content-Type: application/json" -d '{"comando": "ajuda"}'

# Listar memórias
curl -X POST "http://localhost:5000/api/comando" -H "Content-Type: application/json" -d '{"comando": "listar"}'

# Armazenar uma nova memória
curl -X POST "http://localhost:5000/api/comando" -H "Content-Type: application/json" -d '{"comando": "armazenar Esta é uma memória criada via comando"}'

# Buscar memórias
curl -X POST "http://localhost:5000/api/comando" -H "Content-Type: application/json" -d '{"comando": "buscar memória"}'
``` 