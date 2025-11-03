# 2. Conexão MySQL

import mysql.connector
from mysql.connector import Error

# --- Configurações do Banco de Dados ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', 
    'password': '418131909', 
    'database': 'ubs_agendamento' 
}

def conectar_bd():
    """Tenta estabelecer a conexão com o banco de dados."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("✅ Conexão com o MySQL estabelecida com sucesso!")
            return conn
        else:
            print("❌ Falha na conexão com o banco de dados.")
            return None
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return None

def fechar_conexao(conn):
    """Fecha a conexão com o banco de dados."""
    if conn and conn.is_connected():
        conn.close()
        print("🔌 Conexão com o MySQL fechada.")

#--- Teste da Conexão ---
# if __name__ == "__main__":
#     conexao = conectar_bd()
#     if conexao:
#         # Aqui é onde você fará as operações de CRUD
#         pass 
#         fechar_conexao(conexao)