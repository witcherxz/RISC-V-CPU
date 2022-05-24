from myhdl import *

@block
def ALU(x, y, s, z, f):
    @always_comb
    def logic():
        # ADD ###################
        if s == 0:
            z.next = x.signed() + y.signed()
            f.next = 0
        # SUB ###################
        elif s == 1:
            z.next = x.signed() - y.signed()
            f.next = 0
        # XOR ###################
        elif s == 2:
            z.next = x.signed() ^ y.signed()
            f.next = 0

        # OR ############################
        elif s == 3:
            z.next = x.signed() | y.signed()
            f.next = 0
        # AND ##################################
        elif s == 4:
            z.next = x.signed() & y.signed()
            f.next = 0
        # SLL #########################
        elif s == 5:
            z.next = x << y
            f.next = 0
        # SRL #####################
        elif s == 6:
            z.next = x >> y
            f.next = 0
        # SLT ####################
        elif s == 7:
            if x.signed() < y.signed():
                z.next = 1
                f.next = 0
            else:
                z.next = 0
                f.next = 0

        # SLTU #################################
        elif s == 8:
            if x < y:
                z.next = 1
                f.next = 0
            else:
                z.next = 0
                f.next = 0
        # MUL ###############################
        elif s == 9:
            g = intbv(0)[64:]
            g[64:0] = intbv(x.signed() * y.signed())
            z.next = g[32:0].signed()
            f.next = 0

        # MULH #####################################
        elif s == 10:
            g = intbv(0)[64:]
            g[64:0] = intbv(x.signed() * y.signed())
            z.next = g[64:32].signed()
            f.next = 0
        # MULSU ###########################################
        elif s == 11:
            g = intbv(0)[64:]
            g[64:0] = intbv(x.signed() * y)
            z.next = (g[64:32].signed())
            f.next = 0
        # MULU ##############################
        elif s == 12:
            g = intbv(0)[64:]
            g[64:0] = intbv(x * y)
            z.next = g[64:32].signed()
            f.next = 0
        # DIV #################################################
        elif s == 13:
            z.next = x.signed() // y.signed()
            f.next = 0
        # DIVU #################################################
        elif s == 14:
            z.next = x // y
            f.next = 0
        # REM #########################################
        elif s == 15:
            z.next = x.signed() % y.signed()
            f.next = 0
        # REMU ######################################################
        elif s == 16:
            z.next = x % y
            f.next = 0
        # BEQ #######################################################
        elif s == 17:
            if x.signed() == y.signed():
                z.next = 0
                f.next = 1
            else:
                z.next = 0
                f.next = 0
        # BNE ###########################################################
        elif s == 18:
            if x.signed() != y.signed():
                z.next = 0
                f.next = 1
            else:
                z.next = 0
                f.next = 0
        # BLT ####################################################
        elif s == 19:
            if x.signed() < y.signed():
                z.next = 0
                f.next = 1
            else:
                z.next = 0
                f.next = 0
        # BLTU ####################################################
        elif s == 20:
            if x < y:
                z.next = 0
                f.next = 1
            else:
                z.next = 0
                f.next = 0
        # BGE #################################################
        elif s == 21:
            if x.signed() >= y.signed():
                z.next = 0
                f.next = 1
            else:
                z.next = 0
                f.next = 0
        # BGEU ##########################################################
        elif s == 22:
            if x >= y:
                z.next = 0
                f.next = 1
            else:
                z.next = 0
                f.next = 0
        # JAL ###########################################
        elif s == 23:
            z.next = x + 4
            f.next = 1

        # LUI #########################
        elif s == 24:
            z.next = y.signed()
            f.next = 0

        # SRA #################################
        else:
            if int(y) < 0:

                z.next = x.signed() << y.signed() * -1
                f.next = 0
            else:
                z.next = x.signed() >> y.signed()
                f.next = 0

    return logic


def test_bench():
    # symbols = ('+', '-', '^', '|', '&','<<','>>','<','<','*','*','*','*','/','/','%','%','==','!=','<','<','>=','>=','+','+','<<','<<','','','','','')
    # n = (0, 1 ,2 ,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25)
    symbols = (
    'add', 'sub', 'xor', 'or', 'and', 'sll', 'srl', "slt", 'sltu', 'mul', 'mulh', 'mulsu', 'mulu', 'div', 'divu', 'rem',
    'remu', 'beq', 'bne', 'blt', 'bltu', 'bge', 'bgeu', 'jal', 'lui', 'sra')
    table = ['add', 'sub', 'xor', 'or', 'and', 'sll', 'srl', 'slt', 'sltu', 'mul', 'mulh', 'mulsu', 'mulu', 'div',
             'divu', 'rem', 'remu', 'beq', 'bne', 'blt', 'bltu', 'bge', 'bgeu', 'jal', 'lui', 'sra'], [0, 1, 2, 3, 4, 5,
                                                                                                       6, 7, 8, 9, 10,
                                                                                                       11, 12, 13, 14,
                                                                                                       15, 16, 17, 18,
                                                                                                       19, 20, 21, 22,
                                                                                                       23, 24, 25]
    # print(tabulate(table,headers='firstrow',tablefmt='fancy_grid'))
    # print(tabulate({'symbols':[0, 1 ,2 ,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],'operation':[s],'Operations':['add', 'sub', 'xor', 'or', 'and','sll','srl','sra','sltu','mul','mulh','mulsu','mulu','div','divu','rem','remu','beq','bne','blt','bltu','bge','bgeu','jal','lui']},headers="keys",tablefmt='fancy_grid'))

    # print(tabulate({'rs1':[0, 1 ,2 ,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],'Operations':['add', 'sub', 'xor', 'or', 'and','sll','srl','sra','sltu','mul','mulh','mulsu','mulu','div','divu','rem','remu','beq','bne','blt','bltu','bge','bgeu','jal','lui']},headers="keys",tablefmt='fancy_grid'))
    for i in range(1):
        x.next = 5
        y.next = -5
        s.next = 11
        yield delay(10)
        ##print(tabulate({'symbols':s[i],'x':[x],'y':[y]},headers="keys",tablefmt='fancy_grid'))

        print(symbols[s], int(x), ",", int(y), "=", int(z), "   ", "flag =", bool(f))


x = Signal(intbv(0)[32:])
y = Signal(intbv(0)[32:])
s = Signal(intbv(0)[5:])
z = Signal(intbv(0)[32:])
f = Signal(intbv(0)[1:])

inst = ALU(x, y, s, z, f)
# inst2 = test_bench()
# sim = Simulation(inst, inst2).run()
# inst.convert(hdl='Verilog')
