import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import PhotoImage  # Para carregar imagens

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

# Funções do programa
def inserir_disciplina():
    def salvar_disciplina():
        nome = entry_nome.get()
        if nome:
            cursor.execute('INSERT INTO disciplinas (nome) VALUES (?)', (nome,))
            conn.commit()
            messagebox.showinfo("Sucesso", f'Disciplina "{nome}" inserida com sucesso!')
            janela.destroy()
        else:
            messagebox.showwarning("Erro", "O nome da disciplina não pode estar vazio.")

    janela = tk.Toplevel(root)
    janela.title("Inserir Disciplina")
    tk.Label(janela, text="Nome da Disciplina:").pack(pady=5)
    entry_nome = tk.Entry(janela)
    entry_nome.pack(pady=5)
    tk.Button(janela, text="Salvar", command=salvar_disciplina).pack(pady=10)

def consultar_disciplinas():
    janela = tk.Toplevel(root)
    janela.title("Consultar Disciplinas")
    tree = ttk.Treeview(janela, columns=("ID", "Nome"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.pack(fill=tk.BOTH, expand=True)

    cursor.execute('SELECT id, nome FROM disciplinas')
    disciplinas = cursor.fetchall()
    for disciplina in disciplinas:
        tree.insert("", tk.END, values=disciplina)

def eliminar_disciplina():
    def excluir_disciplina():
        disciplina_id = entry_id.get()
        if disciplina_id.isdigit():
            cursor.execute('SELECT id FROM disciplinas WHERE id = ?', (int(disciplina_id),))
            if cursor.fetchone() is None:
                messagebox.showwarning("Erro", f"Disciplina com ID {disciplina_id} não encontrada.")
            else:
                cursor.execute('DELETE FROM notas WHERE disciplina_id = ?', (int(disciplina_id),))
                cursor.execute('DELETE FROM disciplinas WHERE id = ?', (int(disciplina_id),))
                conn.commit()
                messagebox.showinfo("Sucesso", f"Disciplina com ID {disciplina_id} eliminada com sucesso!")
            janela.destroy()
        else:
            messagebox.showwarning("Erro", "O ID deve ser um número válido.")

    janela = tk.Toplevel(root)
    janela.title("Eliminar Disciplina")
    tk.Label(janela, text="ID da Disciplina:").pack(pady=5)
    entry_id = tk.Entry(janela)
    entry_id.pack(pady=5)
    tk.Button(janela, text="Excluir", command=excluir_disciplina).pack(pady=10)

# Função para consultar a grade de disciplinas
def consultar_grade():
    janela = tk.Toplevel(root)
    janela.title("Consultar Grade")
    janela.geometry("800x400")  # Define um tamanho fixo para a janela

    # Criação da tabela
    tree = ttk.Treeview(janela, columns=("ID", "Nome", "Unidade 1", "Unidade 2", "Unidade 3", "Unidade 4", "Prova", "Média", "Resultado"), show="headings", height=15)
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Unidade 1", text="Unidade 1")
    tree.heading("Unidade 2", text="Unidade 2")
    tree.heading("Unidade 3", text="Unidade 3")
    tree.heading("Unidade 4", text="Unidade 4")
    tree.heading("Prova", text="Prova")
    tree.heading("Média", text="Média")
    tree.heading("Resultado", text="Resultado")

    # Definir larguras fixas para as colunas
    tree.column("ID", width=50, anchor="center")
    tree.column("Nome", width=150, anchor="w")
    tree.column("Unidade 1", width=80, anchor="center")
    tree.column("Unidade 2", width=80, anchor="center")
    tree.column("Unidade 3", width=80, anchor="center")
    tree.column("Unidade 4", width=80, anchor="center")
    tree.column("Prova", width=80, anchor="center")
    tree.column("Média", width=80, anchor="center")
    tree.column("Resultado", width=100, anchor="center")

    # Desativar redimensionamento das colunas
    tree.bind("<Button-1>", lambda event: "break" if tree.identify_region(event.x, event.y) == "separator" else None)

    # Adicionar a tabela à janela
    tree.pack(fill=tk.BOTH, expand=True)

    # Consultar os dados do banco de dados
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

    # Inserir os dados na tabela
    for disciplina in disciplinas:
        tree.insert("", tk.END, values=disciplina)

# Função para inserir notas de uma disciplina
def inserir_notas():
    def salvar_notas():
        disciplina_id = entry_id.get()
        unidade1 = entry_u1.get()
        unidade2 = entry_u2.get()
        unidade3 = entry_u3.get()
        unidade4 = entry_u4.get()
        prova = entry_prova.get()

        if disciplina_id.isdigit():
            disciplina_id = int(disciplina_id)
            cursor.execute('SELECT id FROM disciplinas WHERE id = ?', (disciplina_id,))
            if cursor.fetchone() is None:
                messagebox.showwarning("Erro", f"Disciplina com ID {disciplina_id} não encontrada.")
            else:
                # Converter entradas para float ou None
                unidade1 = float(unidade1) if unidade1 else None
                unidade2 = float(unidade2) if unidade2 else None
                unidade3 = float(unidade3) if unidade3 else None
                unidade4 = float(unidade4) if unidade4 else None
                prova = float(prova) if prova else None

                # Calcular média e resultado final
                media_unidades = None
                resultado_final = None
                if None not in (unidade1, unidade2, unidade3, unidade4):
                    media_unidades = (unidade1 + unidade2 + unidade3 + unidade4) / 4
                    if prova is not None:
                        resultado_final = media_unidades * 0.4 + prova * 0.6

                # Inserir ou atualizar as notas no banco de dados
                cursor.execute('SELECT * FROM notas WHERE disciplina_id = ?', (disciplina_id,))
                if cursor.fetchone():
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
                    cursor.execute('''
                        INSERT INTO notas (disciplina_id, unidade1, unidade2, unidade3, unidade4, prova, media_unidades, resultado_final)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (disciplina_id, unidade1, unidade2, unidade3, unidade4, prova, media_unidades, resultado_final))

                conn.commit()
                messagebox.showinfo("Sucesso", f"Notas atualizadas para a disciplina ID {disciplina_id} com sucesso!")
                janela.destroy()
        else:
            messagebox.showwarning("Erro", "O ID deve ser um número válido.")

    janela = tk.Toplevel(root)
    janela.title("Inserir Notas")
    tk.Label(janela, text="ID da Disciplina:").pack(pady=5)
    entry_id = tk.Entry(janela)
    entry_id.pack(pady=5)

    tk.Label(janela, text="Nota Unidade 1:").pack(pady=5)
    entry_u1 = tk.Entry(janela)
    entry_u1.pack(pady=5)

    tk.Label(janela, text="Nota Unidade 2:").pack(pady=5)
    entry_u2 = tk.Entry(janela)
    entry_u2.pack(pady=5)

    tk.Label(janela, text="Nota Unidade 3:").pack(pady=5)
    entry_u3 = tk.Entry(janela)
    entry_u3.pack(pady=5)

    tk.Label(janela, text="Nota Unidade 4:").pack(pady=5)
    entry_u4 = tk.Entry(janela)
    entry_u4.pack(pady=5)

    tk.Label(janela, text="Nota Prova:").pack(pady=5)
    entry_prova = tk.Entry(janela)
    entry_prova.pack(pady=5)

    tk.Button(janela, text="Salvar", command=salvar_notas).pack(pady=10)

# Configuração da janela principal
root = tk.Tk()
root.title("Gerenciador de Disciplinas")

# Carregar imagens
img_inserir = PhotoImage(file="inserir.png")
img_consultar = PhotoImage(file="consultar.png")
img_eliminar = PhotoImage(file="eliminar.png")
img_grade = PhotoImage(file="grade.png")
img_notas = PhotoImage(file="notas.png")

# Barra de menus
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menu "Disciplinas"
menu_disciplinas = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Disciplinas", menu=menu_disciplinas)
menu_disciplinas.add_command(label="Inserir Disciplina", command=inserir_disciplina, image=img_inserir, compound=tk.LEFT)
menu_disciplinas.add_command(label="Consultar Disciplinas", command=consultar_disciplinas, image=img_consultar, compound=tk.LEFT)
menu_disciplinas.add_command(label="Eliminar Disciplina", command=eliminar_disciplina, image=img_eliminar, compound=tk.LEFT)
menu_disciplinas.add_command(label="Consultar Grade", command=consultar_grade, image=img_grade, compound=tk.LEFT)
menu_disciplinas.add_command(label="Inserir Notas", command=inserir_notas, image=img_notas, compound=tk.LEFT)

# Botão para sair
menu_bar.add_command(label="Sair", command=root.quit)

# Loop principal da interface gráfica
root.mainloop()

# Fecha a conexão com o banco de dados ao encerrar
conn.close()