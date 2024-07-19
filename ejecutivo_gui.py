import tkinter as tk
from tkinter import ttk, messagebox
from tiques import obtener_tiques_por_area, actualizar_estado_tique, agregar_observacion_y_cerrar_tique, asignar_tique_a_varios_ejecutivos
from notificaciones import enviar_notificacion_email, enviar_notificacion_sms

class InterfazEjecutivo:
    def __init__(self, root, menu, area_especializada, mostrar_login):
        self.root = root
        self.menu = menu
        self.area_especializada = area_especializada
        self.mostrar_login = mostrar_login
        self.crear_interfaz_area()

    def crear_interfaz_area(self):
        self.frame = ttk.Frame(self.menu)
        self.menu.add(self.frame, text='Área Especializada')
        ttk.Label(self.frame, text="Gestión de Tiques - Área Especializada", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.frame, text="Ver Tiques", command=self.ver_tiques).pack(pady=5)
        ttk.Button(self.frame, text="Asignar Tique a Ejecutivos", command=self.mostrar_asignar_tique).pack(pady=5)
        ttk.Button(self.frame, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)

    def cerrar_sesion(self):
        self.root.withdraw()
        self.mostrar_login()

    def ver_tiques(self):
        tiques = obtener_tiques_por_area(self.area_especializada)
        self.tiques_ventana = tk.Toplevel(self.root)
        self.tiques_ventana.title("Tiques del Área Especializada")
        cols = ["ID", "Nombre Cliente", "Fecha Creación", "Tipo Tique", "Criticidad", "Estado"]
        self.tree = ttk.Treeview(self.tiques_ventana, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        for tique in tiques:
            self.tree.insert("", "end", values=(tique['id'], tique['nombre_cliente'], tique['fecha_creacion'], tique['tipo_tique'], tique['criticidad'], tique['estado']))
        self.tree.pack(expand=True, fill='both')
        ttk.Button(self.tiques_ventana, text="Ver Detalles y Actualizar Estado", command=self.ver_detalles_tique).pack(pady=5)

    def ver_detalles_tique(self):
        selected_item = self.tree.selection()
        if selected_item:
            tique = self.tree.item(selected_item)["values"]
            self.detalles_ventana = tk.Toplevel(self.root)
            self.detalles_ventana.title("Detalles del Tique")
            labels = ["ID", "Nombre Cliente", "Fecha Creación", "Tipo Tique", "Criticidad", "Estado"]
            self.detalle_entries = {}
            for idx, label in enumerate(labels):
                ttk.Label(self.detalles_ventana, text=label).grid(row=idx, column=0)
                entry = ttk.Entry(self.detalles_ventana)
                entry.grid(row=idx, column=1)
                entry.insert(0, tique[idx])
                entry.config(state='readonly')
                self.detalle_entries[label] = entry
            
            ttk.Label(self.detalles_ventana, text="Nuevo Estado:").grid(row=len(labels), column=0)
            self.estado_combobox = ttk.Combobox(self.detalles_ventana, values=["Resuelto", "No aplicable"])
            self.estado_combobox.grid(row=len(labels), column=1)

            ttk.Label(self.detalles_ventana, text="Observación:").grid(row=len(labels)+1, column=0)
            self.observacion_entry = ttk.Entry(self.detalles_ventana)
            self.observacion_entry.grid(row=len(labels)+1, column=1)

            ttk.Button(self.detalles_ventana, text="Actualizar Estado", command=self.actualizar_estado_tique).grid(row=len(labels)+2, columnspan=2)
            ttk.Button(self.detalles_ventana, text="Cerrar Tique", command=self.cerrar_tique).grid(row=len(labels)+3, columnspan=2)

    def actualizar_estado_tique(self):
        tique_id = self.detalle_entries["ID"].get()
        nuevo_estado = self.estado_combobox.get()
        if not nuevo_estado:
            messagebox.showerror("Error de validación", "Debe seleccionar un estado.")
            return
        if actualizar_estado_tique(tique_id, nuevo_estado):
            messagebox.showinfo("Estado Actualizado", "El estado del tique ha sido actualizado exitosamente.")
            self.detalles_ventana.destroy()
            self.tiques_ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el estado del tique.")

    def cerrar_tique(self):
        tique_id = self.detalle_entries["ID"].get()
        observacion = self.observacion_entry.get()
        if not observacion:
            messagebox.showerror("Error de validación", "El campo de observación no puede estar vacío.")
            return
        estado = "Resuelto" 
        if agregar_observacion_y_cerrar_tique(tique_id, observacion, estado):
            messagebox.showinfo("Tique Cerrado", "El tique ha sido cerrado exitosamente.")
            self.detalles_ventana.destroy()
            self.tiques_ventana.destroy()
            enviar_notificacion_email("correo_cliente@example.com", f"Su tique con ID {tique_id} ha sido cerrado.")
            enviar_notificacion_sms("+56912345678", f"Su tique con ID {tique_id} ha sido cerrado.")
        else:
            messagebox.showerror("Error", "No se pudo cerrar el tique.")

    def mostrar_asignar_tique(self):
        self.asignar_ventana = tk.Toplevel(self.root)
        self.asignar_ventana.title("Asignar Tique a Ejecutivos")
        ttk.Label(self.asignar_ventana, text="ID del Tique:").grid(row=0, column=0)
        self.tique_id_combobox = ttk.Combobox(self.asignar_ventana, values=[tique['id'] for tique in obtener_tiques_por_area(self.area_especializada)])
        self.tique_id_combobox.grid(row=0, column=1)
        ttk.Label(self.asignar_ventana, text="Ejecutivos (separados por coma):").grid(row=1, column=0)
        self.ejecutivos_entry = ttk.Entry(self.asignar_ventana)
        self.ejecutivos_entry.grid(row=1, column=1)
        ttk.Button(self.asignar_ventana, text="Asignar", command=self.asignar_tique).grid(row=2, columnspan=2)

    def asignar_tique(self):
        tique_id = self.tique_id_combobox.get()
        ejecutivos = self.ejecutivos_entry.get().split(',')
        if asignar_tique_a_varios_ejecutivos(tique_id, ejecutivos):
            messagebox.showinfo("Asignación Exitosa", "El tique ha sido asignado a los ejecutivos.")
            self.asignar_ventana.destroy()
            for ejecutivo in ejecutivos:
                enviar_notificacion_email(f"{ejecutivo}@example.com", f"Se le ha asignado el tique con ID {tique_id}.")
                enviar_notificacion_sms("+56912345678", f"Se le ha asignado el tique con ID {tique_id}.")
        else:
            messagebox.showerror("Error", "No se pudo asignar el tique.")

# Funciones simuladas para las operaciones de backend
def obtener_tiques_por_area(area_especializada):
    # Simulación de consulta a la base de datos
    return [
        {'id': 1, 'nombre_cliente': 'Cliente A', 'fecha_creacion': '2024-01-01', 'tipo_tique': 'Tipo 1', 'criticidad': 'Alta', 'estado': 'Abierto'},
        {'id': 2, 'nombre_cliente': 'Cliente B', 'fecha_creacion': '2024-01-02', 'tipo_tique': 'Tipo 2', 'criticidad': 'Media', 'estado': 'Abierto'}
    ]

def actualizar_estado_tique(tique_id, nuevo_estado):
    #Simulación de actualización de estado en la base de datos
    print(f"Actualizando estado del tique {tique_id} a {nuevo_estado}")
    return True

def agregar_observacion_y_cerrar_tique(tique_id, observacion, estado):
    #Simulación de agregar observación y cerrar tique en la base de datos
    print(f"Agregando observación y cerrando tique {tique_id} con estado {estado}")
    return True

def asignar_tique_a_varios_ejecutivos(tique_id, ejecutivos_ids):
    #Simulación de asignar tique a varios ejecutivos en la base de datos
    print(f"Asignando tique {tique_id} a ejecutivos {ejecutivos_ids}")
    return True

def enviar_notificacion_email(email, asunto, mensaje):
    #Simulación de envío de notificación por correo
    print(f"Enviando correo a {email}: {asunto} - {mensaje}")

def enviar_notificacion_sms(numero, mensaje):
    #Simulación de envío de notificación por mensaje de texto
    print(f"Enviando SMS a {numero}: {mensaje}")


