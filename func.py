from pymongo import MongoClient
from conexao import colecao_tarefas
from datetime import datetime 

def criar_tarefa():
  opcoes_status = ['pendente', 'em andamento', 'concluída']

  titulo = input('Digite o título da tarefa: ')
  descricao = input('Digite a descrição da tarefa: ')
  data_criacao = datetime.now()
  tags = []
  comentarios = []
  
  while True:
    status = input('Digite o status da tarefa (pendente, em andamento, concluída): ').lower()
    if status in opcoes_status:
      break
    else:
      print('Status inválido. Digite um status valido.')

  tarefa = {
    'titulo': titulo,
    'descricao': descricao,
    'data_criacao': data_criacao,
    'status': status,
    'tags': tags,
    'comentarios': comentarios
  }
  colecao_tarefas.insert_one(tarefa)
  print('Tarefa criada com sucesso!')

def ler_tarefas(): 
    lista_tarefas = list(colecao_tarefas.find())
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

   
    for i, tarefa in enumerate(lista_tarefas, start=1):
        print(f"Tarefa {i}:")  
        print(f"-  Título: {tarefa['titulo']}")
        print('---')

    
    opcao = int(input('Escolha o n° da tarefa que deseja visualizar: '))

    if opcao <= len(lista_tarefas):
        tarefa = lista_tarefas[opcao - 1]
        print(f"-  Título: {tarefa['titulo']}")
        print(f"-  Descrição: {tarefa['descricao']}")  
        print(f"-  Data de criação: {tarefa['data_criacao']}")
        print(f"-  Status: {tarefa['status']}") 
        print(f"-  Tags: {tarefa['tags']}")
        print(f"-  Comentários: {tarefa['comentarios']}") 
    else:
        print('Tarefa não encontrada.')


def atualizar_tarefa():
  lista_tarefas = list(colecao_tarefas.find())
  if not lista_tarefas:
      print("Nenhuma tarefa cadastrada.")
      return

    
  for i, tarefa in enumerate(lista_tarefas, start=1):
        print(f"Tarefa {i}:")  
        print(f"-  Título: {tarefa['titulo']}")
        print('---')

  opcao = int(input('Escolha o n° da tarefa que deseja atualizar: '))

  if not lista_tarefas:
      print("Não existe essa tarefa.")
      return
  else:
     while True:
        print("\nO que deseja atualizar?")
        print("1 - Editar título")
        print("2 - Editar descrição")
        print("3 - Alterar status")
        print("4 - Adicionar tag")
        print("5 - Adicionar comentário")
        print("6 - Sair")
      
        escolha = int(input("Escolha uma opção: "))
        if escolha == 1:
            novo_titulo = input("Digite o novo título: ")
            colecao_tarefas.update_one({"_id": lista_tarefas[opcao - 1]["_id"]}, {"$set": {"titulo": novo_titulo}})
            print("Título atualizado com sucesso!")
        elif escolha == 2:
            nova_descricao = input("Digite a nova descrição: ")
            colecao_tarefas.update_one({"_id": lista_tarefas[opcao - 1]["_id"]}, {"$set": {"descricao": nova_descricao}})
            print("Descrição atualizada com sucesso!")
        elif escolha == 3:
            novo_status = input("Digite o novo status (pendente, em andamento, concluída): ")
            colecao_tarefas.update_one({"_id": lista_tarefas[opcao - 1]["_id"]}, {"$set": {"status": novo_status}})
            print("Status atualizado com sucesso!")
        elif escolha == 4:
            nova_tag = input("Digite a nova tag: ")
            colecao_tarefas.update_one({"_id": lista_tarefas[opcao - 1]["_id"]}, {"$addToSet": {"tags": nova_tag}})
            print("Tag adicionada com sucesso!")
        elif escolha == 5:
            novo_comentario = input("Digite o novo comentário: ")
            colecao_tarefas.update_one({"_id": lista_tarefas[opcao - 1]["_id"]}, {"$addToSet": {"comentarios": novo_comentario}})
            print("Comentário adicionado com sucesso!")
        elif escolha == 6:
            break
        else:
            print("Opção inválida. Tente novamente.")

def deletar_tarefa():
  lista_tarefas = list(colecao_tarefas.find())
  if not lista_tarefas:
      print("Nenhuma tarefa cadastrada.")
      return

    
  for i, tarefa in enumerate(lista_tarefas, start=1):
        print(f"Tarefa {i}:")  
        print(f"-  Título: {tarefa['titulo']}")
        print('---')

  opcao = int(input('Escolha o n° da tarefa que deseja deletar: ')) 

  if opcao > len(lista_tarefas):
      print("Não existe essa tarefa.")        
      return  
  else:
    colecao_tarefas.delete_one({"_id": lista_tarefas[opcao - 1]["_id"]})
    print("Tarefa deletada com sucesso!")

def busca_especifica():
    tipo = int(input('Escolha uma opção:\n1 - Buscar tarefa por status\n2 - Buscar tarefa por data de criação (AAAA-MM-DD)\n3 - Buscar tarefa por tag\n4 - Sair\n'))
    
    if tipo == 4:
        return

    if tipo == 1:
        campo = "status"
        valor = input('Digite o status que deseja buscar (pendente, em andamento, concluída): ')
        filtro = {campo: valor}

    elif tipo == 2:
        campo = "data_criacao"
        valor = input('Digite a data (AAAA-MM-DD): ')
        try:
            
            data_inicio = datetime.strptime(valor, "%Y-%m-%d")
            data_fim = data_inicio.replace(hour=23, minute=59, second=59)
            filtro = {campo: {"$gte": data_inicio, "$lte": data_fim}}
        except ValueError:
            print("Formato de data inválido. Use AAAA-MM-DD.")
            return

    elif tipo == 3:
        campo = "tags"
        valor = input('Digite a tag que deseja buscar: ')
        filtro = {campo: {"$in": [valor]}}

    else:
        print("Opção inválida.")
        return

    tarefas_encontradas = list(colecao_tarefas.find(filtro))
    
    if tarefas_encontradas:
        for tarefa in tarefas_encontradas:
            print(f"Título: {tarefa['titulo']}")
            print(f"Descrição: {tarefa['descricao']}")
            print(f"Data de criação: {tarefa['data_criacao']}")
            print(f"Status: {tarefa['status']}")
            print(f"Tags: {tarefa['tags']}")
            print(f"Comentários: {tarefa['comentarios']}")
            print('---')
    else:
        print("Nenhuma tarefa encontrada.")






        





   


    

    
    

    

