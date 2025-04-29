"""
Utilitários para o Sistema de Memória Contínua.

Este módulo contém funções auxiliares usadas pelos módulos Persona e Alma.
"""

import re
import time
import random
from datetime import datetime

def calcular_similaridade_texto(texto1, texto2):
    """Calcula a similaridade entre dois textos baseado em palavras compartilhadas.
    
    Args:
        texto1 (str): Primeiro texto
        texto2 (str): Segundo texto
        
    Returns:
        float: Índice de similaridade entre 0 e 1
    """
    if not texto1 or not texto2:
        return 0
    
    # Normaliza e divide em palavras
    palavras1 = set(normalizar_texto(texto1).split())
    palavras2 = set(normalizar_texto(texto2).split())
    
    # Remove palavras muito comuns (stopwords simples)
    stopwords = {'a', 'e', 'o', 'as', 'os', 'um', 'uma', 'uns', 'umas', 'de', 'da', 'do', 
                'das', 'dos', 'em', 'no', 'na', 'nos', 'nas', 'para', 'por', 'que', 'com'}
    
    palavras1 = palavras1 - stopwords
    palavras2 = palavras2 - stopwords
    
    # Calcula similaridade por interseção/união (coeficiente de Jaccard)
    if not palavras1 or not palavras2:
        return 0
    
    intersecao = palavras1.intersection(palavras2)
    uniao = palavras1.union(palavras2)
    
    return len(intersecao) / len(uniao)

def normalizar_texto(texto):
    """Normaliza o texto para comparação (minúsculas, sem pontuação).
    
    Args:
        texto (str): Texto para normalizar
        
    Returns:
        str: Texto normalizado
    """
    if not texto:
        return ""
    
    # Converte para minúsculas
    texto = texto.lower()
    
    # Remove pontuação
    texto = re.sub(r'[^\w\s]', '', texto)
    
    # Remove espaços extras
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

def gerar_timestamp():
    """Gera um timestamp formatado.
    
    Returns:
        str: Timestamp no formato ISO
    """
    return datetime.now().isoformat()

def calcular_tempo_decorrido(timestamp_anterior):
    """Calcula o tempo decorrido desde um timestamp anterior.
    
    Args:
        timestamp_anterior (str): Timestamp ISO anterior
        
    Returns:
        float: Tempo decorrido em segundos
    """
    try:
        timestamp_dt = datetime.fromisoformat(timestamp_anterior)
        agora = datetime.now()
        delta = agora - timestamp_dt
        return delta.total_seconds()
    except (ValueError, TypeError):
        return 0

def escolher_aleatoriamente(lista, n=1):
    """Escolhe n elementos aleatórios de uma lista.
    
    Args:
        lista (list): Lista de elementos
        n (int): Número de elementos a escolher
        
    Returns:
        list: Lista com os elementos escolhidos
    """
    if not lista or n <= 0:
        return []
    
    n = min(n, len(lista))
    return random.sample(lista, n)

def combinar_textos(textos, modo="concatenar"):
    """Combina múltiplos textos em um único texto.
    
    Args:
        textos (list): Lista de textos para combinar
        modo (str): Modo de combinação ("concatenar" ou "intercalar")
        
    Returns:
        str: Texto combinado
    """
    if not textos:
        return ""
    
    if len(textos) == 1:
        return textos[0]
    
    if modo == "concatenar":
        return " ".join(textos)
    elif modo == "intercalar":
        # Divide cada texto em frases
        todos_segmentos = []
        for texto in textos:
            segmentos = re.split(r'([.!?]+)', texto)
            partes = []
            for i in range(0, len(segmentos)-1, 2):
                partes.append(segmentos[i] + segmentos[i+1])
            if len(segmentos) % 2 == 1:
                partes.append(segmentos[-1])
            todos_segmentos.extend(partes)
        
        # Embaralha os segmentos e reconstrói
        random.shuffle(todos_segmentos)
        return " ".join(todos_segmentos)
    else:
        return " ".join(textos) 