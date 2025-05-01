import asyncio
from core.persona import Persona
from core.alma import Alma

async def main():
    # Initialize Persona and Alma
    persona = Persona()
    alma = Alma(persona)
    
    # Add some test memories
    print("Adding initial memories...")
    persona.receber_informacao("Sistemas de memória contínua são fundamentais para o aprendizado profundo.")
    persona.receber_informacao("A cognição adaptativa permite evolução constante do conhecimento.")
    persona.receber_informacao("Reflexão e metacognição são processos que melhoram o aprendizado.")
    
    # Run reflection cycle
    print("\nExecuting Alma reflection cycle...")
    await alma.ciclo_reflexao()
    
    # Run a few more cycles
    print("\nRunning multiple reflection cycles...")
    for i in range(3):
        print(f"\n--- Cycle {i+1} ---")
        await alma.ciclo_reflexao()
        await asyncio.sleep(1)  # Short pause between cycles
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    asyncio.run(main()) 