import tkinter as tk
from tkinter import ttk, messagebox
from tiques import obtener_tiques_por_area, agregar_observacion_y_cerrar_tique, actualizar_estado_tique, asignar_tique_a_varios_ejecutivos
from notificaciones import enviar_notificacion_email, enviar_notificacion_sms

class InterfazSoporteTecnico:
    def __init__(self, root, menu, area, mostrar_login):
        self.root = root
        self.menu = menu
        self.area = area if area else 'Área del Técnico'
        self.mostrar_login = mostrar_login
        self.crear_interfaz_soporte_tecnico()

    def crear_interfaz_soporte_tecnico(self):
        self.frame = ttk.Frame(self.menu)
        self.menu.add(self.frame, text='Técnico de Soporte')
        ttk.Label(self.frame, text="Gestión de Tiques - Técnico de Soporte", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.frame, text="Ver Tiques", command=self.ver_tiques).pack(pady=5)
        ttk.Button(self.frame, text="Asignar Tique a Ejecutivos", command=self.mostrar_asignar_tique).pack(pady=5)
        ttk.Button(self.frame, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)

    def cerrar_sesion(self):
        self.root.withdraw()
        self.mostrar_login()

    def ver_tiques(self):
        tiques = obtener_tiques_por_area(self.area)
        print(f"Tiques obtenidos para el área {self.area}:", tiques)
        self.tiques_ventana = tk.Toplevel(self.root)
        self.tiques_ventana.title("Tiques del Área Especializada")
        cols = ["ID", "Nombre Cliente", "Fecha Creación", "Tipo Tique", "Criticidad", "Estado"]
        self.tree = ttk.Treeview(self.tiques_ventana, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        for tique in tiques:
            print("Insertando tique:", tique)
            self.tree.insert("", "end", values=(tique['id'], tique['nombre_cliente'], tique['fecha_creacion'], tique['tipo_tique'], tique['criticidad'], tique['estado']))
        self.tree.pack(expand=True, fill='both')
        ttk.Button(self.tiques_ventana, text="Ver Detalles y Cerrar", command=self.ver_detalles_tique).pack(pady=5)
        ttk.Button(self.tiques_ventana, text="Volver", command=self.tiques_ventana.destroy).pack(pady=5)  # Botón de Volver

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
            ttk.Label(self.detalles_ventana, text="Observación:").grid(row=len(labels), column=0)
            self.observacion_entry = ttk.Entry(self.detalles_ventana)
            self.observacion_entry.grid(row=len(labels), column=1)
            ttk.Button(self.detalles_ventana, text="Cerrar Tique", command=self.cerrar_tique).grid(row=len(labels)+1, columnspan=2)

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
        self.tique_id_combobox = ttk.Combobox(self.asignar_ventana, values=[tique['id'] for tique in obtener_tiques_por_area(self.area)])
        self.tique_id_combobox.grid(row=0, column=1)
        ttk.Label(self.asignar_ventana, text="Ejecutivos (separados por coma):").grid(row=1, column=0)
        self.ejecutivos_entry = ttk.Entry(self.asignar_ventana)
        self.ejecutivos_entry.grid(row=1, column=1)
        ttk.Button(self.asignar_ventana, text="Asignar", command=self.asignar_tique).grid(row=2, columnspan=2)
        ttk.Button(self.asignar_ventana, text="Volver", command=self.asignar_ventana.destroy).grid(row=3, columnspan=2)  # Botón de Volver

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

class LoginVentana:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")
        self.crear_login()

    def crear_login(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Usuario:").pack(pady=5)
        self.usuario_entry = ttk.Entry(frame)
        self.usuario_entry.pack(pady=5)

        ttk.Label(frame, text="Contraseña:").pack(pady=5)
        self.contrasena_entry = ttk.Entry(frame, show="*")
        self.contrasena_entry.pack(pady=5)

        ttk.Button(frame, text="Login", command=self.login).pack(pady=20)

    def login(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        if usuario == "soporte" and contrasena == "1234":
            self.mostrar_interfaz_soporte()
        else:
            messagebox.showerror("Error de autenticación", "Credenciales incorrectas")

    def mostrar_interfaz_soporte(self):
        self.root.withdraw() 
        root = tk.Tk()
        menu = ttk.Notebook(root)
        menu.pack(fill='both', expand=True)
        area = 'Área del Técnico' 
        app = InterfazSoporteTecnico(root, menu, area, self.mostrar_login)
        root.mainloop()

    def mostrar_login(self):
        self.root.deiconify()  


