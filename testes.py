import io
import unittest
from contextlib import redirect_stdout

from cpu import CPU
from ula import ula, limitar_8bits
import programas


def rodar(programa, **kw):
    """Cria uma CPU, carrega o programa e executa (silenciando a saída)."""
    cpu = CPU()
    cpu.carregar_programa(programa)
    with redirect_stdout(io.StringIO()):
        cpu.executar(**kw)
    return cpu


class TestULA(unittest.TestCase):
    def test_add(self):
        self.assertEqual(ula("ADD", 5, 8), 13)

    def test_sub(self):
        self.assertEqual(ula("SUB", 8, 5), 3)

    def test_and(self):
        self.assertEqual(ula("AND", 12, 10), 8)

    def test_or(self):
        self.assertEqual(ula("OR", 12, 10), 14)

    def test_xor(self):
        self.assertEqual(ula("XOR", 12, 10), 6)

    def test_operacao_invalida(self):
        with self.assertRaises(ValueError):
            ula("MUL", 1, 2)


class TestOitoBits(unittest.TestCase):
    def test_limitar(self):
        self.assertEqual(limitar_8bits(256), 0)
        self.assertEqual(limitar_8bits(-1), 255)

    def test_ula_overflow_add(self):
        self.assertEqual(ula("ADD", 250, 10), 4)

    def test_ula_underflow_sub(self):
        self.assertEqual(ula("SUB", 5, 8), 253)

    def test_load_acima_de_255(self):
        cpu = rodar(["LOAD R0, 300", "HALT"])
        self.assertEqual(cpu.registradores["R0"], 44)

    def test_overflow_na_cpu(self):
        cpu = rodar(programas.OVERFLOW)
        self.assertEqual(cpu.registradores["R0"], 4)
        self.assertEqual(cpu.registradores["R2"], 253)

    def test_store_respeita_8_bits(self):
        cpu = rodar(["LOAD R0, 257", "STORE R0, 15", "HALT"])
        self.assertEqual(cpu.memoria[15], 1)


class TestRegistradoresEMemoria(unittest.TestCase):
    def test_estado_inicial(self):
        cpu = CPU()
        self.assertEqual(list(cpu.registradores), ["R0", "R1", "R2", "R3"])
        self.assertTrue(all(v == 0 for v in cpu.registradores.values()))
        self.assertEqual(len(cpu.memoria), 16)
        self.assertEqual(cpu.pc, 0)

    def test_registrador_invalido(self):
        with self.assertRaises(ValueError):
            rodar(["LOAD R9, 1", "HALT"])

    def test_endereco_invalido(self):
        with self.assertRaises(ValueError):
            rodar(["LOAD R0, 1", "STORE R0, 16", "HALT"])


class TestInstrucoes(unittest.TestCase):
    def test_load(self):
        cpu = rodar(["LOAD R0, 25", "HALT"])
        self.assertEqual(cpu.registradores["R0"], 25)

    def test_load_todos_registradores(self):
        cpu = rodar(["LOAD R0, 1", "LOAD R1, 2", "LOAD R2, 3", "LOAD R3, 4", "HALT"])
        self.assertEqual(list(cpu.registradores.values()), [1, 2, 3, 4])

    def test_store(self):
        cpu = rodar(["LOAD R0, 42", "STORE R0, 15", "HALT"])
        self.assertEqual(cpu.memoria[15], 42)

    def test_add(self):
        cpu = rodar(["LOAD R0, 5", "LOAD R1, 8", "ADD R0, R1", "HALT"])
        self.assertEqual(cpu.registradores["R0"], 13)
        self.assertEqual(cpu.registradores["R1"], 8)  # origem não muda

    def test_sub(self):
        cpu = rodar(["LOAD R0, 9", "LOAD R1, 4", "SUB R0, R1", "HALT"])
        self.assertEqual(cpu.registradores["R0"], 5)

    def test_sub_negativo_vira_8bits(self):
        cpu = rodar(["LOAD R0, 5", "LOAD R1, 8", "SUB R0, R1", "HALT"])
        self.assertEqual(cpu.registradores["R0"], 253)

    def test_and(self):
        cpu = rodar(["LOAD R0, 12", "LOAD R1, 10", "AND R0, R1", "HALT"])
        self.assertEqual(cpu.registradores["R0"], 8)

    def test_or(self):
        cpu = rodar(["LOAD R0, 12", "LOAD R1, 10", "OR R0, R1", "HALT"])
        self.assertEqual(cpu.registradores["R0"], 14)

    def test_xor(self):
        cpu = rodar(["LOAD R0, 12", "LOAD R1, 10", "XOR R0, R1", "HALT"])
        self.assertEqual(cpu.registradores["R0"], 6)

    def test_instrucao_desconhecida(self):
        with self.assertRaises(ValueError):
            rodar(["NOP", "HALT"])


class TestPC(unittest.TestCase):
    def test_pc_avanca_um_a_um(self):
        cpu = CPU()
        cpu.carregar_programa(["LOAD R0, 1", "LOAD R1, 2", "ADD R0, R1", "HALT"])
        with redirect_stdout(io.StringIO()):
            for esperado in (1, 2, 3):
                cpu.ciclo()
                self.assertEqual(cpu.pc, esperado)

    def test_jmp_altera_pc(self):
        cpu = CPU()
        cpu.carregar_programa(programas.COM_JMP)
        with redirect_stdout(io.StringIO()):
            cpu.ciclo()                 # LOAD R0, 10
            self.assertEqual(cpu.pc, 1)
            cpu.ciclo()                 # JMP 4
            self.assertEqual(cpu.pc, 4)

    def test_jmp_pula_instrucoes(self):
        cpu = rodar(programas.COM_JMP)
        self.assertEqual(cpu.registradores["R0"], 10)  # LOAD R0, 99 foi pulado
        self.assertEqual(cpu.registradores["R1"], 20)

    def test_jmp_endereco_invalido(self):
        with self.assertRaises(ValueError):
            rodar(["JMP 16"])

    def test_loop_infinito_detectado(self):
        with self.assertRaises(RuntimeError):
            rodar(["JMP 0"], max_ciclos=10)


class TestHalt(unittest.TestCase):
    def test_halt_para_execucao(self):
        cpu = rodar(["HALT", "LOAD R0, 99"])
        self.assertTrue(cpu.halted)
        self.assertEqual(cpu.registradores["R0"], 0)  # nada após HALT executou

    def test_halt_nao_avanca_instrucoes_seguintes(self):
        cpu = rodar(["LOAD R0, 1", "HALT", "LOAD R0, 2"])
        self.assertEqual(cpu.registradores["R0"], 1)

    def test_ciclo_apos_halt_nao_faz_nada(self):
        cpu = rodar(["HALT"])
        pc = cpu.pc
        with redirect_stdout(io.StringIO()):
            cpu.ciclo()
        self.assertEqual(cpu.pc, pc)


class TestProgramas(unittest.TestCase):
    def test_programa_exemplo(self):
        cpu = rodar(programas.EXEMPLO)
        self.assertEqual(cpu.memoria[15], 13)

    def test_programa_proprio(self):
        cpu = rodar(programas.PROPRIO)
        self.assertEqual(cpu.registradores["R0"], 13)
        self.assertEqual(cpu.registradores["R2"], 1)
        self.assertEqual(cpu.memoria[15], 13)
        self.assertEqual(cpu.memoria[14], 1)

    def test_programa_proprio_tem_8_ou_mais_instrucoes(self):
        self.assertGreaterEqual(len(programas.PROPRIO), 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
