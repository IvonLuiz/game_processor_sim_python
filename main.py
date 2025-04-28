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
    "JPC 2",
    "BRFL R8 0010000 0010000",  # Branch to [R8] if flags match (mask = 0010000)
    "RET",               # Return (program end)

    # Subroutine (R7 points here, address 9)
    "ADD R2 R1",         # R2 += R1 (increment inside subroutine)
    "SUB R5 R2",         # R2 -= R1
    "MUL R5 R2",         # R2 *= R1
    "DIV R6 R1",         # R2 /= R1

    "AND R9 R1",        # R6 &= R1
    "OR R10 R1",         # R6 |= R1
    "SHL R11 R1",        # R6 <<= R1
    "SHR R12 R1",        # R6 >>= R1
    "CMP R13 R2",         # Compare R1 and R2
    "CMP R13 R5",         # Compare R2 and R1

    "JR R20",           # Jump to address in R7 (back to main program)

    "NOP",               # No operation (NOP)
    "NOP",               # No operation (NOP)
    "NOP",               # No operation (NOP)

    'RET'
]

mem = Memory()  # Initialize 1K memory
mem.load_program(program)
proc = Processor(mem)

# Initialize registers
proc.registers[1] = 1   # R1 = 1
proc.registers[3] = 10  # R3 = base memory address
proc.registers[7] = 9   # R7 = address of the subroutine (line 9)
proc.registers[8] = 5   # R8 = target for BRFL if condition matches
proc.registers[9] = 11 
proc.registers[10] = 11
proc.registers[11] = 11
proc.registers[12] = 11
proc.registers[13] = 1
proc.registers[19] = 19
proc.registers[20] = 23

# Simulate processor flags for BRFL
#proc.flags['equal'] = 1  # Set 'equal' flag to true

# Run the program
proc.run()

# Print results
for i in range(len(proc.registers)):
    print(f"R{i}:", proc.registers[i])  # Print all registers
print("MEM[10]:", mem.load(10))      # Expected: 2 (stored value)
print("PC final:", proc.PC)          # Where the program stopped
print("Stack:", proc.stack)          # Should be empty after RET
print("Flags:", proc.flags)          # Check flags after execution
