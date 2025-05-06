import random

class ProcessadorPensamento:
    def __init__(self, memoria):
        self.memoria = memoria

    def gerar_resposta(self, info: str) -> str:
        """Gera uma resposta simples baseada na memória recente."""
        memorias = self.memoria.buscar_memoria('curto_prazo')
        if memorias:
            # Escolhe uma memória recente aleatoriamente
            escolhida = random.choice(memorias)
            return f"Baseado em memórias recentes: {escolhida['info']}"
        return "Ainda não tenho memórias suficientes para responder."

    def gerar_pensamento_rapido(self) -> str:
        """Pensa de forma espontânea durante o recebimento de novas informações."""
        memorias = self.memoria.buscar_memoria('longo_prazo')
        if memorias:
            escolhida = random.choice(memorias)
            return f"Pensamento espontâneo: {escolhida['info']}"
        return None

    def gerar_sintese(self) -> str:
        """Combina duas memórias para criar um novo pensamento."""
        memorias = self.memoria.buscar_memoria('longo_prazo')
        if len(memorias) >= 2:
            escolhidas = random.sample(memorias, 2)
            nova_ideia = f"Conexão entre '{escolhidas[0]['info']}' e '{escolhidas[1]['info']}'"
            return nova_ideia
        return None 