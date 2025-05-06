"""
Módulo Persona - Implementa a interface básica do sistema Persona.
"""

from persona.memoria import Memoria
from persona.processador_pensamento import ProcessadorPensamento

class Persona:
    def __init__(self):
        """Inicializa o sistema Persona."""
        self.memoria = Memoria()
        self.processador = ProcessadorPensamento(self.memoria)
        
    def _carregar_memorias(self):
        """
        Carrega as memórias do sistema.
        
        Returns:
            dict: O conteúdo do arquivo de memórias
        """
        return self.memoria._carregar_memorias()
        
    def adicionar_memoria(self, conteudo: str) -> str:
        """
        Adiciona uma nova memória ao sistema.
        
        Args:
            conteudo: Conteúdo da memória a ser armazenada
            
        Returns:
            ID da memória armazenada
        """
        return self.memoria.adicionar_memoria(conteudo)
    
    def listar_memorias(self, n: int = 5) -> list:
        """
        Lista as últimas n memórias.
        
        Args:
            n: Número de memórias a retornar
            
        Returns:
            Lista de memórias
        """
        return self.memoria.listar_memorias(n)
    
    def buscar_memorias(self, termo: str) -> list:
        """
        Busca memórias contendo o termo especificado.
        
        Args:
            termo: Termo a ser buscado
            
        Returns:
            Lista de memórias encontradas
        """
        return self.memoria.buscar_memorias(termo)
    
    def buscar_memorias_semanticamente(self, consulta: str) -> list:
        """
        Busca memórias semanticamente relacionadas à consulta.
        
        Args:
            consulta: Texto para busca semântica
            
        Returns:
            Lista de memórias semanticamente relacionadas
        """
        # Implementação básica - retorna busca textual normal
        return self.buscar_memorias(consulta) 