import tkinter as tk
from .list_clients import ListClients

class MainWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Client Management System")
        self.root.attributes("-fullscreen", True)
        ListClients(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
