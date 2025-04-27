# main.py

from core.processor import Processor
from core.memory import Memory

program = [
    # Main program
    "MOV R2 R1",         # R2 <- R1 (initialize R2 with R1)
    "CALL R7",           # Call subroutine at address stored in R7
    "SW R2 0(R3)",       # Store R2 into memory at address (R3 + 0)
    "LW R4 0(R3)",       # Load memory at (R3 + 0) into R4
    "JPC 3",             # Jump PC forward by 2 instructions
    "NOP",               # This NOP should be skipped by JPC
    "JPC 2",               # This NOP should be skipped by JPC
    "BRFL R8 0010000 0010000",  # Branch to [R8] if flags match (mask = 0010000)
    "RET",               # Return (program end)

    # Subroutine (R7 points here, address 8)
    "ADD R2 R1",         # R2 += R1 (increment inside subroutine)
    "RET",               # Return to caller
]

mem = Memory()  # Initialize 1K memory
mem.load_program(program)
proc = Processor(mem)

# Initialize registers
proc.registers[1] = 1   # R1 = 1
proc.registers[3] = 10  # R3 = base memory address
proc.registers[7] = 9   # R7 = address of the subroutine (line 9)
proc.registers[8] = 5   # R8 = target for BRFL if condition matches

# Simulate processor flags for BRFL
proc.flags['equal'] = 1  # Set 'equal' flag to true

# Run the program
proc.run()

# Print results
print("R2:", proc.registers[2])      # Expected: 2 (1 + 1)
print("R4:", proc.registers[4])      # Expected: 2 (loaded from memory)
print("MEM[10]:", mem.load(10))      # Expected: 2 (stored value)
print("PC final:", proc.PC)          # Where the program stopped
print("Stack:", proc.stack)          # Should be empty after RET
