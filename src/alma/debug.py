"""
Módulo de debug e monitoramento para o sistema de memória contínua.
Fornece funções para rastrear o estado do sistema e diagnosticar problemas.
"""
import logging
import time
import psutil
import os
import sys
from datetime import datetime

logger = logging.getLogger("memoria_continua.debug")

class MonitorSistema:
    """Classe para monitorar o estado do sistema e recursos."""
    
    def __init__(self):
        """Inicializa o monitor de sistema."""
        self.inicio = time.time()
        self.ultimo_check = time.time()
        self.metricas = {
            "memoria_uso": [],
            "cpu_uso": [],
            "tempo_execucao": 0
        }
    
    def coletar_metricas(self):
        """Coleta métricas sobre o estado atual do sistema."""
        process = psutil.Process(os.getpid())
        
        # Coleta uso de memória
        memoria_info = process.memory_info()
        self.metricas["memoria_uso"].append(memoria_info.rss / 1024 / 1024)  # Em MB
        
        # Coleta uso de CPU
        self.metricas["cpu_uso"].append(process.cpu_percent())
        
        # Atualiza tempo de execução
        self.metricas["tempo_execucao"] = time.time() - self.inicio
        
        # Atualiza timestamp do último check
        self.ultimo_check = time.time()
        
        return self.metricas
    
    def relatorio_atual(self):
        """Gera um relatório com as métricas atuais do sistema."""
        metricas = self.coletar_metricas()
        relatorio = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "memoria_mb": metricas["memoria_uso"][-1] if metricas["memoria_uso"] else 0,
            "cpu_percent": metricas["cpu_uso"][-1] if metricas["cpu_uso"] else 0,
            "tempo_execucao_s": round(metricas["tempo_execucao"], 2)
        }
        return relatorio

    def imprimir_relatorio(self):
        """Imprime um relatório formatado no console."""
        relatorio = self.relatorio_atual()
        print("\n=== Relatório de Sistema ===")
        print(f"Timestamp: {relatorio['timestamp']}")
        print(f"Memória utilizada: {relatorio['memoria_mb']:.2f} MB")
        print(f"CPU: {relatorio['cpu_percent']:.1f}%")
        print(f"Tempo de execução: {relatorio['tempo_execucao_s']} segundos")
        print("===========================\n")
        
        # Log também para o arquivo de log
        logger.info(f"Relatório - Memória: {relatorio['memoria_mb']:.2f}MB, "
                    f"CPU: {relatorio['cpu_percent']:.1f}%, "
                    f"Execução: {relatorio['tempo_execucao_s']}s")

def analisar_componente(componente, nivel=0):
    """Analisa um componente do sistema e retorna informações sobre seu estado.
    
    Args:
        componente: Objeto a ser analisado (ex: memória, processador, etc)
        nivel: Nível de detalhe da análise (0-básico, 1-detalhado, 2-completo)
        
    Returns:
        dict: Dicionário com informações sobre o componente
    """
    info = {"tipo": type(componente).__name__}
    
    if nivel == 0:
        # Análise básica - apenas tamanho e tipo
        if hasattr(componente, "__len__"):
            info["tamanho"] = len(componente)
    
    elif nivel >= 1:
        # Análise detalhada - atributos e métodos
        if hasattr(componente, "__dict__"):
            info["atributos"] = list(componente.__dict__.keys())
            
        if nivel >= 2:
            # Análise completa - valores
            if hasattr(componente, "__dict__"):
                for key, value in componente.__dict__.items():
                    if not callable(value) and not key.startswith("_"):
                        if hasattr(value, "__len__") and not isinstance(value, str):
                            info[key] = f"Lista/Dicionário com {len(value)} itens"
                        else:
                            info[key] = str(value)[:100] + ("..." if len(str(value)) > 100 else "")
    
    return info 