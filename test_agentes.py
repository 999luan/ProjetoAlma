"""
Testa os agentes especializados implementados na Fase 3.

Este script inicializa todos os agentes e executa uma série de testes
para verificar que estão funcionando corretamente.
"""

import asyncio
from core.persona import Persona
from core.alma import Alma

async def test_agentes():
    print("=== Teste de Agentes Especializados ===")
    
    # Inicializa os componentes
    persona = Persona()
    alma = Alma(persona)
    
    # Adiciona algumas memórias para teste
    memórias_teste = [
        "O aprendizado contínuo é essencial para inteligências artificiais avançadas.",
        "Sistemas cognitivos devem evoluir constantemente para se adaptar.",
        "A inconsistência de informações é um problema grave em sistemas de IA.",
        "O processamento emocional não é relevante para sistemas puramente lógicos.",
        "Padrões recorrentes podem indicar temas importantes para um sistema cognitivo."
    ]
    
    print("\nAdicionando memórias de teste...")
    for memoria in memórias_teste:
        persona.receber_informacao(memoria)
        await asyncio.sleep(0.5)
    
    # Testa cada agente
    print("\n--- Testando Agente de Reflexão ---")
    await alma.ativar_agente_reflexao()
    await asyncio.sleep(1)
    
    print("\n--- Testando Agente de Metacognição ---")
    await alma.ativar_agente_metacognicao()
    await asyncio.sleep(1)
    
    print("\n--- Testando Agente Emocional ---")
    await alma.ativar_agente_emocional()
    await asyncio.sleep(1)
    
    print("\n--- Testando Agente de Consistência ---")
    await alma.ativar_agente_consistencia()
    await asyncio.sleep(1)
    
    print("\n--- Testando Agente de Padrões ---")
    await alma.ativar_agente_padrao()
    await asyncio.sleep(1)
    
    # Verifica resultados
    print("\n=== Resultados ===")
    print(f"Reflexões realizadas: {alma.reflexoes_realizadas}")
    print(f"Metacognições realizadas: {alma.metacognicoes_realizadas}")
    print(f"Processamentos emocionais: {alma.agente_emocional.processamentos}")
    print(f"Inconsistências detectadas: {alma.agente_consistencia.inconsistencias_detectadas}")
    print(f"Resoluções aplicadas: {alma.agente_consistencia.resolucoes_aplicadas}")
    print(f"Padrões detectados: {len(alma.agente_padrao.padroes_detectados)}")
    
    if len(alma.agente_padrao.padroes_detectados) > 0:
        print("\nTemas detectados:")
        for padrao in alma.agente_padrao.padroes_detectados:
            print(f"  - {padrao['tema']}")
    
    print("\n=== Teste concluído com sucesso! ===")

if __name__ == "__main__":
    asyncio.run(test_agentes()) 