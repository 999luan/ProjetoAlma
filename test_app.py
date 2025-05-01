"""
Script de teste para o Sistema de Memória Contínua e Reflexão Autônoma
"""

import asyncio
import pytest
import os
import json
from app import PersonaSimples, AlmaSimples, processar_comandos, setup_environment

def limpar_dados():
    """Limpa os dados de teste."""
    if os.path.exists('data/memorias.json'):
        os.remove('data/memorias.json')

async def test_setup_environment():
    """Testa a configuração do ambiente."""
    await setup_environment()
    # Verifica se os diretórios foram criados
    assert os.path.exists('data')
    assert os.path.exists('logs')

async def test_persona_basic_operations():
    """Testa operações básicas da Persona."""
    limpar_dados()
    persona = PersonaSimples()
    
    # Testa adicionar memória
    id1 = persona.adicionar_memoria("Teste de memória 1")
    id2 = persona.adicionar_memoria("Teste de memória 2")
    assert id1 == 1
    assert id2 == 2
    
    # Testa listar memórias
    memorias = persona.listar_memorias(2)
    assert len(memorias) == 2
    assert memorias[0]["id"] == 2
    assert memorias[1]["id"] == 1
    
    # Testa buscar memórias
    resultados = persona.buscar_memorias("Teste")
    assert len(resultados) == 2
    
    # Testa buscar memória específica
    resultados = persona.buscar_memorias("memória 1")
    assert len(resultados) == 1
    assert resultados[0]["id"] == 1

async def test_alma_operations():
    """Testa operações da Alma."""
    limpar_dados()
    persona = PersonaSimples()
    alma = AlmaSimples(persona)
    
    # Adiciona algumas memórias para processar
    persona.adicionar_memoria("Memória para reflexão 1")
    persona.adicionar_memoria("Memória para reflexão 2")
    
    # Testa ciclo de reflexão
    resultado = await alma.ciclo_reflexao()
    assert "Ciclo de reflexão" in resultado
    
    # Testa ciclo contínuo
    try:
        # Inicia o ciclo e aguarda um pouco
        task = asyncio.create_task(alma.ciclo_reflexao_continuo(intervalo=1))
        await asyncio.sleep(2)
        task.cancel()
    except asyncio.CancelledError:
        pass

async def test_processar_comandos():
    """Testa o processamento de comandos."""
    limpar_dados()
    persona = PersonaSimples()
    alma = AlmaSimples(persona)
    
    # Testa comando ajuda
    resultado = await processar_comandos("ajuda", persona, alma)
    assert "Comandos disponíveis" in resultado
    
    # Testa comando armazenar
    resultado = await processar_comandos("armazenar teste de comando", persona, alma)
    assert "Memória armazenada com ID" in resultado
    
    # Testa comando listar
    resultado = await processar_comandos("listar 2", persona, alma)
    assert "ID" in resultado
    
    # Testa comando buscar
    resultado = await processar_comandos("buscar teste", persona, alma)
    assert "ID" in resultado
    
    # Testa comando refletir
    resultado = await processar_comandos("refletir", persona, alma)
    assert "Ciclo de reflexão concluído" in resultado
    
    # Testa comando inválido
    resultado = await processar_comandos("comando_invalido", persona, alma)
    assert "não reconhecido" in resultado

async def run_all_tests():
    """Executa todos os testes."""
    print("Iniciando testes...")
    
    print("\nTestando setup_environment...")
    await test_setup_environment()
    print("✓ setup_environment OK")
    
    print("\nTestando operações básicas da Persona...")
    await test_persona_basic_operations()
    print("✓ Operações da Persona OK")
    
    print("\nTestando operações da Alma...")
    await test_alma_operations()
    print("✓ Operações da Alma OK")
    
    print("\nTestando processamento de comandos...")
    await test_processar_comandos()
    print("✓ Processamento de comandos OK")
    
    print("\nTodos os testes concluídos com sucesso!")

if __name__ == "__main__":
    asyncio.run(run_all_tests()) 