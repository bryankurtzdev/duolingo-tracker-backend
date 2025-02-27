from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import json  # Apenas para depuração
import requests
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

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

def get_english_xp(user_id):
    """ Obtém o XP do curso de inglês ('en') de um usuário pelo ID """
    url = f"https://www.duolingo.com/2017-06-30/users/{user_id}?fields=courses"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        courses = data.get("courses", [])  # Obtém a lista de cursos

        # Verifica se há cursos
        if not courses:
            print(f"⚠ Nenhum curso encontrado para o usuário {user_id}")
            return 0

        # Procura o curso de inglês
        for course in courses:
            if course.get("learningLanguage") == "en":
                return course.get("xp", 0)  # Retorna o XP do curso de inglês

        print(f"⚠ Usuário {user_id} não está aprendendo inglês.")
        return 0  # Retorna 0 se o usuário não estiver aprendendo inglês

    print(f"❌ Erro na requisição para {user_id}, Status Code: {response.status_code}")
    return 0  # Retorna 0 em caso de erro na requisição

print(get_english_xp(get_user_id(username='marianabonatow')))  # Teste da função
@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "duotracker.png", mimetype="image/png")

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    data = request.json
    users = data.get("users", [])
    meta_xp = data.get("meta_xp", 0)

    resultados = []
    for username in users:
        user_id = get_user_id(username)
        if user_id:
            xp_ingles = get_english_xp(user_id)  # Obtém apenas o XP do curso de inglês
            resultados.append({"Usuário": username, "XP Inglês": xp_ingles, "Meta XP": meta_xp})

    # Criar e salvar planilha
    file_path = "duolingo_xp.xlsx"
    df = pd.DataFrame(resultados)
    df.to_excel(file_path, index=False)

    return jsonify({
        "message": "Planilha criada com sucesso!", 
        "file_url": "/download",
        "dados": resultados  # Retorna a lista de usuários e XP do curso de inglês
    })

@app.route('/download')
def download():
    file_path = "duolingo_xp.xlsx"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "Arquivo não encontrado!", 404

if __name__ == '__main__':
    app.run(debug=True)