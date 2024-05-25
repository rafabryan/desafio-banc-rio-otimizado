import textwrap

def menu():
    menu = """\n
    ==================MENU====================
    
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar Conta
    [nu]\tNovo usuário
    [q]\tSair
    => """
    
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é invalido. @@@")
    
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    
    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excedeu o limite. @@@")
    
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Numero de saques passou do limite. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 3
        print("\n=== Saque realizado com sucesso!!! ===")
        
    else:
        print("\n@@@ Operação falhou! O valor informado é invalido. @@@")
        
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n======================= EXTRATO ======================")
    print("Não foram realizado movimentação na conta." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("========================================================")
    
def criar_usuario(usuarios):
    cpf = input("Informe o CPF por favor (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento(dd-mm-aaaa): ")
    endereco = input("Infome o endereço (logradoro, nro - bairro - cidade / estado): ")
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    
    print("=== Usuario criado com sucesso! ====")
    
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuarios in usuarios if usuario["cpf"] == cpf]
    usuario = filtrar_usuario(cpf, usuarios)
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuario: ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("\n=== Conta criada com sucesso!! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
        print("\n@@@ Usuario não encontrado, fluxo de criação de conta encerrado por não ter encontrado usuario! @@@")

def listar_contas(conta):
    for conta in conta:
        linha = f"""\
            Agencia:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            """
        print("=" * 100)
        print(textwrap.dedent(linha)) 
            
def main():
    LIMITE_SAQUES = 10
    AGENCIA = "0001"
    
    saldo = 0
    limite = 750
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            
            saldo, extrato = depositar(saldo, valor, extrato)
        
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
    
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )    
    
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
            
        elif opcao == "nu":
            criar_usuario(usuarios)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            
            if conta:
                contas.append(conta)
                
        elif opcao == "lc":
            listar_contas(contas)
        
        elif opcao == "q" :
            break
        
        else:
            print("Operação invalida, por favor selecione novamente a operação desejada.")
            
main()