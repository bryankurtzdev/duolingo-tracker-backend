from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import requests
import pandas as pd
import os

app = Flask(__name__)

# Cabeçalho para evitar bloqueio
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def get_user_id(username):
    """ Obtém o ID de um usuário do Duolingo a partir do nome de usuário """
    url = f"https://www.duolingo.com/2017-06-30/users?username={username}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        if "users" in data and data["users"]:
            return data["users"][0].get("id")
    return None

def get_total_xp(user_id):
    """ Obtém o XP total de um usuário pelo ID """
    url = f"https://www.duolingo.com/2017-06-30/users/{user_id}?fields=totalXp,id"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        return data.get("totalXp")
    return None

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "duotracker.png", mimetype="image/png")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    data = request.json
    users = data.get("users", [])
    meta_xp = data.get("meta_xp", 0)

    resultados = []
    for username in users:
        user_id = get_user_id(username)
        if user_id:
            xp_total = get_total_xp(user_id)
            resultados.append({"Usuário": username, "XP Total": xp_total, "Meta XP": meta_xp})

    # Criar e salvar planilha
    file_path = "duolingo_xp.xlsx"
    df = pd.DataFrame(resultados)
    df.to_excel(file_path, index=False)

    return jsonify({
        "message": "Planilha criada com sucesso!", 
        "file_url": "/download",
        "dados": resultados  # Agora retorna a lista de usuários e XP
    })

@app.route('/download')
def download():
    file_path = "duolingo_xp.xlsx"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "Arquivo não encontrado!", 404

if __name__ == '__main__':
    app.run(debug=True)