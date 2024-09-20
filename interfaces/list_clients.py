import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from utils.MaskPhone import format_phone
from tkinter import PhotoImage
from .client_form import ClientForm
from services.database_service import SessionLocal
from models.client import Client

# Importando o novo serviço
from services.google_drive_service import GoogleDriveService


def load_icon(file_path):
    return PhotoImage(file=file_path)


class ListClients:

    def __init__(self, root):
        self.googleService = GoogleDriveService();
        self.next_button = None
        self.page_label = None
        self.prev_button = None
        self.filter_entry = None
        self.tree = None
        self.button_frame = None
        self.root = root
        self.root.title("Gestão de Clientes")

        self.trash_icon = load_icon("resources/images/4021663.png")
        self.drive_icon = load_icon("resources/images/drive_icon.png")
        self.edit_icon = load_icon("resources/images/edit_icon.png")
        self.trash_buttons = {}
        self.edit_buttons = {}
        self.upload_buttons = {}

        # Variáveis de paginação
        self.page_size = 10
        self.current_page = 1
        self.total_pages = 1

        self.create_styles()
        self.create_widgets()
        self.refresh_tree()

        # Ocupando o tamanho total da tela disponível
        self.root.attributes('-zoomed', True)  # No Windows
        self.root.geometry(
            "{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))  # Em Linux
        self.root.resizable(True, True)  # Permite redimensionar a janela

    def create_styles(self):
        style = ttk.Style(self.root)
        style.configure("Treeview.Heading", anchor="center")
        style.configure("Treeview", rowheight=40, font=("Arial", 12))
        style.map("Treeview", background=[('selected', 'darkblue')], foreground=[('selected', 'white')])
        style.map("Treeview.Cell", padding=[('selected', 2)])
        style.configure("striped.Treeview", background=['#F0F0F0', '#FFFFFF'])

    def create_widgets(self):
        self.button_frame = self.create_button_frame()
        self.create_add_client_button()
        self.create_filter_entry()
        self.tree = self.create_treeview()
        self.tree.bind("<Button-1>", self.on_tree_click)  # Bind click event
        self.create_pagination_buttons()

    def create_button_frame(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(padx=10, pady=10, side=tk.TOP, fill=tk.X)
        return button_frame

    def create_add_client_button(self):
        add_client_button = ttk.Button(self.button_frame, text="Adicionar Cliente", command=self.open_client_form)
        add_client_button.pack(side=tk.LEFT, padx=5)

    def create_filter_entry(self):
        filter_label = ttk.Label(self.button_frame, text="Filtrar Clientes:")
        filter_label.pack(side=tk.RIGHT, padx=(0, 5))

        self.filter_entry = ttk.Entry(self.button_frame)
        self.filter_entry.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        self.filter_entry.bind("<KeyRelease>", self.filter_clients)  # Dynamic filtering

    def create_pagination_buttons(self):
        pagination_frame = ttk.Frame(self.root)
        pagination_frame.pack(padx=10, pady=10, side=tk.BOTTOM, fill=tk.X)

        self.prev_button = ttk.Button(pagination_frame, text="Voltar Página", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.page_label = ttk.Label(pagination_frame, text=f"Página {self.current_page}")
        self.page_label.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(pagination_frame, text="Próxima Página", command=self.next_page)
        self.next_button.pack(side=tk.LEFT, padx=5)

    def create_treeview(self):
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Email", "Phone", "Actions"), show="headings",
                            style="striped.Treeview")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name", anchor="center")
        tree.heading("Email", text="Email", anchor="center")
        tree.heading("Phone", text="Telefone", anchor="center")
        tree.heading("Actions", text="Ações", anchor="center")
        tree.column("ID", anchor="center")
        tree.column("Name", anchor="center")
        tree.column("Email", anchor="center")
        tree.column("Phone", anchor="center")
        tree.column("Actions", anchor="center", width=200)
        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        return tree

    def open_client_form(self):
        ClientForm(self.root, self)

    def refresh_tree(self, query=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Limpar todos os botões antigos
        for btn in self.edit_buttons.values():
            btn.destroy()
        for btn in self.upload_buttons.values():
            btn.destroy()
        for btn in self.trash_buttons.values():
            btn.destroy()

        self.edit_buttons.clear()
        self.upload_buttons.clear()
        self.trash_buttons.clear()

        session = SessionLocal()
        try:
            base_query = session.query(Client)
            if query:
                base_query = base_query.filter(Client.name.ilike(f"%{query}%"))

            total_items = base_query.count()
            self.total_pages = total_items // self.page_size + (1 if total_items % self.page_size else 0)

            clients = base_query.offset((self.current_page - 1) * self.page_size).limit(self.page_size).all()

            for client in clients:
                self.tree.insert("", "end", iid=client.id,
                                 values=(client.id, client.name, client.email, format_phone(client.phone)))
            self.root.after(100, self.add_action_buttons_to_tree)

            # Atualizar o estado dos botões de paginação
            self.prev_button.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
            self.next_button.config(state=tk.NORMAL if self.current_page < self.total_pages else tk.DISABLED)
            self.page_label.config(text=f"Página {self.current_page} de {self.total_pages}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocorreu um erro: {e}")
        finally:
            session.close()

    def add_action_buttons_to_tree(self):
        for item in self.tree.get_children():
            self.add_action_buttons(item)

    def add_action_buttons(self, item_id):
        try:
            x, y, width, height = self.tree.bbox(item_id, column="#5")
            if width > 0:
                edit_btn = tk.Button(self.tree, image=self.edit_icon, command=lambda: self.edit_client(item_id), bd=0)
                upload_btn = tk.Button(self.tree, image=self.drive_icon, command=lambda: self.googleService.select_and_upload_file(self.tree.item(item_id, 'values')[1]),
                                       bd=0, foreground="white")
                trash_btn = tk.Button(self.tree, image=self.trash_icon, command=lambda: self.delete_client(item_id),
                                      bd=0)

                button_width = self.trash_icon.width()
                spacing = 20
                edit_btn.place(x=x + (width - 3 * button_width - 2 * spacing) // 2,
                               y=y + (height - self.edit_icon.height()) // 2)
                upload_btn.place(x=x + (width - button_width + -10) // 2,
                                 y=y + (height - 24) // 2)
                trash_btn.place(x=x + (width + button_width + spacing) // 2,
                                y=y + (height - self.trash_icon.height()) // 2)

                self.edit_buttons[item_id] = edit_btn
                self.upload_buttons[item_id] = upload_btn
                self.trash_buttons[item_id] = trash_btn
        except tk.TclError:
            pass

    def on_tree_click(self, event):
        item_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if column == "#5":
            if item_id in self.trash_buttons and self.trash_buttons[item_id].winfo_contains(event.x_root, event.y_root):
                self.delete_client(item_id)
            elif item_id in self.edit_buttons and self.edit_buttons[item_id].winfo_contains(event.x_root, event.y_root):
                self.edit_client(item_id)

    def delete_client(self, item_id):
        confirm = messagebox.askyesno("Confirme que quer Deletar",
                                      "Tem certeza de que deseja excluir o cliente selecionado?")
        if confirm:
            selected_client_id = self.tree.item(item_id, 'values')[0]
            session = SessionLocal()
            try:

                client_to_remove = session.query(Client).filter(Client.id == selected_client_id).first()
                if client_to_remove:
                    session.delete(client_to_remove)
                    session.commit()
                    messagebox.showinfo("Success", "Cliente removido com sucesso")

                    self.tree.delete(item_id)
                    if item_id in self.edit_buttons:
                        self.edit_buttons[item_id].destroy()
                        del self.edit_buttons[item_id]
                    if item_id in self.upload_buttons:
                        self.upload_buttons[item_id].destroy()
                        del self.upload_buttons[item_id]
                    if item_id in self.trash_buttons:
                        self.trash_buttons[item_id].destroy()
                        del self.trash_buttons[item_id]
                else:
                    messagebox.showerror("Error", "Cliente não encontrado")
            except Exception as e:
                session.rollback()
                messagebox.showerror("Error", f"Ocorreu um erro: {e}")
            finally:
                session.close()
            self.refresh_tree()

    def edit_client(self, item_id):
        selected_client_id = self.tree.item(item_id, 'values')[0]
        ClientForm(self.root, self, client_id=selected_client_id)

    def filter_clients(self, event):
        query = self.filter_entry.get()
        self.current_page = 1  # Reset to first page on filter
        self.refresh_tree(query)

    def next_page(self):
        self.current_page += 1
        self.refresh_tree(self.filter_entry.get())

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_tree(self.filter_entry.get())


if __name__ == "__main__":
    root = tk.Tk()
    app = ListClients(root)
    root.mainloop()