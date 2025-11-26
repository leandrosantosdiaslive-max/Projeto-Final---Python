import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter

# -----------------------------------------------------------
# BANCO DE DADOS
# -----------------------------------------------------------
def conectar():
    return sqlite3.connect('leads.db')


def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads(
            nome TEXT,
            email TEXT,
            telefone TEXT,
            interesse TEXT,
            status TEXT
        )  
    ''')
    conn.commit()
    conn.close()


# -----------------------------------------------------------
# CREATE
# -----------------------------------------------------------
def inserir_lead():
    nome = nome_entry.get()
    email = email_entry.get()
    telefone = telefone_entry.get()
    interesse = interesse_entry.get()
    status = status_combo.get()

    if nome and email and telefone and interesse:
        conn = conectar()
        c = conn.cursor()
        c.execute("INSERT INTO leads VALUES(?,?,?,?,?)",
                  (nome, email, telefone, interesse, status))
        conn.commit()
        conn.close()
        messagebox.showinfo('', 'LEAD CADASTRADO COM SUCESSO!')
        mostrar_leads()
    else:
        messagebox.showwarning('', 'PREENCHA TODOS OS CAMPOS!')


# -----------------------------------------------------------
# READ
# -----------------------------------------------------------
def mostrar_leads():
    for row in tree.get_children():
        tree.delete(row)

    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM leads')
    dados = c.fetchall()

    for lead in dados:
        tree.insert("", "end", values=lead)

    conn.close()


# -----------------------------------------------------------
# UPDATE
# -----------------------------------------------------------
def atualizar():
    selecao = tree.selection()
    if selecao:
        dado_edit = tree.item(selecao)['values'][1]  # usa email como chave

        novo_nome = nome_entry.get()
        novo_email = email_entry.get()
        novo_telefone = telefone_entry.get()
        novo_interesse = interesse_entry.get()
        novo_status = status_combo.get()

        if novo_nome and novo_email:
            conn = conectar()
            c = conn.cursor()
            c.execute("""UPDATE leads
                         SET nome=?, telefone=?, interesse=?, status=?, email=?
                         WHERE email = ?""",
                      (novo_nome, novo_telefone, novo_interesse,
                       novo_status, novo_email, dado_edit))
            conn.commit()
            conn.close()

            messagebox.showinfo('', 'LEAD ATUALIZADO COM SUCESSO!')
            mostrar_leads()
        else:
            messagebox.showwarning('', 'TODOS OS CAMPOS PRECISAM SER PREENCHIDOS')
    else:
        messagebox.showwarning('', 'SELECIONE UM LEAD PARA ATUALIZAR')


# -----------------------------------------------------------
# DELETE
# -----------------------------------------------------------
def delete_lead():
    selecao = tree.selection()
    if selecao:
        email_del = tree.item(selecao)['values'][1]

        conn = conectar()
        c = conn.cursor()
        c.execute("DELETE FROM leads WHERE email = ?", (email_del,))
        conn.commit()
        conn.close()

        messagebox.showinfo('', 'LEAD DELETADO COM SUCESSO')
        mostrar_leads()
    else:
        messagebox.showerror('', 'SELECIONE UM LEAD PARA DELETAR')


# -----------------------------------------------------------
# INTERFACE GRÁFICA
# -----------------------------------------------------------

janela = customtkinter.CTk()
janela.configure(fg_color='#444444')  # fundo
janela.title('GERENCIADOR DE LEADS - MARKETING DIGITAL')
janela.geometry('950x750')
caminho = 'm_ico.ico'
janela.iconbitmap(caminho)

tk.Label(
    janela,
    text='FORMULÁRIO DE LEADS',
    font=('Arial', 22, 'bold'),
    bg='#444444',
    fg='white'
).grid(row=0, column=0, pady=20)

# FRAME DO FORM
fr0 = customtkinter.CTkFrame(janela, fg_color='#DCDCDC', corner_radius=10)
fr0.grid(columnspan=3, pady=10, padx=20)

# Nome
tk.Label(fr0, text='Nome', font=('Arial', 15), bg='#DCDCDC').grid(row=1, column=0, pady=12, padx=15)
nome_entry = tk.Entry(fr0, font=('Arial', 15), width=28)
nome_entry.grid(row=1, column=1, pady=12, padx=15)

# E-mail
tk.Label(fr0, text='E-mail', font=('Arial', 15), bg='#DCDCDC').grid(row=2, column=0, pady=12, padx=15)
email_entry = tk.Entry(fr0, font=('Arial', 15), width=28)
email_entry.grid(row=2, column=1, pady=12, padx=15)

# Telefone
tk.Label(fr0, text='Telefone', font=('Arial', 15), bg='#DCDCDC').grid(row=3, column=0, pady=12, padx=15)
telefone_entry = tk.Entry(fr0, font=('Arial', 15), width=28)
telefone_entry.grid(row=3, column=1, pady=12, padx=15)

# Interesse
tk.Label(fr0, text='Interesse', font=('Arial', 15), bg='#DCDCDC').grid(row=4, column=0, pady=12, padx=15)
interesse_entry = tk.Entry(fr0, font=('Arial', 15), width=28)
interesse_entry.grid(row=4, column=1, pady=12, padx=15)

# Status
tk.Label(fr0, text='Status', font=('Arial', 15), bg='#DCDCDC').grid(row=5, column=0, pady=12, padx=15)
status_combo = ttk.Combobox(fr0, values=["Em andamento", "Convertido", "Perdido"],
                            font=('Arial', 15), width=26)
status_combo.current(0)
status_combo.grid(row=5, column=1, pady=12, padx=15)

# FRAME DOS BOTÕES
fr = customtkinter.CTkFrame(janela, fg_color='#DCDCDC', corner_radius=10)
fr.grid(columnspan=2, pady=20)

btn_salvar = customtkinter.CTkButton(fr, text='SALVAR', font=('Arial', 15),
                                     command=inserir_lead,
                                     fg_color='#6A0DAD', width=150)
btn_salvar.grid(row=0, column=0, padx=20, pady=15)

btn_atualizar = customtkinter.CTkButton(fr, text='ATUALIZAR', font=('Arial', 15),
                                        command=atualizar,
                                        fg_color='#6A0DAD', width=150)
btn_atualizar.grid(row=0, column=1, padx=20, pady=15)

btn_delete = customtkinter.CTkButton(fr, text='DELETAR', font=('Arial', 15),
                                     command=delete_lead,
                                     fg_color='#6A0DAD', width=150)
btn_delete.grid(row=0, column=2, padx=20, pady=15)

# FRAME DA TABELA
fr2 = customtkinter.CTkFrame(janela, fg_color='#DCDCDC', corner_radius=10)
fr2.grid(columnspan=2, pady=20, padx=20)

colunas = ('Nome', 'E-mail', 'Telefone', 'Interesse', 'Status')
tree = ttk.Treeview(fr2, columns=colunas, show='headings', height=18)
tree.grid(row=6, column=0, padx=15, pady=15, sticky='nsew')

for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=160)

# Inicializar
criar_tabela()
mostrar_leads()

janela.mainloop()