import streamlit as st
import sqlite3
import pandas as pd

# Função para criar uma conexão com o banco de dados SQLite
def create_connection():
    conn = sqlite3.connect("data.db")
    return conn

# Função para criar a tabela no banco de dados, se ela não existir
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Função para adicionar um usuário ao banco de dados
def add_user(name, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

# Função para buscar todos os usuários no banco de dados
def get_all_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Função para deletar um usuário do banco de dados
def delete_user(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()

# Função para atualizar um usuário no banco de dados
def update_user(id, name, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name=?, email=? WHERE id=?", (name, email, id))
    conn.commit()
    conn.close()

# Função principal para executar o aplicativo
def main():
    st.title("CRUD com Streamlit e SQLite")

    create_table()

    # Sidebar para adicionar/editar usuários
    st.sidebar.header("Adicionar/Editar Usuário")
    selected_user = st.sidebar.selectbox("Selecionar Usuário", ["Novo"] + [f"{user[1]} - {user[2]}" for user in get_all_users()])
    name = ""
    email = ""
    if selected_user != "Novo":
        user_id = int(selected_user.split(" - ")[0])
        user_data = [user for user in get_all_users() if user[0] == user_id][0]
        name = user_data[1]
        email = user_data[2]
    name = st.sidebar.text_input("Nome", name)
    email = st.sidebar.text_input("Email", email)
    if st.sidebar.button("Salvar"):
        if selected_user == "Novo":
            add_user(name, email)
            st.sidebar.success("Usuário adicionado com sucesso!")
        else:
            user_id = int(selected_user.split(" - ")[0])
            update_user(user_id, name, email)
            st.sidebar.success("Usuário atualizado com sucesso!")

    # Listagem de usuários em formato de tabela
    st.header("Lista de Usuários")
    users_df = pd.DataFrame(get_all_users(), columns=["ID", "Nome", "Email"])
    st.dataframe(users_df)

    # Opção para deletar usuário
    if st.button("Deletar Usuário"):
        selected_user_id = st.text_input("ID do Usuário")
        if selected_user_id:
            delete_user(int(selected_user_id))
            st.success("Usuário deletado com sucesso!")

if __name__ == "__main__":
    main()
