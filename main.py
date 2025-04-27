# main.py

from core.processor import Processor
from core.memory import Memory

program = [
    "MOV R2 R1",        # R2 <- 1
    "ADD R2 R1",        # R2 += 1
    "SW R2 0(R3)",      # MEM[R3 + 0] <- R2
    "LW R4 0(R3)",      # R4 <- MEM[R3 + 0]
    #"JPC -2",           # Loop
    "RET"
]

mem = Memory()  # 1K memory
mem.load_program(program)
proc = Processor(mem)

proc.registers[1] = 1  # R1 = 1
proc.registers[3] = 10  # R3 = endereço base

proc.run()

print("R2:", proc.registers[2])
print("R4:", proc.registers[4])
print("MEM[10]:", mem.load(10))
