import tkinter as tk
from tkinter import ttk, messagebox
from usuarios import crear_usuario

class InterfazUsuario:
    def __init__(self, root, menu, mostrar_login):
        self.root = root
        self.menu = menu
        self.mostrar_login = mostrar_login
        self.crear_interfaz_usuario()

    def crear_interfaz_usuario(self):
        self.frame = ttk.Frame(self.menu)
        self.menu.add(self.frame, text='Usuario')
        ttk.Label(self.frame, text="Gestión de Usuarios - Sistema de Tickets", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(self.frame, text="Crear Usuario", command=self.mostrar_formulario_crear_usuario).grid(row=1, column=0, pady=5)
        ttk.Button(self.frame, text="Cerrar Sesión", command=self.cerrar_sesion).grid(row=1, column=1, pady=5)

    def cerrar_sesion(self):
        self.root.withdraw()
        self.mostrar_login()

    def mostrar_formulario_crear_usuario(self):
        self.nuevo_usuario_ventana = tk.Toplevel(self.root)
        self.nuevo_usuario_ventana.title("Crear Usuario")
        labels = ["Nombre", "Correo", "Contraseña", "Tipo de Usuario"]
        self.entries = {}
        for idx, label in enumerate(labels):
            ttk.Label(self.nuevo_usuario_ventana, text=label).grid(row=idx, column=0)
            if label == "Tipo de Usuario":
                self.entries[label] = ttk.Combobox(self.nuevo_usuario_ventana, values=["Usuario", "Administrador", "Técnico de Soporte", "Ejecutivo de Mesa de Ayuda", "Ejecutivo de Área Específica", "Mesa de Ayuda", "Ejecutivo"])
                self.entries[label].set("Ejecutivo")  # Valor predeterminado
                self.entries[label].grid(row=idx, column=1)
            else:
                entry = ttk.Entry(self.nuevo_usuario_ventana)
                entry.grid(row=idx, column=1)
                self.entries[label] = entry
        ttk.Button(self.nuevo_usuario_ventana, text="Crear Usuario", command=self.crear_usuario).grid(row=len(labels), columnspan=2)

    def crear_usuario(self):
        data = {label: entry.get() for label, entry in self.entries.items()}
        data["Activo"] = 1  # Establecer como activo por defecto
        print(data)  # Línea de depuración
        if crear_usuario(data):
            messagebox.showinfo("Usuario Creado", "El usuario ha sido creado exitosamente.")
            self.nuevo_usuario_ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario.")

# Configuración inicial de Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestión de Usuarios")
    menu = ttk.Notebook(root)
    menu.pack(expand=1, fill='both')

    def mostrar_login():
        # Aquí puedes implementar la lógica para mostrar la ventana de login nuevamente
        pass

    app = InterfazUsuario(root, menu, mostrar_login)
    root.mainloop()
