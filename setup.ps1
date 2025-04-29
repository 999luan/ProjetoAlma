# Script de configuração do ambiente para o Sistema de Memória Contínua
# Execução: .\setup.ps1

Write-Host "Configurando ambiente para o Sistema de Memória Contínua e Reflexão Autônoma..." -ForegroundColor Green

# Verifica se o Python está instalado
try {
    $pythonVersion = python --version
    Write-Host "Python encontrado: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "Python não encontrado. Por favor, instale o Python 3.8+ e tente novamente." -ForegroundColor Red
    exit
}

# Cria e ativa o ambiente virtual se não existir
if (-not (Test-Path .\venv)) {
    Write-Host "Criando ambiente virtual Python..." -ForegroundColor Yellow
    python -m venv venv
}

# Ativa o ambiente virtual
Write-Host "Ativando ambiente virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Instala as dependências
Write-Host "Instalando dependências..." -ForegroundColor Yellow
pip install -r requirements.txt

# Cria diretórios do sistema se não existirem
$coreDirs = @("core")
foreach ($dir in $coreDirs) {
    if (-not (Test-Path $dir)) {
        Write-Host "Criando diretório: $dir" -ForegroundColor Yellow
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
    }
}

# Verifica a estrutura de arquivos básica
$coreFiles = @(
    "core\persona.py",
    "core\alma.py",
    "core\utils.py",
    "core\config.py"
)

foreach ($file in $coreFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "Aviso: Arquivo $file não encontrado. Será criado durante a execução." -ForegroundColor Yellow
    }
}

Write-Host "`nAmbiente configurado com sucesso!" -ForegroundColor Green
Write-Host "`nPara iniciar o sistema, execute:" -ForegroundColor Cyan
Write-Host "   python main.py" -ForegroundColor White

# Mantém o ambiente virtual ativo
Write-Host "`nO ambiente virtual está ativo. Para desativá-lo, digite 'deactivate'." -ForegroundColor Yellow 