from typing import Dict, Any

class AgenteReflexao:
    def __init__(self):
        self.nome = "Agente de Reflexão"

    async def processar(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma informação através da reflexão."""
        if not info or 'info' not in info:
            return info

        # Adiciona uma reflexão básica à informação
        reflexao = f"Reflexão sobre: {info['info']}"
        
        # Cria uma nova versão da informação com a reflexão
        resultado = info.copy()
        resultado['reflexao'] = reflexao
        
        return resultado

    def __str__(self):
        return self.nome 