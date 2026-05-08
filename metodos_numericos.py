"""Motor matematico para Metodos Millonarios.
Funciones reutilizables para generar y validar mini-retos dinamicos.
"""
from __future__ import annotations

import math
from typing import Callable, Iterable, List, Sequence, Tuple

Number = float


def biseccion(f: Callable[[Number], Number], a: Number, b: Number, tol: Number = 1e-6, max_iter: int = 100) -> Tuple[Number, int]:
    fa, fb = f(a), f(b)
    if fa == 0:
        return a, 0
    if fb == 0:
        return b, 0
    if fa * fb > 0:
        raise ValueError("El intervalo no encierra una raiz: f(a) y f(b) tienen el mismo signo.")
    c = a
    for k in range(1, max_iter + 1):
        c = (a + b) / 2
        fc = f(c)
        if abs(fc) < tol or abs(b - a) / 2 < tol:
            return c, k
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return c, max_iter


def newton_raphson(f: Callable[[Number], Number], df: Callable[[Number], Number], x0: Number, tol: Number = 1e-6, max_iter: int = 50) -> Tuple[Number, int]:
    x = x0
    for k in range(1, max_iter + 1):
        dfx = df(x)
        if abs(dfx) < 1e-14:
            raise ZeroDivisionError("La derivada es demasiado cercana a cero.")
        x_new = x - f(x) / dfx
        if abs(x_new - x) < tol:
            return x_new, k
        x = x_new
    return x, max_iter


def jacobi(A: Sequence[Sequence[Number]], b: Sequence[Number], x0: Sequence[Number] | None = None, tol: Number = 1e-6, max_iter: int = 100) -> Tuple[List[Number], int]:
    n = len(A)
    x = list(x0) if x0 is not None else [0.0] * n
    for k in range(1, max_iter + 1):
        x_new = x[:]
        for i in range(n):
            if abs(A[i][i]) < 1e-14:
                raise ZeroDivisionError("Cero en la diagonal principal.")
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        if max(abs(x_new[i] - x[i]) for i in range(n)) < tol:
            return x_new, k
        x = x_new
    return x, max_iter


def gauss_seidel(A: Sequence[Sequence[Number]], b: Sequence[Number], x0: Sequence[Number] | None = None, tol: Number = 1e-6, max_iter: int = 100) -> Tuple[List[Number], int]:
    n = len(A)
    x = list(x0) if x0 is not None else [0.0] * n
    for k in range(1, max_iter + 1):
        anterior = x[:]
        for i in range(n):
            if abs(A[i][i]) < 1e-14:
                raise ZeroDivisionError("Cero en la diagonal principal.")
            s1 = sum(A[i][j] * x[j] for j in range(i))
            s2 = sum(A[i][j] * anterior[j] for j in range(i + 1, n))
            x[i] = (b[i] - s1 - s2) / A[i][i]
        if max(abs(x[i] - anterior[i]) for i in range(n)) < tol:
            return x, k
    return x, max_iter


def lagrange_interpolar(puntos: Sequence[Tuple[Number, Number]], x_eval: Number) -> Number:
    total = 0.0
    for i, (xi, yi) in enumerate(puntos):
        Li = 1.0
        for j, (xj, _yj) in enumerate(puntos):
            if i != j:
                Li *= (x_eval - xj) / (xi - xj)
        total += yi * Li
    return total


def trapecio(f: Callable[[Number], Number], a: Number, b: Number, n: int) -> Number:
    if n <= 0:
        raise ValueError("n debe ser positivo.")
    h = (b - a) / n
    return h * (0.5 * f(a) + sum(f(a + i * h) for i in range(1, n)) + 0.5 * f(b))


def simpson_13(f: Callable[[Number], Number], a: Number, b: Number, n: int) -> Number:
    if n <= 0 or n % 2 != 0:
        raise ValueError("Simpson 1/3 requiere n positivo y par.")
    h = (b - a) / n
    s = f(a) + f(b)
    s += 4 * sum(f(a + i * h) for i in range(1, n, 2))
    s += 2 * sum(f(a + i * h) for i in range(2, n, 2))
    return h * s / 3


def runge_kutta4(f: Callable[[Number, Number], Number], y0: Number, t0: Number, tf: Number, h: Number) -> Tuple[List[Number], List[Number]]:
    if h <= 0:
        raise ValueError("h debe ser positivo.")
    t_values = [t0]
    y_values = [y0]
    t, y = t0, y0
    while t < tf - 1e-12:
        paso = min(h, tf - t)
        k1 = f(t, y)
        k2 = f(t + paso / 2, y + paso * k1 / 2)
        k3 = f(t + paso / 2, y + paso * k2 / 2)
        k4 = f(t + paso, y + paso * k3)
        y += paso * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t += paso
        t_values.append(t)
        y_values.append(y)
    return t_values, y_values
