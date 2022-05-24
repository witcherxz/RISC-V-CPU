from random import randrange

from myhdl import intbv, block, Signal, always_comb, always, delay, bin, concat, instances
from tabulate import tabulate


@block
def load_slicer(din, sel, dout):
    @always_comb
    def comp():
        if sel == 0:
            dout.next = din[8:]
        elif sel == 1:
            dout.next = din[16:]
        elif sel == 2:
            dout.next = din
        elif sel == 4:
            dout.next = concat(intbv(2 ** 24 - 1) * din[7], din[8:])
        else:
            dout.next = concat(intbv(2 ** 16 - 1) * din[15], din[16:])

    return instances()


@block
def testb():
    din, dout = [Signal(intbv(0)[32:]) for i in range(2)]
    sel = Signal(intbv(0)[3:])

    ls = load_slicer(din, sel, dout)

    @always(delay(5))
    def test():
        din.next = randrange(2 ** 32 - 1)
        sel.next = randrange(2 ** 3 - 1)
        table = ["din", "sel", "dout"], [bin(din, 32), sel, bin(dout, 32)]

        print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

    return ls, test

# testb().run_sim(100)
