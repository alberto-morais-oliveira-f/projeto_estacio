import tkinter as tk
from tkinter import ttk, messagebox

from models.client import Client
from services.database_service import SessionLocal
from .client_form import ClientForm

class MainWindow:
    def __init__(self, root):
        self.remove_client = None
        self.remove_client_button = None
        self.tree = None
        self.add_client_button = None
        self.root = root
        self.root.title("Client Management System")
        self.root.attributes("-fullscreen", True)
        self.create_widgets()

    def create_widgets(self):
        # Frame para os botões
        button_frame = ttk.Frame(self.root)
        button_frame.pack(padx=10, pady=10, side=tk.TOP, fill=tk.X)

        self.add_client_button = ttk.Button(button_frame, text="Add Client", command=self.open_client_form)
        self.add_client_button.pack(side=tk.LEFT, padx=5)

        # Botão para remover cliente
        self.remove_client_button = ttk.Button(button_frame, text="Remove Client", command=self.remove_client)
        self.remove_client_button.pack(side=tk.LEFT, padx=5)

        # Frame para a Treeview
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Treeview para exibir clientes
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def open_client_form(self):
        ClientForm(self.root, self)

    def refresh_tree(self):
        # Limpar a Treeview antes de atualizar
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Criar uma nova sessão para o banco de dados
        session = SessionLocal()
        try:
            # Consultar todos os clientes
            clients = session.query(Client).all()
            for client in clients:
                # Inserir dados na Treeview
                self.tree.insert("", "end", values=(client.id, client.name, client.email))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            session.close()
