import tkinter as tk
from base_gui import BaseGUI
from login import LoginRegistro

def lanzar_aplicacion_principal(tipo_usuario, usuario, correo):
    root = tk.Tk()
    root.geometry("800x600")
    app = BaseGUI(root, mostrar_login)
    app.app_principal(tipo_usuario, usuario, correo)
    root.mainloop()

def mostrar_login():
    root = tk.Tk()
    root.geometry("800x600")
    app = LoginRegistro(root, lanzar_aplicacion_principal)
    root.mainloop()

def main():
    mostrar_login()

if __name__ == "__main__":
    main()
