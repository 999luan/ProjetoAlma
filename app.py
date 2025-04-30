"""
API do Sistema de Memória Contínua e Reflexão Autônoma
Versão simplificada sem dependências avançadas
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from flask import Flask, request, jsonify

# Configurar app
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Sistema simulado simplificado
class PersonaSimples:
    def __init__(self):
        self.memorias = []
        self.contador_id = 0
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        self._carregar_memorias()
        logger.info("Persona inicializada")
    
    def _carregar_memorias(self):
        try:
            arquivo_memoria = os.path.join(self.data_dir, "memorias.json")
            if os.path.exists(arquivo_memoria):
                with open(arquivo_memoria, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.memorias = dados.get("memorias", [])
                    self.contador_id = dados.get("contador", 0)
                    logger.info(f"Carregadas {len(self.memorias)} memórias")
        except Exception as e:
            logger.error(f"Erro ao carregar memórias: {e}")
    
    def _salvar_memorias(self):
        try:
            arquivo_memoria = os.path.join(self.data_dir, "memorias.json")
            with open(arquivo_memoria, 'w', encoding='utf-8') as f:
                json.dump({
                    "memorias": self.memorias,
                    "contador": self.contador_id
                }, f, ensure_ascii=False, indent=2)
            logger.info("Memórias salvas com sucesso")
        except Exception as e:
            logger.error(f"Erro ao salvar memórias: {e}")
    
    def adicionar_memoria(self, conteudo):
        self.contador_id += 1
        nova_memoria = {
            "id": self.contador_id,
            "conteudo": conteudo,
            "timestamp": datetime.now().isoformat(),
            "processada": False
        }
        self.memorias.append(nova_memoria)
        self._salvar_memorias()
        logger.info(f"Memória adicionada: ID {self.contador_id}")
        return self.contador_id
    
    def listar_memorias(self, limite=5):
        return sorted(self.memorias, key=lambda m: m["id"], reverse=True)[:limite]
    
    def buscar_memorias(self, termo):
        return [m for m in self.memorias if termo.lower() in m["conteudo"].lower()]

class AlmaSimples:
    def __init__(self, persona):
        self.persona = persona
        self.ciclos_reflexao = 0
        self.insights = []
        logger.info("Alma inicializada")
    
    async def ciclo_reflexao(self):
        """Executa um ciclo de reflexão."""
        return await self.ciclo_de_reflexao()
    
    async def ciclo_reflexao_continuo(self, intervalo=60):
        """Inicia o ciclo contínuo de reflexão."""
        await self.iniciar_ciclo_reflexao(intervalo=intervalo)

# Inicializar componentes do sistema
persona = None
alma = None

async def setup_environment():
    """Configura o ambiente de execução, garantindo que diretórios necessários existam."""
    diretorios = ['data', 'logs']
    
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)
    
    logger.info("Ambiente configurado com sucesso")

async def processar_comandos(comando, persona, alma):
    """Processa comandos do usuário."""
    partes = comando.lower().split()
    
    if partes[0] == "ajuda":
        return """
        Comandos disponíveis:
        - ajuda: Mostra esta mensagem
        - armazenar [mensagem]: Armazena uma nova memória
        - listar [n]: Lista as últimas n memórias (padrão: 5)
        - buscar [termo]: Busca memórias contendo o termo
        - refletir: Executa um ciclo de reflexão
        - sair: Encerra o programa
        """
    
    elif partes[0] == "armazenar" and len(partes) > 1:
        conteudo = " ".join(partes[1:])
        resultado = persona.adicionar_memoria(conteudo)
        return f"Memória armazenada com ID: {resultado}"
    
    elif partes[0] == "listar":
        n = 5  # padrão
        if len(partes) > 1 and partes[1].isdigit():
            n = int(partes[1])
        
        memorias = persona.listar_memorias(n)
        resultado = ""
        for memoria in memorias:
            resultado += f"ID {memoria['id']}: {memoria['conteudo']}\n"
        
        return resultado if resultado else "Nenhuma memória encontrada."
    
    elif partes[0] == "buscar" and len(partes) > 1:
        termo = " ".join(partes[1:])
        memorias = persona.buscar_memorias(termo)
        
        resultado = ""
        for memoria in memorias:
            resultado += f"ID {memoria['id']}: {memoria['conteudo']}\n"
        
        return resultado if resultado else f"Nenhuma memória encontrada com o termo '{termo}'."
    
    elif partes[0] == "refletir":
        resultado = await alma.ciclo_reflexao()
        return "Ciclo de reflexão concluído."
    
    elif partes[0] == "sair":
        return "sair"
    
    else:
        return "Comando não reconhecido. Digite 'ajuda' para ver os comandos disponíveis."

def inicializar_sistema():
    global persona, alma
    # Configurar ambiente de forma síncrona
    for diretorio in ['data', 'logs']:
        os.makedirs(diretorio, exist_ok=True)
    
    persona = PersonaSimples()
    alma = AlmaSimples(persona)
    
    # Iniciar tarefas em background
    iniciar_tarefas_background()
    
    return True

def iniciar_tarefas_background():
    """Inicia as tarefas em background em um novo thread para não bloquear a API"""
    import threading
    
    def run_background_tasks():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Criar e executar tarefas
        task = loop.create_task(alma.iniciar_ciclo_reflexao(intervalo=60))
        
        # Executar o loop
        try:
            loop.run_forever()
        finally:
            # Cancelar tarefas e fechar o loop
            task.cancel()
            loop.run_until_complete(asyncio.gather(task, return_exceptions=True))
            loop.close()
    
    # Iniciar thread
    thread = threading.Thread(target=run_background_tasks, daemon=True)
    thread.start()

# Rota raiz para verificar se a API está online
@app.route('/')
def index():
    return jsonify({"status": "online", "sistema": "Sistema de Memória Contínua e Reflexão Autônoma (Simplificado)"})

# API - Obter todas as memórias
@app.route('/api/memorias', methods=['GET'])
def obter_memorias():
    if not persona:
        return jsonify({"erro": "Sistema não inicializado"}), 500
    
    limit = request.args.get('limit', default=10, type=int)
    memorias = persona.listar_memorias(limit)
    return jsonify(memorias)

# API - Adicionar nova memória
@app.route('/api/memorias', methods=['POST'])
def adicionar_memoria():
    if not persona:
        return jsonify({"erro": "Sistema não inicializado"}), 500
    
    data = request.get_json()
    if not data or 'conteudo' not in data:
        return jsonify({"erro": "Conteúdo da memória não fornecido"}), 400
    
    resultado = persona.adicionar_memoria(data['conteudo'])
    return jsonify({"sucesso": True, "id": resultado})

# API - Buscar memórias
@app.route('/api/memorias/buscar', methods=['GET'])
def buscar_memorias():
    if not persona:
        return jsonify({"erro": "Sistema não inicializado"}), 500
    
    termo = request.args.get('termo', '')
    if not termo:
        return jsonify({"erro": "Termo de busca não fornecido"}), 400
    
    memorias = persona.buscar_memorias(termo)
    return jsonify(memorias)

# API - Processar comando
@app.route('/api/comando', methods=['POST'])
def processar_comando():
    if not persona or not alma:
        return jsonify({"erro": "Sistema não inicializado"}), 500
    
    data = request.get_json()
    if not data or 'comando' not in data:
        return jsonify({"erro": "Comando não fornecido"}), 400
    
    comando = data['comando']
    try:
        # Executar o processamento do comando de forma assíncrona
        resultado = asyncio.run(processar_comandos(comando, persona, alma))
        return jsonify({"resultado": resultado})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# API - Executar ciclo de reflexão manual
@app.route('/api/reflexao', methods=['POST'])
def executar_reflexao():
    if not alma:
        return jsonify({"erro": "Sistema não inicializado"}), 500
    
    try:
        resultado = asyncio.run(alma.ciclo_reflexao())
        return jsonify({"sucesso": True, "mensagem": resultado})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# API - Obter status do sistema
@app.route('/api/status', methods=['GET'])
def obter_status():
    if not persona or not alma:
        return jsonify({"erro": "Sistema não inicializado"}), 500
    
    return jsonify({
        "memorias_total": len(persona.memorias),
        "memoria_ultima_id": persona.contador_id,
        "ciclos_reflexao": alma.ciclos_reflexao,
        "insights_totais": len(alma.insights)
    })

if __name__ == '__main__':
    inicializar_sistema()
    app.run(debug=True, port=5000) 