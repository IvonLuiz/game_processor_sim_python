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

    def run(self):
        while not self.halted:
            self.step()

    def execute(self, instr):
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

            case 'NOP':
                pass

            # Transfer of Control
            case 'JPC':
                offset = int(args[0])
                self.PC += offset - 1  # -1 porque o PC já foi incrementado após o fetch

            case 'RET':
                self.halted = True

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
