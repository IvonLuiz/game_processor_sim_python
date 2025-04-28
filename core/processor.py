# core/processor.py

class Processor:
    def __init__(self, memory):
        self.registers = [0] * 32  # R0-R31
        self.flags = {
            'overflow': 0,
            'above': 0,
            'equal': 0,
            'below': 0,
            'between': 0,
            'collision': 0,
            'error': 0
        }
        self.PC = 0
        self.memory = memory
        self.halted = False
        self.stack = []

    def reset(self):
        self.registers = [0] * 32
        self.PC = 0
        self.halted = False
        for key in self.flags:
            self.flags[key] = 0

    def step(self):
        instr = self.memory.get_instruction(self.PC)
        self.execute(instr)
        self.PC += 1

    def run(self, max_steps=1000):
        steps = 0
        while not self.halted and steps < max_steps:
            self.step()
            steps += 1
        if steps == max_steps:
            print("Warning: Max steps reached. Possible infinite loop.")


    def execute(self, instr):
        """
        Executes a single instruction.
        The instruction is a string in the format 'OPCODE ARG1, ARG2, ...'.
        RD, RS, and RB are register indices (0-31).
        """
        opcode, *args = instr.strip().split()
        print(f"PC: {self.PC}, Executing: {instr}")

        # Types of instructions
        match opcode:
            # Data transfer instructions
            case 'LW':
                rd = self._reg_index(args[0])
                offset, rb = self._parse_mem_ref(args[1])
                addr = self.registers[rb] + offset
                self.registers[rd] = self.memory.load(addr)

            case 'SW':
                rs = self._reg_index(args[0])
                offset, rb = self._parse_mem_ref(args[1])
                addr = self.registers[rb] + offset
                self.memory.store(addr, self.registers[rs])

            case 'MOV':
                rd, rs = map(self._reg_index, args)
                self.registers[rd] = self.registers[rs]

            # Arithmetic instructions
            case 'ADD':
                rd, rs = map(self._reg_index, args)
                self.registers[rd] += self.registers[rs]

            case 'SUB':
                rd, rs = map(self._reg_index, args)
                self.registers[rd] -= self.registers[rs]

            case 'MUL':
                rd, rs = map(self._reg_index, args)
                self.registers[rd] *= self.registers[rs]
            
            case 'DIV':
                rd, rs = map(self._reg_index, args)
                if self.registers[rs] == 0:
                    print("Division by zero error")
                    self.flags['error'] = 1
                    self.halted = True
                else:
                    self.registers[rd] //= self.registers[rs]

            # Logical instructions
            case 'AND':
                rd, rs = map(self._reg_index, args)
                self.registers[rd] &= self.registers[rs]

            case 'OR':
                rd, rs = map(self._reg_index, args)
                self.registers[rd] |= self.registers[rs]
            
            case 'SHL':
                rd, rs = map(self._reg_index, args)
                self.registers[rd] <<= self.registers[rs]

            case 'SHR':
                rd, rs = map(self._reg_index, args)
                self.registers[rd] >>= self.registers[rs]

            case 'CMP':
                rd, rs = map(self._reg_index, args)
                if self.registers[rd] == self.registers[rs]:
                    self.flags['equal'] = 1
                elif self.registers[rd] > self.registers[rs]:
                    self.flags['above'] = 1
                else:
                    self.flags['below'] = 1

            case 'NOT':
                rd, rs = map(self._reg_index, args)
                self.registers[rd] = ~self.registers[rs]

            # Transfer of Control
            case 'JR':
                offset = self._reg_index(args[0])
                self.PC = self.registers[offset] - 1 # -1 because the PC is incremented after fetch

            case 'JPC':
                offset = int(args[0])
                self.PC += offset - 1 # -1 because the PC is incremented after fetch

            case 'BRFL':
                r = self._reg_index(args[0])
                i7 = int(args[1], 2)  # Expected flags
                m7 = int(args[2], 2)  # Mask
                rflags_value = self._rflags_to_int()
                if (rflags_value & m7) == (i7 & m7):
                    self.PC = self.registers[r] - 1  # Jump to address in register r
                    return

            case 'CALL':
                r = self._reg_index(args[0])
                self.stack.append(self.PC)  # Save current position
                self.PC = self.registers[r] - 1

            case 'RET':
                if self.stack:
                    self.PC = self.stack.pop()
                else:
                    print("Stack underflow on RET")
                    self.halted = True

            case 'NOP':
                pass

            # Default case for unknown instructions
            case _:
                print(f"Unknown instruction: {opcode}")
                self.flags['error'] = 1
                self.halted = True

    def _reg_index(self, reg):
        return int(reg.replace('R', ''))

    def _parse_mem_ref(self, ref):
        # Formato: I16(RB)
        offset, rb = ref.replace(')', '').split('(')
        return int(offset), self._reg_index(rb)

    def _rflags_to_int(self):
        """Converte o dict de flags em um inteiro de 7 bits"""
        bits = [
            self.flags['overflow'],
            self.flags['above'],
            self.flags['equal'],
            self.flags['below'],
            self.flags['between'],
            self.flags['collision'],
            self.flags['error']
        ]
        value = 0
        for bit in bits:
            value = (value << 1) | bit
        return value