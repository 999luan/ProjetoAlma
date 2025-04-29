import asyncio
import signal
import sys
from core.persona import Persona
from core.alma import Alma

# Global variables to manage the task
alma_task = None
shutdown_event = None

async def run_continuous_cycle(intervalo=60):
    """Run the continuous reflection cycle with the specified interval."""
    persona = Persona()
    alma = Alma(persona)
    
    print(f"Starting continuous reflection cycle every {intervalo} seconds...")
    print("Press Ctrl+C to stop the program")
    
    try:
        await alma.iniciar_ciclo_reflexao(intervalo=intervalo)
    except asyncio.CancelledError:
        print("Reflection cycle was cancelled, shutting down...")

def signal_handler(sig, frame):
    """Handle Ctrl+C to gracefully shut down."""
    print("\nShutting down the reflection cycle...")
    if alma_task and not alma_task.done():
        alma_task.cancel()

async def main():
    global alma_task
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Get the interval from command line if specified
    intervalo = 60  # Default interval
    if len(sys.argv) > 1:
        try:
            intervalo = int(sys.argv[1])
        except ValueError:
            print(f"Invalid interval '{sys.argv[1]}', using default of 60 seconds")
    
    # Start the continuous cycle
    alma_task = asyncio.create_task(run_continuous_cycle(intervalo))
    
    # Wait for the task to complete (after cancellation)
    await alma_task

if __name__ == "__main__":
    asyncio.run(main()) 