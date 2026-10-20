"""
CPU SIMULADA — implementação de 8 bits
AOC 2026.2

Registradores R0-R3, memória de 16 posições, PC e ciclo
Fetch -> Decode -> Execute.
"""

from ula import ula, limitar_8bits


class CPU:
    def __init__(self):
        self.registradores = {"R0": 0, "R1": 0, "R2": 0, "R3": 0}
        self.memoria = [0] * 16
        self.pc = 0
        self.halted = False

    def executar_instrucao(self, instrucao):
        partes = instrucao.replace(",", "").split()
        if not partes:
            raise ValueError("Instrução vazia")

        operacao = partes[0].upper()

        if operacao == "LOAD":
            if len(partes) != 3:
                raise ValueError("Sintaxe esperada: LOAD R0, valor")
            registrador = partes[1].upper()
            self._validar_registrador(registrador)
            valor = int(partes[2])
            self.registradores[registrador] = limitar_8bits(valor)
            self.pc += 1

        elif operacao == "STORE":
            if len(partes) != 3:
                raise ValueError("Sintaxe esperada: STORE R0, endereço")
            registrador = partes[1].upper()
            self._validar_registrador(registrador)
            endereco = int(partes[2])
            self._validar_endereco(endereco)
            self.memoria[endereco] = self.registradores[registrador]
            self.pc += 1

        elif operacao in ("ADD", "SUB", "AND", "OR", "XOR"):
            if len(partes) != 3:
                raise ValueError(f"Sintaxe esperada: {operacao} R0, R1")
            destino = partes[1].upper()
            origem = partes[2].upper()
            self._validar_registrador(destino)
            self._validar_registrador(origem)
            self.registradores[destino] = ula(
                operacao,
                self.registradores[destino],
                self.registradores[origem]
            )
            self.pc += 1

        elif operacao == "JMP":
            if len(partes) != 2:
                raise ValueError("Sintaxe esperada: JMP endereço")
            endereco = int(partes[1])
            self._validar_endereco(endereco)
            self.pc = endereco

        elif operacao == "HALT":
            self.halted = True

        else:
            raise ValueError(f"Instrução desconhecida: {operacao}")

    def _validar_registrador(self, registrador):
        if registrador not in self.registradores:
            raise ValueError(f"Registrador inválido: {registrador}")

    def _validar_endereco(self, endereco):
        if endereco < 0 or endereco >= len(self.memoria):
            raise ValueError(f"Endereço de memória inválido: {endereco}")

    def ciclo(self):
        if self.halted:
            return
        self._validar_endereco(self.pc)
        instrucao = self.memoria[self.pc]
        if not isinstance(instrucao, str):
            raise ValueError(
                f"Não há instrução válida na posição {self.pc} da memória."
            )

        print()
        print("--------------------------------")
        print("FETCH")
        print(f"PC: {self.pc:02d}")
        print("Instrução:", instrucao)
        print("DECODE + EXECUTE")
        print("Executando...")
        self.executar_instrucao(instrucao)
        self.mostrar_estado()
        print(f"Próximo PC: {self.pc:02d}")

    def executar(self, max_ciclos=100, passo_a_passo=False):
        """Executa até HALT. Com passo_a_passo=True, espera ENTER a cada ciclo."""
        ciclos = 0
        while not self.halted:
            if passo_a_passo:
                input("\n[ENTER] para executar o próximo ciclo...")
            if ciclos >= max_ciclos:
                raise RuntimeError(
                    "Número máximo de ciclos atingido. "
                    "Verifique se existe um loop infinito."
                )
            self.ciclo()
            ciclos += 1

    def carregar_programa(self, programa):
        """Grava uma lista de instruções na memória, a partir da posição 0."""
        if len(programa) > len(self.memoria):
            raise ValueError("Programa maior que a memória (16 posições)")
        for endereco, instrucao in enumerate(programa):
            self.memoria[endereco] = instrucao

    def mostrar_estado(self):
        print("Registradores:")
        for nome, valor in self.registradores.items():
            print(f"  {nome} = {valor:02X} ({valor})")
