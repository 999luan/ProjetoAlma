"""
Módulo responsável pelo processamento de pensamentos baseados 
na memória armazenada.
"""
import random

class ProcessadorPensamento:
    def __init__(self, memoria):
        """Inicializa o processador com uma referência à memória.
        
        Args:
            memoria (Memoria): Instância da classe Memoria
        """
        self.memoria = memoria

    def gerar_pensamento(self):
        """Gera um pensamento aleatório baseado na memória de longo prazo.
        
        Returns:
            str: O pensamento gerado ou None se não houver memória
        """
        if self.memoria.longo_prazo:
            escolhido = random.choice(self.memoria.longo_prazo)
            return f"Pensando sobre: {escolhido['info']}"
        else:
            print("Memória de longo prazo vazia. Não é possível gerar pensamentos.")
            return None
    
    def gerar_resposta(self, info):
        """Gera uma resposta simples baseada na entrada recebida.
        
        Args:
            info (str): Informação recebida
            
        Returns:
            str: Resposta gerada
        """
        return f"Resposta ao estímulo: '{info}'"
        
    def gerar_pensamento_rapido(self):
        """Pensa de forma espontânea baseado na memória recente.
        
        Returns:
            str: Pensamento rápido ou None se não houver memória
        """
        memoria_curto = self.memoria.buscar_memoria("curto")
        if memoria_curto:
            escolhido = random.choice(memoria_curto)
            return f"Pensamento rápido sobre: {escolhido['info']}"
        else:
            return None 