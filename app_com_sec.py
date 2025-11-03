import re
import logging
import sqlite3
from flask import Flask, request, render_template_string

logging.basicConfig(
    filename='suspicious_logs.log',
    level=logging.WARNING,
    format='%(asctime)s - %(message)s'
)

def is_suspicious(input_string):
    patterns = [r"--", r"#", r"\s+OR\s+"]
    
    for pattern in patterns:
        if re.search(pattern, input_string, re.IGNORECASE):
            return True
    
    return False

#----------------SITE----------------
app = Flask(__name__)

DB_NAME = "user.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    
    cur.execute(" DELETE FROM users ")
    
    cur.execute(" INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "senhasecreta123"))
    
    conn.commit()
    conn.close()
    print("Banco de Dados iniciado como ADMIN")
    
HTML_LOGIN_FORM = HTML_LOGIN_FORM = '''
<!DOCTYPE html>
<html>
<head><title>Login Vulnerável</title></head>
<body>
    <h2>Login</h2>
    <form method="POST" action="/login">
        Usuário: <input type="text" name="username"><br>
        Senha: <input type="password" name="password"><br>
        <input type="submit" value="Entrar">
    </form>
    
    <hr>
    
    <h2>Registrar</h2>
    <form method="POST" action="/register">
        Usuário: <input type="text" name="username"><br>
        Senha: <input type="password" name="password"><br>
        <input type="submit" value="Registrar">
    </form>
</body>
</html>
'''
@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_LOGIN_FORM)
    
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        
        conn.commit()
        conn.close()
        return f"Usuario '{username}' registrado com sucesso!"
    except sqlite3.Error as e:
        return f"Erro ao registrar: {e}", 400
    
@app.route('/login', methods=['POST'])
def login():
    username =  request.form['username']
    password =  request.form['password']
    
    if is_suspicious(username) or is_suspicious(password):
        logging.warning(
            f"Tentativa de SQLI detectada! "
            f"IP: {request.remote_addr}, "
            f"User: '{username}', Pass: '{password}' "
        )
        
        
    conn = sqlite3.connect(DB_NAME, timeout=10)
    cur = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username = ? AND password = ? "
    print(f"[DEBUG] Executando query segura com placeholders. ")
    
    try:
        cur.execute(query, (username, password))
        user = cur.fetchone()
        
        if user:
            return f"Login bem sucedido! Bem-vindo, {user[1]}"
        else:
            return f"Falha no login: usuario ou senha invalidos."
    except sqlite3.Error as e:
        return f"Erro de SQL detectado: {e}", 500
    finally:
        conn.close()
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)