import tkinter as tk
from tkinter import ttk
from admin_gui import InterfazAdmin
from usuario_gui import InterfazUsuario
from soporte_tecnico_gui import InterfazSoporteTecnico
from mesa_ayuda_gui import InterfazMesaAyuda
from ejecutivo_gui import InterfazEjecutivo 
from jefe_mesa_gui import InterfazJefeMesa

class BaseGUI:
    def __init__(self, root, mostrar_login):
        self.root = root
        self.root.title("Sistema de Gestión de Tickets")
        self.mostrar_login = mostrar_login
        self.menu = ttk.Notebook(self.root)
        self.menu.grid(row=0, column=0, sticky="NSEW")

    def app_principal(self, tipo_usuario, usuario, correo, area_especializada=None):
        for widget in self.root.winfo_children():
            widget.grid_forget()
        self.menu = ttk.Notebook(self.root)
        self.menu.grid(row=0, column=0, sticky="NSEW")
    
        if tipo_usuario == "Administrador":
            InterfazAdmin(self.root, self.menu, self.mostrar_login)
        elif tipo_usuario == "Usuario":
            InterfazUsuario(self.root, self.menu, usuario, correo, self.mostrar_login)
        elif tipo_usuario == "Técnico de Soporte":
            InterfazSoporteTecnico(self.root, self.menu, area_especializada, self.mostrar_login)
        elif tipo_usuario == "Mesa de Ayuda":
            InterfazMesaAyuda(self.root, self.menu, self.mostrar_login)
        elif tipo_usuario == "Ejecutivo":
            InterfazEjecutivo(self.root, self.menu, area_especializada, self.mostrar_login)
        elif tipo_usuario == "Jefe de Mesa":
            InterfazJefeMesa(self.root, self.menu, self.mostrar_login)

        self.menu.grid(row=0, column=0, sticky="NSEW")
