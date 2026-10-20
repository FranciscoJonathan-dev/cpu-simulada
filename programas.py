"""
Programas utilizados nos testes e na demonstração.
Cada programa é uma lista de instruções; a posição na lista é o endereço.
"""

# Programa de exemplo do enunciado: 5 + 8, resultado em MEM[15] = 13.
EXEMPLO = [
    "LOAD R0, 5",
    "LOAD R1, 8",
    "ADD R0, R1",
    "STORE R0, 15",
    "HALT",
]

# Programa próprio (9 instruções): usa LOAD, STORE, ADD, XOR e SUB.
#   R0 = 5 + 8 = 13            -> MEM[15] = 13
#   R2 = (3 XOR 1) - 1 = 1     -> MEM[14] = 1
PROPRIO = [
    "LOAD R0, 5",
    "LOAD R1, 8",
    "ADD R0, R1",
    "LOAD R2, 3",
    "LOAD R3, 1",
    "XOR R2, R3",
    "SUB R2, R3",
    "STORE R0, 15",
    "STORE R2, 14",
    "HALT",
]

# Demonstra JMP: a instrução da posição 2 é pulada.
COM_JMP = [
    "LOAD R0, 10",
    "JMP 4",
    "LOAD R0, 99",
    "HALT",
    "LOAD R1, 20",
    "HALT",
]

# Demonstra a limitação de 8 bits (overflow e underflow).
OVERFLOW = [
    "LOAD R0, 250",
    "LOAD R1, 10",
    "ADD R0, R1",     # 260 -> 4
    "LOAD R2, 5",
    "LOAD R3, 8",
    "SUB R2, R3",     # -3 -> 253
    "HALT",
]
