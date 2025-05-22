import func

while True:
  menu_tarefas = int(input('Escolha uma opção:\n1 - Criar tarefa\n2 - Ler tarefas\n3 - Atualizar tarefa\n4 - Deletar tarefa\n5 - Buscar tarefa\n6 - Sair\n'))

  if menu_tarefas == 1:
    func.criar_tarefa()

  elif menu_tarefas == 2:
    func.ler_tarefas()

  elif menu_tarefas == 3:
    func.atualizar_tarefa()

  elif menu_tarefas == 4:
    func.deletar_tarefa()

  elif menu_tarefas == 5: 
    func.busca_especifica()

  elif menu_tarefas == 6:   
    print('Saindo do programa...')

  else:
    print('Opção inválida. Tente novamente.')