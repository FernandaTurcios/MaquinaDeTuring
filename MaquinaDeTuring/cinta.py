# -*- coding: utf-8 -*-

SIMBOLO_VACIO = "_"  # Se define el símbolo que representa una celda vacía

class TMTape:
    def __init__(self, entrada: str = ""):
        # Se almacena la cinta como una lista de caracteres
        self.cinta = list(entrada) if entrada else []
        # Se coloca el cabezal al inicio (posición 0)
        self.posicion = 0
        # Se asegura que exista al menos una celda para leer/escribir
        self._asegurar_celda()

    def _asegurar_celda(self):
        # Si el cabezal se mueve a la izquierda del índice 0, se inserta una celda vacía
        while self.posicion < 0:
            self.cinta.insert(0, SIMBOLO_VACIO)
            self.posicion += 1
        # Si el cabezal pasa el final, se agrega una celda vacía al final
        if self.posicion >= len(self.cinta):
            self.cinta.append(SIMBOLO_VACIO)

    def leer(self) -> str:
        # Se asegura que la posición sea válida antes de leer
        self._asegurar_celda()
        # Se devuelve el símbolo bajo el cabezal
        return self.cinta[self.posicion]

    def escribir(self, simbolo: str) -> None:
        # Se asegura que la posición sea válida antes de escribir
        self._asegurar_celda()
        # Se escribe el símbolo en la posición actual
        self.cinta[self.posicion] = simbolo

    def mover(self, direccion: str) -> None:
        # Se mueve el cabezal una celda a la izquierda o derecha
        if direccion == "L":
            self.posicion -= 1
        elif direccion == "R":
            self.posicion += 1
        # Se valida que la cinta tenga celdas donde sea necesario
        self._asegurar_celda()

    def ventana(self, radio: int = 20):
        # Se calcula una ventana alrededor del cabezal para visualizar
        inicio = max(0, self.posicion - radio)
        fin = self.posicion + radio + 1
        # Se devuelve el rango y el segmento visible de la cinta
        return inicio, fin, self.cinta[inicio:fin]