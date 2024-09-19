from tkinter import Toplevel, Label, Entry, Button, messagebox, StringVar
from tkinter import E, W
import re
from services.ClientService import ClientService
from models.client import Client
from services.database_service import SessionLocal
from validations.validation_service import is_valid_email, is_valid_phone
from utils.MaskPhone import MaskPhone

class ClientForm:
    def __init__(self, parent, main_app, client_id=None):
        self.submit_button = None
        self.phone_entry = None
        self.email_entry = None
        self.name_entry = None
        self.parent = parent
        self.main_app = main_app
        self.client_id = client_id

        self.window = Toplevel(parent)
        self.window.title("Cadastrar Cliente")

        self.phone_var = StringVar()

        self.create_widgets()
        self.window.update_idletasks()
        self.window.minsize(400, self.window.winfo_height())

        self.center_window()

        if self.client_id:
            self.load_client_data()

        # Utilizar a classe MaskPhone para formatar a entrada do telefone
        self.mask_phone = MaskPhone(self.phone_var, self.phone_entry)

    def create_widgets(self):
        # Configuração do layout
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=3)

        Label(self.window, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky=E)
        self.name_entry = Entry(self.window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=E + W)

        Label(self.window, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky=E)
        self.email_entry = Entry(self.window)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5, sticky=E + W)

        Label(self.window, text="Telefone:").grid(row=2, column=0, padx=10, pady=5, sticky=E)
        self.phone_entry = Entry(self.window, textvariable=self.phone_var)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5, sticky=E + W)

        self.submit_button = Button(self.window, text="Save", command=self.save_client)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def center_window(self):
        main_width = self.parent.winfo_width()
        main_height = self.parent.winfo_height()
        main_x = self.parent.winfo_rootx()
        main_y = self.parent.winfo_rooty()

        self.window.update_idletasks()

        width = max(400, self.window.winfo_width())
        height = self.window.winfo_height()

        x = main_x + (main_width // 2) - (width // 2)
        y = main_y + (main_height // 2) - (height // 2)

        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def load_client_data(self):
        session = SessionLocal()
        try:
            client = session.query(Client).filter(Client.id == self.client_id).first()
            if client:
                self.name_entry.insert(0, client.name)
                self.email_entry.insert(0, client.email)
                self.phone_var.set(client.phone)
        except Exception as e:
            messagebox.showerror("Error", f"Ocorreu um erro: {e}")
        finally:
            session.close()

    def save_client(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_var.get()

        if len(name) < 3:
            messagebox.showwarning("Input error", "Name must have at least 3 characters.")
            return

        if not is_valid_email(email):
            messagebox.showwarning("Input error", "Invalid email address.")
            return

        if not is_valid_phone(phone):
            messagebox.showwarning("Input error", "Phone must be in the format (xx) xxxxx-xxxx.")
            return

        phone = re.sub(r'\D', '', phone)  # Remove phone mask

        try:
            client_service = ClientService()
            client_service.save_client(self.client_id, name, email, phone)
            self.window.destroy()
            self.main_app.refresh_tree()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"Ocorreu um erro: {e}")
