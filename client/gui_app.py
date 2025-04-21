import tkinter as tk
from tkinter import ttk

from model.conexion import *

def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu = barra_menu, width= 300, height= 300)
    
    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Inicio", menu = menu_inicio)
    
    menu_inicio.add_command(label="Crear Registro en BD")
    menu_inicio.add_command(label="Eliminar Registro en BD")
    menu_inicio.add_command(label="Salir", command=root.destroy)
    
    barra_menu.add_cascade(label="Consultas")
    barra_menu.add_cascade(label="Configuracion")
    barra_menu.add_cascade(label="Ayuda")
    
class Frame(tk.Frame):
    def __init__(self, root = None):
        super().__init__(root, width = 480, height=320)
        self.root = root
        self.pack()
        self.config(bg="white")
        self.campos_pelicula()
        self.deshabilitar_campos()
        self.tabla_pelicula()
    
    def campos_pelicula(self):
        self.label_nombre = tk.Label(self, text="Nombre Aspirante:")
        self.label_nombre.config(font=("Arial", 12, "bold"),bg="white")
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10)
        
        self.label_telefono = tk.Label(self, text="Telefono Aspirante:")
        self.label_telefono.config(font=("Arial", 12, "bold"),bg="white")
        self.label_telefono.grid(row=1, column=0, padx=10, pady=10)
        
        self.label_correo = tk.Label(self, text="Correo Aspirante:")
        self.label_correo.config(font=("Arial", 12, "bold"),bg="white")
        self.label_correo.grid(row=2, column=0, padx=10, pady=10)
        
        self.label_direccion = tk.Label(self, text="Direccin Aspirante:")
        self.label_direccion.config(font=("Arial", 12, "bold"),bg="white")
        self.label_direccion.grid(row=3, column=0, padx=10, pady=10)
        
        
        self.mi_nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self,textvariable= self.mi_nombre)
        self.entry_nombre.config(width=50,font=("Arial", 12, "bold"),bg="white")
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
        
        self.mi_telefono = tk.StringVar()
        self.entry_telefono = tk.Entry(self,textvariable= self.mi_telefono)
        self.entry_telefono.config(width=50,font=("Arial", 12, "bold"),bg="white")
        self.entry_telefono.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        
        self.mi_correo = tk.StringVar()
        self.entry_correo = tk.Entry(self,textvariable= self.mi_correo)
        self.entry_correo.config(width=50,font=("Arial", 12, "bold"),bg="white")
        self.entry_correo.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
        
        self.mi_direccion = tk.StringVar()
        self.entry_direccion = tk.Entry(self,textvariable= self.mi_direccion)
        self.entry_direccion.config(width=50,font=("Arial", 12, "bold"),bg="white")
        self.entry_direccion.grid(row=3, column=1, padx=10, pady=10, columnspan=2)
        
        self.boton_nuevo = tk.Button(self, text="Nuevo", command=self.habilitar_campos)
        self.boton_nuevo.config (width= 20, font=("Arial", 12, "bold"),fg="white", bg="#158645", cursor="hand2", activebackground="#35BD6F")
        self.boton_nuevo.grid(row=4, column=0, padx=10, pady=10)
        
        self.boton_guardar = tk.Button(self, text="Guardar",command=self.guardar_datos)
        self.boton_guardar.config (width= 20, font=("Arial", 12, "bold"),fg="white", bg="#1558A2", cursor="hand2", activebackground="#4986C9")
        self.boton_guardar.grid(row=4, column=1, padx=10, pady=10)
        
        self.boton_borrar = tk.Button(self, text="Borrar", command=self.deshabilitar_campos)
        self.boton_borrar.config (width= 20, font=("Arial", 12, "bold"),fg="white", bg="#BD152E", cursor="hand2", activebackground="#DB576B")
        self.boton_borrar.grid(row=4, column=2, padx=10, pady=10)
    
    def habilitar_campos(self):
        self.mi_nombre.set("")
        self.mi_telefono.set("")
        self.mi_correo.set("")
        self.mi_direccion.set("")
        
        self.entry_nombre.config(state="normal")
        self.entry_telefono.config(state="normal")
        self.entry_correo.config(state="normal")
        self.entry_direccion.config(state="normal")
        
        self.boton_guardar.config(state="normal")
        self.boton_borrar.config(state="normal")
        
    def deshabilitar_campos(self):
        self.mi_nombre.set("")
        self.mi_telefono.set("")
        self.mi_correo.set("")
        self.mi_direccion.set("")
        
        self.entry_nombre.config(state="disabled")
        self.entry_telefono.config(state="disabled")
        self.entry_correo.config(state="disabled")
        self.entry_direccion.config(state="disabled")
        
        self.boton_guardar.config(state="disabled")
        self.boton_borrar.config(state="disabled")
    
    def guardar_datos(self):
        
        db_py = ConexionDB('mongodb://ElDunkin:Colombia2025@cluster0-shard-00-00.lb9ox.mongodb.net:27017,cluster0-shard-00-01.lb9ox.mongodb.net:27017,cluster0-shard-00-02.lb9ox.mongodb.net:27017/?replicaSet=atlas-8cchfh-shard-0&ssl=true&authSource=admin', 
                        'Petfriendly', 
                        'Aspirante_Adopcion')
        db_py.insertar_datos({"nombre_aspirante": self.mi_nombre.get(), "telefono_aspirante": self.mi_telefono.get(), "correo_aspirante": self.mi_correo.get(), "direccion_aspirante": self.mi_direccion.get()})
        self.deshabilitar_campos()
        self.actualizar_tabla()
    
    def actualizar_tabla(self):
    # Borra filas existentes
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        
    # Vuelve a cargar los datos
        db_py = ConexionDB('mongodb://ElDunkin:Colombia2025@cluster0-shard-00-00.lb9ox.mongodb.net:27017,cluster0-shard-00-01.lb9ox.mongodb.net:27017,cluster0-shard-00-02.lb9ox.mongodb.net:27017/?replicaSet=atlas-8cchfh-shard-0&ssl=true&authSource=admin', 
                        'Petfriendly', 
                        'Aspirante_Adopcion')
        datos = db_py.obtener_todos()
    
        if not datos:
            print("No hay data")
        else:
            for i, dato in enumerate(datos, start=1):
                nombre = dato.get("nombre_aspirante", "")
                telefono = dato.get("telefono_aspirante", "")
                correo = dato.get("correo_aspirante", "")
                direccion = dato.get("direccion_aspirante", "")
            
                self.tabla.insert("", "end", text=str(i), values=(dato.get("_id", ""), nombre, telefono, correo, direccion))

    
    def tabla_pelicula(self):
        
        db_py = ConexionDB('mongodb://ElDunkin:Colombia2025@cluster0-shard-00-00.lb9ox.mongodb.net:27017,cluster0-shard-00-01.lb9ox.mongodb.net:27017,cluster0-shard-00-02.lb9ox.mongodb.net:27017/?replicaSet=atlas-8cchfh-shard-0&ssl=true&authSource=admin', 
                        'Petfriendly', 
                        'Aspirante_Adopcion')
        
        datos = {}
        
        datos = db_py.obtener_todos()
        
        self.tabla = ttk.Treeview(self, columns=("ID", "Nombre Aspirante", "Telefono Aspirante", "Correo Aspirante", "Dirección Aspirante"), show='headings')
        self.tabla.grid(row=4, column=0, columnspan=4, padx=10, pady=10)
        
        self.tabla.heading("#1", text="ID")
        self.tabla.heading("#2", text="Nombre Aspirante")
        self.tabla.heading("#3", text="Telefono Aspirante")
        self.tabla.heading("#4", text="Correo Aspirante")
        self.tabla.heading("#5", text="Direccion Aspirante")
        
        
        
        
        self.boton_editar = tk.Button(self, text="Editar")
        self.boton_editar.config(width= 20, font=("Arial", 12, "bold"), fg = "white", bg="#158645", cursor="hand2", activebackground="#35bd6f")
        self.boton_editar.grid(row=5, column=0, padx=10, pady=10)
        
        self.boton_eliminar = tk.Button(self, text="Eliminar")
        self.boton_eliminar.config(width= 20, font=("Arial", 12, "bold"), fg = "white", bg="#BD152E", cursor="hand2", activebackground="#E15370")
        self.boton_eliminar.grid(row=5, column=1, padx=10, pady=10)
        