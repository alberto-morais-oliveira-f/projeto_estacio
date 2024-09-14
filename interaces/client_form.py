import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from services.database_service import SessionLocal
from models.client import Client


class ClientForm:
    def __init__(self, root, main_window):
        self.email_entry = None
        self.name_entry = None
        self.root = root
        self.main_window = main_window
        self.top = tk.Toplevel(root)
        self.top.title("Add/Edit Client")
        self.create_widgets()

    def create_widgets(self):
        # Formulário para adicionar/editar cliente
        ttk.Label(self.top, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = ttk.Entry(self.top)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.name_entry.focus_set()

        ttk.Label(self.top, text="Email:").grid(row=1, column=0, padx=10, pady=5)
        self.email_entry = ttk.Entry(self.top)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(self.top, text="Save", command=self.save_client).grid(row=2, column=0, columnspan=2, pady=10)

    def save_client(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        # Validar os dados
        if not name or not email:
            messagebox.showerror("Input Error", "Nome e Email são obrigatórios")
            return

        # Criar uma nova sessão para o banco de dados
        session = SessionLocal()
        try:
            # Verificar se o cliente já existe pelo email
            existing_client = session.query(Client).filter_by(email=email).first()
            if existing_client:
                messagebox.showerror("Input Error", "Já existe um cliente com esse email")
                return

            # Criar uma instância do modelo Client
            new_client = Client(name=name, email=email)
            session.add(new_client)
            session.commit()
            messagebox.showinfo("Success", "Cliente adicionado com sucesso")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"Ocorreu um error: {e}")
        finally:
            session.close()

        # Fechar a janela do formulário
        self.top.destroy()

        # Atualizar a Treeview na janela principal
        self.main_window.refresh_tree()
