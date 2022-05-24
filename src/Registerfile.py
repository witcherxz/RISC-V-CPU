from random import randrange

from myhdl import intbv, block, Signal, always, delay, instance, always_seq, always_comb
from tabulate import tabulate

register_file = [Signal(intbv(0)[32:].signed()) for i in range(32)]


@block
def Registerfile(din, rd, rs1, rs2, we, data1, data2, clk):
    @always_comb
    def read():
        data1.next = register_file[rs1]
        data2.next = register_file[rs2]

    @always_seq(clk.posedge, None)
    def write():
        if we:
            if rd != 0:
                register_file[0] = 0
                register_file[rd].next = din

    return write, read


@block
def test():
    clk = Signal(intbv(0)[1:])
    din = Signal(intbv(0)[32:])  # 32-bit
    rd = Signal(intbv(0)[5:])  # 5-bit
    rs1 = Signal(intbv(0)[5:])  # 5-bit
    rs2 = Signal(intbv(0)[5:])  # 5-bit
    data1, data2 = [Signal(intbv(0)[32:]) for i in range(2)]
    we = Signal(intbv(0)[1:])
    register_1 = Registerfile(din, rd, rs1, rs2, we, data1, data2, clk)

    @always(delay(5))
    def clock():
        clk.next = not clk

    @instance
    def reg():
        we.next = 1
        for i in range(32):
            rd.next = i
            rs1.next = randrange(32)
            rs2.next = randrange(32)
            din.next = randrange((2 ** 31) - 1)
            yield delay(6)
            table = ['din', 'rd', 'rs1', 'rs2', 'we', 'data1', 'data2'], [int(din), int(rd), int(rs1), int(rs2), int(we)
                , int(data1), int(data2)]
            print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
            yield delay(6)

        print("------------------------------------------------------------------\n")

        we.next = 0
        for i in range(32):
            rd.next = i
            rs1.next = randrange(32)
            rs2.next = randrange(32)
            din.next = randrange((2 ** 31) - 1)
            yield delay(6)
            table = ['din', 'rd', 'rs1', 'rs2', 'we', 'data1', 'data2'], [int(din), int(rd), int(rs1), int(rs2), int(we)
                , int(data1), int(data2)]
            print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
            yield delay(6)

    return reg, register_1, clock


# test().run_sim(500)

def convert():
    clk = Signal(intbv(0)[1:])
    din = Signal(intbv(0)[32:])
    rd = Signal(intbv(0)[5:])
    rs1 = Signal(intbv(0)[5:])
    rs2 = Signal(intbv(0)[5:])
    data1, data2 = [Signal(intbv(0)[32:]) for i in range(2)]
    we = Signal(intbv(0)[1:])
    register_1 = Registerfile(din, rd, rs1, rs2, we, data1, data2, clk)
    register_1.convert(hdl='Verilog')
# convert()

# test().run_sim()
