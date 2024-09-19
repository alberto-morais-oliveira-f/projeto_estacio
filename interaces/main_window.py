import time
import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors
from .list_clients import ListClients  # Certifique-se de ajustar o caminho do import conforme necessário


class MainWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Controle De Clientes")
        self.root.geometry("800x600")  # Defina o tamanho da janela principal
        self.root.resizable(True, True)  # Permite redimensionar a janela
        self.show_splash()
        ListClients(self.root)

    def show_splash(self):
        splash = tk.Toplevel(self.root)  # Use Toplevel vinculado ao root
        splash.overrideredirect(True)  # Remove a borda da janela

        # Obter informações sobre o monitor principal
        primary_monitor = get_monitors()[0]
        screen_width = primary_monitor.width
        screen_height = primary_monitor.height

        # Definir o tamanho e a posição da janela splash para centralizar no monitor principal
        splash_width = 600
        splash_height = 400
        x = (screen_width // 2) - (splash_width // 2)
        y = (screen_height // 2) - (splash_height // 2)
        splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

        # Adicionar um rótulo com uma mensagem de splash
        label = ttk.Label(splash, text="Controle De Clientes\n", font=("Helvetica", 32))
        label.pack(expand=True)

        splash.update()

        # Mantém o splash na tela por 3 segundos usando after em vez de sleep
        self.root.after(3000, splash.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
