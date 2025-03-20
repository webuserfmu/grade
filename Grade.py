import sqlite3
from prettytable import PrettyTable

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('projeto.db')
cursor = conn.cursor()

# Criação das tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS disciplinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disciplina_id INTEGER NOT NULL,
    unidade1 REAL,
    unidade2 REAL,
    unidade3 REAL,
    unidade4 REAL,
    prova REAL,
    media_unidades REAL,
    resultado_final REAL,
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id)
)
''')

conn.commit()

# Função para inserir uma nova disciplina
def inserir_disciplina(nome):
    cursor.execute('INSERT INTO disciplinas (nome) VALUES (?)', (nome,))
    conn.commit()
    print(f'Disciplina "{nome}" inserida com sucesso!')

# Função para consultar a grade de disciplinas
def consultar_grade():
    cursor.execute('''
        SELECT d.id, d.nome, 
               COALESCE(n.unidade1, '') AS unidade1, 
               COALESCE(n.unidade2, '') AS unidade2, 
               COALESCE(n.unidade3, '') AS unidade3, 
               COALESCE(n.unidade4, '') AS unidade4, 
               COALESCE(n.prova, '') AS prova, 
               COALESCE(n.media_unidades, '') AS media_unidades, 
               COALESCE(n.resultado_final, '') AS resultado_final
        FROM disciplinas d
        LEFT JOIN notas n ON d.id = n.disciplina_id
    ''')
    disciplinas = cursor.fetchall()

    # Criar tabela formatada
    tabela = PrettyTable()
    tabela.field_names = ["ID", "Nome", "Unidade 1", "Unidade 2", "Unidade 3", "Unidade 4", "Prova", "Média Unidades", "Resultado Final"]

    for disciplina in disciplinas:
        tabela.add_row(disciplina)

    print("Grade de Disciplinas:")
    print(tabela)

# Função para inserir notas de uma disciplina
def inserir_notas(disciplina_id, unidade1=None, unidade2=None, unidade3=None, unidade4=None, prova=None):
    # Obter as notas existentes, caso já tenham sido inseridas
    cursor.execute('SELECT unidade1, unidade2, unidade3, unidade4, prova FROM notas WHERE disciplina_id = ?', (disciplina_id,))
    notas_existentes = cursor.fetchone()

    # Atualizar as notas com os valores fornecidos ou manter as existentes
    unidade1 = unidade1 if unidade1 is not None else (notas_existentes[0] if notas_existentes else None)
    unidade2 = unidade2 if unidade2 is not None else (notas_existentes[1] if notas_existentes else None)
    unidade3 = unidade3 if unidade3 is not None else (notas_existentes[2] if notas_existentes else None)
    unidade4 = unidade4 if unidade4 is not None else (notas_existentes[3] if notas_existentes else None)
    prova = prova if prova is not None else (notas_existentes[4] if notas_existentes else None)

    # Calcular a média das unidades e o resultado final apenas se todas as notas forem fornecidas
    media_unidades = None
    resultado_final = None
    if None not in (unidade1, unidade2, unidade3, unidade4):
        media_unidades = (unidade1 + unidade2 + unidade3 + unidade4) / 4
        if prova is not None:
            resultado_final = media_unidades * 0.4 + prova * 0.6

    # Inserir ou atualizar as notas no banco de dados
    if notas_existentes:
        # Atualizar apenas os campos que possuem valores fornecidos
        cursor.execute('''
            UPDATE notas
            SET unidade1 = COALESCE(?, unidade1),
                unidade2 = COALESCE(?, unidade2),
                unidade3 = COALESCE(?, unidade3),
                unidade4 = COALESCE(?, unidade4),
                prova = COALESCE(?, prova),
                media_unidades = COALESCE(?, media_unidades),
                resultado_final = COALESCE(?, resultado_final)
            WHERE disciplina_id = ?
        ''', (unidade1, unidade2, unidade3, unidade4, prova, media_unidades, resultado_final, disciplina_id))
    else:
        # Inserir apenas se pelo menos uma nota for fornecida
        if any(nota is not None for nota in [unidade1, unidade2, unidade3, unidade4, prova]):
            cursor.execute('''
                INSERT INTO notas (disciplina_id, unidade1, unidade2, unidade3, unidade4, prova, media_unidades, resultado_final)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (disciplina_id, unidade1, unidade2, unidade3, unidade4, prova, media_unidades, resultado_final))

    conn.commit()
    print(f'Notas atualizadas para a disciplina ID {disciplina_id} com sucesso!')

# Função para consultar todas as disciplinas
def consultar_disciplinas():
    cursor.execute('SELECT id, nome FROM disciplinas')
    disciplinas = cursor.fetchall()

    if disciplinas:
        print("\nDisciplinas cadastradas:")
        for disciplina in disciplinas:
            print(f"ID: {disciplina[0]}, Nome: {disciplina[1]}")
    else:
        print("\nNenhuma disciplina cadastrada.")

# Função para eliminar uma disciplina
def eliminar_disciplina(disciplina_id):
    # Verificar se a disciplina existe
    cursor.execute('SELECT id FROM disciplinas WHERE id = ?', (disciplina_id,))
    if cursor.fetchone() is None:
        print(f"Disciplina com ID {disciplina_id} não encontrada.")
        return

    # Excluir a disciplina e suas notas associadas
    cursor.execute('DELETE FROM notas WHERE disciplina_id = ?', (disciplina_id,))
    cursor.execute('DELETE FROM disciplinas WHERE id = ?', (disciplina_id,))
    conn.commit()
    print(f"Disciplina com ID {disciplina_id} eliminada com sucesso!")

# Atualização do menu de opções
def menu():
    while True:
        print("\nMenu:")
        print("1. Inserir Disciplina")
        print("2. Consultar Grade")
        print("3. Inserir Notas")
        print("4. Consultar Disciplinas")
        print("5. Eliminar Disciplina")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Digite o nome da disciplina: ")
            inserir_disciplina(nome)
        elif opcao == '2':
            consultar_grade()
        elif opcao == '3':
            disciplina_id = int(input("Digite o ID da disciplina: "))
            unidade1 = input("Nota Unidade 1 (pressione Enter para ignorar): ")
            unidade2 = input("Nota Unidade 2 (pressione Enter para ignorar): ")
            unidade3 = input("Nota Unidade 3 (pressione Enter para ignorar): ")
            unidade4 = input("Nota Unidade 4 (pressione Enter para ignorar): ")
            prova = input("Nota Prova (pressione Enter para ignorar): ")

            # Converter entradas para float ou None
            unidade1 = float(unidade1) if unidade1 else None
            unidade2 = float(unidade2) if unidade2 else None
            unidade3 = float(unidade3) if unidade3 else None
            unidade4 = float(unidade4) if unidade4 else None
            prova = float(prova) if prova else None

            inserir_notas(disciplina_id, unidade1, unidade2, unidade3, unidade4, prova)
        elif opcao == '4':
            consultar_disciplinas()
        elif opcao == '5':
            disciplina_id = int(input("Digite o ID da disciplina a ser eliminada: "))
            eliminar_disciplina(disciplina_id)
        elif opcao == '6':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executa o menu
menu()

# Fecha a conexão com o banco de dados
conn.close()