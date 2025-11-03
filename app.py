# 1. Interface do Usuário (Menu)

from data_manager import criar_paciente, listar_pacientes, buscar_paciente_por_id, atualizar_paciente, excluir_paciente
from datetime import datetime

def validar_e_formatar_data(data_str):
    """
    Tenta converter a data de DD/MM/AAAA para o formato MySQL AAAA-MM-DD.
    Retorna a string formatada ou None em caso de erro.
    """
    try:
        # 1. Converte a string do usuário para um objeto datetime
        data_obj = datetime.strptime(data_str, '%d/%m/%Y')
        
        # 2. Converte o objeto datetime para o formato SQL
        data_sql = data_obj.strftime('%Y-%m-%d')
        return data_sql
    
    except ValueError:
        print("\n❌ Formato de Data de Nascimento inválido. Use o formato DD/MM/AAAA.")
        return None

def cadastrar_paciente():
    """Lógica para coletar e cadastrar um novo paciente."""
    print("\n--- Cadastro de Novo Paciente ---")
    
    # 1. Coleta dos dados
    nome = input("Nome Completo: ").strip()
    cpf = input("CPF (apenas números ou pontuação): ").strip()
    
    # 2. Validação e Formatação da Data (Fronteira da Responsabilidade)
    while True:
        data_nasc_usuario = input("Data de Nascimento (DD/MM/AAAA): ").strip()
        data_nasc_sql = validar_e_formatar_data(data_nasc_usuario)
        if data_nasc_sql:
            break
            
    telefone = input("Telefone (obrigatório): ").strip()
    endereco = input("Endereço (opcional, deixe vazio para pular): ").strip()
    
    # Se o endereço for vazio, passamos None para o banco de dados
    if not endereco:
        endereco = None 
        
    # TODO: Implementar validação de campos obrigatórios e formato de CPF/Telefone
    
    # 3. Chamada da função de persistência
    if nome and cpf and telefone: # Checagem básica de campos obrigatórios
        criar_paciente(nome, cpf, data_nasc_sql, telefone, endereco)
    else:
        print("❌ Por favor, preencha todos os campos obrigatórios (Nome, CPF, Telefone).")

def exibir_pacientes():
    """Busca e exibe a lista de pacientes de forma formatada."""
    print("\n--- Lista de Pacientes Cadastrados ---")
    
    lista = listar_pacientes()
    
    if not lista:
        print("Nenhum paciente cadastrado.")
        return

    # Formatação do cabeçalho
    print("-" * 70)
    print(f"{'ID':<4} {'Nome':<30} {'CPF':<18} {'Telefone':<15}")
    print("-" * 70)

    # Iteração e exibição dos dados
    for p in lista:
        # A data_nascimento é um objeto date do Python, convertemos para string para exibir.
        data_nasc_str = p['data_nascimento'].strftime('%d/%m/%Y')
        
        print(f"{p['paciente_id']:<4} {p['nome']:<30} {p['cpf']:<18} {p['telefone']:<15}{data_nasc_str:<12}")
        # Poderíamos exibir mais informações aqui se necessário.
    print("-" * 70)

def modificar_paciente():
    """Lógica para buscar, coletar novos dados e atualizar um paciente."""
    print("\n--- Modificar Paciente ---")
    
    # 1. Solicitar o ID do paciente
    try:
        paciente_id = int(input("Digite o ID do paciente que deseja modificar: "))
    except ValueError:
        print("❌ ID inválido. Por favor, digite um número.")
        return

    # 2. Buscar o paciente existente
    paciente = buscar_paciente_por_id(paciente_id)
    
    if not paciente:
        print(f"❌ Paciente com ID {paciente_id} não encontrado.")
        return
        
    print("\n--- Dados Atuais ---")
    # Formata a data de nascimento para exibição amigável
    data_nasc_atual_str = paciente['data_nascimento'].strftime('%d/%m/%Y')
    
    print(f"Nome: {paciente['nome']}")
    print(f"CPF: {paciente['cpf']}")
    print(f"Data Nasc: {data_nasc_atual_str}")
    print(f"Telefone: {paciente['telefone']}")
    print(f"Endereço: {paciente['endereco'] if paciente['endereco'] else '[Não informado]'}")

    print("\n--- Digite os Novos Dados (ou ENTER para manter o atual) ---")

    # 3. Coletar Novos Dados (mantendo o original se o usuário apertar Enter)
    novo_nome = input(f"Novo Nome ({paciente['nome']}): ").strip() or paciente['nome']
    
    # CPF é crucial e deve ser único. Vamos forçar a entrada ou manter o original.
    novo_cpf = input(f"Novo CPF ({paciente['cpf']}): ").strip() or paciente['cpf']
    
    # Tratamento da Data de Nascimento (continua com o loop de validação)
    novo_data_nasc_sql = paciente['data_nascimento'].strftime('%Y-%m-%d') # Mantém o formato SQL atual por padrão
    while True:
        nova_data_nasc_usuario = input(f"Nova Data Nasc (DD/MM/AAAA) ({data_nasc_atual_str}): ").strip()
        
        if not nova_data_nasc_usuario:
            break # Usuário apertou ENTER, mantém a data original (já setada em novo_data_nasc_sql)
        
        # Valida e formata a nova data
        validada = validar_e_formatar_data(nova_data_nasc_usuario)
        if validada:
            novo_data_nasc_sql = validada
            break

    novo_telefone = input(f"Novo Telefone ({paciente['telefone']}): ").strip() or paciente['telefone']
    novo_endereco = input(f"Novo Endereço ({paciente['endereco'] if paciente['endereco'] else 'Opcional'}): ").strip() or paciente['endereco']
    
    # 4. Executar a atualização
    atualizar_paciente(
        paciente_id,
        novo_nome,
        novo_cpf,
        novo_data_nasc_sql,
        novo_telefone,
        novo_endereco
    )

def remover_paciente():
    """Lógica para solicitar o ID, confirmar e excluir um paciente."""
    print("\n--- Remover Paciente ---")
    
    # 1. Solicitar o ID
    try:
        paciente_id = int(input("Digite o ID do paciente que deseja REMOVER: "))
    except ValueError:
        print("❌ ID inválido. Por favor, digite um número.")
        return

    # 2. Buscar e Confirmar (Boas Práticas)
    paciente = buscar_paciente_por_id(paciente_id)
    
    if not paciente:
        print(f"❌ Paciente com ID {paciente_id} não encontrado.")
        return
        
    confirmacao = input(f"CONFIRME a exclusão do paciente {paciente['nome']} (S/N): ").upper()
    
    if confirmacao == 'S':
        # 3. Executar a exclusão
        excluir_paciente(paciente_id)
    else:
        print("Operação de exclusão cancelada.")


# ... Modificar menu_principal para incluir a nova opção ...
def menu_principal():
    """Exibe o menu principal do sistema."""
    while True:
        print("\n=== Sistema UBS Agendamento ===")
        print("1. Cadastrar Novo Paciente")
        print("2. Listar Pacientes")
        print("3. Modificar Paciente")
        print("4. Remover Paciente") # Nova opção!
        print("5. Gerenciar Profissionais")
        print("6. Agendar Consulta")
        print("7. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            cadastrar_paciente()
        elif opcao == '2':
            exibir_pacientes()
        elif opcao == '3':
            modificar_paciente()
        elif opcao == '4': # Nova Ação
            remover_paciente()
        elif opcao == '7':
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Execução do programa
if __name__ == "__main__":
    menu_principal()