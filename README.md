# CPU Simulada — 8 bits

Trabalho prático de Arquitetura de Computadores (UFC Sobral, 2026.2).
Autor(es): André Parente Portela - 579060
Francisco Jônathan Lima Paula - 581253

Modelo executável de uma CPU didática em Python, que permite observar o
ciclo **Fetch → Decode → Execute** passo a passo.

## Arquitetura

```
        Memória (16 x 8 bits)                CPU
      +-----------------+        +----------------------------+
      | [00] LOAD R0, 5 |        |     Unidade de Controle    |
      | [01] LOAD R1, 8 | <----> |   (cpu.py: ciclo/decode)   |
      | [02] ADD R0, R1 | end.   |        |            |      |
      | ...             | dados  |  Registradores    ULA      |
      | [15] 00         |        |  R0 R1 R2 R3   ADD SUB AND |
      +-----------------+        |  PC            OR  XOR     |
                                 +----------------------------+
```

| Componente | Especificação | Onde está |
|---|---|---|
| Dados | 8 bits (0–255), via máscara `& 0xFF` | `ula.py` (`limitar_8bits`) |
| Registradores | R0, R1, R2, R3 | `cpu.py` (`self.registradores`) |
| Contador de programa | PC | `cpu.py` (`self.pc`) |
| Memória | 16 posições (0–15), instruções e dados no mesmo espaço | `cpu.py` (`self.memoria`) |
| ULA | ADD, SUB, AND, OR, XOR | `ula.py` (`ula`) |
| Execução | Fetch → Decode → Execute | `cpu.py` (`ciclo`, `executar_instrucao`) |

### Representação na memória
Cada posição guarda **uma instrução como texto** (ex.: `"ADD R0, R1"`) ou
**um valor inteiro** (ex.: resultado de um `STORE`). Posições não usadas
contêm `0`.

### Ciclo de instrução
1. **FETCH**: lê `memoria[PC]`.
2. **DECODE**: separa o mnemônico e os operandos (`partes = instrucao.replace(",", "").split()`).
3. **EXECUTE**: executa a operação (usando a ULA quando aplicável) e atualiza
   registradores, memória ou PC. O PC avança em 1, exceto em `JMP` (recebe o
   endereço) e `HALT` (para a CPU).

## Conjunto de instruções

| Instrução | Exemplo | Função |
|---|---|---|
| LOAD | `LOAD R0, 5` | R0 ← 5 |
| STORE | `STORE R0, 15` | MEM[15] ← R0 |
| ADD | `ADD R0, R1` | R0 ← R0 + R1 |
| SUB | `SUB R0, R1` | R0 ← R0 − R1 |
| AND | `AND R0, R1` | R0 ← R0 AND R1 |
| OR | `OR R0, R1` | R0 ← R0 OR R1 |
| XOR | `XOR R0, R1` | R0 ← R0 XOR R1 |
| JMP | `JMP 8` | PC ← 8 |
| HALT | `HALT` | encerra a execução |

### Comportamento de 8 bits
Todos os resultados são limitados a 0–255. Exemplos: `250 + 10 = 4`,
`5 − 8 = 253` (complemento de dois sem sinal), `LOAD R0, 300` grava 44.

### Erros tratados
Registrador inválido, endereço fora de 0–15, instrução desconhecida,
sintaxe incorreta, posição sem instrução e loop infinito (limite de 100
ciclos, configurável em `executar(max_ciclos=...)`).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `cpu.py` | Classe `CPU` (registradores, memória, PC, ciclo) |
| `ula.py` | Operações da ULA e `limitar_8bits` |
| `programas.py` | Programas usados nos testes e na demonstração |
| `testes.py` | Testes automáticos (`unittest`) |
| `main.py` | Execução e visualização passo a passo |

## Como executar

Requer Python 3 (sem dependências externas).

```bash
python main.py              # programa próprio, execução contínua
python main.py --passo      # modo passo a passo (ENTER a cada ciclo)
python main.py --exemplo    # programa do enunciado (5 + 8 -> MEM[15] = 13)
python testes.py            # roda todos os testes
```

Saída de cada ciclo (exemplo):

```
--------------------------------
FETCH
PC: 02
Instrução: ADD R0, R1
DECODE + EXECUTE
Executando...
Registradores:
  R0 = 0D (13)
  R1 = 08 (8)
  R2 = 00 (0)
  R3 = 00 (0)
Próximo PC: 03
```

## Programa próprio (`programas.PROPRIO`)

```
[00] LOAD R0, 5      R0 = 5
[01] LOAD R1, 8      R1 = 8
[02] ADD R0, R1      R0 = 13
[03] LOAD R2, 3      R2 = 3
[04] LOAD R3, 1      R3 = 1
[05] XOR R2, R3      R2 = 3 ^ 1 = 2
[06] SUB R2, R3      R2 = 2 - 1 = 1
[07] STORE R0, 15    MEM[15] = 13
[08] STORE R2, 14    MEM[14] = 1
[09] HALT
```

Usa LOAD, STORE e três operações da ULA (ADD, XOR, SUB).
Resultado esperado: `R0 = 13`, `R2 = 1`, `MEM[15] = 13`, `MEM[14] = 1`.

## Testes

36 testes em `testes.py`, cobrindo todos os itens obrigatórios do enunciado:
LOAD, STORE, ADD, SUB, AND, OR, XOR, avanço do PC, JMP (valor do PC e
desvio), HALT, programa de exemplo e limite de 8 bits (na ULA e na CPU),
além de casos de erro.
