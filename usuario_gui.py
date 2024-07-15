import tkinter as tk
from tkinter import ttk, messagebox
from tiques import crear_tique

class InterfazUsuario:
    def __init__(self, root, menu, usuario, correo, mostrar_login):
        self.root = root
        self.menu = menu
        self.usuario = usuario
        self.correo = correo
        self.mostrar_login = mostrar_login
        self.crear_interfaz_usuario()

    def crear_interfaz_usuario(self):
        self.frame = ttk.Frame(self.menu)
        self.menu.add(self.frame, text='Usuario')
        ttk.Label(self.frame, text="Gestión de Tiques - Usuario", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(self.frame, text="Crear Tique", command=self.mostrar_formulario_crear_tique).grid(row=1, column=0, pady=5)
        ttk.Button(self.frame, text="Cerrar Sesión", command=self.cerrar_sesion).grid(row=1, column=1, pady=5)

    def cerrar_sesion(self):
        self.root.withdraw()
        self.mostrar_login()

    def mostrar_formulario_crear_tique(self):
        self.nuevo_tique_ventana = tk.Toplevel(self.root)
        self.nuevo_tique_ventana.title("Crear Tique")
        labels = ["Nombre del cliente", "Rut", "Teléfono", "Correo electrónico", "Tipo de tique", "Criticidad", "Detalle del servicio", "Detalle del problema", "Área Ejecutiva"]
        self.entries = {}
        for idx, label in enumerate(labels):
            ttk.Label(self.nuevo_tique_ventana, text=label).grid(row=idx, column=0)
            if label == "Tipo de tique":
                self.entries[label] = ttk.Combobox(self.nuevo_tique_ventana, values=["Felicitación", "Consulta", "Reclamo", "Problema"])
                self.entries[label].grid(row=idx, column=1)
            elif label == "Criticidad":
                self.entries[label] = ttk.Combobox(self.nuevo_tique_ventana, values=["leve", "media", "alta"])
                self.entries[label].grid(row=idx, column=1)
            elif label == "Área Ejecutiva":
                self.entries[label] = ttk.Combobox(self.nuevo_tique_ventana, values=self.obtener_areas_validas())
                self.entries[label].grid(row=idx, column=1)
            elif label == "Nombre del cliente":
                entry = ttk.Entry(self.nuevo_tique_ventana)
                entry.insert(0, self.usuario)
                entry.config(state='readonly')
                entry.grid(row=idx, column=1)
                self.entries[label] = entry
            elif label == "Correo electrónico":
                entry = ttk.Entry(self.nuevo_tique_ventana)
                entry.insert(0, self.correo)
                entry.config(state='readonly')
                entry.grid(row=idx, column=1)
                self.entries[label] = entry
            else:
                entry = ttk.Entry(self.nuevo_tique_ventana)
                entry.grid(row=idx, column=1)
                self.entries[label] = entry
        ttk.Button(self.nuevo_tique_ventana, text="Previsualizar Tique", command=self.previsualizar_tique).grid(row=len(labels), columnspan=2)

    def obtener_areas_validas(self):
        return ["Área del Técnico", "Mesa de Ayuda", "Ejecutivo"]

    def validar_rut(self, rut):
        import re
        pattern = re.compile(r"^\d{1,2}\.\d{3}\.\d{3}-[0-9Kk]$")
        return pattern.match(rut)

    def validar_telefono(self, telefono):
        import re
        pattern = re.compile(r"^\d{9}$")
        return pattern.match(telefono)

    def validar_email(self, email):
        import re
        pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return pattern.match(email)

    def previsualizar_tique(self):
        data = {label: entry.get() for label, entry in self.entries.items()}
        # Validaciones
        if any(not value for value in data.values()):
            messagebox.showerror("Error de validación", "Todos los campos son obligatorios.")
            return
        if not self.validar_rut(data["Rut"]):
            messagebox.showerror("Error de validación", "El RUT no tiene un formato válido. (Ejemplo: 12.345.678-9)")
            return
        if not self.validar_telefono(data["Teléfono"]):
            messagebox.showerror("Error de validación", "El teléfono no tiene un formato válido. (Ejemplo: 912345678)")
            return
        if not self.validar_email(data["Correo electrónico"]):
            messagebox.showerror("Error de validación", "El correo electrónico no tiene un formato válido.")
            return
        if data["Tipo de tique"] not in ["Felicitación", "Consulta", "Reclamo", "Problema"]:
            messagebox.showerror("Error de validación", "Debe seleccionar un tipo de tique válido.")
            return
        if data["Criticidad"] not in ["leve", "media", "alta"]:
            messagebox.showerror("Error de validación", "Debe seleccionar una criticidad válida.")
            return
        if data["Área Ejecutiva"] not in self.obtener_areas_validas():
            messagebox.showerror("Error de validación", "Debe seleccionar un área ejecutiva válida.")
            return
        
        data["Responsable"] = self.usuario  
        previsualizacion_ventana = tk.Toplevel(self.root)
        previsualizacion_ventana.title("Previsualización del Tique")
        for idx, (key, value) in enumerate(data.items()):
            ttk.Label(previsualizacion_ventana, text=f"{key}: {value}").grid(row=idx, column=0)
        ttk.Button(previsualizacion_ventana, text="Confirmar y Crear Tique", command=lambda: self.crear_tique(data, previsualizacion_ventana)).grid(row=len(data), columnspan=2)

    def crear_tique(self, data, previsualizacion_ventana):
        if crear_tique(data):
            messagebox.showinfo("Tique Creado", "El tique ha sido creado exitosamente.")
            self.nuevo_tique_ventana.destroy()
            previsualizacion_ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear el tique.")
