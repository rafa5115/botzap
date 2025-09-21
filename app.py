import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIGURAÇÕES DA Z-API ---
# Substitua pelos seus dados
ZAPI_SESSION_ID = "3E77B2035F45402782BF326225A8F6AC" 
ZAPI_KEY = "6DB75F5621F7FF2F4A24B285"
ZAPI_CLIENT_TOKEN = "F30d06daf1a0749b8991c7b3c37e0e873S"

# --- LISTA DE GRUPOS PARA INSPECIONAR ---
# Adicione aqui os IDs dos grupos. Você pode obter o ID do grupo no log da Z-API,
# no campo "phone" de uma mensagem vinda do grupo.
LISTA_GRUPOS_ALVO = [
    "554299643515-1487078215",
    "5517992430766-1488577373",
    "120363023658550638-group",
    "120363041476355433-group",
    "120363025413377651-group",
    "558791464546-1505848145",
    "557491275840-1496505309",
    "5517992430766-1488577579",
    "5517992430766-1488635463",
    "558894961134-1433431681",
    "5527997091137-1459720332",
    "556899269715-1494639838",
    "557599947878-1485986234",
    "5519988110438-1505739833",
    "5519982222829-1504468047",
    "5519987392060-1494342988",
    "555499469372-1500336205",
    "557388781780-1491689267",
    "555198361866-1505749326",
    "555192333601-1507723773",
    "5511940026075-1508255644",
    "555497085776-1499284001",
    "553491538774-1498170762",
    "5524992465572-1497485830",
    "559684159028-1494809937",
    "559492378468-1492629620",
    "555492440708-1455096858",
    "557598225245-1436661941"
]

# --- Rota para receber os Webhooks da Z-API ---
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        data = request.json
        print("Webhook recebido:", json.dumps(data, indent=2))

        # Verifica se o evento é uma mensagem recebida e não foi enviada pelo próprio bot
        if data.get('type') == 'ReceivedCallback' and data.get('fromMe') == False:
            
            # Pega o ID do grupo (o campo 'phone' para grupos)
            group_id = data.get('phone')
            
            # Verifica se o grupo da mensagem está na sua lista de grupos alvo
            if group_id in LISTA_GRUPOS_ALVO:
                print(f"Mensagem recebida do grupo alvo: {data.get('chatName')}. Enviando resposta...")
                
                # Responde para o grupo todo, e não para o chat particular da pessoa
                send_automatic_reply_to_group(group_id)
            else:
                print(f"Mensagem recebida de um grupo fora da lista de alvos. Ignorando.")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Erro ao processar o webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Função para enviar a mensagem de resposta ao grupo ---
def send_automatic_reply_to_group(group_id):
    """Envia uma mensagem de texto para o grupo especificado."""
    
    # Endpoint para enviar mensagens para grupos
    url = f"https://api.z-api.io/instances/{ZAPI_SESSION_ID}/token/{ZAPI_KEY}/send-image"

    # --- A MENSAGEM FOI SUBSTITUÍDA AQUI ---
    message_content = """✅ GRUPO DE PUXADAS GRATIS ✅

ENTRE NO GRUPO NO WHATSAPP GRÁTIS E PUXE DADOS
https://entrar-agora.short.gy/grupo-puxadas-whatsapp

🚨 ATENÇÃO: 🚨
- GRUPO COM ACESSO LIMITADO
- BOT PUXANDO 24 HORAS
- RESPEITO COM TODOS OS MEMBROS 

🔥 LINK DO GRUPO NO WHATSAPP: 🔥
https://entrar-agora.short.gy/grupo-puxadas-whatsapp
https://entrar-agora.short.gy/grupo-puxadas-whatsapp



✅ GRUPO DE PUXADAS GRATIS ✅

ENTRE NO GRUPO NO WHATSAPP GRÁTIS E PUXE DADOS
https://chat.whatsapp.com/Cri5Xv3yBDDDI7u8zq15Pw

🚨 ATENÇÃO: 🚨
- GRUPO COM ACESSO LIMITADO
- BOT PUXANDO 24 HORAS
- RESPEITO COM TODOS OS MEMBROS 

🔥 LINK DO GRUPO NO WHATSAPP: 🔥
https://entrar-agora.short.gy/grupo-puxadas-whatsapp
https://entrar-agora.short.gy/grupo-puxadas-whatsapp
https://entrar-agora.short.gy/grupo-puxadas-whatsapp"""

    payload = {
        # O telefone aqui é o ID do grupo
        "phone": group_id,
        "image": "https://i.pinimg.com/736x/19/e9/ce/19e9ce9bdd9d35955f3f6dded8edbb4d.jpg",
        "caption": message_content
    }
    
    headers = {
        "Content-Type": "application/json",
        "client-token": ZAPI_CLIENT_TOKEN
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            print("Mensagem de resposta enviada com sucesso para o grupo!")
        else:
            print(f"Erro ao enviar a resposta. Código: {response.status_code}")
            print("Detalhes do erro:", response.text)
    
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao tentar enviar a resposta: {e}")

if __name__ == "__main__":
    app.run(host='82.25.85.25', port=8080)