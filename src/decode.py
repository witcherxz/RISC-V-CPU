from random import randrange

from myhdl import intbv, block, Signal, always, delay, concat, bin, always_comb
from tabulate import tabulate


@block
def mux32(a0, a1, a2, a3, a4, a5, s, z):
    @always_comb
    def mux():
        if s == 0:
            z.next = a0
        elif s == 1:
            z.next = a1
        elif s == 2:
            z.next = a2
        elif s == 3:
            z.next = a3
        elif s == 4:
            z.next = a4
        elif s == 5:
            z.next = a5
        elif s == 6:
            z.next = 0
        elif s == 7:
            z.next = 0
        else:
            z.next = 0

    return mux


@block
def slicer(instruction, opcode, rd, rs1, rs2, funct3, funct7, imm_I, imm_S, imm_B, imm_U, imm_J, imm_shift):
    """

    :param instruction:
    :param opcode:
    :param rd:
    :param rs1:
    :param rs2:
    :param funct3:
    :param funct7: 2-bit output bit 5 and bit 0 from the funct7 since these are the only bits needed for the control unit to select the type of operation in RV32IM.
    :param imm_I:
    :param imm_S:
    :param imm_B:
    :param imm_U:
    :param imm_J:
    :param imm_shift:
    :return:
    """

    @always(instruction)
    def decode():
        opcode.next = instruction[7:2]
        rs1.next = instruction[20:15]
        rs2.next = instruction[25:20]
        rd.next = instruction[12:7]
        funct3.next = instruction[15:12]
        # bit 5 and bit 0 from the funct7 since these are the only bits needed for the control unit to select the type
        # of operation in RV32IM.
        funct7.next = concat(instruction[31], instruction[25])
        imm_5bit = instruction[12:7]
        imm_7bit = instruction[32:25]
        imm_20bit = instruction[32:12]
        #  modified. They are runtime constants in verilog
        i = instruction[31] * ((2 ** 20) - 1)
        imm_I.next = concat(intbv(i)[20:], instruction[32:20]).signed()  # imm_I
        imm_S.next = concat(intbv(i)[20:], imm_7bit, imm_5bit).signed()  # imm_S
        b = instruction[31] * ((2 ** 19) - 1)
        imm_B.next = concat(intbv(b)[19:], imm_7bit[6], imm_5bit[0], imm_7bit[6:0], imm_5bit[5:1],
                            intbv(0)[1:]).signed()  # imm_B
        imm_U.next = intbv(imm_20bit << 12)[12:].signed()  # imm_U #TODO: MOD
        j = instruction[31] * ((2 ** 12) - 1)
        imm_J.next = concat(intbv(j)[11:], imm_20bit[19], imm_20bit[8:], imm_20bit[8], imm_20bit[19:9],
                            intbv(0)[1:]).signed()  # imm_J
        imm_shift.next = instruction[25:20]  # imm_shift

    return decode


@block
def decoder(instruction, sel, opcode, rd, rs1, rs2, funct3, funct7, imm):
    imm_I = Signal(intbv(0)[32:].signed())
    imm_S = Signal(intbv(0)[32:].signed())
    imm_B = Signal(intbv(0)[32:].signed())
    imm_U = Signal(intbv(0)[32:].signed())
    imm_J = Signal(intbv(0)[32:].signed())
    imm_shift = Signal(intbv(0)[32:].signed())
    imm_buffer = Signal(intbv(0)[32:].signed())
    slicer_1 = slicer(instruction, opcode, rd, rs1, rs2, funct3, funct7, imm_I, imm_S, imm_B, imm_U, imm_J, imm_shift)
    mux32_1 = mux32(imm_I, imm_S, imm_B, imm_U, imm_J, imm_shift, sel, imm_buffer)

    @always_comb
    def decode():
        imm.next = imm_buffer

    return decode, slicer_1, mux32_1


@block
def test_bench():
    rd, rs1, rs2 = [Signal(intbv(0)[5:]) for i in range(3)]
    # opcode, funct7 = [Signal(intbv(0)[8:]) for i in range(2)]
    opcode = Signal(intbv(0)[5:])
    funct7 = Signal(intbv(0)[2:])
    funct3 = Signal(intbv(0)[4:])
    imm_I = Signal(intbv(0)[32:])
    imm_S = Signal(intbv(0)[32:])
    imm_B = Signal(intbv(0)[32:])
    imm_U = Signal(intbv(0)[32:])
    imm_J = Signal(intbv(0)[32:])
    imm_shift = Signal(intbv(0)[32:])
    imm = Signal(intbv(0)[32:])
    inst = Signal(intbv(0)[32:])
    sel = Signal(intbv(0)[3:])
    isSigned = Signal(intbv(0)[1:])

    # mydecoder = decoder(inst, sel, isSigned, opcode, rd, rs1, rs2, funct3, funct7, imm)
    inst = Signal(intbv(0)[32:])
    decoder_1 = decoder(inst, sel, opcode, rd, rs1, rs2, funct3, funct7, imm)

    @always(delay(5))
    def decoder_tb():
        inst.next = randrange(2 ** 32 - 1)
        sel.next = randrange(2 ** 3 - 1)
        table = ["Instruction", "opcode", "rd", "rs1", "rs2", "funct3", "funct7", "imm_sel", "imm"], [bin(inst, 32),
                                                                                                      bin(opcode,
                                                                                                          5) + "11", rd,
                                                                                                      rs1, rs2, funct3,
                                                                                                      funct7, sel,
                                                                                                      bin(imm, 32)]

        print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

    return decoder_tb, decoder_1


# test_bench().run_sim(100)

def conv():
    rd, rs1, rs2 = [Signal(intbv(0)[5:]) for i in range(3)]
    opcode = Signal(intbv(0)[5:])
    funct7 = Signal(intbv(0)[2:])
    funct3 = Signal(intbv(0)[3:])
    imm_I = Signal(intbv(0)[32:])
    imm_S = Signal(intbv(0)[32:])
    imm_B = Signal(intbv(0)[32:])
    imm_U = Signal(intbv(0)[32:])
    imm_J = Signal(intbv(0)[32:])
    imm_shift = Signal(intbv(0)[32:])
    imm = Signal(intbv(0)[32:])
    inst = Signal(intbv(0)[32:])
    sel = Signal(intbv(0)[3:])
    isSigned = Signal(intbv(0)[1:])

    # mydecoder = decoder(inst, sel, isSigned, opcode, rd, rs1, rs2, funct3, funct7, imm)
    inst = Signal(intbv(0)[32:])
    decoder_1 = decoder(inst, sel, opcode, rd, rs1, rs2, funct3, funct7, imm)
    decoder_1.convert(hdl="verilog")


# conv()
