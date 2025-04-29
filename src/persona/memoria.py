"""
Módulo de memória responsável pelo armazenamento de informações
de curto e longo prazo.
"""

class Memoria:
    def __init__(self):
        """Inicializa as memórias de curto e longo prazo."""
        self.curto_prazo = []
        self.longo_prazo = []

    def armazenar_curto_prazo(self, informacao):
        """Armazena uma nova informação no curto prazo.
        
        Args:
            informacao (str): A informação a ser armazenada
        """
        self.curto_prazo.append({"info": informacao})
        print(f"Memória de curto prazo: '{informacao}' armazenada.")

    def transferir_para_longo_prazo(self):
        """Move informações do curto prazo para o longo prazo."""
        if not self.curto_prazo:
            print("Memória de curto prazo vazia. Nada para transferir.")
            return
        
        self.longo_prazo.extend(self.curto_prazo)
        quantidade = len(self.curto_prazo)
        self.curto_prazo.clear()
        print(f"{quantidade} memórias transferidas para o longo prazo.")
    
    def buscar_memoria(self, tipo="longo"):
        """Busca informações da memória.
        
        Args:
            tipo (str): Tipo de memória para buscar ('curto' ou 'longo')
            
        Returns:
            list: Lista de memórias do tipo solicitado
        """
        if tipo == "curto":
            return self.curto_prazo
        else:
            return self.longo_prazo 