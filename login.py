import tkinter as tk
from tkinter import ttk, messagebox
from usuarios import validar_usuario, crear_usuario, correo_existe

class LoginRegistro:
    def __init__(self, root, lanzar_aplicacion_principal):
        self.root = root
        self.root.title("Sistema de Gestión de Tickets - Login y Registro")
        self.lanzar_aplicacion_principal = lanzar_aplicacion_principal
        self.crear_login()

    def crear_login(self):
        frame_login = ttk.Frame(self.root, padding="10")
        frame_login.grid(row=0, column=0, sticky="EW")

        ttk.Label(frame_login, text="Usuario:").grid(row=0, column=0, sticky="W")
        self.usuario_entry = ttk.Entry(frame_login)
        self.usuario_entry.grid(row=0, column=1, sticky="EW")

        ttk.Label(frame_login, text="Contraseña:").grid(row=1, column=0, sticky="W")
        self.contraseña_entry = ttk.Entry(frame_login, show="*")
        self.contraseña_entry.grid(row=1, column=1, sticky="EW")

        ttk.Button(frame_login, text="Iniciar Sesión", command=self.login).grid(row=2, columnspan=2)

        ttk.Button(frame_login, text="Registrar", command=self.crear_registro).grid(row=3, columnspan=2)

    def login(self):
        nombre_usuario = self.usuario_entry.get()
        contraseña = self.contraseña_entry.get()
        valido, tipo_usuario, correo, activo = validar_usuario(nombre_usuario, contraseña)
        if valido:
            if activo:
                messagebox.showinfo("Login exitoso", f"Bienvenido {tipo_usuario}")
                self.root.withdraw()
                self.lanzar_aplicacion_principal(tipo_usuario, nombre_usuario, correo)
            else:
                messagebox.showerror("Error de acceso", "Usuario desactivado. Contacte al administrador.")
        else:
            messagebox.showerror("Error de login", "Usuario o contraseña incorrectos.")

    def crear_registro(self):
        self.registro_ventana = tk.Toplevel(self.root)
        self.registro_ventana.title("Registrar Nuevo Usuario")

        frame_registro = ttk.Frame(self.registro_ventana, padding="10")
        frame_registro.grid(row=0, column=0, sticky="EW")

        ttk.Label(frame_registro, text="Nombre de Usuario:").grid(row=0, column=0, sticky="W")
        self.reg_usuario_entry = ttk.Entry(frame_registro)
        self.reg_usuario_entry.grid(row=0, column=1, sticky="EW")

        ttk.Label(frame_registro, text="Correo Electrónico:").grid(row=1, column=0, sticky="W")
        self.reg_correo_entry = ttk.Entry(frame_registro)
        self.reg_correo_entry.grid(row=1, column=1, sticky="EW")

        ttk.Label(frame_registro, text="Contraseña:").grid(row=2, column=0, sticky="W")
        self.reg_contraseña_entry = ttk.Entry(frame_registro, show="*")
        self.reg_contraseña_entry.grid(row=2, column=1, sticky="EW")

        ttk.Label(frame_registro, text="Tipo de Usuario:").grid(row=3, column=0, sticky="W")
        self.tipo_usuario = ttk.Combobox(frame_registro, values=["Usuario", "Administrador", "Técnico de Soporte", "Mesa de Ayuda", "Ejecutivo", "Jefe de Mesa"])
        self.tipo_usuario.grid(row=3, column=1, sticky="EW")
        self.tipo_usuario.bind("<<ComboboxSelected>>", self.mostrar_codigo)

        self.codigo_label = ttk.Label(frame_registro, text="Código:")
        self.codigo_entry = ttk.Entry(frame_registro, show="*")

        ttk.Button(frame_registro, text="Registrar", command=self.registrar).grid(row=5, columnspan=2)
        ttk.Button(frame_registro, text="Volver", command=self.registro_ventana.destroy).grid(row=6, columnspan=2)

    def mostrar_codigo(self, event):
        tipo = self.tipo_usuario.get()
        if tipo != "Usuario":
            self.codigo_label.grid(row=4, column=0, sticky="W")
            self.codigo_entry.grid(row=4, column=1, sticky="EW")
        else:
            self.codigo_label.grid_forget()
            self.codigo_entry.grid_forget()

    def validar_email(self, email):
        import re
        pattern = re.compile(r"[^@]+@(gmail\.com|outlook\.es)$")
        return pattern.match(email)

    def registrar(self):
        nombre_usuario = self.reg_usuario_entry.get()
        correo = self.reg_correo_entry.get()
        contraseña = self.reg_contraseña_entry.get()
        tipo_usuario = self.tipo_usuario.get()
        codigo = self.codigo_entry.get()

        if not nombre_usuario or not correo or not contraseña or not tipo_usuario:
            messagebox.showerror("Error de registro", "Todos los campos son obligatorios.")
            return

        if not self.validar_email(correo):
            messagebox.showerror("Error de registro", "El correo electrónico debe ser @gmail.com o @outlook.es.")
            return

        if tipo_usuario != "Usuario" and codigo != "1234":
            messagebox.showerror("Error de registro", "Código incorrecto.")
            return

        if correo_existe(correo):
            messagebox.showerror("Error de registro", "El correo ya está registrado.")
            return

        if crear_usuario(nombre_usuario, correo, contraseña, tipo_usuario):
            messagebox.showinfo("Registro exitoso", "Usuario registrado exitosamente.")
            self.registro_ventana.destroy()
        else:
            messagebox.showerror("Error de registro", "Error al registrar el usuario.")
