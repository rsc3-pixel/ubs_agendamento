# 3. Lógica CRUD/SQL
import mysql.connector
from db_connector import conectar_bd, fechar_conexao
from mysql.connector import Error

def criar_paciente(nome, cpf, data_nascimento, telefone, endereco=None):
    """
    Insere um novo registro de paciente na tabela Pacientes.
    
    Args:
        nome (str): Nome do paciente.
        cpf (str): CPF do paciente (UNIQUE).
        data_nascimento (str): Data no formato 'AAAA-MM-DD'.
        telefone (str): Telefone de contato.
        endereco (str, optional): Endereço (opcional).

    Returns:
        int/bool: O ID do novo paciente se for bem-sucedido, False se houver erro.
    """
    conexao = conectar_bd()
    if conexao is None:
        print("❌ Falha na operação: Sem conexão com o banco de dados.")
        return False
    
    cursor = conexao.cursor()
    
    # Comando SQL de Inserção
    sql = """
        INSERT INTO Pacientes 
        (nome, cpf, data_nascimento, telefone, endereco) 
        VALUES (%s, %s, %s, %s, %s)
    """
    
    valores = (nome, cpf, data_nascimento, telefone, endereco)
    
    try:
        # Execução e Confirmação
        cursor.execute(sql, valores)
        conexao.commit()
        novo_id = cursor.lastrowid
        
        print(f"✅ Paciente '{nome}' cadastrado com sucesso! ID: {novo_id}")
        return novo_id

    except mysql.connector.Error as e:
        # Trata erros específicos do MySQL (como CPF duplicado)
        print(f"❌ Falha ao cadastrar Paciente: {e}")
        conexao.rollback()
        return False

    finally:
        # O 'finally' garante que a conexão será fechada, mesmo que ocorra um erro.
        cursor.close()
        fechar_conexao(conexao) # Usa a função importada    
        

def listar_pacientes():
    """
    Busca todos os registros de pacientes no banco de dados.
    
    Returns:
        list: Uma lista de dicionários contendo os dados dos pacientes.
              Retorna uma lista vazia se houver erro ou nenhum registro.
    """
    conexao = conectar_bd()
    if conexao is None:
        return []
    
    cursor = conexao.cursor(dictionary=True) # Usar dictionary=True para retornar resultados como dicionários Python!
    
    # Comando SQL de Seleção (SELECT)
    sql = "SELECT paciente_id, nome, cpf, data_nascimento, telefone FROM Pacientes"
    
    try:
        cursor.execute(sql)
        
        # O fetchall() pega todos os resultados da consulta
        pacientes = cursor.fetchall() 
        
        # print(f"✅ {len(pacientes)} pacientes encontrados.")
        return pacientes

    except mysql.connector.Error as e:
        print(f"❌ Falha ao listar Pacientes: {e}")
        return []

    finally:
        cursor.close()
        fechar_conexao(conexao)     
        
def buscar_paciente_por_id(paciente_id):
    """
    Busca um único paciente pelo ID.
    
    Args:
        paciente_id (int): O ID único do paciente.

    Returns:
        dict/None: Dicionário do paciente encontrado ou None se não existir.
    """
    conexao = conectar_bd()
    if conexao is None:
        return None
    
    # Usamos dictionary=True para o retorno ser um dicionário
    cursor = conexao.cursor(dictionary=True) 
    
    # Comando SQL: SELECT com a cláusula WHERE para filtrar pelo ID
    sql = "SELECT paciente_id, nome, cpf, data_nascimento, telefone, endereco FROM Pacientes WHERE paciente_id = %s"
    
    try:
        cursor.execute(sql, (paciente_id,)) # O (paciente_id,) é uma tupla de um elemento
        
        # O fetchone() pega apenas o primeiro (e único) resultado
        paciente = cursor.fetchone() 
        return paciente

    except mysql.connector.Error as e:
        print(f"❌ Falha ao buscar Paciente por ID: {e}")
        return None

    finally:
        cursor.close()
        fechar_conexao(conexao)  
        
def atualizar_paciente(paciente_id, nome, cpf, data_nascimento, telefone, endereco=None):
    """
    Executa o comando SQL UPDATE para modificar um paciente existente.
    
    Args:
        paciente_id (int): O ID do paciente a ser atualizado (crucial para o WHERE).
        ... demais campos ...

    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário.
    """
    conexao = conectar_bd()
    if conexao is None:
        return False
    
    cursor = conexao.cursor()
    
    # Comando SQL de Atualização (UPDATE)
    # ATENÇÃO: A cláusula WHERE paciente_id = %s é VITAL para atualizar APENAS o registro correto.
    sql = """
        UPDATE Pacientes
        SET nome = %s, 
            cpf = %s, 
            data_nascimento = %s, 
            telefone = %s, 
            endereco = %s
        WHERE paciente_id = %s
    """
    
    # A ordem dos valores DEVE ser a mesma da ordem das colunas no SET,
    # e o último valor DEVE ser o paciente_id para a cláusula WHERE.
    valores = (nome, cpf, data_nascimento, telefone, endereco, paciente_id)
    
    try:
        cursor.execute(sql, valores)
        conexao.commit()
        
        # O rowcount verifica quantas linhas foram afetadas (deve ser 1)
        if cursor.rowcount > 0:
            print(f"✅ Paciente ID {paciente_id} atualizado com sucesso!")
            return True
        else:
            print(f"⚠️ Paciente ID {paciente_id} não encontrado para atualização.")
            return False

    except mysql.connector.Error as e:
        print(f"❌ Falha ao atualizar Paciente: {e}")
        conexao.rollback()
        return False

    finally:
        cursor.close()
        fechar_conexao(conexao)   

def excluir_paciente(paciente_id):
    """
    Executa o comando SQL DELETE para remover um paciente existente.
    
    Args:
        paciente_id (int): O ID do paciente a ser removido (crucial para o WHERE).

    Returns:
        bool: True se a exclusão foi bem-sucedida, False caso contrário.
    """
    conexao = conectar_bd()
    if conexao is None:
        return False
    
    cursor = conexao.cursor()
    
    # Comando SQL de Exclusão (DELETE)
    # ATENÇÃO: A cláusula WHERE paciente_id = %s é ABSOLUTAMENTE VITAL.
    sql = "DELETE FROM Pacientes WHERE paciente_id = %s"
    
    try:
        cursor.execute(sql, (paciente_id,))
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"✅ Paciente ID {paciente_id} excluído com sucesso!")
            return True
        else:
            print(f"⚠️ Paciente ID {paciente_id} não encontrado.")
            return False

    except mysql.connector.Error as e:
        # A exclusão pode falhar se houver consultas agendadas para este paciente (FOREIGN KEY)
        print(f"❌ Falha ao excluir Paciente: {e}") 
        conexao.rollback()
        return False

    finally:
        cursor.close()
        fechar_conexao(conexao)              