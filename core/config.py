"""
Configurações para o Sistema de Memória Contínua.

Este módulo contém as configurações globais do sistema.
"""

# Configurações da Persona
PERSONA_CONFIG = {
    # Caminho para o arquivo de memórias
    "memoria_path": "core/memoria.json",
    
    # Limite de memórias de curto prazo antes de transferir para longo prazo
    "limite_memoria_curto_prazo": 5,
    
    # Limiar de similaridade para considerar memórias relacionadas (0-1)
    "limiar_similaridade": 0.3,
    
    # Número máximo de memórias a considerar para síntese
    "max_memorias_sintese": 3
}

# Configurações da Alma
ALMA_CONFIG = {
    # Intervalo entre ciclos de reflexão (em segundos)
    "intervalo_reflexao": 30,
    
    # Probabilidade de escolher reflexão vs metacognição
    "probabilidade_reflexao": 0.7,
    
    # Limite de qualidade para memórias que precisam revisão
    "limiar_qualidade_revisao": 4,
    
    # Máximo de ciclos de reflexão por sessão
    "max_ciclos_reflexao": 100
}

# Configurações de log
LOG_CONFIG = {
    # Nível de log
    "nivel": "INFO",
    
    # Formato do log
    "formato": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    
    # Caminho para o arquivo de log
    "arquivo": "sistema.log",
    
    # Se deve mostrar logs no console
    "console": True
}

# Stopwords - palavras comuns a ignorar na análise
STOPWORDS = {
    'a', 'e', 'o', 'as', 'os', 'um', 'uma', 'uns', 'umas', 'de', 'da', 'do', 
    'das', 'dos', 'em', 'no', 'na', 'nos', 'nas', 'para', 'por', 'que', 'com',
    'se', 'ao', 'aos', 'à', 'às', 'pelo', 'pela', 'pelos', 'pelas', 'é'
} 