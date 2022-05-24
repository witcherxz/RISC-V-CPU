from random import randrange

from myhdl import intbv, block, Signal, always_comb, always, delay, bin, concat
from tabulate import tabulate


# TODO: ADD Load Control
@block
def control(opcode, funct3, funct7, decode_imm_type, RegWE, MEMWE, ALUSel, ALUSrc1, ALUSrc2, BranchAddSrc, RegWriteSrc,
            Branch, MEMRE, callOS):
    """
    Control Unit

    :param opcode: 5-bit input taken from the 5 msb from the opcode since the two least significant bit in the opcode is the same in all instruction types and will not help the control distinguish between the instruction types.
    :param funct3: 3-bit input to help the control distinguish between the instruction from the same type.
    :param funct7: 2-bit input bit-5 and bit-0 from the funct7 since these two bit are the only bits needed to help the control unit distinguish between the instruction from the same type in RV32IM.
    :param decode_imm_type: the selector for the 32mux to select the correct immediate for the instruction.
    :param RegWE: Register Write Enable.
    :param MEMWE: Memory Write Enable.
    :param ALUSel: ALU Selector.
    :param ALUSrc1: ALU Source 1 when it's to 0 the input to the first input to the ALU is the value of the rs1 register and when it's 1 the input is the PC.
    :param ALUSrc2: ALU Source 2 when it's to 0 the input to the first input to the ALU is the value of the rs2 register and when it's 1 the input is the immediate.
    :param BranchAddSrc: Branch Adder Source when it's 0 the PC = PC + imm (jal) and when it's 1 PC = rs1 + imm (jalr)
    :param RegWriteSrc: Register Write Source when 0 the data input to the register file will be the output of the ALU and when it's 1 will be the output of the memory.
    :param Branch: determin if the instruction is branch instruction.
    :param MEMRE: read enable to only read when the instruction need that.
    :param callOS: to move control to the OS if the instruction is ecall
    """

    @always_comb
    def controler():
        # R-Type
        if opcode == 0b01100:
            RegWE.next = 1
            MEMWE.next = 0
            ALUSrc1.next = 0
            ALUSrc2.next = 0
            BranchAddSrc.next = 0
            RegWriteSrc.next = 0
            Branch.next = 0
            decode_imm_type.next = 0
            callOS.next = 0
            MEMRE.next = 0
            if funct7 == 0:
                if funct3 == 0:
                    ALUSel.next = 0  # ADD
                elif funct3 == 1:
                    ALUSel.next = 2  # XOR
                elif funct3 == 2:
                    ALUSel.next = 3  # OR
                elif funct3 == 3:
                    ALUSel.next = 4  # AND
                elif funct3 == 4:
                    ALUSel.next = 5  # sll
                elif funct3 == 5:
                    ALUSel.next = 6  # srl
                elif funct3 == 6:
                    ALUSel.next = 7  # slt
                else:
                    ALUSel.next = 8  # sltu
            elif funct7 == 1:
                if funct3 == 0:
                    ALUSel.next = 9  # mul
                elif funct3 == 1:
                    ALUSel.next = 10  # mulh
                elif funct3 == 2:
                    ALUSel.next = 11  # mulhsu
                elif funct3 == 3:
                    ALUSel.next = 12  # mulhu
                elif funct3 == 4:
                    ALUSel.next = 13  # div
                elif funct3 == 5:
                    ALUSel.next = 14  # divu
                elif funct3 == 6:
                    ALUSel.next = 15  # rem
                else:
                    ALUSel.next = 16  # remu
            else:
                if funct3 == 0:
                    ALUSel.next = 1  # SUB
                else:
                    ALUSel.next = 25  # sra


        # I-Type
        elif opcode == 0b00100:
            RegWE.next = 1
            MEMWE.next = 0
            ALUSrc1.next = 0
            ALUSrc2.next = 1
            BranchAddSrc.next = 0
            RegWriteSrc.next = 0
            Branch.next = 0
            callOS.next = 0
            MEMRE.next = 0
            if funct3 == 1 or funct3 == 5:
                decode_imm_type.next = 5
            else:
                decode_imm_type.next = 0

            if funct3 == 0:
                ALUSel.next = 0  # ADD
            elif funct3 == 1:
                ALUSel.next = 2  # XOR
            elif funct3 == 2:
                ALUSel.next = 3  # OR
            elif funct3 == 3:
                ALUSel.next = 4  # AND
            elif funct3 == 4:
                ALUSel.next = 5  # sll
            elif funct3 == 5:
                if funct7 == 0:
                    ALUSel.next = 6  # srl
                else:
                    ALUSel.next = 25  # sra
            elif funct3 == 6:
                ALUSel.next = 7  # slt
            else:
                ALUSel.next = 8  # sltu

        # Load
        elif opcode == 0b00000:
            RegWE.next = 1
            MEMWE.next = 0
            ALUSrc1.next = 0
            ALUSrc2.next = 1
            BranchAddSrc.next = 0
            RegWriteSrc.next = 1
            Branch.next = 0
            decode_imm_type.next = 0
            ALUSel.next = 0  # ADD
            callOS.next = 0
            MEMRE.next = 1



        # B-type
        elif opcode == 0b11000:

            RegWE.next = 0
            MEMWE.next = 0
            ALUSrc1.next = 0
            ALUSrc2.next = 0
            BranchAddSrc.next = 0
            RegWriteSrc.next = 0
            Branch.next = 1
            decode_imm_type.next = 2
            callOS.next = 0
            MEMRE.next = 0

            if funct3 == 0:
                ALUSel.next = 17  # beq
            elif funct3 == 1:
                ALUSel.next = 18  # bne
            elif funct3 == 4:
                ALUSel.next = 19  # blt
            elif funct3 == 5:
                ALUSel.next = 21  # bge
            elif funct3 == 6:
                ALUSel.next = 20  # bltu
            else:
                ALUSel.next = 22  # bgeu

        # S-type
        elif opcode == 0b01000:
            RegWE.next = 0
            MEMWE.next = 1
            ALUSrc1.next = 0
            ALUSrc2.next = 1
            BranchAddSrc.next = 0
            RegWriteSrc.next = 0
            Branch.next = 0
            decode_imm_type.next = 1
            ALUSel.next = 0  # ADD
            callOS.next = 0
            MEMRE.next = 1

        # lui
        elif opcode == 0b01101:
            RegWE.next = 1
            MEMWE.next = 0
            ALUSrc1.next = 0
            ALUSrc2.next = 1
            BranchAddSrc.next = 0
            RegWriteSrc.next = 0
            Branch.next = 0
            decode_imm_type.next = 3
            ALUSel.next = 24  # rd = imm
            callOS.next = 0
            MEMRE.next = 0

        # auipc
        elif opcode == 0b00101:
            RegWE.next = 1
            MEMWE.next = 0
            ALUSrc1.next = 1
            ALUSrc2.next = 1
            BranchAddSrc.next = 0
            RegWriteSrc.next = 0
            Branch.next = 0
            decode_imm_type.next = 3
            ALUSel.next = 0  # ADD
            callOS.next = 0
            MEMRE.next = 0

        # jal
        elif opcode == 0b11011:
            RegWE.next = 1
            MEMWE.next = 0
            ALUSrc1.next = 1
            ALUSrc2.next = 0
            BranchAddSrc.next = 0
            RegWriteSrc.next = 0
            Branch.next = 1
            decode_imm_type.next = 4
            ALUSel.next = 23  # rd = PC + 4
            callOS.next = 0
            MEMRE.next = 0

        elif opcode == 0b11100:
            RegWE.next = 0
            MEMWE.next = 0
            ALUSrc1.next = 0
            ALUSrc2.next = 0
            BranchAddSrc.next = 0
            RegWriteSrc.next = 0
            Branch.next = 0
            decode_imm_type.next = 0
            ALUSel.next = 0  # rd = PC + 4
            callOS.next = 1
            MEMRE.next = 0

        # jalr
        else:
            RegWE.next = 1
            MEMWE.next = 0
            ALUSrc1.next = 1
            ALUSrc2.next = 0
            BranchAddSrc.next = 1
            RegWriteSrc.next = 0
            Branch.next = 1
            decode_imm_type.next = 0
            ALUSel.next = 23  # rd = PC + 4
            callOS.next = 0
            MEMRE.next = 0

    return controler


@block
def test_bench():
    RegWE, MEMWE, ALUSrc1, ALURSrc2, BranchAddSrc, RegWriteSrc, Branch, MEMRE, callOS = [Signal(intbv(0)[1:]) for i in
                                                                                         range(9)]
    funct7 = Signal(intbv(0)[2:])
    ALUSel = Signal(intbv(0)[5:])
    opcode = Signal(intbv(0)[5:])
    funct3 = Signal(intbv(0)[3:])
    decode_imm_type = Signal(intbv(0)[3:])
    control_1 = control(opcode, funct3, funct7, decode_imm_type, RegWE, MEMWE, ALUSel, ALUSrc1, ALURSrc2, BranchAddSrc,
                        RegWriteSrc, Branch, MEMRE, callOS)

    @always(delay(10))
    def control_tb():
        inst = [0b11111111000001010000010100010011,
                0b00000010110001011000011100110011,
                0b00000000110001011000011010110011,
                0b11111111111111110000111100010011,
                0b11111110000011110001100011100011,
                0b00000000000000001000000001100111,
                0b00000000000011101010010110110111]
        randinst = randrange(7)
        selected_inst = intbv(inst[randinst])
        funct7.next = concat(selected_inst[32], selected_inst[25])
        funct3.next = selected_inst[15:12]
        opcode.next = selected_inst[7:2]
        symbols = ('add', 'sub', 'xor', 'or', 'and', 'sll', 'srl', "slt", 'sltu', 'mul', 'mulh', 'mulsu', 'mulu', 'div',
                   'divu', 'rem', 'remu', 'beq', 'bne', 'blt', 'bltu', 'bge', 'bgeu', 'jal', 'lui', 'sra')
        imm = ["imm_I", "imm_S", "imm_B", "imm_U", "imm_J", "imm_Shift"]
        table = ["Opcode", "Funct3", "Funct7", "decode_imm_type", "RegWE", "MEMWE", "ALUSel", "ALUSrc1", "ALURSrc2",
                 "BranchAddSrc", "RegWriteSrc", "Branch"], [bin(opcode, 5) + "11", funct3, funct7, imm[decode_imm_type],
                                                            RegWE, MEMWE,
                                                            symbols[ALUSel], ALUSrc1, ALURSrc2, BranchAddSrc,
                                                            RegWriteSrc,
                                                            Branch]
        print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

    return control_tb, control_1


# test_bench().run_sim(100)


def conv():
    RegWE, MEMWE, ALUSrc1, ALURSrc2, BranchAddSrc, RegWriteSrc, Branch, MEMRE, callOS = [Signal(intbv(0)[1:]) for i in
                                                                                         range(9)]
    funct7 = Signal(intbv(0)[2:])
    ALUSel = Signal(intbv(0)[5:])
    opcode = Signal(intbv(0)[5:])
    funct3 = Signal(intbv(0)[3:])
    decode_imm_type = Signal(intbv(0)[3:])
    control_1 = control(opcode, funct3, funct7, decode_imm_type, RegWE, MEMWE, ALUSel, ALUSrc1, ALURSrc2, BranchAddSrc,
                        RegWriteSrc, Branch, MEMRE, callOS)
    control_1.convert(hdl='Verilog')

# conv()
