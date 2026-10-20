import sys
from cpu import CPU
import programas

passo = "--passo" in sys.argv
programa = programas.EXEMPLO if "--exemplo" in sys.argv else programas.PROPRIO

cpu = CPU()
cpu.carregar_programa(programa)

print("======================================")
print("       CPU SIMULADA — 8 BITS")
print("======================================")
print("Programa carregado na memória:")
for i, instr in enumerate(programa):
    print(f"  [{i:02d}] {instr}")

cpu.executar(passo_a_passo=passo)

print()
print("======================================")
print("RESULTADO FINAL")
print("======================================")
cpu.mostrar_estado()
print(f"PC final: {cpu.pc:02d}")
print("Memória de dados:")
for i in range(len(programa), 16):
    print(f"  MEM[{i:02d}] = {cpu.memoria[i]}")
