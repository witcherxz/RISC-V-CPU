from random import randrange

from myhdl import block, intbv, always_comb, instances, Signal, always, delay


@block
def Adder(input1, input2, output):
    @always_comb
    def plus():
        output.next = input1 + input2

    return instances()


@block
def teas_b():
    input1, input2, output = [Signal(intbv(0)[32:]) for i in range(3)]
    adder_1 = Adder(input1, input2, output)

    @always(delay(5))
    def test():
        input1.next = randrange(2 ** 32 - 1)
        input2.next = randrange(2 ** 32 - 1)
        print(output)

    return instances()

# teas_b().run_sim(100)
