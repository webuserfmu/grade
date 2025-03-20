import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import PhotoImage  # Para carregar imagens
import os
import sys

# Obter o caminho base do executável ou script
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # Caminho temporário usado pelo PyInstaller
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Caminhos para os arquivos
db_path = os.path.join(base_path, "projeto.db")
png_path = os.path.join(base_path, "png")

# Conexão com o banco de dados SQLite
conn = sqlite3.connect(db_path)
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
def criar_janela_filha(titulo):
    """Cria uma janela filha dentro do MDI."""
    child = tk.Toplevel(root)
    child.title(titulo)
    child.geometry("600x400")
    child.transient(root)  # Faz com que a janela filha fique acima da principal
    return child

def fechar_main_frame():
    """Limpa o conteúdo do main_frame."""
    for widget in main_frame.winfo_children():
        widget.destroy()

def inserir_disciplina():
    # Limpar o conteúdo existente no main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Adicionar título
    tk.Label(main_frame, text="Inserir Disciplina", font=("Arial", 16)).pack(pady=10)

    # Campo para inserir o nome da disciplina
    tk.Label(main_frame, text="Nome da Disciplina:").pack(pady=5)
    entry_nome = tk.Entry(main_frame)
    entry_nome.pack(pady=5)

    # Função para salvar a disciplina no banco de dados
    def salvar_disciplina():
        nome = entry_nome.get()
        if nome:
            cursor.execute('INSERT INTO disciplinas (nome) VALUES (?)', (nome,))
            conn.commit()
            messagebox.showinfo("Sucesso", f'Disciplina "{nome}" inserida com sucesso!')
            entry_nome.delete(0, tk.END)  # Limpar o campo de entrada
        else:
            messagebox.showwarning("Erro", "O nome da disciplina não pode estar vazio.")

    # Botão para salvar a disciplina
    tk.Button(main_frame, text="Salvar", command=salvar_disciplina).pack(pady=10)

    # Botão para fechar
    tk.Button(main_frame, text="Fechar", command=fechar_main_frame).pack(pady=10)

def consultar_disciplinas():
    # Limpar o conteúdo existente no main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Adicionar título
    tk.Label(main_frame, text="Consultar Disciplinas", font=("Arial", 16)).pack(pady=10)

    # Criação da tabela
    tree = ttk.Treeview(main_frame, columns=("ID", "Nome"), show="headings", height=15)
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.column("ID", width=50, anchor="center")
    tree.column("Nome", width=200, anchor="w")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Consultar os dados do banco de dados
    cursor.execute('SELECT id, nome FROM disciplinas')
    disciplinas = cursor.fetchall()

    # Inserir os dados na tabela
    for disciplina in disciplinas:
        tree.insert("", tk.END, values=disciplina)

    # Botão para fechar
    tk.Button(main_frame, text="Fechar", command=fechar_main_frame).pack(pady=10)

def eliminar_disciplina():
    # Limpar o conteúdo existente no main_frame
    fechar_main_frame()

    # Adicionar título
    tk.Label(main_frame, text="Eliminar Disciplina", font=("Arial", 16)).pack(pady=10)

    # Função para excluir a disciplina selecionada
    def excluir_disciplina():
        disciplina_nome = combo_disciplina.get()
        if disciplina_nome:
            cursor.execute('SELECT id FROM disciplinas WHERE nome = ?', (disciplina_nome,))
            result = cursor.fetchone()
            if result:
                disciplina_id = result[0]
                # Excluir as notas associadas e a disciplina
                cursor.execute('DELETE FROM notas WHERE disciplina_id = ?', (disciplina_id,))
                cursor.execute('DELETE FROM disciplinas WHERE id = ?', (disciplina_id,))
                conn.commit()
                messagebox.showinfo("Sucesso", f'Disciplina "{disciplina_nome}" eliminada com sucesso!')
                eliminar_disciplina()  # Atualizar a lista de disciplinas
            else:
                messagebox.showwarning("Erro", f'Disciplina "{disciplina_nome}" não encontrada.')
        else:
            messagebox.showwarning("Erro", "Selecione uma disciplina válida.")

    # Obter os nomes das disciplinas para o Combobox
    cursor.execute('SELECT nome FROM disciplinas')
    disciplinas = [row[0] for row in cursor.fetchall()]

    # Adicionar widgets para seleção e exclusão
    tk.Label(main_frame, text="Selecione a Disciplina:").pack(pady=5)
    combo_disciplina = ttk.Combobox(main_frame, values=disciplinas, state="readonly")
    combo_disciplina.pack(pady=5)
    tk.Button(main_frame, text="Excluir", command=excluir_disciplina).pack(pady=10)

    # Botão para fechar
    tk.Button(main_frame, text="Fechar", command=fechar_main_frame).pack(pady=10)

# Função para consultar a grade de disciplinas
def consultar_grade():
    # Limpar o conteúdo existente no main form
    fechar_main_frame()

    # Adicionar título
    tk.Label(main_frame, text="Consultar Grade", font=("Arial", 16)).pack(pady=10)

    # Criação da tabela
    tree = ttk.Treeview(main_frame, columns=("ID", "Nome", "Unidade 1", "Unidade 2", "Unidade 3", "Unidade 4", "Prova", "Média", "Resultado"), show="headings", height=15)
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

    # Adicionar a tabela ao frame principal
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Configurar estilos de tags
    tree.tag_configure("yellow", background="yellow")
    tree.tag_configure("green", background="green")
    tree.tag_configure("red", background="red")

    # Consultar os dados do banco de dados
    cursor.execute('''
        SELECT d.id, d.nome, 
               COALESCE(n.unidade1, '') AS unidade1, 
               COALESCE(n.unidade2, '') AS unidade2, 
               COALESCE(n.unidade3, '') AS unidade3, 
               COALESCE(n.unidade4, '') AS unidade4, 
               COALESCE(n.prova, '') AS prova, 
               CASE 
                   WHEN n.unidade1 IS NOT NULL AND n.unidade2 IS NOT NULL AND n.unidade3 IS NOT NULL AND n.unidade4 IS NOT NULL THEN 
                       ROUND((n.unidade1 + n.unidade2 + n.unidade3 + n.unidade4) / 4, 2)
                   ELSE ''
               END AS media_unidades, 
               CASE 
                   WHEN n.unidade1 IS NOT NULL AND n.unidade2 IS NOT NULL AND n.unidade3 IS NOT NULL AND n.unidade4 IS NOT NULL AND n.prova IS NOT NULL THEN 
                       ROUND(((n.unidade1 + n.unidade2 + n.unidade3 + n.unidade4) / 4) * 0.4 + n.prova * 0.6, 2)
                   ELSE ''
               END AS resultado_final
        FROM disciplinas d
        LEFT JOIN notas n ON d.id = n.disciplina_id
    ''')
    disciplinas = cursor.fetchall()

    # Inserir os dados na tabela com as cores apropriadas
    for disciplina in disciplinas:
        resultado_final = disciplina[8]  # Índice da coluna "Resultado"
        if resultado_final == '':
            tag = "yellow"
        elif float(resultado_final) >= 6:
            tag = "green"
        else:
            tag = "red"
        tree.insert("", tk.END, values=disciplina, tags=(tag,))

    # Botão para fechar
    tk.Button(main_frame, text="Fechar", command=fechar_main_frame).pack(pady=10)

# Função para inserir notas de uma disciplina
def inserir_notas():
    # Limpar o conteúdo existente no main_frame
    fechar_main_frame()

    # Adicionar título
    tk.Label(main_frame, text="Inserir Notas", font=("Arial", 16)).pack(pady=10)

    # Obter os nomes das disciplinas para o Combobox
    cursor.execute('SELECT nome FROM disciplinas')
    disciplinas = [row[0] for row in cursor.fetchall()]

    tk.Label(main_frame, text="Disciplina:").pack(pady=5)
    combo_disciplina = ttk.Combobox(main_frame, values=disciplinas, state="readonly")
    combo_disciplina.pack(pady=5)

    # Campos de entrada para as notas
    tk.Label(main_frame, text="Nota Unidade 1:").pack(pady=5)
    entry_u1 = tk.Entry(main_frame)
    entry_u1.pack(pady=5)

    tk.Label(main_frame, text="Nota Unidade 2:").pack(pady=5)
    entry_u2 = tk.Entry(main_frame)
    entry_u2.pack(pady=5)

    tk.Label(main_frame, text="Nota Unidade 3:").pack(pady=5)
    entry_u3 = tk.Entry(main_frame)
    entry_u3.pack(pady=5)

    tk.Label(main_frame, text="Nota Unidade 4:").pack(pady=5)
    entry_u4 = tk.Entry(main_frame)
    entry_u4.pack(pady=5)

    tk.Label(main_frame, text="Nota Prova:").pack(pady=5)
    entry_prova = tk.Entry(main_frame)
    entry_prova.pack(pady=5)

    # Função para carregar os valores existentes no banco de dados
    def carregar_notas(event):
        disciplina_nome = combo_disciplina.get()
        cursor.execute('''
            SELECT unidade1, unidade2, unidade3, unidade4, prova
            FROM notas
            INNER JOIN disciplinas ON notas.disciplina_id = disciplinas.id
            WHERE disciplinas.nome = ?
        ''', (disciplina_nome,))
        result = cursor.fetchone()

        # Preencher os campos com os valores existentes ou limpar se não houver valores
        if result:
            entry_u1.delete(0, tk.END)
            entry_u1.insert(0, result[0] if result[0] is not None else "")

            entry_u2.delete(0, tk.END)
            entry_u2.insert(0, result[1] if result[1] is not None else "")

            entry_u3.delete(0, tk.END)
            entry_u3.insert(0, result[2] if result[2] is not None else "")

            entry_u4.delete(0, tk.END)
            entry_u4.insert(0, result[3] if result[3] is not None else "")

            entry_prova.delete(0, tk.END)
            entry_prova.insert(0, result[4] if result[4] is not None else "")
        else:
            # Limpar os campos se não houver notas
            entry_u1.delete(0, tk.END)
            entry_u2.delete(0, tk.END)
            entry_u3.delete(0, tk.END)
            entry_u4.delete(0, tk.END)
            entry_prova.delete(0, tk.END)

    # Vincular a seleção do Combobox à função de carregar notas
    combo_disciplina.bind("<<ComboboxSelected>>", carregar_notas)

    # Função para salvar as notas no banco de dados
    def salvar_notas():
        disciplina_nome = combo_disciplina.get()
        unidade1 = entry_u1.get()
        unidade2 = entry_u2.get()
        unidade3 = entry_u3.get()
        unidade4 = entry_u4.get()
        prova = entry_prova.get()

        # Obter o ID da disciplina com base no nome selecionado
        cursor.execute('SELECT id FROM disciplinas WHERE nome = ?', (disciplina_nome,))
        result = cursor.fetchone()
        if result:
            disciplina_id = result[0]
        else:
            messagebox.showwarning("Erro", "Selecione uma disciplina válida.")
            return

        # Converter entradas para float ou None
        try:
            unidade1 = float(unidade1) if unidade1 else None
            unidade2 = float(unidade2) if unidade2 else None
            unidade3 = float(unidade3) if unidade3 else None
            unidade4 = float(unidade4) if unidade4 else None
            prova = float(prova) if prova else None
        except ValueError:
            messagebox.showwarning("Erro", "Insira valores numéricos válidos para as notas.")
            return

        # Calcular média e resultado final apenas se todas as unidades forem fornecidas
        media_unidades = None
        resultado_final = None
        if None not in (unidade1, unidade2, unidade3, unidade4):
            media_unidades = (unidade1 + unidade2 + unidade3 + unidade4) / 4
            if prova is not None:
                resultado_final = media_unidades * 0.4 + prova * 0.6

        # Inserir ou atualizar as notas no banco de dados
        cursor.execute('SELECT * FROM notas WHERE disciplina_id = ?', (disciplina_id,))
        if cursor.fetchone():
            # Atualizar os campos, permitindo que valores vazios sejam definidos como NULL
            cursor.execute('''
                UPDATE notas
                SET unidade1 = ?,
                    unidade2 = ?,
                    unidade3 = ?,
                    unidade4 = ?,
                    prova = ?,
                    media_unidades = ?,
                    resultado_final = ?
                WHERE disciplina_id = ?
            ''', (unidade1, unidade2, unidade3, unidade4, prova, media_unidades, resultado_final, disciplina_id))
        else:
            # Inserir apenas se pelo menos um valor for fornecido
            if any(value is not None for value in [unidade1, unidade2, unidade3, unidade4, prova]):
                cursor.execute('''
                    INSERT INTO notas (disciplina_id, unidade1, unidade2, unidade3, unidade4, prova, media_unidades, resultado_final)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (disciplina_id, unidade1, unidade2, unidade3, unidade4, prova, media_unidades, resultado_final))
            else:
                messagebox.showwarning("Erro", "Insira pelo menos um valor para atualizar as notas.")
                return

        conn.commit()
        messagebox.showinfo("Sucesso", f"Notas atualizadas para a disciplina '{disciplina_nome}' com sucesso!")

    # Botão para salvar as notas
    tk.Button(main_frame, text="Salvar", command=salvar_notas).pack(pady=10)

    # Botão para fechar
    tk.Button(main_frame, text="Fechar", command=fechar_main_frame).pack(pady=10)

def executar_consulta_sql():
    # Criar uma nova janela para a consulta SQL
    janela_sql = tk.Toplevel(root)
    janela_sql.title("Executar Consulta SQL")
    janela_sql.geometry("1000x600")  # Define o tamanho da janela

    # Tornar a janela sempre no topo
    janela_sql.attributes("-topmost", True)

    # Centralizar a janela na tela
    largura_janela = 1000
    altura_janela = 600
    largura_tela = janela_sql.winfo_screenwidth()
    altura_tela = janela_sql.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    janela_sql.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    # Adicionar título
    tk.Label(janela_sql, text="Executar Consulta SQL", font=("Arial", 16)).pack(pady=10)

    # Frame para exibir as tabelas e campos
    frame_explorar = tk.Frame(janela_sql)
    frame_explorar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Listbox para exibir as tabelas
    tk.Label(frame_explorar, text="Tabelas:", font=("Arial", 12)).pack(pady=5)
    listbox_tabelas = tk.Listbox(frame_explorar, height=15, width=30)
    listbox_tabelas.pack(fill=tk.BOTH, expand=True)

    # Listbox para exibir os campos da tabela selecionada
    tk.Label(frame_explorar, text="Campos:", font=("Arial", 12)).pack(pady=5)
    listbox_campos = tk.Listbox(frame_explorar, height=15, width=30)
    listbox_campos.pack(fill=tk.BOTH, expand=True)

    # Frame para entrada da consulta SQL
    frame_sql = tk.Frame(janela_sql)
    frame_sql.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Campo de entrada para a consulta SQL
    tk.Label(frame_sql, text="Digite sua consulta SQL:").pack(pady=5)
    entry_sql = tk.Text(frame_sql, height=5, width=80, wrap=tk.WORD)
    entry_sql.pack(pady=5)

    # Frame para exibir os resultados
    result_frame = tk.Frame(janela_sql)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Função para carregar as tabelas do banco de dados
    def carregar_tabelas():
        listbox_tabelas.delete(0, tk.END)
        # Excluir a tabela sqlite_sequence da lista
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
        tabelas = cursor.fetchall()
        for tabela in tabelas:
            listbox_tabelas.insert(tk.END, tabela[0])

    # Função para carregar os campos da tabela selecionada
    def carregar_campos(event):
        listbox_campos.delete(0, tk.END)
        tabela_selecionada = listbox_tabelas.get(listbox_tabelas.curselection())
        cursor.execute(f"PRAGMA table_info({tabela_selecionada})")
        campos = cursor.fetchall()
        for campo in campos:
            nome = campo[1]
            tipo = campo[2]
            listbox_campos.insert(tk.END, f"{nome} - {tipo}")

    # Vincular o evento de seleção de tabela
    listbox_tabelas.bind("<<ListboxSelect>>", carregar_campos)

    # Função para executar a consulta SQL
    def executar():
        query = entry_sql.get("1.0", tk.END).strip()  # Obter o texto do campo
        if not query:
            messagebox.showwarning("Erro", "A consulta SQL não pode estar vazia.")
            return

        try:
            cursor.execute(query)
            conn.commit()
            resultados = cursor.fetchall()

            # Limpar resultados anteriores
            for widget in result_frame.winfo_children():
                widget.destroy()

            # Exibir os resultados em uma tabela
            if resultados:
                colunas = [desc[0] for desc in cursor.description]
                tree = ttk.Treeview(result_frame, columns=colunas, show="headings")
                for col in colunas:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=100)
                tree.pack(fill=tk.BOTH, expand=True)

                for row in resultados:
                    tree.insert("", tk.END, values=row)
            else:
                tk.Label(result_frame, text="Consulta executada com sucesso, sem resultados para exibir.", font=("Arial", 12)).pack(pady=10)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao executar a consulta SQL:\n{e}")

    # Botão para executar a consulta
    tk.Button(frame_sql, text="Executar", command=executar).pack(pady=10)

    # Botão para fechar a janela
    tk.Button(janela_sql, text="Fechar", command=janela_sql.destroy).pack(pady=10)

    # Carregar as tabelas ao abrir a janela
    carregar_tabelas()

# Configuração da janela principal (MDI Form)
root = tk.Tk()
root.title("Gerenciador de Disciplinas - MDI")
root.geometry("800x600")  # Dimensão inicial (opcional)
root.state('zoomed')  # Inicia a janela maximizada

# Frame principal para exibir o conteúdo
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Carregar imagens
img_inserir = PhotoImage(file=os.path.join(png_path, "inserir.png"))
img_consultar = PhotoImage(file=os.path.join(png_path, "consultar.png"))
img_eliminar = PhotoImage(file=os.path.join(png_path, "eliminar.png"))
img_grade = PhotoImage(file=os.path.join(png_path, "grade.png"))
img_notas = PhotoImage(file=os.path.join(png_path, "notas.png"))

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

# Adicionar menu "Utilitários"
menu_utilitarios = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Utilitários", menu=menu_utilitarios)
menu_utilitarios.add_command(label="Executar Consulta SQL", command=executar_consulta_sql)


# Botão para sair
menu_bar.add_command(label="Sair", command=root.quit)

root.mainloop()
conn.close()