import tkinter as tk
import os
from client.gui_app import Frame, barra_menu

IMAGES_PATH = os.path.join(os.path.dirname(__file__), "img")
IMAGE_ICO = os.path.join(IMAGES_PATH,"2459778.ico")

def main():
    # configuracion de la ventana principal
    root = tk.Tk()
    
    # Titulo de la ventana
    root.title("Aspirante Adopcion")
    
    # icono que acompañana al titulo de la ventana
    root.iconbitmap(IMAGE_ICO)
    
    # tamaño Ventana
    root.resizable(0,0)
    
    # Barra menu
    barra_menu(root)
    
    app=Frame(root = root)
    
    
    app.mainloop()
    
if __name__ == "__main__":
    main() 