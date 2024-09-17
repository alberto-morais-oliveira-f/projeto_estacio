from models.client import Client
from tkinter import messagebox

from services.database_service import SessionLocal

class ClientService:
    def __init__(self):
        self.client = Client

    def save_client(self, client_id, name, email, phone):
        session = SessionLocal()
        try:
            if client_id:
                client = session.query(self.client).filter(Client.id == client_id).first()
                if client:
                    client.name = name
                    client.email = email
                    client.phone = phone
                    session.commit()
                    messagebox.showinfo("Success", "Client updated successfully")
            else:
                new_client = Client(name=name, email=email, phone=phone)
                session.add(new_client)
                session.commit()
                messagebox.showinfo("Success", "Client added successfully")
        except Exception as e:
            print(e)
            session.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            session.close()
