from random import randrange

from myhdl import block, always_seq, intbv, Signal, always, delay, ResetSignal
from tabulate import tabulate


@block
def pcRegister(Inp, Out, we, clk):
    """a Program Counter register (PC)
        :param Inp (Input)
        :param Out (Output)
        :param we  (Write Enable)
        :param clk (Clock input)
        :param reset (asynchronous reset input)
    """

    @always_seq(clk.posedge, None)
    def seq():
        if we == 1:
            Out.next = Inp

    return seq


# Test Bench
@block
def test_pc():
    we, clk = (Signal(intbv(0)[1:]) for i in range(2))
    Inp = Signal(intbv(0)[32:])
    Out = Signal(intbv(0)[32:])
    reset = ResetSignal(1, active=0, isasync=True)
    pcr_1 = pcRegister(Inp, Out, we, clk, reset)

    @always(delay(10))
    def clock():
        clk.next = not clk

    @always(delay(20))
    def test():
        Inp.next = randrange(2 ** 32)
        we.next = randrange(2)
        table = ['Input', 'Output', 'WEnable'], [int(Inp), int(Out), int(we)]
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    return test, pcr_1, clock


# tp = test_pc()
# tp.run_sim(700)


# Convert to Verilog
def convert():
    we, clk = (Signal(intbv(0)[1:]) for i in range(2))
    Inp = Signal(intbv(0)[32:])
    Out = Signal(intbv(0)[32:])
    reset = ResetSignal(1, active=0, isasync=True)
    pcr_1 = pcRegister(Inp, Out, we, clk, reset)
    pcr_1.convert(hdl='Verilog')
# convert()
