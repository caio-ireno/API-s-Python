def fatorial(n):
    if n < 0:
        raise ValueError("Fatorial não é definido para números negativos")
    if n == 0 or n == 1:
        return 1
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado
