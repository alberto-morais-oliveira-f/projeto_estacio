from interaces.main_window import MainWindow
from tkinter import Tk

root = Tk()

def main():
    app = MainWindow(root)
    root.mainloop()

# Função para ajustar a janela para tela cheia
def enter_fullscreen(event=None):
    root.attributes('-fullscreen', True)

# Função para sair do modo tela cheia
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)

root.bind("<Escape>", exit_fullscreen)

root.bind("<F11>", enter_fullscreen)

if __name__ == "__main__":
    main()
