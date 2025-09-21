import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIGURAÇÕES DA Z-API ---
ZAPI_SESSION_ID = "3E77B2035F45402782BF326225A8F6AC"
ZAPI_KEY = "6DB75F5621F7FF2F4A24B285"
ZAPI_CLIENT_TOKEN = "F30d06daf1a074b8991c7b3c37e0e873S"  # opcional

# --- URL RAW DO JSON NO GITHUB ---
URL_GRUPOS_JSON = "https://raw.githubusercontent.com/rafa5115/botzap/main/grupos.json"

def carregar_grupos_remoto():
    """Busca lista de grupos de um JSON hospedado no GitHub."""
    try:
        resp = requests.get(URL_GRUPOS_JSON, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("grupos", [])
        else:
            print(f"[ERRO] Não consegui buscar grupos. HTTP {resp.status_code}")
    except Exception as e:
        print("Erro ao buscar grupos remotos:", e)
    return []

# Carrega lista de grupos ao iniciar
LISTA_GRUPOS_ALVO = carregar_grupos_remoto()

# --- Rota para receber os Webhooks da Z-API ---
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        data = request.json
        print("Webhook recebido:", json.dumps(data, indent=2))

        # Atualiza lista sempre que chegar mensagem (dinâmico)
        grupos = carregar_grupos_remoto()

        if data.get('type') == 'ReceivedCallback' and data.get('fromMe') == False:
            group_id = data.get('phone')

            if group_id in grupos:
                print(f"Mensagem recebida do grupo alvo: {data.get('chatName')}. Enviando resposta...")
                send_automatic_reply_to_group(group_id)
            else:
                print("Mensagem recebida de grupo fora da lista. Ignorando.")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Erro ao processar o webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Função para enviar a mensagem de resposta ao grupo ---
def send_automatic_reply_to_group(group_id):
    """Envia uma mensagem de texto com imagem para o grupo especificado."""
    url = f"https://api.z-api.io/instances/{ZAPI_SESSION_ID}/token/{ZAPI_KEY}/send-image"

    message_content = """✅ GRUPO DE PUXADAS GRATIS ✅

ENTRE NO GRUPO NO WHATSAPP GRÁTIS E PUXE DADOS
https://entrar-agora.short.gy/grupo-puxadas-whatsapp

🚨 ATENÇÃO: 🚨
- GRUPO COM ACESSO LIMITADO
- BOT PUXANDO 24 HORAS
- RESPEITO COM TODOS OS MEMBROS 

🔥 LINK DO GRUPO NO WHATSAPP: 🔥
https://entrar-agora.short.gy/grupo-puxadas-whatsapp
"""

    payload = {
        "phone": group_id,
        "image": "https://i.pinimg.com/736x/19/e9/ce/19e9ce9bdd9d35955f3f6dded8edbb4d.jpg",
        "caption": message_content
    }

    # monta os headers dinamicamente
    headers = {"Content-Type": "application/json"}
    if ZAPI_CLIENT_TOKEN:  # só adiciona se tiver token configurado
        headers["client-token"] = ZAPI_CLIENT_TOKEN

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("Mensagem enviada com sucesso para o grupo!")
        else:
            print(f"Erro ao enviar resposta. Código: {response.status_code}")
            print("Detalhes:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao tentar enviar a resposta: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
