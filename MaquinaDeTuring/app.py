# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
from cinta import SIMBOLO_VACIO

CUENTA_CELDAS = 41           # Número de celdas visibles 
ANCHO_CELDA   = 2            # Ancho de cada celda en caracteres
PADX_CELDA    = 3            # Espacio horizontal interno de la celda
PADY_CELDA    = 3            # Espacio vertical interno de la celda
RADIO_VISTA   = CUENTA_CELDAS // 2  # Radio de la ventana respecto al cabezal
ESPACIO_CENTRO = 20          # Blancos a cada lado al cargar la cadena

class App:
    def __init__(self, raiz, maquinas: dict):
        # Se guarda la referencia a Tk y a las máquinas disponibles
        self.raiz = raiz
        self.maquinas = maquinas
        self.raiz.title("Simulador de Turing")

        # Se intenta maximizar la ventana 
        try:
            self.raiz.state("zoomed")
        except Exception:
            self.raiz.geometry("1200x700")  # Tamaño grande de respaldo

        # Se fija la ejecución automática a una velocidad razonable
        self.en_ejecucion = False
        self.retraso_ms = 250

        # Se toma la primera máquina por defecto
        self.nombre_mt = list(self.maquinas.keys())[0]
        self.mt = self.maquinas[self.nombre_mt]

        # Estructuras para marcado visual de celdas leídas
        self.indices_leidos = set()   # Guarda índices absolutos ya leídos
        self.marca_texto = {}         # idx absoluto -> caracter p/q/r mostrado

        # Se define un grid general para centrar la cinta en la ventana
        self.raiz.rowconfigure(1, weight=1)
        self.raiz.rowconfigure(3, weight=1)
        self.raiz.columnconfigure(0, weight=1)

        # Se construye la interfaz y se deja lista
        self._construir_ui()
        self._centrar_cadena()
        self._actualizar_vista()

    def _construir_ui(self):
        # Barra superior (entrada de cadenas y selector de lenguaje)
        barra = ttk.Frame(self.raiz, padding=(12, 10))
        barra.grid(row=0, column=0, sticky="ew")
        barra.columnconfigure(3, weight=1)

        ttk.Label(barra, text="Cadenas:").grid(row=0, column=0, sticky="w")
        self.txt_cadena = ttk.Entry(barra, width=48)
        self.txt_cadena.grid(row=0, column=1, sticky="w", padx=(6, 12))

        ttk.Button(barra, text="Aplicar", command=self._aplicar_entrada).grid(row=0, column=2, sticky="w")

        ttk.Label(barra, text="L:", padding=(12, 0)).grid(row=0, column=3, sticky="e")
        self.cmb_mt = ttk.Combobox(barra, state="readonly",
                                   values=list(self.maquinas.keys()), width=28)
        self.cmb_mt.current(0)
        self.cmb_mt.bind("<<ComboboxSelected>>", self._al_seleccionar_mt)
        self.cmb_mt.grid(row=0, column=4, sticky="w", padx=(6, 0))

        # Espaciador superior 
        ttk.Frame(self.raiz).grid(row=1, column=0, sticky="nsew")

        # Caja de la cinta 
        envoltura_cinta = ttk.Frame(self.raiz, padding=(12, 0))
        envoltura_cinta.grid(row=2, column=0, sticky="n")

        marco_cinta = ttk.LabelFrame(envoltura_cinta, text="Cinta", padding=16)
        marco_cinta.grid()

        interior = ttk.Frame(marco_cinta)
        interior.grid()

        # Fila de celdas visibles
        self.lbl_celdas = []
        fila_celdas = ttk.Frame(interior)
        fila_celdas.grid()
        for _ in range(CUENTA_CELDAS):
            # Se usa tk.Label para poder cambiar fondo fácilmente
            celda = tk.Label(
                fila_celdas, text="_", width=ANCHO_CELDA, bd=1, relief="groove",
                padx=PADX_CELDA, pady=PADY_CELDA, bg="white"
            )
            celda.pack(side="left", padx=1, pady=2)
            self.lbl_celdas.append(celda)

        # Fila de flechas 
        self.lbl_flechas = []
        fila_flechas = ttk.Frame(interior)
        fila_flechas.grid(pady=(2, 0))
        for _ in range(CUENTA_CELDAS):
            flecha = tk.Label(
                fila_flechas, text=" ", width=ANCHO_CELDA,
                padx=PADX_CELDA, pady=0, bg=self.raiz.cget("background")
            )
            flecha.pack(side="left", padx=1)
            self.lbl_flechas.append(flecha)

        # Resultado debajo de la cinta 
        self.lbl_resultado = ttk.Label(marco_cinta, text="", font=("Segoe UI", 11, "bold"))
        self.lbl_resultado.grid(pady=(8, 0))

        # Espaciador inferior 
        ttk.Frame(self.raiz).grid(row=3, column=0, sticky="nsew")

        # Controles inferiores
        controles = ttk.Frame(self.raiz, padding=(12, 10))
        controles.grid(row=4, column=0, sticky="ew")
        controles.columnconfigure(0, weight=1)

        cont_botones = ttk.Frame(controles)
        cont_botones.grid(row=0, column=0)
        ttk.Button(cont_botones, text="Paso", command=self._hacer_paso).pack(side="left", padx=10)
        ttk.Button(cont_botones, text="Iniciar", command=self._iniciar).pack(side="left", padx=10)
        ttk.Button(cont_botones, text="Reiniciar", command=self._reiniciar).pack(side="left", padx=10)

        # Barra de estado inferior
        estado = ttk.Frame(self.raiz, padding=(12, 0))
        estado.grid(row=5, column=0, sticky="ew")
        self.lbl_estado = ttk.Label(estado, text="Estado: q0")
        self.lbl_estado.pack(side="left")
        self.lbl_info = ttk.Label(estado, text="Listo", foreground="blue")
        self.lbl_info.pack(side="right")

    def _al_seleccionar_mt(self, _):
        # Se obtiene el nombre escogido y se cambia la MT activa
        self.nombre_mt = self.cmb_mt.get()
        self.mt = self.maquinas[self.nombre_mt]
        # Se reinicia la vista con la nueva MT
        self._reiniciar()

    def _mapa_simbolo_visual(self):
        # Se construye el mapeo de lectura a p/q/r según el alfabeto de la MT
        A = self.mt.alfabeto_entrada
        if A.issubset({"0", "1"}):
            return {"0": "p", "1": "q"}        # 0 -> p, 1 -> q
        if A.issubset({"a", "b"}):
            return {"a": "p", "b": "q"}        # a -> p, b -> q
        if A.issubset({"a", "b", "c"}):
            return {"a": "p", "b": "q", "c": "r"}  # a -> p, b -> q, c -> r
        return {}

    def _centrar_cadena(self):
        # Se toma la cadena que escribió el usuario
        cadena = self.txt_cadena.get()
        # Se reinicia la MT con esa cadena
        self.mt.reiniciar(cadena)
        # Se agregan blancos a ambos lados para centrar visualmente
        self.mt.cinta.cinta = [SIMBOLO_VACIO]*ESPACIO_CENTRO + self.mt.cinta.cinta + [SIMBOLO_VACIO]*ESPACIO_CENTRO
        # Se coloca el cabezal en el primer símbolo real de la cadena
        self.mt.cinta.posicion = ESPACIO_CENTRO
        # Se limpian marcas visuales previas
        self.indices_leidos.clear()
        self.marca_texto.clear()
        # Se limpia el resultado textual
        self.lbl_resultado.config(text="", foreground="black")

    def _aplicar_entrada(self):
        # Se valida que todos los símbolos pertenezcan al alfabeto de la MT activa
        cadena = self.txt_cadena.get()
        if not all(ch in self.mt.alfabeto_entrada for ch in cadena):
            messagebox.showerror("Error", f"Símbolos fuera del alfabeto: {self.mt.alfabeto_entrada}")
            return
        # Se centra y se refresca la vista
        self._centrar_cadena()
        self.lbl_info.config(text="Listo", foreground="blue")
        self._actualizar_vista()

    def _reiniciar(self):
        # Se detiene el bucle automático y se centra la cadena nuevamente
        self.en_ejecucion = False
        self._centrar_cadena()
        self.lbl_info.config(text="Listo", foreground="blue")
        self._actualizar_vista()

    def _hacer_paso(self):
        # Si ya se detuvo, no avanza
        if self.mt.detendida:
            return

        # Se marca visualmente la celda que está leyendo AHORA
        idx = self.mt.cinta.posicion
        simbolo = self.mt.cinta.leer()
        mapa = self._mapa_simbolo_visual()
        if simbolo in mapa:
            # Se guarda el caracter de marca (p/q/r) para ese índice absoluto
            self.marca_texto[idx] = mapa[simbolo]
        # Se registra que esa celda ya fue leída
        self.indices_leidos.add(idx)

        # Se ejecuta un paso real de la MT (escribir/mover/cambiar estado)
        self.mt.avanzar()

        # Si ya se detuvo, se muestra el veredicto textual
        if self.mt.detendida:
            if self.mt.aceptada:
                self.lbl_resultado.config(text="Cadena ACEPTADA", foreground="green")
            else:
                self.lbl_resultado.config(text="Cadena RECHAZADA", foreground="red")

        # Se actualiza la vista después del paso
        self._actualizar_vista()

    def _iniciar(self):
        # Si ya está corriendo, se ignora
        if self.en_ejecucion:
            return
        # Se inicia el bucle automático
        self.en_ejecucion = True
        self._bucle()

    def _bucle(self):
        # Si se detuvo o pausó, no continúa
        if not self.en_ejecucion:
            return
        # Si la MT no ha terminado, ejecuta un paso
        if not self.mt.detendida:
            self._hacer_paso()
        # Mientras siga en ejecución y no se haya detenido, agenda el siguiente paso
        if self.en_ejecucion and not self.mt.detendida:
            self.raiz.after(self.retraso_ms, self._bucle)

    def _actualizar_vista(self):
        # Se calcula la ventana de celdas a mostrar alrededor del cabezal
        inicio = max(0, self.mt.cinta.posicion - RADIO_VISTA)
        fin = self.mt.cinta.posicion + RADIO_VISTA + 1
        ventana = self.mt.cinta.cinta[inicio:fin]
        idx_cabezal = self.mt.cinta.posicion - inicio  # índice de la flecha

        # Se dibujan las celdas
        for i, lbl in enumerate(self.lbl_celdas):
            if i < len(ventana):
                idx_abs = inicio + i
                ch = ventana[i]
                # Si la celda ya se leyó y hay marca, se muestra p/q/r en vez del símbolo real
                if idx_abs in self.marca_texto:
                    ch = self.marca_texto[idx_abs]
                lbl.config(text=ch)

                # Se colorea la celda actual o las ya leídas
                if idx_abs == self.mt.cinta.posicion:
                    lbl.config(bg="#cfe8ff")      # celda del cabezal 
                elif idx_abs in self.indices_leidos:
                    lbl.config(bg="#eeeeee")      # celda ya leída 
                else:
                    lbl.config(bg="white")        # celda normal
            else:
                # Si no hay celda en la ventana, se dibuja vacío
                lbl.config(text=SIMBOLO_VACIO, bg="white")

        # Se dibuja la flecha solo en la posición del cabezal
        for i, flecha in enumerate(self.lbl_flechas):
            flecha.config(text="^" if i == idx_cabezal else " ")

        # Se actualiza el texto de estado
        self.lbl_estado.config(text=f"Estado: {self.mt.estado}")