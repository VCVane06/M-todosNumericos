"""
╔══════════════════════════════════════════════════════════════════════════╗
║           MÉTODOS MILLONARIOS — Simulador de Aprendizaje Numérico       ║
║           Equipo 3 | Métodos Numéricos | FIME - UANL                    ║
╠══════════════════════════════════════════════════════════════════════════╣
║  Integrantes:                                                            ║
║    • Vanessa Jazmín Villarreal Contreras   2094656                      ║
║    • Jaime Daniel Moreno Ponce             1827891                      ║
║    • Ana Paola González Márquez            2070081                      ║
║    • Adrian Zarate Ruiz                   2102484                      ║
║    • Diego Alonso Pérez Barrón            2099212                      ║
╚══════════════════════════════════════════════════════════════════════════╝

INSTRUCCIONES:
    pip install matplotlib pygame
    Coloca metodos_numericos.py en la misma carpeta.
    (Opcional) Carpeta sonidos/ con archivos .wav para efectos.
    python metodos_millonarios.py
"""

# ══════════════════════════════════════════════════════════
#  IMPORTS
# ══════════════════════════════════════════════════════════

import csv
import os
import random
import tkinter as tk
from datetime import datetime
from tkinter import font as tkfont, messagebox, simpledialog

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_OK = True
except Exception:
    MATPLOTLIB_OK = False

try:
    import pygame
    pygame.mixer.init()
    PYGAME_OK = True
except Exception:
    PYGAME_OK = False

from metodos_numericos import (
    biseccion,
    gauss_seidel,
    jacobi,
    lagrange_interpolar,
    newton_raphson,
    runge_kutta4,
    simpson_13,
    trapecio,
)


# ══════════════════════════════════════════════════════════
#  CONSTANTES GLOBALES
# ══════════════════════════════════════════════════════════

PREMIOS = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
PENALIZACION = 0.5
HISTORIAL_CSV = "historial_puntajes.csv"

# Tiempo por defecto en segundos (conceptual / dinámica)
TIEMPOS_DEFAULT = {
    1: {"conceptual": 60,  "dinamica": 90},
    2: {"conceptual": 75,  "dinamica": 120},
    3: {"conceptual": 90,  "dinamica": 150},
}


# ══════════════════════════════════════════════════════════
#  BANCO DE PREGUNTAS CONCEPTUALES  (6 por etapa)
# ══════════════════════════════════════════════════════════

PREGUNTAS = {

    # ── ETAPA 1: Teoría de errores · Bisección · Newton-Raphson ──────────
    1: [
        {
            "tipo": "conceptual",
            "pregunta": "El error relativo porcentual se define como:",
            "opciones": [
                "|(valor verdadero - aprox) / aprox| x 100",
                "|(valor verdadero - aprox) / verdadero| x 100",
                "|(aprox - verdadero)| x 100",
                "|(verdadero) / aprox| x 100",
            ],
            "correcta": 1,
            "pista": "Fórmula: εr = |(Vv − Va) / Vv| × 100%",
            "explicacion": "El error relativo usa el valor verdadero en el denominador para normalizar el error absoluto.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "En Bisección, si f(a)·f(c) < 0, la raíz está en:",
            "opciones": [
                "El intervalo [c, b]",
                "El intervalo [a, c]",
                "Exactamente en c",
                "Fuera del intervalo [a, b]",
            ],
            "correcta": 1,
            "pista": "Si f(a) y f(c) tienen signos opuestos, la raíz está entre a y c.",
            "explicacion": "Por el Teorema del Valor Intermedio, si f(a)·f(c) < 0 existe una raíz en [a, c].",
        },
        {
            "tipo": "conceptual",
            "pregunta": "La fórmula iterativa de Newton-Raphson es:",
            "opciones": [
                "x_{n+1} = x_n − f(x_n) / f'(x_n)",
                "x_{n+1} = x_n + f(x_n) / f'(x_n)",
                "x_{n+1} = x_n − f'(x_n) / f(x_n)",
                "x_{n+1} = (a + b) / 2",
            ],
            "correcta": 0,
            "pista": "Newton-Raphson usa la tangente: x_{n+1} = x_n − f(x_n)/f'(x_n)",
            "explicacion": "Newton-Raphson aproxima la raíz usando la línea tangente en el punto actual.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "Si el error absoluto disminuye en cada iteración, el método:",
            "opciones": ["Diverge", "Converge", "Es exacto", "No tiene solución"],
            "correcta": 1,
            "pista": "Converger significa acercarse progresivamente a la solución.",
            "explicacion": "Un método converge cuando sus aproximaciones tienden hacia la solución buscada.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "Newton-Raphson puede fallar si:",
            "opciones": [
                "f'(x_n) es cero o muy pequeña",
                "La función es continua",
                "El error es porcentual",
                "El intervalo tiene cambio de signo",
            ],
            "correcta": 0,
            "pista": "La derivada aparece en el denominador de la fórmula.",
            "explicacion": "Si f'(x_n) ≈ 0, la fórmula divide entre cero y el método falla.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "El Teorema del Valor Intermedio garantiza raíz en [a,b] si:",
            "opciones": [
                "f(a) > 0 y f(b) > 0",
                "f(a) · f(b) < 0",
                "f(a) = f(b)",
                "f(a) + f(b) = 0",
            ],
            "correcta": 1,
            "pista": "Se necesita un cambio de signo entre los extremos del intervalo.",
            "explicacion": "Si f(a) y f(b) tienen signos opuestos, por continuidad debe existir al menos una raíz.",
        },
    ],

    # ── ETAPA 2: Jacobi · Gauss-Seidel · Interpolación de Lagrange ───────
    2: [
        {
            "tipo": "conceptual",
            "pregunta": "Para que Jacobi converja de forma garantizada, la matriz debe ser:",
            "opciones": [
                "Simétrica",
                "Estrictamente diagonal dominante",
                "Triangular superior",
                "Ortogonal",
            ],
            "correcta": 1,
            "pista": "|a_ii| > suma de los otros valores absolutos de la fila.",
            "explicacion": "La diagonal dominante estricta es condición suficiente de convergencia para Jacobi.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "¿Cuál método usa los valores recién calculados dentro de la misma iteración?",
            "opciones": ["Jacobi", "Gauss-Seidel", "Lagrange", "Trapecio"],
            "correcta": 1,
            "pista": "Gauss-Seidel actualiza y reutiliza al instante.",
            "explicacion": "Gauss-Seidel usa los valores más recientes para acelerar la convergencia.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "La interpolación de Lagrange para n+1 puntos produce un polinomio de grado:",
            "opciones": ["n+1", "n", "n−1", "2n"],
            "correcta": 1,
            "pista": "n+1 puntos generan grado a lo más n.",
            "explicacion": "Con n+1 puntos se construye un único polinomio de grado ≤ n que pasa por todos ellos.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "En Jacobi, los nuevos valores se calculan usando:",
            "opciones": [
                "Solo los valores de la iteración anterior",
                "Solo los valores exactos",
                "Los valores nuevos de inmediato",
                "La regla de Simpson",
            ],
            "correcta": 0,
            "pista": "Jacobi espera terminar toda la iteración antes de actualizar.",
            "explicacion": "Jacobi calcula todo x^(k+1) usando únicamente x^(k), a diferencia de Gauss-Seidel.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "La interpolación de Lagrange sirve principalmente para:",
            "opciones": [
                "Resolver matrices",
                "Aproximar valores entre datos conocidos",
                "Calcular derivadas exactas",
                "Ordenar vectores",
            ],
            "correcta": 1,
            "pista": "Inter-polar: estimar entre puntos.",
            "explicacion": "La interpolación estima valores dentro del rango de datos conocidos.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "Una matriz diagonal dominante por filas cumple:",
            "opciones": [
                "|a_ii| >= suma de |a_ij| para j ≠ i",
                "a_ii = 0",
                "Todas las filas son iguales",
                "El determinante siempre es 1",
            ],
            "correcta": 0,
            "pista": "La diagonal debe dominar a los demás elementos de su fila.",
            "explicacion": "La dominancia diagonal compara el elemento diagonal con la suma del resto de la fila.",
        },
    ],

    # ── ETAPA 3: Trapecio · Simpson 1/3 · Runge-Kutta 4 ─────────────────
    3: [
        {
            "tipo": "conceptual",
            "pregunta": "La Regla de Simpson 1/3 requiere que el número de subintervalos sea:",
            "opciones": ["Impar", "Par", "Múltiplo de 3", "Cualquier entero positivo"],
            "correcta": 1,
            "pista": "Simpson 1/3 agrupa pares de subintervalos.",
            "explicacion": "Simpson 1/3 requiere n par porque aplica la fórmula de tres puntos en grupos de dos subintervalos.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "El orden de error global de Runge-Kutta de 4to orden es:",
            "opciones": ["O(h²)", "O(h³)", "O(h⁴)", "O(h⁵)"],
            "correcta": 2,
            "pista": "RK4 tiene error local O(h⁵), lo que da error global O(h⁴).",
            "explicacion": "El error global de RK4 es O(h⁴), un excelente balance entre precisión y costo.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "La Regla del Trapecio compuesta tiene error de orden:",
            "opciones": ["O(h)", "O(h²)", "O(h³)", "O(h⁴)"],
            "correcta": 1,
            "pista": "Error del Trapecio: −(b−a)h²/12 · f''(ξ) → O(h²).",
            "explicacion": "La regla del trapecio compuesta tiene error O(h²), menos precisa que Simpson O(h⁴).",
        },
        {
            "tipo": "conceptual",
            "pregunta": "Simpson 1/3 es más preciso que Trapecio porque:",
            "opciones": [
                "Usa aproximación cuadrática (parábolas)",
                "No requiere evaluar la función",
                "Siempre da el valor exacto",
                "No usa subintervalos",
            ],
            "correcta": 0,
            "pista": "Trapecio usa rectas; Simpson usa parábolas.",
            "explicacion": "Simpson aproxima la curva con polinomios de segundo grado, logrando mayor precisión.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "En RK4, las cuatro pendientes k1, k2, k3, k4 se combinan con pesos:",
            "opciones": [
                "1, 2, 2, 1  (divididos entre 6)",
                "1, 1, 1, 1  (divididos entre 4)",
                "1, 3, 3, 1  (divididos entre 8)",
                "2, 1, 1, 2  (divididos entre 6)",
            ],
            "correcta": 0,
            "pista": "La combinación es (k1 + 2k2 + 2k3 + k4) / 6.",
            "explicacion": "RK4 da doble peso a las pendientes del punto medio k2 y k3, y peso simple a los extremos.",
        },
        {
            "tipo": "conceptual",
            "pregunta": "La Regla del Trapecio aproxima el área bajo la curva usando:",
            "opciones": ["Rectángulos", "Trapecios", "Parábolas", "Triángulos equiláteros"],
            "correcta": 1,
            "pista": "El nombre lo dice: trapecios.",
            "explicacion": "La curva se aproxima con segmentos rectos que forman trapecios entre los puntos evaluados.",
        },
    ],
}


# ══════════════════════════════════════════════════════════
#  GENERADORES DE MINI-RETOS DINÁMICOS
#  Usan metodos_numericos.py para calcular la respuesta real.
# ══════════════════════════════════════════════════════════

def _opciones_numericas(valor, decimales=3):
    """Genera 4 opciones plausibles alrededor del valor correcto."""
    correcto = round(valor, decimales)
    deltas = [0.25, -0.25, 0.5, -0.5, 1.0, -1.0, 0.1, -0.1]
    opciones = {correcto}
    for d in deltas:
        if len(opciones) == 4:
            break
        opciones.add(round(correcto + d, decimales))
    opciones = list(opciones)[:4]
    random.shuffle(opciones)
    return [str(x) for x in opciones], opciones.index(correcto)


# ── Etapa 1 ──────────────────────────────────────────────

def _reto_biseccion():
    r = random.randint(2, 8)
    f = lambda x: x * x - r
    raiz, it = biseccion(f, 1.0, r * 1.0, tol=0.01)
    opciones, correcta = _opciones_numericas(raiz, 2)
    return {
        "tipo": "dinamica",
        "pregunta": f"Mini-reto: usa Bisección en f(x)=x²−{r}, intervalo [1,{r}], tol=0.01. ¿Cuál es la raíz aproximada?",
        "opciones": opciones, "correcta": correcta,
        "pista": "Aplica c=(a+b)/2 y conserva el subintervalo con cambio de signo.",
        "explicacion": f"La raíz aproximada es {raiz:.2f}, obtenida en {it} iteraciones.",
    }


def _reto_newton():
    n = random.choice([2, 3, 5, 7])
    f  = lambda x: x * x - n
    df = lambda x: 2 * x
    raiz, it = newton_raphson(f, df, x0=2.0, tol=0.001)
    opciones, correcta = _opciones_numericas(raiz, 3)
    return {
        "tipo": "dinamica",
        "pregunta": f"Mini-reto: Newton-Raphson para f(x)=x²−{n}, x₀=2, tol=0.001. ¿Cuál es la raíz?",
        "opciones": opciones, "correcta": correcta,
        "pista": "Usa x_{n+1} = x_n − f(x_n)/f'(x_n).",
        "explicacion": f"La raíz aproximada es {raiz:.3f}, alcanzada en {it} iteraciones.",
    }


# ── Etapa 2 ──────────────────────────────────────────────

def _reto_interpolacion():
    a = random.randint(1, 4)
    b = random.randint(0, 5)
    puntos = [(0, b), (1, a + b), (2, 2 * a + b)]
    x_eval = random.choice([3, 4])
    y = lagrange_interpolar(puntos, x_eval)
    opciones, correcta = _opciones_numericas(y, 0)
    return {
        "tipo": "dinamica",
        "pregunta": f"Mini-reto: interpola con Lagrange los puntos {puntos}. ¿Qué valor estimas en x={x_eval}?",
        "opciones": opciones, "correcta": correcta,
        "pista": "Construye el polinomio que pasa exactamente por los tres puntos.",
        "explicacion": f"Los puntos pertenecen a y={a}x+{b}, por eso y({x_eval})={y:.0f}.",
    }


def _reto_gauss_seidel():
    c = random.randint(4, 8)
    A = [[4, 1], [1, 3]]
    b = [c, c + 1]
    sol, it = gauss_seidel(A, b, [0.0, 0.0], tol=0.001)
    opciones, correcta = _opciones_numericas(sol[0], 3)
    return {
        "tipo": "dinamica",
        "pregunta": f"Mini-reto: sistema 4x+y={c}, x+3y={c+1}. Estima x con Gauss-Seidel desde (0,0).",
        "opciones": opciones, "correcta": correcta,
        "pista": "Despeja x=(b₁−y)/4, y=(b₂−x)/3, reutilizando el valor nuevo de x.",
        "explicacion": f"Gauss-Seidel converge a x={sol[0]:.3f}, y={sol[1]:.3f} en {it} iteraciones.",
    }


def _reto_jacobi():
    c = random.randint(3, 7)
    A = [[5, 1], [1, 4]]
    b = [c, c + 2]
    sol, it = jacobi(A, b, [0.0, 0.0], tol=0.001)
    opciones, correcta = _opciones_numericas(sol[0], 3)
    return {
        "tipo": "dinamica",
        "pregunta": f"Mini-reto: sistema 5x+y={c}, x+4y={c+2}. Estima x con Jacobi desde (0,0).",
        "opciones": opciones, "correcta": correcta,
        "pista": "Jacobi despeja con los valores de la iteración ANTERIOR: x=(b₁−y_ant)/5.",
        "explicacion": f"Jacobi converge a x={sol[0]:.3f}, y={sol[1]:.3f} en {it} iteraciones.",
    }


# ── Etapa 3 ──────────────────────────────────────────────

def _reto_simpson():
    k = random.randint(1, 4)
    f = lambda x: k * x * x
    val = simpson_13(f, 0, 2, 2)
    opciones, correcta = _opciones_numericas(val, 3)
    return {
        "tipo": "dinamica",
        "pregunta": f"Mini-reto: aproxima ∫₀² {k}x² dx con Simpson 1/3 y n=2.",
        "opciones": opciones, "correcta": correcta,
        "pista": "Fórmula: h/3 · [f(x₀) + 4f(x₁) + f(x₂)], h=(b−a)/n.",
        "explicacion": f"El resultado es {val:.3f}. Simpson 1/3 es exacto para polinomios de grado ≤ 3.",
    }


def _reto_trapecio():
    k = random.randint(2, 6)
    f = lambda x: k * x + 1
    val = trapecio(f, 0, 4, 4)
    opciones, correcta = _opciones_numericas(val, 2)
    return {
        "tipo": "dinamica",
        "pregunta": f"Mini-reto: aproxima ∫₀⁴ ({k}x+1) dx con Trapecio compuesto y n=4.",
        "opciones": opciones, "correcta": correcta,
        "pista": "Para funciones lineales, Trapecio da el área exacta.",
        "explicacion": f"El valor es {val:.2f}. La función lineal hace que el error del trapecio sea cero.",
    }


def _reto_rk4():
    k = random.choice([1, 2, 3])
    tf = random.choice([1.0, 2.0])
    h = 0.5
    f_ode = lambda t, y: k * t      # EDO: y' = k·t  →  exacta: y = 1 + k·t²/2
    _, y_vals = runge_kutta4(f_ode, 1.0, 0.0, tf, h)
    y_final = y_vals[-1]
    exacto = 1.0 + k * tf ** 2 / 2
    opciones, correcta = _opciones_numericas(y_final, 3)
    return {
        "tipo": "dinamica",
        "pregunta": f"Mini-reto: resuelve y'={k}t, y(0)=1 con RK4 y h={h} hasta t={tf:.1f}. ¿Cuánto vale y({tf:.1f})?",
        "opciones": opciones, "correcta": correcta,
        "pista": f"La solución exacta es y = 1 + {k}t²/2. RK4 es muy preciso.",
        "explicacion": f"RK4 da y({tf:.1f}) ≈ {y_final:.3f}. Valor exacto: {exacto:.3f}.",
    }


def _generar_dinamicas(etapa):
    """Retorna la lista de mini-retos dinámicos para cada etapa."""
    if etapa == 1:
        return [_reto_biseccion(), _reto_newton()]
    if etapa == 2:
        return [_reto_interpolacion(), _reto_gauss_seidel(), _reto_jacobi()]
    return [_reto_simpson(), _reto_trapecio(), _reto_rk4()]


# ══════════════════════════════════════════════════════════
#  LÓGICA DEL JUEGO
# ══════════════════════════════════════════════════════════

class JuegoMillonarios:

    def __init__(self):
        self.nombre_jugador = ""
        self.etapa_actual   = 1
        self.pregunta_index = 0
        self.puntos         = 0.0
        self.preguntas_etapa = []
        self.comodines = {"5050": True, "experto": True, "convergencia": True}
        self.tiempo_restante = 60
        self.respuestas_eliminadas = []
        self.timer_id = None
        self.tiempos  = {et: vals.copy() for et, vals in TIEMPOS_DEFAULT.items()}

    def cargar_etapa(self, etapa):
        self.etapa_actual   = etapa
        self.pregunta_index = 0
        preguntas = PREGUNTAS[etapa][:] + _generar_dinamicas(etapa)
        random.shuffle(preguntas)
        self.preguntas_etapa = preguntas

    def pregunta_actual(self):
        if self.pregunta_index < len(self.preguntas_etapa):
            return self.preguntas_etapa[self.pregunta_index]
        return None

    def verificar_respuesta(self, idx):
        p = self.pregunta_actual()
        return p is not None and idx == p["correcta"]

    def aplicar_5050(self):
        p = self.pregunta_actual()
        incorrectas = [i for i in range(4) if i != p["correcta"]]
        random.shuffle(incorrectas)
        self.respuestas_eliminadas = incorrectas[:2]
        self.comodines["5050"] = False
        return self.respuestas_eliminadas

    def obtener_pista(self):
        self.comodines["experto"] = False
        return self.pregunta_actual()["pista"]

    def nivel_actual(self):
        base = {1: 0, 2: 4, 3: 7}
        return min(base[self.etapa_actual] + self.pregunta_index, len(PREMIOS) - 1)

    def tiempo_para_pregunta(self):
        p    = self.pregunta_actual() or {"tipo": "conceptual"}
        tipo = p.get("tipo", "conceptual")
        return self.tiempos[self.etapa_actual].get(tipo, 60)


# ══════════════════════════════════════════════════════════
#  INTERFAZ GRÁFICA
# ══════════════════════════════════════════════════════════

class App(tk.Tk):

    # ── Paleta ─────────────────────────────────────────────
    BG_DARK   = "#070B18"
    BG_PANEL  = "#101935"
    BG_OPTION = "#172548"
    BLUE_NEON = "#00D4FF"
    BLUE_MID  = "#145DCC"
    GREEN_OK  = "#00E676"
    RED_FAIL  = "#FF1744"
    GOLD      = "#FFD700"
    WHITE     = "#FFFFFF"
    GRAY      = "#AAB6C8"
    ORANGE    = "#FF8C00"

    def __init__(self):
        super().__init__()
        self.juego  = JuegoMillonarios()
        self._pulse = 0
        self.title("Métodos Millonarios — FIME UANL")
        self.geometry("1050x700")
        self.resizable(False, False)
        self.configure(bg=self.BG_DARK)

        self.f_titulo  = tkfont.Font(family="Courier New", size=20, weight="bold")
        self.f_grande  = tkfont.Font(family="Courier New", size=13, weight="bold")
        self.f_normal  = tkfont.Font(family="Courier New", size=10)
        self.f_pequeno = tkfont.Font(family="Courier New", size=9)
        self.f_opcion  = tkfont.Font(family="Courier New", size=11)

        self._pantalla_inicio()

    # ── Helpers generales ──────────────────────────────────

    def _limpiar(self):
        if self.juego.timer_id:
            try:
                self.after_cancel(self.juego.timer_id)
            except Exception:
                pass
            self.juego.timer_id = None
        for w in self.winfo_children():
            w.destroy()

    def _btn(self, parent, texto, cmd, color=None, w=30, h=2):
        bg = color or self.BLUE_MID
        b  = tk.Button(
            parent, text=texto, command=cmd,
            bg=bg, fg=self.WHITE, relief="flat",
            font=self.f_normal, width=w, height=h,
            activebackground=self.BLUE_NEON, cursor="hand2",
            bd=0, highlightthickness=1, highlightbackground=self.BLUE_NEON,
        )
        self._hover(b, bg)
        return b

    def _hover(self, boton, color_base):
        def on_enter(_): 
            if str(boton.cget("state")) != "disabled":
                boton.config(bg=self.BLUE_NEON, fg=self.BG_DARK)
        def on_leave(_): 
            if str(boton.cget("state")) != "disabled":
                boton.config(bg=color_base, fg=self.WHITE)
        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)

    def _fondo_neon(self):
        c = tk.Canvas(self, width=1050, height=700,
                      bg=self.BG_DARK, highlightthickness=0)
        c.place(x=0, y=0, relwidth=1, relheight=1)
        for i in range(-200, 1200, 80):
            c.create_line(i, 0, i + 260, 700, fill="#0D3A68", width=1)
        for i in range(0, 1100, 90):
            c.create_line(i, 700, i + 180, 0, fill="#1A1148", width=1)
        c.create_oval(210, 85, 840, 625, outline="#123C8C", width=3)
        c.create_oval(250, 120, 800, 590, outline="#00D4FF", width=1)
        c.create_oval(310, 180, 740, 530, outline="#3A1C85", width=2)
        for x in [40, 1000]:
            for y in range(80, 620, 75):
                c.create_oval(x-8, y-8, x+8, y+8, fill="#00D4FF", outline="")
        return c

    def _marco_tv(self, parent):
        externo = tk.Frame(parent, bg=self.BLUE_NEON, padx=2, pady=2)
        interno = tk.Frame(externo, bg=self.BG_PANEL, padx=18, pady=14)
        interno.pack(fill="both", expand=True)
        return externo, interno

    def _flash(self, color, n=4):
        orig = self.cget("bg")
        def paso(i=0):
            if i >= n:
                self.configure(bg=orig)
                return
            self.configure(bg=color if i % 2 == 0 else self.BG_DARK)
            self.after(120, lambda: paso(i + 1))
        paso()

    def _sonido(self, tipo):
        if not PYGAME_OK:
            return
        base    = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.path.join(base, "sonidos")
        for ext in (".wav", ".mp3", ".ogg"):
            ruta = os.path.join(carpeta, tipo + ext)
            if os.path.exists(ruta):
                try:
                    pygame.mixer.Sound(ruta).play()
                except Exception:
                    pass
                return

    def _musica_fondo(self):
        if not PYGAME_OK:
            return
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos", "fondo.wav")
        if os.path.exists(ruta):
            try:
                pygame.mixer.music.load(ruta)
                pygame.mixer.music.set_volume(0.18)
                pygame.mixer.music.play(-1)
            except Exception:
                pass

    def _transicion(self, callback, texto="Preparando pregunta...", delay=850):
        self._limpiar()
        self._fondo_neon()
        self._sonido("transicion")
        cont  = tk.Frame(self, bg=self.BG_DARK)
        cont.pack(expand=True, fill="both")
        label = tk.Label(cont, text=texto, bg=self.BG_DARK,
                         fg=self.BLUE_NEON, font=self.f_titulo)
        label.pack(pady=(250, 12))
        tk.Label(cont, text="* * *", bg=self.BG_DARK,
                 fg=self.GOLD, font=self.f_grande).pack()
        colores = [self.BLUE_NEON, self.WHITE, self.GOLD]
        def parpadear(i=0):
            if not label.winfo_exists():
                return
            label.config(fg=colores[i % len(colores)])
            if i < 5:
                self.after(140, lambda: parpadear(i + 1))
        parpadear()
        self.after(delay, callback)

    # ── Historial CSV ──────────────────────────────────────

    def _guardar_historial(self, resultado):
        existe = os.path.exists(HISTORIAL_CSV)
        with open(HISTORIAL_CSV, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if not existe:
                w.writerow(["fecha", "jugador", "puntos", "etapa_final", "resultado"])
            w.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.juego.nombre_jugador,
                f"{self.juego.puntos:.1f}",
                self.juego.etapa_actual,
                resultado,
            ])

    def _mostrar_historial(self):
        if not os.path.exists(HISTORIAL_CSV):
            messagebox.showinfo("Historial", "Aún no hay puntajes guardados.")
            return
        with open(HISTORIAL_CSV, "r", encoding="utf-8") as f:
            filas = list(csv.reader(f))[-11:]   # encabezado + 10 últimos
        texto = "\n".join(" | ".join(fila) for fila in filas)
        messagebox.showinfo("Últimos puntajes", texto)

    # ══════════════════════════════════════════════════════
    #  PANTALLAS
    # ══════════════════════════════════════════════════════

    # ── Inicio ─────────────────────────────────────────────

    def _pantalla_inicio(self):
        self._limpiar()
        self._fondo_neon()
        self._musica_fondo()
        self._sonido("inicio")

        titulo = tk.Label(self, text="◆  MÉTODOS MILLONARIOS  ◆",
                          bg=self.BG_DARK, fg=self.BLUE_NEON,
                          font=self.f_titulo, padx=25, pady=10,
                          highlightbackground=self.BLUE_NEON, highlightthickness=2)
        titulo.pack(pady=(45, 8))
        self._animar_titulo(titulo)

        tk.Label(self, text="Simulador de Aprendizaje Numérico",
                 bg=self.BG_DARK, fg=self.GRAY, font=self.f_normal).pack()
        tk.Label(self, text="FIME — UANL  |  Métodos Numéricos",
                 bg=self.BG_DARK, fg=self.GRAY, font=self.f_pequeno).pack(pady=(0, 25))

        tk.Label(self, text="Ingresa tu nombre:",
                 bg=self.BG_DARK, fg=self.WHITE, font=self.f_normal).pack()
        self._entry = tk.Entry(
            self, font=self.f_grande, width=25,
            bg=self.BG_PANEL, fg=self.WHITE,
            insertbackground=self.WHITE, bd=0, relief="flat", justify="center",
        )
        self._entry.pack(ipady=8, pady=10)
        self._entry.focus()

        self._btn(self, "⚙  Configurar tiempos",
                  self._configurar_tiempos, color="#4A148C", w=24).pack(pady=8)

        tk.Label(self, text="Selecciona nivel de inicio:",
                 bg=self.BG_DARK, fg=self.GRAY, font=self.f_pequeno).pack(pady=(12, 5))

        frame = tk.Frame(self, bg=self.BG_DARK)
        frame.pack()
        niveles = [
            ("BÁSICO\nErrores · Bisección · N-R",              1, "#1B5E20"),
            ("INTERMEDIO\nJacobi · Gauss-Seidel · Lagrange",   2, "#1A237E"),
            ("AVANZADO\nSimpson · Trapecio · RK4",             3, "#4A148C"),
        ]
        for texto, n, color in niveles:
            tk.Button(
                frame, text=texto,
                command=lambda n=n: self._iniciar_juego(n),
                bg=color, fg=self.WHITE, relief="flat",
                font=self.f_pequeno, width=24, height=4,
                activebackground=self.BLUE_NEON, cursor="hand2", bd=0,
            ).pack(side="left", padx=8)

        self._btn(self, "📋  Ver historial",
                  self._mostrar_historial, color="#263238", w=18).pack(pady=18)

        tk.Label(self, text="Equipo 3 — Vanessa · Jaime · Ana · Adrian · Diego",
                 bg=self.BG_DARK, fg=self.GRAY, font=self.f_pequeno).pack(pady=4)

    def _animar_titulo(self, label):
        if not label.winfo_exists():
            return
        colores = [self.BLUE_NEON, self.WHITE, self.GOLD]
        label.config(fg=colores[self._pulse % len(colores)])
        self._pulse += 1
        self.after(650, lambda: self._animar_titulo(label))

    def _configurar_tiempos(self):
        nombres = {1: "Básica", 2: "Intermedia", 3: "Avanzada"}
        for etapa in [1, 2, 3]:
            for tipo in ["conceptual", "dinamica"]:
                actual = self.juego.tiempos[etapa][tipo]
                nuevo  = simpledialog.askinteger(
                    "Tiempo",
                    f"Etapa {etapa} ({nombres[etapa]}), pregunta {tipo}: segundos",
                    initialvalue=actual, minvalue=10, maxvalue=1800, parent=self,
                )
                if nuevo:
                    self.juego.tiempos[etapa][tipo] = nuevo

    def _iniciar_juego(self, etapa):
        self.juego.nombre_jugador = self._entry.get().strip() or "Jugador"
        self.juego.puntos   = 0.0
        self.juego.comodines = {"5050": True, "experto": True, "convergencia": True}
        self.juego.cargar_etapa(etapa)
        self._transicion(self._pantalla_juego, "Iniciando partida...", 900)

    # ── Pantalla principal de juego ────────────────────────

    def _pantalla_juego(self):
        self._limpiar()
        self._fondo_neon()
        self.juego.respuestas_eliminadas = []
        p = self.juego.pregunta_actual()
        if p is None:
            self._pantalla_fin(True)
            return

        nivel = self.juego.nivel_actual()
        etapa = self.juego.etapa_actual

        # Barra superior
        top = tk.Frame(self, bg=self.BG_DARK)
        top.pack(fill="x", padx=20, pady=8)
        etapa_txt = {1: "ETAPA 1 — BÁSICA", 2: "ETAPA 2 — INTERMEDIA", 3: "ETAPA 3 — AVANZADA"}
        tk.Label(top, text=etapa_txt[etapa],
                 bg=self.BG_DARK, fg=self.BLUE_NEON, font=self.f_pequeno).pack(side="left")
        tk.Label(top, text=f"Jugador: {self.juego.nombre_jugador}  |  Pts: {self.juego.puntos:.1f}",
                 bg=self.BG_DARK, fg=self.GOLD, font=self.f_pequeno).pack(side="right")
        tk.Frame(self, bg=self.BLUE_NEON, height=2).pack(fill="x", padx=20)

        # Pregunta
        marco_ext, marco_q = self._marco_tv(self)
        marco_ext.pack(fill="x", padx=28, pady=14)
        tk.Label(
            marco_q,
            text=f"Pregunta {self.juego.pregunta_index + 1} / {len(self.juego.preguntas_etapa)}"
                 f"  [{p.get('tipo', 'conceptual')}]",
            bg=self.BG_PANEL, fg=self.BLUE_NEON, font=self.f_pequeno,
        ).pack(anchor="w")
        tk.Label(
            marco_q, text=p["pregunta"],
            bg=self.BG_PANEL, fg=self.WHITE, font=self.f_grande,
            wraplength=760, justify="left",
        ).pack(anchor="w", pady=(6, 0))

        # Opciones
        self._botones_opciones = []
        frame_ops = tk.Frame(self, bg=self.BG_DARK)
        frame_ops.pack(padx=20, pady=4, fill="x")
        letras = ["A", "B", "C", "D"]
        for i, opcion in enumerate(p["opciones"]):
            btn = tk.Button(
                frame_ops,
                text=f"  {letras[i]})  {opcion}",
                command=lambda idx=i: self._responder(idx),
                bg=self.BG_OPTION, fg=self.WHITE, font=self.f_opcion,
                relief="flat", width=46, height=2, anchor="w",
                activebackground=self.BLUE_NEON, cursor="hand2", bd=0, padx=10,
            )
            btn.grid(row=i // 2, column=i % 2, padx=8, pady=5)
            self._hover(btn, self.BG_OPTION)
            self._botones_opciones.append(btn)

        # Comodines + temporizador
        frame_com = tk.Frame(self, bg=self.BG_DARK)
        frame_com.pack(pady=10)
        self._btn_5050  = self._btn(frame_com, "½  50/50", self._usar_5050,
                                    "#1B5E20" if self.juego.comodines["5050"] else "#333", w=10, h=1)
        self._btn_5050.pack(side="left", padx=4)
        self._btn_experto = self._btn(frame_com, "Σ  Fórmula", self._usar_experto,
                                      "#1A237E" if self.juego.comodines["experto"] else "#333", w=12, h=1)
        self._btn_experto.pack(side="left", padx=4)
        self._btn_conv  = self._btn(frame_com, "~  Convergencia", self._usar_convergencia,
                                    "#4A148C" if self.juego.comodines["convergencia"] else "#333", w=16, h=1)
        self._btn_conv.pack(side="left", padx=4)
        self._label_tiempo = tk.Label(frame_com, text="",
                                      bg="#350000", fg=self.WHITE, font=self.f_normal, width=8)
        self._label_tiempo.pack(side="left", padx=12)

        # Tabla de premios lateral
        frame_premios = tk.Frame(self, bg=self.BG_PANEL, padx=8, pady=4)
        frame_premios.place(x=875, y=85)
        tk.Label(frame_premios, text="PREMIOS", bg=self.BG_PANEL,
                 fg=self.GOLD, font=self.f_pequeno).pack()
        for i, pts in reversed(list(enumerate(PREMIOS))):
            color = self.BLUE_NEON if i == nivel else (self.GOLD if i < nivel else self.GRAY)
            tk.Label(frame_premios, text=f"P{i+1:02d}  {pts:.1f} pts",
                     bg=self.BG_PANEL, fg=color, font=self.f_pequeno, width=12).pack()

        # Mensaje / feedback
        self._label_msg = tk.Label(self, text="", bg=self.BG_DARK,
                                   fg=self.WHITE, font=self.f_normal, wraplength=720)
        self._label_msg.pack(pady=6)

        self._iniciar_timer()

    # ── Temporizador ───────────────────────────────────────

    def _iniciar_timer(self):
        self.juego.tiempo_restante = self.juego.tiempo_para_pregunta()
        self._tick_timer()

    def _tick_timer(self):
        t = self.juego.tiempo_restante
        if not hasattr(self, "_label_tiempo") or not self._label_tiempo.winfo_exists():
            return
        color = self.RED_FAIL if t <= 10 else (self.ORANGE if t <= 20 else self.WHITE)
        self._label_tiempo.config(text=f" {t:03d}s ", fg=color)
        if t <= 0:
            self._tiempo_agotado()
            return
        self.juego.tiempo_restante -= 1
        self.juego.timer_id = self.after(1000, self._tick_timer)

    def _cancelar_timer(self):
        if self.juego.timer_id:
            self.after_cancel(self.juego.timer_id)
            self.juego.timer_id = None

    def _deshabilitar_opciones(self):
        for b in self._botones_opciones:
            b.config(state="disabled", cursor="arrow")

    def _popup_explicacion(self, titulo, texto, correcta=True):
        win = tk.Toplevel(self)
        win.title(titulo)
        win.geometry("520x280")
        win.configure(bg=self.BG_DARK)
        tk.Label(win, text=titulo, bg=self.BG_DARK,
                 fg=self.GREEN_OK if correcta else self.RED_FAIL,
                 font=self.f_grande).pack(pady=15)
        tk.Label(win, text=texto, bg=self.BG_DARK, fg=self.WHITE,
                 font=self.f_normal, wraplength=460, justify="left").pack(padx=20, pady=10)
        tk.Button(win, text="Continuar", command=win.destroy,
                  bg=self.BLUE_MID, fg=self.WHITE, relief="flat",
                  font=self.f_normal, cursor="hand2").pack(pady=15)
        self.after(3000, lambda: win.destroy() if win.winfo_exists() else None)

    # ── Respuesta / tiempo ────────────────────────────────

    def _tiempo_agotado(self):
        self._cancelar_timer()
        self._sonido("tiempo")
        self._flash(self.RED_FAIL)
        p = self.juego.pregunta_actual()
        self.juego.puntos = max(0, self.juego.puntos - PENALIZACION)
        texto = (f"Tiempo agotado. Correcta: "
                 f"{['A','B','C','D'][p['correcta']]}) {p['opciones'][p['correcta']]}\n\n"
                 f"{p['explicacion']}")
        self._label_msg.config(text=texto, fg=self.RED_FAIL)
        self._botones_opciones[p["correcta"]].config(bg=self.GREEN_OK)
        self._deshabilitar_opciones()
        self._popup_explicacion("Tiempo agotado", texto, False)
        self.after(3600, self._siguiente_pregunta)

    def _responder(self, idx):
        self._cancelar_timer()
        self._deshabilitar_opciones()
        p        = self.juego.pregunta_actual()
        correcta = p["correcta"]

        if idx == correcta:
            self._sonido("correcto")
            self._flash(self.GREEN_OK)
            self._botones_opciones[idx].config(bg=self.GREEN_OK)
            pts = PREMIOS[self.juego.nivel_actual()]
            self.juego.puntos += pts
            self._label_msg.config(
                text=f"✓ Correcto! +{pts:.1f} pts\n{p['explicacion']}",
                fg=self.GREEN_OK,
            )
            self.juego.pregunta_index += 1
            if self.juego.pregunta_index >= len(self.juego.preguntas_etapa):
                siguiente = self.juego.etapa_actual + 1
                self.after(2300, lambda: (
                    self._subir_etapa(siguiente) if siguiente <= 3
                    else self._pantalla_fin(True)
                ))
            else:
                self.after(2300, lambda: self._transicion(self._pantalla_juego, "Siguiente pregunta...", 900))
        else:
            self._sonido("incorrecto")
            self._flash(self.RED_FAIL)
            self._botones_opciones[idx].config(bg=self.RED_FAIL)
            self._botones_opciones[correcta].config(bg=self.GREEN_OK)
            self.juego.puntos = max(0, self.juego.puntos - PENALIZACION)
            texto = (f"Incorrecto. La respuesta era "
                     f"{['A','B','C','D'][correcta]}) {p['opciones'][correcta]}\n\n"
                     f"{p['explicacion']}")
            self._label_msg.config(text=texto, fg=self.RED_FAIL)
            self._popup_explicacion("Explicación", texto, False)
            self.after(3200, lambda: self._transicion(self._pantalla_fin_derrota, "Fin del juego...", 900))

    def _siguiente_pregunta(self):
        self.juego.pregunta_index += 1
        if self.juego.pregunta_index >= len(self.juego.preguntas_etapa):
            siguiente = self.juego.etapa_actual + 1
            if siguiente <= 3:
                self._subir_etapa(siguiente)
            else:
                self._pantalla_fin(True)
        else:
            self._transicion(self._pantalla_juego, "Siguiente pregunta...", 900)

    def _subir_etapa(self, nueva_etapa):
        self._limpiar()
        self._fondo_neon()
        self._sonido("cambio")
        txt = {2: "ETAPA 2 — INTERMEDIA", 3: "ETAPA 3 — AVANZADA"}.get(nueva_etapa, "")
        tk.Label(self, text="NUEVA ETAPA DESBLOQUEADA",
                 bg=self.BG_DARK, fg=self.GOLD, font=self.f_titulo).pack(pady=(175, 10))
        tk.Label(self, text="Superaste la etapa anterior",
                 bg=self.BG_DARK, fg=self.GREEN_OK, font=self.f_grande).pack(pady=(0, 10))
        tk.Label(self, text=f"Siguiente: {txt}",
                 bg=self.BG_DARK, fg=self.BLUE_NEON, font=self.f_grande).pack()
        self._btn(
            self, "Continuar →",
            lambda: [
                self.juego.cargar_etapa(nueva_etapa),
                self._transicion(self._pantalla_juego, "Cargando nueva etapa...", 900),
            ],
        ).pack(pady=30)

    # ── Comodines ──────────────────────────────────────────

    def _usar_5050(self):
        if not self.juego.comodines["5050"]:
            return
        for idx in self.juego.aplicar_5050():
            self._botones_opciones[idx].config(text="", state="disabled",
                                                bg=self.BG_DARK, cursor="arrow")
        self._btn_5050.config(bg="#333", cursor="arrow")

    def _usar_experto(self):
        if not self.juego.comodines["experto"]:
            return
        self._label_msg.config(
            text=f"💡 Fórmula: {self.juego.obtener_pista()}", fg=self.BLUE_NEON)
        self._btn_experto.config(bg="#333", cursor="arrow")

    def _usar_convergencia(self):
        if not self.juego.comodines["convergencia"]:
            return
        self.juego.comodines["convergencia"] = False
        self._btn_conv.config(bg="#333", cursor="arrow")

        p      = self.juego.pregunta_actual()
        letras = ["A", "B", "C", "D"]
        pesos  = [random.randint(8, 24) for _ in range(4)]
        pesos[p["correcta"]] += random.randint(35, 55)
        for idx in self.juego.respuestas_eliminadas:
            pesos[idx] = 0
        total      = sum(pesos) or 1
        porcentajes = [round(v * 100 / total, 1) for v in pesos]

        win = tk.Toplevel(self)
        win.title("Convergencia del Público")
        win.geometry("560x390")
        win.configure(bg=self.BG_DARK)
        tk.Label(win, text="~ Convergencia del Público ~",
                 bg=self.BG_DARK, fg=self.BLUE_NEON, font=self.f_grande).pack(pady=10)

        if MATPLOTLIB_OK:
            fig, ax = plt.subplots(figsize=(5, 2.7))
            ax.bar(letras, porcentajes, color=["#145DCC"] * 4)
            ax.set_ylim(0, 100)
            ax.set_ylabel("Probabilidad (%)")
            ax.set_title("Distribución de respuestas")
            fig.patch.set_facecolor("#101935")
            ax.set_facecolor("#101935")
            ax.tick_params(colors="white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")
            canvas = FigureCanvasTkAgg(fig, master=win)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=8)
        else:
            texto = "  ".join(f"{letras[i]}: {porcentajes[i]}%" for i in range(4))
            tk.Label(win, text=texto, bg=self.BG_DARK, fg=self.WHITE,
                     font=self.f_normal).pack(pady=40)
            tk.Label(win, text="Instala matplotlib para ver la gráfica.",
                     bg=self.BG_DARK, fg=self.GRAY, font=self.f_pequeno).pack()

        tk.Button(win, text="Cerrar", command=win.destroy,
                  bg=self.BLUE_MID, fg=self.WHITE, relief="flat",
                  cursor="hand2").pack(pady=10)

    # ── Pantallas de fin ───────────────────────────────────

    def _pantalla_fin(self, victoria=True):
        self._cancelar_timer()
        self._limpiar()
        self._fondo_neon()
        self._sonido("final" if victoria else "incorrecto")
        self._guardar_historial("victoria" if victoria else "derrota")

        msg   = "¡FELICIDADES!" if victoria else "FIN DEL JUEGO"
        color = self.GREEN_OK   if victoria else self.RED_FAIL
        tk.Label(self, text=msg, bg=self.BG_DARK, fg=color,
                 font=self.f_titulo).pack(pady=(120, 10))
        tk.Label(self, text=self.juego.nombre_jugador,
                 bg=self.BG_DARK, fg=self.WHITE, font=self.f_grande).pack()
        tk.Label(self, text=f"Puntuación final: {self.juego.puntos:.1f} pts",
                 bg=self.BG_DARK, fg=self.GOLD, font=self.f_titulo).pack(pady=15)

        frame = tk.Frame(self, bg=self.BG_DARK)
        frame.pack(pady=20)
        self._btn(frame, "Jugar de nuevo", self._pantalla_inicio, w=20).pack(side="left", padx=10)
        self._btn(frame, "📋  Historial",  self._mostrar_historial, color="#263238", w=16).pack(side="left", padx=10)
        self._btn(frame, "Salir",          self.destroy, color="#8B0000", w=12).pack(side="left", padx=10)

    def _pantalla_fin_derrota(self):
        self._pantalla_fin(False)


# ══════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = App()
    app.mainloop()
