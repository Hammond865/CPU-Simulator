# from https://www.geeksforgeeks.org/extract-k-bits-given-position-number/
# collect k bits, starting p-1 digits from the right
def extract_bits(number, k, p):
    return ((1 << k) - 1) & (number >> (p - 1))


def build_instruction(opcode, Rd, Rs1, Rs2, immed):
    instr = opcode << 28
    if Rd is not None:
        instr = instr + (Rd << 24)
    if Rs1 is not None:
        instr = instr + (Rs1 << 20)
    if Rs2 is not None:
        instr = instr + (Rs2 << 16)
    if immed is not None:
        instr = instr + immed
    return instr


class CPU:
    MEM_SIZE = 65536
    NUM_REGISTERS = 16
    pc = -1
    next_pc = -1
    memory = [MEM_SIZE]
    regs = [NUM_REGISTERS]

    def __init__(self):
        self.memory = [0] * self.MEM_SIZE
        self.regs = [0] * self.NUM_REGISTERS
        return

    def fetch_instruction(self, pc):
        self.pc = pc
        self.next_pc = pc + 1
        return self.memory[pc]

    def decode_instruction(self, instr):
        # extract_bits indexes right to left, starting with 0
        # grab bits from positions 28-31
        opcode = extract_bits(instr, 4, 29)
        # grab bits from positions 24-27
        Rd = extract_bits(instr, 4, 25)
        # grab bits from positions 20-23
        Rs1 = extract_bits(instr, 4, 21)
        # grab bits from positions 16-19
        Rs2 = extract_bits(instr, 4, 17)
        # grab bits from positions 0-15
        immed = extract_bits(instr, 16, 1)
        self.execute(opcode, Rd, Rs1, Rs2, immed)
        return

    def execute(self, opcode, Rd, Rs1, Rs2, immed):

        #ADD
        if opcode == 1:
            alu_result = self.regs[Rs1] + self.regs[Rs2]
            if Rd != 0:
                self.regs[Rd] = alu_result

        #ADDI
        if opcode == 2:
            alu_result = self.regs[Rs1] + immed
            if Rd != 0:
                self.regs[Rd] = alu_result

        #BEQ
        if opcode == 3:
            if self.regs[Rs1] == self.regs[Rs2]:
                self.next_pc = self.pc + immed

        #JAL
        if opcode == 4:
            alu_result = self.pc + 1
            if Rd != 0:
                self.regs[Rd] = alu_result
            self.next_pc = self.pc + immed

        #LW
        if opcode == 5:
            eff_address = self.regs[Rs1] + immed
            if Rd != 0:
                self.regs[Rd] = self.memory[eff_address]

        #SW
        if opcode == 6:
            eff_address = self.regs[Rs2] + immed
            if Rd != 0:
                self.regs[Rd] = self.memory[eff_address]



        return


# 1011000

"""
#11000
print(extract_bits(88, 5, 1))
# 0
print(extract_bits(88, 2, 2))
# 100
print(extract_bits(88, 3, 2))
# 10
print(extract_bits(88, 2, 3))
# 110
print(extract_bits(88, 3, 3))
# 1100
print(extract_bits(88, 4, 2))
"""

NOOP = 0
ADD = 1
ADDI = 2
BEQ = 3
JAL = 4
LW = 5
SW = 6
RETURN = 7

R0 = 0
R1 = 1
R2 = 2
R3 = 3
R4 = 4
R5 = 5
R6 = 6
R7 = 7
R8 = 8
R9 = 9
R10 = 10
R11 = 11
R12 = 12
R13 = 13
R14 = 14
R15 = 15
R16 = 16

i0 = build_instruction(NOOP, None, None, None, None)
i1 = build_instruction(ADDI, R1, R0, None, 8)
i2 = build_instruction(ADDI, R2, R0, None, 7)
i3 = build_instruction(ADD, R3, R1, R1, None)
i4 = build_instruction(ADD, R4, R2, R2, None)
i5 = build_instruction(BEQ, None, R3, R4, 3)
i6 = build_instruction(ADDI, R8, R0, None, 10)
i7 = build_instruction(JAL, R0, None, None, 2)
i8 = build_instruction(ADDI, R8, R0, None, 1000)
i9 = build_instruction(SW, None, None, R2, 16)
i10 = build_instruction(LW, None, R5, None, 16)
#i11 = build_instruction(JAL, R9, None, None, 4)


#print(i5)

cpu = CPU()
#cpu.decode_instruction(i11)
cpu.memory[100] = i0
cpu.memory[101] = i1
cpu.memory[102] = i2
cpu.memory[103] = i3
cpu.memory[104] = i4
cpu.memory[105] = i5
cpu.memory[106] = i6
cpu.memory[107] = i7
cpu.memory[108] = i8
cpu.memory[109] = i9
cpu.memory[110] = i10

cpu.pc = 100
#print(i7)
while cpu.next_pc <= 110:
    instr = cpu.fetch_instruction(cpu.pc)
    cpu.next_pc = cpu.pc + 1
    cpu.decode_instruction(instr)
    cpu.pc = cpu.next_pc

# for testing:
for reg in cpu.regs:
        print(reg)
