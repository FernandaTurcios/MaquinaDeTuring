# -*- coding: utf-8 -*-

import tkinter as tk
from turing import construir_maquinas
from app import App

def main():
    # Se construye el conjunto de máquinas disponibles
    maquinas = construir_maquinas()
    # Se crea la ventana Tk
    raiz = tk.Tk()
    # Se instancia la aplicación con la ventana y las máquinas
    App(raiz, maquinas)
    # Se inicia el loop de eventos
    raiz.mainloop()

if __name__ == "__main__":
    main()