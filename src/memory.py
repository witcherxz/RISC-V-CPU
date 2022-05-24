import random

from myhdl import intbv, block, Signal, always, delay, concat, always_comb
from tabulate import tabulate

data = open('memory').read().splitlines()
mem0 = [Signal(intbv(int(data[i], 2))[8:]) for i in range(len(data))]
mem1 = [Signal(intbv(int(data[i], 2))[16:8]) for i in range(len(data))]
mem2 = [Signal(intbv(int(data[i], 2))[24:16]) for i in range(len(data))]
mem3 = [Signal(intbv(int(data[i], 2))[32:24]) for i in range(len(data))]


@block
def memory(din, addr, wsize, we, clk, dout, en):
    @always(clk.posedge)
    def write():
        if we:
            address = addr // 4
            # Store byte
            if wsize == 0:
                mem0[address] = din[8:]
            # Store half word
            elif wsize == 1:
                mem1[address] = din[16:8]
                mem0[address] = din[8:]
            # Store Word
            else:
                mem3[address] = din[32:24]
                mem2[address] = din[24:16]
                mem1[address] = din[16:8]
                mem0[address] = din[8:]

    @always_comb
    def read():
        address = 0
        # if read enable
        if en:
            address = addr // 4
        dout.next = concat(mem3[address], mem2[address], mem1[address], mem0[address])

    return write, read


@block
def mem_testbench():
    din, add = [Signal(intbv(0)[32:].signed()) for i in range(2)]
    dout = Signal(intbv(0)[32:])
    we, clk = [Signal(intbv(0)[1:]) for i in range(2)]
    wsize = Signal(intbv(0)[3:])

    @always(delay(5))
    def clock():
        clk.next = not clk

    mem_1 = memory(din, add, wsize, we, clk, dout)

    # clock will write on positive edge
    @always(delay(5))
    def testbench():
        din.next = random.randrange(100)
        add.next = random.randrange(100)
        we.next = 1
        wsize.next = 0
        table = ["Address", "Data in", "Write Enable", "Write Size", "clock", "Data Out"], [add, din, we, wsize, clk,
                                                                                            dout]
        print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

    return testbench, mem_1, clock


# mem_testbench().run_sim(100)


def conv():
    din, add = [Signal(intbv(0)[32:].signed()) for i in range(2)]
    dout = Signal(intbv(0)[32:])
    we, clk, en = [Signal(intbv(0)[1:]) for i in range(3)]
    wsize = Signal(intbv(0)[2:])
    mem_1 = memory(din, add, wsize, we, clk, dout, en)
    mem_1.convert(hdl="verilog")


# conv()
