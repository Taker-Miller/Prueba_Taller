import tkinter as tk
from tkinter import ttk, messagebox
from usuarios import crear_usuario, desactivar_usuario, obtener_usuarios, correo_existe
from tiques import obtener_todos_los_tiques, filtrar_tiques, asignar_tique_a_varios_ejecutivos, obtener_tiques_por_area
from areas import obtener_areas, agregar_area, editar_area
from tipos_tique import obtener_tipos_tique, agregar_tipo_tique, editar_tipo_tique
from criticidades import obtener_criticidades, agregar_criticidad, editar_criticidad

class InterfazAdmin:
    def __init__(self, root, menu, mostrar_login):
        self.root = root
        self.menu = menu
        self.mostrar_login = mostrar_login
        self.crear_interfaz_admin()

    def crear_interfaz_admin(self):
        self.frame = ttk.Frame(self.menu)
        self.menu.add(self.frame, text='Administración')
        ttk.Label(self.frame, text="Gestión de Usuarios y Tiques - Administración", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.frame, text="Crear Usuario", command=self.mostrar_crear_usuario).pack(pady=5)
        ttk.Button(self.frame, text="Desactivar Usuario", command=self.mostrar_desactivar_usuario).pack(pady=5)
        ttk.Button(self.frame, text="Ver Tiques", command=self.ver_tiques).pack(pady=5)
        ttk.Button(self.frame, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)

    def cerrar_sesion(self):
        self.root.withdraw()
        self.mostrar_login()

    def mostrar_crear_usuario(self):
        self.crear_usuario_ventana = tk.Toplevel(self.root)
        self.crear_usuario_ventana.title("Crear Nuevo Usuario")

        frame_crear = ttk.Frame(self.crear_usuario_ventana, padding="10")
        frame_crear.grid(row=0, column=0, sticky="EW")

        ttk.Label(frame_crear, text="Nombre de Usuario:").grid(row=0, column=0, sticky="W")
        self.usuario_entry = ttk.Entry(frame_crear)
        self.usuario_entry.grid(row=0, column=1, sticky="EW")

        ttk.Label(frame_crear, text="Correo Electrónico:").grid(row=1, column=0, sticky="W")
        self.correo_entry = ttk.Entry(frame_crear)
        self.correo_entry.grid(row=1, column=1, sticky="EW")

        ttk.Label(frame_crear, text="Contraseña:").grid(row=2, column=0, sticky="W")
        self.contraseña_entry = ttk.Entry(frame_crear, show="*")
        self.contraseña_entry.grid(row=2, column=1, sticky="EW")

        ttk.Label(frame_crear, text="Tipo de Usuario:").grid(row=3, column=0, sticky="W")
        self.tipo_usuario = ttk.Combobox(frame_crear, values=["Usuario", "Administrador", "Técnico de Soporte", "Mesa de Ayuda", "Ejecutivo", "Jefe de Mesa"])
        self.tipo_usuario.grid(row=3, column=1, sticky="EW")
        self.tipo_usuario.bind("<<ComboboxSelected>>", self.mostrar_codigo)

        self.codigo_label = ttk.Label(frame_crear, text="Código:")
        self.codigo_entry = ttk.Entry(frame_crear, show="*")

        ttk.Button(frame_crear, text="Registrar", command=self.registrar_usuario).grid(row=5, columnspan=2)
        ttk.Button(frame_crear, text="Volver", command=self.crear_usuario_ventana.destroy).grid(row=6, columnspan=2)

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

    def registrar_usuario(self):
        nombre_usuario = self.usuario_entry.get()
        correo = self.correo_entry.get()
        contraseña = self.contraseña_entry.get()
        tipo_usuario = self.tipo_usuario.get()
        codigo = self.codigo_entry.get()

        if not nombre_usuario or not correo or not contraseña:
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
            self.crear_usuario_ventana.destroy()
        else:
            messagebox.showerror("Error de registro", "Error al registrar el usuario.")

    def mostrar_desactivar_usuario(self):
        self.desactivar_usuario_ventana = tk.Toplevel(self.root)
        self.desactivar_usuario_ventana.title("Desactivar Usuario")

        frame_desactivar = ttk.Frame(self.desactivar_usuario_ventana, padding="10")
        frame_desactivar.grid(row=0, column=0, sticky="EW")

        ttk.Label(frame_desactivar, text="Seleccionar Usuario:").grid(row=0, column=0, sticky="W")
        self.usuario_combobox = ttk.Combobox(frame_desactivar, values=obtener_usuarios())
        self.usuario_combobox.grid(row=0, column=1, sticky="EW")

        ttk.Button(frame_desactivar, text="Desactivar", command=self.desactivar_usuario).grid(row=1, columnspan=2)
        ttk.Button(frame_desactivar, text="Volver", command=self.desactivar_usuario_ventana.destroy).grid(row=2, columnspan=2)

    def desactivar_usuario(self):
        usuario = self.usuario_combobox.get()
        if not usuario:
            messagebox.showerror("Error", "Debe seleccionar un usuario.")
            return

        if desactivar_usuario(usuario):
            messagebox.showinfo("Usuario Desactivado", "El usuario ha sido desactivado exitosamente.")
            self.desactivar_usuario_ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo desactivar el usuario.")

    def ver_tiques(self):
        tiques = obtener_todos_los_tiques()
        self.tiques_ventana = tk.Toplevel(self.root)
        self.tiques_ventana.title("Listado de Tiques")
        cols = ["ID", "Nombre Cliente", "Fecha Creación", "Tipo Tique", "Criticidad", "Área", "Estado"]
        self.tree = ttk.Treeview(self.tiques_ventana, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        for tique in tiques:
            self.tree.insert("", "end", values=(tique['id'], tique['nombre_cliente'], tique['fecha_creacion'], tique['tipo_tique'], tique['criticidad'], tique['area'], tique['estado']))
        self.tree.pack(expand=True, fill='both')
        ttk.Button(self.tiques_ventana, text="Filtrar Tiques", command=self.mostrar_filtro).pack(pady=5)
        ttk.Button(self.tiques_ventana, text="Cerrar", command=self.tiques_ventana.destroy).pack(pady=5)

    def mostrar_filtro(self):
        self.filtro_ventana = tk.Toplevel(self.root)
        self.filtro_ventana.title("Filtrar Tiques")

        frame_filtro = ttk.Frame(self.filtro_ventana, padding="10")
        frame_filtro.grid(row=0, column=0, sticky="EW")

        ttk.Label(frame_filtro, text="Filtrar por:").grid(row=0, column=0, sticky="W")
        self.filtro_combobox = ttk.Combobox(frame_filtro, values=["Fecha", "Criticidad", "Tipo de Tique", "Estado", "Área"])
        self.filtro_combobox.grid(row=0, column=1, sticky="EW")
        self.filtro_combobox.bind("<<ComboboxSelected>>", self.actualizar_filtro_opciones)

        self.filtro_combobox_opciones = ttk.Combobox(frame_filtro)
        self.filtro_combobox_opciones.grid(row=1, column=1, sticky="EW")

        ttk.Button(frame_filtro, text="Aplicar Filtro", command=self.aplicar_filtro).grid(row=2, columnspan=2)
        ttk.Button(frame_filtro, text="Volver", command=self.filtro_ventana.destroy).grid(row=3, columnspan=2)

    def actualizar_filtro_opciones(self, event):
        filtro = self.filtro_combobox.get()
        if filtro == "Fecha":
            self.filtro_combobox_opciones['values'] = ["2024-07-14", "2024-07-13"]  
        elif filtro == "Criticidad":
            self.filtro_combobox_opciones['values'] = ["leve", "media", "alta"]
        elif filtro == "Tipo de Tique":
            self.filtro_combobox_opciones['values'] = ["Felicitación", "Consulta", "Reclamo", "Problema"]
        elif filtro == "Estado":
            self.filtro_combobox_opciones['values'] = ["Abierto", "En proceso", "Cerrado"]
        elif filtro == "Área":
            self.filtro_combobox_opciones['values'] = ["Área Del Tecnico", "Mesa de Ayuda", "Ejecutivo"]

    def aplicar_filtro(self):
        filtro = self.filtro_combobox.get()
        opcion = self.filtro_combobox_opciones.get()
        if filtro.lower() == "área":
            filtro = "area"
        filtros = {filtro.lower(): opcion}
        tiques = filtrar_tiques(filtros)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for tique in tiques:
            self.tree.insert("", "end", values=(tique['id'], tique['nombre_cliente'], tique['fecha_creacion'], tique['tipo_tique'], tique['criticidad'], tique['area'], tique['estado']))
        self.filtro_ventana.destroy()
