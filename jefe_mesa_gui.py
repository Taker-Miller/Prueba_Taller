import tkinter as tk
from tkinter import ttk, messagebox
from areas import obtener_areas, agregar_area, editar_area
from tipos_tique import obtener_tipos_tique, agregar_tipo_tique, editar_tipo_tique
from criticidades import obtener_criticidades, agregar_criticidad, editar_criticidad

class InterfazJefeMesa:
    def __init__(self, root, menu, mostrar_login):
        self.root = root
        self.menu = menu
        self.mostrar_login = mostrar_login
        self.crear_interfaz_jefe_mesa()

    def crear_interfaz_jefe_mesa(self):
        self.frame = ttk.Frame(self.menu)
        self.menu.add(self.frame, text='Jefe de Mesa')
        ttk.Label(self.frame, text="Gestión de Tiques - Jefe de Mesa", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.frame, text="Gestionar Áreas", command=self.mostrar_gestionar_areas).pack(pady=5)
        ttk.Button(self.frame, text="Gestionar Tipos de Tique", command=self.mostrar_gestionar_tipos_tique).pack(pady=5)
        ttk.Button(self.frame, text="Gestionar Criticidades", command=self.mostrar_gestionar_criticidades).pack(pady=5)
        ttk.Button(self.frame, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)

    def cerrar_sesion(self):
        self.root.withdraw()
        self.mostrar_login()

    def mostrar_gestionar_areas(self):
        self.gestionar_areas_ventana = tk.Toplevel(self.root)
        self.gestionar_areas_ventana.title("Gestionar Áreas")

        frame_areas = ttk.Frame(self.gestionar_areas_ventana, padding="10")
        frame_areas.grid(row=0, column=0, sticky="EW")

        ttk.Label(frame_areas, text="Nombre del Área Actual:").grid(row=0, column=0, sticky="W")
        self.area_entry = ttk.Entry(frame_areas)
        self.area_entry.grid(row=0, column=1, sticky="EW")

        ttk.Label(frame_areas, text="Nuevo Nombre del Área:").grid(row=1, column=0, sticky="W")
        self.nueva_area_entry = ttk.Entry(frame_areas)
        self.nueva_area_entry.grid(row=1, column=1, sticky="EW")

        ttk.Button(frame_areas, text="Agregar", command=self.agregar_area).grid(row=2, columnspan=2, pady=5)
        ttk.Button(frame_areas, text="Editar", command=self.editar_area).grid(row=3, columnspan=2, pady=5)

    def agregar_area(self):
        nombre_area = self.area_entry.get()
        if not nombre_area:
            messagebox.showerror("Error", "El campo de nombre del área no puede estar vacío.")
            return
        if agregar_area(nombre_area):
            messagebox.showinfo("Éxito", "Área agregada exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo agregar el área.")

    def editar_area(self):
        nombre_area = self.area_entry.get()
        nuevo_nombre_area = self.nueva_area_entry.get()
        if not nombre_area or not nuevo_nombre_area:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if editar_area(nombre_area, nuevo_nombre_area):
            messagebox.showinfo("Éxito", "Área editada exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo editar el área.")

    def mostrar_gestionar_tipos_tique(self):
        self.gestionar_tipos_tique_ventana = tk.Toplevel(self.root)
        self.gestionar_tipos_tique_ventana.title("Gestionar Tipos de Tique")

        frame_tipos_tique = ttk.Frame(self.gestionar_tipos_tique_ventana, padding="10")
        frame_tipos_tique.grid(row=0, column=0, sticky="EW")

        ttk.Label(frame_tipos_tique, text="Nombre del Tipo de Tique Actual:").grid(row=0, column=0, sticky="W")
        self.tipo_tique_entry = ttk.Entry(frame_tipos_tique)
        self.tipo_tique_entry.grid(row=0, column=1, sticky="EW")

        ttk.Label(frame_tipos_tique, text="Nuevo Nombre del Tipo de Tique:").grid(row=1, column=0, sticky="W")
        self.nuevo_tipo_tique_entry = ttk.Entry(frame_tipos_tique)
        self.nuevo_tipo_tique_entry.grid(row=1, column=1, sticky="EW")

        ttk.Button(frame_tipos_tique, text="Agregar", command=self.agregar_tipo_tique).grid(row=2, columnspan=2, pady=5)
        ttk.Button(frame_tipos_tique, text="Editar", command=self.editar_tipo_tique).grid(row=3, columnspan=2, pady=5)

    def agregar_tipo_tique(self):
        nombre_tipo_tique = self.tipo_tique_entry.get()
        if not nombre_tipo_tique:
            messagebox.showerror("Error", "El campo de nombre del tipo de tique no puede estar vacío.")
            return
        if agregar_tipo_tique(nombre_tipo_tique):
            messagebox.showinfo("Éxito", "Tipo de tique agregado exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo agregar el tipo de tique.")

    def editar_tipo_tique(self):
        nombre_tipo_tique = self.tipo_tique_entry.get()
        nuevo_nombre_tipo_tique = self.nuevo_tipo_tique_entry.get()
        if not nombre_tipo_tique or not nuevo_nombre_tipo_tique:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if editar_tipo_tique(nombre_tipo_tique, nuevo_nombre_tipo_tique):
            messagebox.showinfo("Éxito", "Tipo de tique editado exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo editar el tipo de tique.")

    def mostrar_gestionar_criticidades(self):
        self.gestionar_criticidades_ventana = tk.Toplevel(self.root)
        self.gestionar_criticidades_ventana.title("Gestionar Criticidades")

        frame_criticidades = ttk.Frame(self.gestionar_criticidades_ventana, padding="10")
        frame_criticidades.grid(row=0, column=0, sticky="EW")

        ttk.Label(frame_criticidades, text="Nombre de la Criticidad Actual:").grid(row=0, column=0, sticky="W")
        self.criticidad_entry = ttk.Entry(frame_criticidades)
        self.criticidad_entry.grid(row=0, column=1, sticky="EW")

        ttk.Label(frame_criticidades, text="Nuevo Nombre de la Criticidad:").grid(row=1, column=0, sticky="W")
        self.nueva_criticidad_entry = ttk.Entry(frame_criticidades)
        self.nueva_criticidad_entry.grid(row=1, column=1, sticky="EW")

        ttk.Button(frame_criticidades, text="Agregar", command=self.agregar_criticidad).grid(row=2, columnspan=2, pady=5)
        ttk.Button(frame_criticidades, text="Editar", command=self.editar_criticidad).grid(row=3, columnspan=2, pady=5)

    def agregar_criticidad(self):
        nombre_criticidad = self.criticidad_entry.get()
        if not nombre_criticidad:
            messagebox.showerror("Error", "El campo de nombre de la criticidad no puede estar vacío.")
            return
        if agregar_criticidad(nombre_criticidad):
            messagebox.showinfo("Éxito", "Criticidad agregada exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo agregar la criticidad.")

    def editar_criticidad(self):
        nombre_criticidad = self.criticidad_entry.get()
        nuevo_nombre_criticidad = self.nueva_criticidad_entry.get()
        if not nombre_criticidad or not nuevo_nombre_criticidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if editar_criticidad(nombre_criticidad, nuevo_nombre_criticidad):
            messagebox.showinfo("Éxito", "Criticidad editada exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo editar la criticidad.")
