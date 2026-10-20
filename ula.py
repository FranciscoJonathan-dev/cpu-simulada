"""
ULA — Unidade Lógica e Aritmética da CPU simulada de 8 bits.
AOC 2026.2
"""

def limitar_8bits(valor):
    """Mantém somente os 8 bits menos significativos (0 a 255)."""
    return valor & 0xFF


def ula(operacao, a, b=0):
    """Executa uma operação aritmética ou lógica de 8 bits."""
    a = limitar_8bits(a)
    b = limitar_8bits(b)

    if operacao == "ADD":
        resultado = a + b
    elif operacao == "SUB":
        resultado = a - b
    elif operacao == "AND":
        resultado = a & b
    elif operacao == "OR":
        resultado = a | b
    elif operacao == "XOR":
        resultado = a ^ b
    else:
        raise ValueError(f"Operação inválida: {operacao}")

    return limitar_8bits(resultado)
