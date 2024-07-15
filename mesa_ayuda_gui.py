import tkinter as tk
from tkinter import ttk, messagebox
from tiques import crear_tique, asignar_tique_a_area
from usuarios import obtener_usuarios

class InterfazMesaAyuda:
    def __init__(self, root, menu, mostrar_login):
        self.root = root
        self.menu = menu
        self.mostrar_login = mostrar_login
        self.crear_interfaz_mesa_ayuda()

    def crear_interfaz_mesa_ayuda(self):
        self.frame = ttk.Frame(self.menu)
        self.menu.add(self.frame, text='Mesa de Ayuda')
        ttk.Label(self.frame, text="Gestión de Tiques - Mesa de Ayuda", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.frame, text="Crear Tique", command=self.mostrar_crear_tique).pack(pady=5)
        ttk.Button(self.frame, text="Asignar Tique a Área", command=self.mostrar_asignar_tique).pack(pady=5)
        ttk.Button(self.frame, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)

    def cerrar_sesion(self):
        self.root.withdraw()
        self.mostrar_login()

    def mostrar_crear_tique(self):
        self.crear_tique_ventana = tk.Toplevel(self.root)
        self.crear_tique_ventana.title("Crear Tique")

        frame_tique = ttk.Frame(self.crear_tique_ventana, padding="10")
        frame_tique.grid(row=0, column=0, sticky="EW")

        ttk.Label(frame_tique, text="Nombre del cliente:").grid(row=0, column=0, sticky="W")
        self.nombre_cliente_entry = ttk.Entry(frame_tique)
        self.nombre_cliente_entry.grid(row=0, column=1, sticky="EW")

        ttk.Label(frame_tique, text="Rut:").grid(row=1, column=0, sticky="W")
        self.rut_entry = ttk.Entry(frame_tique)
        self.rut_entry.grid(row=1, column=1, sticky="EW")

        ttk.Label(frame_tique, text="Teléfono:").grid(row=2, column=0, sticky="W")
        self.telefono_entry = ttk.Entry(frame_tique)
        self.telefono_entry.grid(row=2, column=1, sticky="EW")

        ttk.Label(frame_tique, text="Correo electrónico:").grid(row=3, column=0, sticky="W")
        self.correo_entry = ttk.Entry(frame_tique)
        self.correo_entry.grid(row=3, column=1, sticky="EW")

        ttk.Label(frame_tique, text="Tipo de tique:").grid(row=4, column=0, sticky="W")
        self.tipo_tique_combobox = ttk.Combobox(frame_tique, values=["Felicitación", "Consulta", "Reclamo", "Problema"])
        self.tipo_tique_combobox.grid(row=4, column=1, sticky="EW")

        ttk.Label(frame_tique, text="Criticidad:").grid(row=5, column=0, sticky="W")
        self.criticidad_combobox = ttk.Combobox(frame_tique, values=["Leve", "Media", "Alta"])
        self.criticidad_combobox.grid(row=5, column=1, sticky="EW")

        ttk.Label(frame_tique, text="Detalle del servicio:").grid(row=6, column=0, sticky="W")
        self.detalle_servicio_entry = ttk.Entry(frame_tique)
        self.detalle_servicio_entry.grid(row=6, column=1, sticky="EW")

        ttk.Label(frame_tique, text="Detalle del problema:").grid(row=7, column=0, sticky="W")
        self.detalle_problema_entry = ttk.Entry(frame_tique)
        self.detalle_problema_entry.grid(row=7, column=1, sticky="EW")

        ttk.Label(frame_tique, text="Área para derivar:").grid(row=8, column=0, sticky="W")
        self.area_combobox = ttk.Combobox(frame_tique, values=["Área del Técnico", "Mesa de Ayuda", "Área de Soporte"])
        self.area_combobox.grid(row=8, column=1, sticky="EW")

        ttk.Label(frame_tique, text="Responsable:").grid(row=9, column=0, sticky="W")
        self.responsable_entry = ttk.Entry(frame_tique)
        self.responsable_entry.grid(row=9, column=1, sticky="EW")

        ttk.Button(frame_tique, text="Crear", command=self.crear_tique).grid(row=10, columnspan=2)

    def crear_tique(self):
        data = {
            "Nombre del cliente": self.nombre_cliente_entry.get(),
            "Rut": self.rut_entry.get(),
            "Teléfono": self.telefono_entry.get(),
            "Correo electrónico": self.correo_entry.get(),
            "Tipo de tique": self.tipo_tique_combobox.get(),
            "Criticidad": self.criticidad_combobox.get(),
            "Detalle del servicio": self.detalle_servicio_entry.get(),
            "Detalle del problema": self.detalle_problema_entry.get(),
            "Área para derivar": self.area_combobox.get(),
            "Responsable": self.responsable_entry.get()
        }
        if crear_tique(data):
            messagebox.showinfo("Tique Creado", "El tique ha sido creado exitosamente.")
            self.crear_tique_ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear el tique.")

    def mostrar_asignar_tique(self):
        self.asignar_tique_ventana = tk.Toplevel(self.root)
        self.asignar_tique_ventana.title("Asignar Tique a Área")

        frame_asignar = ttk.Frame(self.asignar_tique_ventana, padding="10")
        frame_asignar.grid(row=0, column=0, sticky="EW")

        ttk.Label(frame_asignar, text="ID del Tique:").grid(row=0, column=0, sticky="W")
        self.tique_id_entry = ttk.Entry(frame_asignar)
        self.tique_id_entry.grid(row=0, column=1, sticky="EW")

        ttk.Label(frame_asignar, text="Área para Asignar:").grid(row=1, column=0, sticky="W")
        self.area_asignar_combobox = ttk.Combobox(frame_asignar, values=["Área del Técnico", "Mesa de Ayuda", "Área de Soporte"])
        self.area_asignar_combobox.grid(row=1, column=1, sticky="EW")

        ttk.Button(frame_asignar, text="Asignar", command=self.asignar_tique).grid(row=2, columnspan=2)

    def asignar_tique(self):
        tique_id = self.tique_id_entry.get()
        area = self.area_asignar_combobox.get()
        if asignar_tique_a_area(tique_id, area):
            messagebox.showinfo("Asignación Exitosa", "El tique ha sido asignado al área.")
            self.asignar_tique_ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo asignar el tique.")
