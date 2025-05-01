"""
Script para testar cada função do Sistema de Memória Contínua e Reflexão Autônoma
"""

import asyncio
import os
import json
from app import PersonaSimples, AlmaSimples, processar_comandos, setup_environment

async def test_persona_functions():
    """Testa todas as funções da classe PersonaSimples"""
    print("\n=== Testando Funções da Persona ===")
    
    # Limpa dados anteriores
    if os.path.exists('data/memorias.json'):
        os.remove('data/memorias.json')
    
    persona = PersonaSimples()
    
    # Teste 1: Adicionar memória
    print("\n1. Testando adicionar_memoria:")
    id1 = persona.adicionar_memoria("Primeira memória de teste")
    id2 = persona.adicionar_memoria("Segunda memória de teste")
    print(f"✓ Memórias adicionadas com IDs: {id1}, {id2}")
    
    # Teste 2: Listar memórias
    print("\n2. Testando listar_memorias:")
    memorias = persona.listar_memorias(2)
    print(f"✓ Memórias listadas: {len(memorias)}")
    for m in memorias:
        print(f"  - ID {m['id']}: {m['conteudo']}")
    
    # Teste 3: Buscar memórias
    print("\n3. Testando buscar_memorias:")
    resultados = persona.buscar_memorias("teste")
    print(f"✓ Resultados da busca: {len(resultados)}")
    for r in resultados:
        print(f"  - ID {r['id']}: {r['conteudo']}")

async def test_alma_functions():
    """Testa todas as funções da classe AlmaSimples"""
    print("\n=== Testando Funções da Alma ===")
    
    persona = PersonaSimples()
    alma = AlmaSimples(persona)
    
    # Teste 1: Ciclo de reflexão
    print("\n1. Testando ciclo_reflexao:")
    resultado = await alma.ciclo_reflexao()
    print(f"✓ Resultado do ciclo: {resultado}")
    
    # Teste 2: Ciclo contínuo
    print("\n2. Testando ciclo_reflexao_continuo:")
    try:
        task = asyncio.create_task(alma.ciclo_reflexao_continuo(intervalo=1))
        await asyncio.sleep(2)
        task.cancel()
        print("✓ Ciclo contínuo iniciado e cancelado com sucesso")
    except asyncio.CancelledError:
        pass

async def test_command_processing():
    """Testa o processamento de comandos"""
    print("\n=== Testando Processamento de Comandos ===")
    
    persona = PersonaSimples()
    alma = AlmaSimples(persona)
    
    # Teste 1: Comando ajuda
    print("\n1. Testando comando 'ajuda':")
    resultado = await processar_comandos("ajuda", persona, alma)
    print("✓ Comando ajuda processado")
    
    # Teste 2: Comando armazenar
    print("\n2. Testando comando 'armazenar':")
    resultado = await processar_comandos("armazenar memória via comando", persona, alma)
    print(f"✓ {resultado}")
    
    # Teste 3: Comando listar
    print("\n3. Testando comando 'listar':")
    resultado = await processar_comandos("listar 2", persona, alma)
    print("✓ Listagem de memórias:")
    print(resultado)
    
    # Teste 4: Comando buscar
    print("\n4. Testando comando 'buscar':")
    resultado = await processar_comandos("buscar memória", persona, alma)
    print("✓ Resultados da busca:")
    print(resultado)
    
    # Teste 5: Comando refletir
    print("\n5. Testando comando 'refletir':")
    resultado = await processar_comandos("refletir", persona, alma)
    print(f"✓ {resultado}")

async def test_api_endpoints():
    """Testa os endpoints da API"""
    print("\n=== Testando Endpoints da API ===")
    
    import requests
    
    base_url = "http://localhost:5000"
    
    # Teste 1: Status da API
    print("\n1. Testando endpoint '/':")
    response = requests.get(f"{base_url}/")
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Resposta: {response.json()}")
    
    # Teste 2: Adicionar memória
    print("\n2. Testando POST '/api/memorias':")
    data = {"conteudo": "Teste via API"}
    response = requests.post(f"{base_url}/api/memorias", json=data)
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Resposta: {response.json()}")
    
    # Teste 3: Listar memórias
    print("\n3. Testando GET '/api/memorias':")
    response = requests.get(f"{base_url}/api/memorias")
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Resposta: {response.json()}")
    
    # Teste 4: Buscar memórias
    print("\n4. Testando GET '/api/memorias/buscar':")
    response = requests.get(f"{base_url}/api/memorias/buscar?termo=Teste")
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Resposta: {response.json()}")
    
    # Teste 5: Status do sistema
    print("\n5. Testando GET '/api/status':")
    response = requests.get(f"{base_url}/api/status")
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Resposta: {response.json()}")
    
    # Teste 6: Executar reflexão
    print("\n6. Testando POST '/api/reflexao':")
    response = requests.post(f"{base_url}/api/reflexao")
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Resposta: {response.json()}")

async def run_all_tests():
    """Executa todos os testes"""
    print("Iniciando testes do sistema...")
    
    # Configurar ambiente
    await setup_environment()
    
    # Testar funções da Persona
    await test_persona_functions()
    
    # Testar funções da Alma
    await test_alma_functions()
    
    # Testar processamento de comandos
    await test_command_processing()
    
    # Testar endpoints da API
    await test_api_endpoints()
    
    print("\nTodos os testes concluídos!")

if __name__ == "__main__":
    asyncio.run(run_all_tests()) 