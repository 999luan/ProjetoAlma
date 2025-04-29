"""
Testa o sistema de aprendizado implementado na Fase 4.

Este script inicializa os componentes do sistema e realiza um teste
acelerado do ciclo de aprendizado para verificar seu funcionamento.
"""

import asyncio
from core.persona import Persona
from core.alma import Alma
from core.learning import GerenciadorAprendizado

async def test_learning():
    print("=== Teste de Aprendizado Contínuo ===")
    
    # Inicializa os componentes
    persona = Persona()
    alma = Alma(persona)
    gerenciador = GerenciadorAprendizado(persona, alma)
    
    # Configura referência circular
    alma.configurar_gerenciador_aprendizado(gerenciador)
    
    # Adiciona memórias diversas para teste
    memórias_teste = [
        "O aprendizado contínuo permite que sistemas evoluam ao longo do tempo.",
        "Sistemas de IA precisam se adaptar a novas informações constantemente.",
        "A metacognição é essencial para sistemas que se automonitoram.",
        "As emoções desempenham um papel importante na tomada de decisões.",
        "Padrões recorrentes podem indicar conceitos fundamentais em um domínio.",
        "A detecção de inconsistências lógicas melhora a qualidade do conhecimento.",
        "Sistemas que não aprendem se tornam obsoletos rapidamente.",
        "O refinamento constante de ideias leva a insights mais profundos.",
        "A síntese de conceitos diferentes frequentemente gera inovação.",
        "Sistemas inteligentes devem questionar suas próprias conclusões."
    ]
    
    print("\nAdicionando memórias diversificadas...")
    for memoria in memórias_teste:
        persona.receber_informacao(memoria)
        await asyncio.sleep(0.2)
    
    # Executa alguns ciclos de reflexão para gerar dados de agentes
    print("\nExecutando ciclos de reflexão para gerar dados...")
    for i in range(5):
        print(f"\n--- Ciclo de reflexão {i+1} ---")
        await alma.ciclo_de_reflexao()
        await asyncio.sleep(0.5)
    
    # Testa o processo de otimização
    print("\n=== Testando otimização do processo de pensamento ===")
    await gerenciador.otimizar_processo()
    
    # Verifica seleção de agentes após otimização
    print("\n=== Testando seleção de agentes otimizada ===")
    selecionados = {}
    for _ in range(20):
        agente = gerenciador.selecionar_agente()
        selecionados[agente] = selecionados.get(agente, 0) + 1
    
    print("Distribuição de seleção de agentes após otimização:")
    for agente, contagem in selecionados.items():
        print(f"  {agente}: {contagem} ({contagem/20:.0%})")
    
    # Testa estratégias de aprendizado específicas
    print("\n=== Testando estratégias de aprendizado ===")
    await gerenciador._aplicar_estrategias_aprendizado()
    
    # Verificação final
    dados = persona._carregar_memorias()
    print(f"\nTotal de memórias após teste: {len(dados['memorias'])}")
    
    # Conta tipos de memória
    origens = {}
    for memoria in dados["memorias"]:
        origem = memoria.get("origem", "desconhecida")
        origens[origem] = origens.get(origem, 0) + 1
    
    print("\nTipos de memória:")
    for origem, contagem in origens.items():
        print(f"  {origem}: {contagem}")
    
    print("\n=== Teste concluído com sucesso! ===")

if __name__ == "__main__":
    asyncio.run(test_learning()) 