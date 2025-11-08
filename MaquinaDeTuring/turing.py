# -*- coding: utf-8 -*-

from cinta import TMTape, SIMBOLO_VACIO

class TuringMachine:
    def __init__(
        self,
        estados,
        alfabeto_entrada,
        alfabeto_cinta,
        transiciones,
        estado_inicial,
        estados_aceptacion,
        estados_rechazo=None,
    ):
        # Se normalizan las colecciones y se guarda la tabla de transiciones
        self.estados = set(estados)
        self.alfabeto_entrada = set(alfabeto_entrada)
        self.alfabeto_cinta = set(alfabeto_cinta) | {SIMBOLO_VACIO}
        # Transición: (estado, simbolo_leido) -> (simbolo_escribir, mover, estado_siguiente)
        self.transiciones = dict(transiciones)
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = set(estados_aceptacion)
        self.estados_rechazo = set(estados_rechazo) if estados_rechazo else set()
        # Se prepara la MT en blanco
        self.reiniciar("")

    def reiniciar(self, cadena: str) -> None:
        # Se coloca el estado inicial y la cinta con la cadena dada
        self.estado = self.estado_inicial
        self.cinta = TMTape(cadena)
        # Se marca que aún no se ha detenido ni decidido
        self.detendida = False
        self.aceptada = None

    def avanzar(self) -> None:
        # Si ya se detuvo, no hace nada
        if self.detendida:
            return
        # Se lee el símbolo bajo el cabezal
        simbolo = self.cinta.leer()
        clave = (self.estado, simbolo)
        # Si no hay transición definida, se detiene y decide según el estado actual
        if clave not in self.transiciones:
            self.detendida = True
            self.aceptada = self.estado in self.estados_aceptacion
            return
        # Se aplica la transición: escribir, mover cabezal y cambiar estado
        escribir, mover, siguiente = self.transiciones[clave]
        self.cinta.escribir(escribir)
        self.cinta.mover(mover)
        self.estado = siguiente


# L1: a(b|aa)*  sobre {a,b}
def construir_mt_a_baa_est():
    estados = ["q0", "qB", "qA", "q_acc", "q_rej"]
    A = {"a", "b"}
    T = {}
    # Debe iniciar con 'a'
    T[("q0", "a")] = ("a", "R", "qB")
    T[("q0", "b")] = ("b", "S", "q_rej")
    T[("q0", SIMBOLO_VACIO)] = (SIMBOLO_VACIO, "S", "q_rej")
    # Entre bloques: permite 'b' o la primera 'a' de 'aa'
    T[("qB", "b")] = ("b", "R", "qB")
    T[("qB", "a")] = ("a", "R", "qA")
    T[("qB", SIMBOLO_VACIO)] = (SIMBOLO_VACIO, "S", "q_acc")
    # Dentro del bloque 'aa': exige la segunda 'a'
    T[("qA", "a")] = ("a", "R", "qB")
    T[("qA", "b")] = ("b", "S", "q_rej")
    T[("qA", SIMBOLO_VACIO)] = (SIMBOLO_VACIO, "S", "q_rej")
    return TuringMachine(estados, A, A, T, "q0", {"q_acc"}, {"q_rej"})

# L2: 0*1*  sobre {0,1}
def construir_mt_0_est_1_est():
    estados = ["q0", "q1", "q_acc", "q_rej"]
    A = {"0", "1"}
    T = {}
    # En q0 se aceptan 0's; si ve 1, pasa a q1; BLANK en q0 acepta (todos 0 o vacía)
    T[("q0", "0")] = ("0", "R", "q0")
    T[("q0", "1")] = ("1", "R", "q1")
    T[("q0", SIMBOLO_VACIO)] = (SIMBOLO_VACIO, "S", "q_acc")
    # En q1 solo se aceptan 1's; si ve 0 rompe la forma 0*1*
    T[("q1", "1")] = ("1", "R", "q1")
    T[("q1", "0")] = ("0", "S", "q_rej")
    T[("q1", SIMBOLO_VACIO)] = (SIMBOLO_VACIO, "S", "q_acc")
    return TuringMachine(estados, A, A, T, "q0", {"q_acc"}, {"q_rej"})

# L3: ([ab] | c[ab])* c  sobre {a,b,c}  (equivalente: termina en 'c' y no contiene 'cc')
def construir_mt_termina_c_sin_cc():
    estados = ["qN", "qC", "q_acc", "q_rej"]
    A = {"a", "b", "c"}
    T = {}
    # qN = último no fue 'c'; qC = último fue 'c'
    T[("qN", "a")] = ("a", "R", "qN")
    T[("qN", "b")] = ("b", "R", "qN")
    T[("qN", "c")] = ("c", "R", "qC")
    T[("qN", SIMBOLO_VACIO)] = (SIMBOLO_VACIO, "S", "q_rej")   # no termina en c
    # En qC no se puede leer otra 'c'; si BLANK, acepta
    T[("qC", "a")] = ("a", "R", "qN")
    T[("qC", "b")] = ("b", "R", "qN")
    T[("qC", "c")] = ("c", "S", "q_rej")
    T[("qC", SIMBOLO_VACIO)] = (SIMBOLO_VACIO, "S", "q_acc")
    return TuringMachine(estados, A, A, T, "qN", {"q_acc"}, {"q_rej"})

# L4: (a|b)* a (a|b)*  sobre {a,b}   (contiene al menos una 'a')
def construir_mt_contiene_a():
    estados = ["qN", "qY", "q_acc", "q_rej"]  # qN: no vio 'a'; qY: ya vio 'a'
    A = {"a", "b"}
    T = {}
    T[("qN", "a")] = ("a", "R", "qY")
    T[("qN", "b")] = ("b", "R", "qN")
    T[("qN", SIMBOLO_VACIO)] = (SIMBOLO_VACIO, "S", "q_rej")
    T[("qY", "a")] = ("a", "R", "qY")
    T[("qY", "b")] = ("b", "R", "qY")
    T[("qY", SIMBOLO_VACIO)] = (SIMBOLO_VACIO, "S", "q_acc")
    return TuringMachine(estados, A, A, T, "qN", {"q_acc"}, {"q_rej"})

# L5: 1(01)*0  sobre {0,1}
def construir_mt_1_01_est_0():
    estados = ["q0", "q1", "q2", "q_acc", "q_rej"]
    A = {"0", "1"}
    T = {}
    # Debe iniciar en 1
    T[("q0", "1")] = ("1", "R", "q1")
    T[("q0", "0")] = ("0", "S", "q_rej")
    T[("q0", SIMBOLO_VACIO)] = (SIMBOLO_VACIO, "S", "q_rej")
    # En q1 espera 0 para formar '10'
    T[("q1", "0")] = ("0", "R", "q2")
    T[("q1", "1")] = ("1", "S", "q_rej")
    T[("q1", SIMBOLO_VACIO)] = (SIMBOLO_VACIO, "S", "q_rej")
    # En q2 puede repetir bloque '01' (si ve 1) o terminar (si BLANK)
    T[("q2", "1")] = ("1", "R", "q1")
    T[("q2", "0")] = ("0", "S", "q_rej")  # no se permiten dos ceros seguidos
    T[("q2", SIMBOLO_VACIO)] = (SIMBOLO_VACIO, "S", "q_acc")
    return TuringMachine(estados, A, A, T, "q0", {"q_acc"}, {"q_rej"})

# Construye las 5 máquinas y devuelve un dict nombre -> instancia
def construir_maquinas():
    return {
        "L1: a(b|aa)*"       : construir_mt_a_baa_est(),
        "L2: 0*1*"           : construir_mt_0_est_1_est(),
        "L3: ([ab]|c[ab])*c" : construir_mt_termina_c_sin_cc(),
        "L4: (a|b)*a(a|b)*"  : construir_mt_contiene_a(),
        "L5: 1(01)*0"        : construir_mt_1_01_est_0(),
    }