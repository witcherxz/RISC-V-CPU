from random import randrange

from myhdl import block, always_comb, intbv, Signal, delay, instance


@block
def mux2x1(a0, a1, s, z):
    @always_comb
    def comb():
        if s == 1:
            z.next = a1
        else:
            z.next = a0

    return comb


a0, a1, z, s = [Signal(intbv(0)[1:]) for i in range(4)]


@block
def test_mux2x1():
    a0, a1, z, s = [Signal(intbv(0)[1:]) for i in range(4)]
    mux_1 = mux2x1(a0, a1, s, z)

    @instance
    def test():
        print("a1 a0 s  z")
        for i in range(12):
            a0.next, a1.next, s.next = randrange(2), randrange(2), randrange(2)
            yield delay(1)
            print("%s  %s  %s  %s" % (a1, a0, s, z))

    return test, mux_1


#
# tp = test_mux2x1()
# tp.run_sim()


def conv_mux2x1():
    a0, a1, z, s = [Signal(intbv(0)[1:]) for i in range(4)]
    mux = mux2x1(a0, a1, s, z)
    mux.convert(hdl='Verilog')


# conv_mux2x1()

@block
def mux32(a0, a1, a2, a3, a4, a5, s, z, sign):
    @always_comb
    def mux():
        if s == 0:
            z.next = a0
            sign.next = a0[11]

        elif s == 1:
            z.next = a1
            sign.next = a1[11]

        elif s == 2:
            z.next = a2
            sign.next = a2[12]

        elif s == 3:
            z.next = a3
            sign.next = a3[19]

        elif s == 4:
            z.next = a4
            sign.next = a4[20]
        else:
            z.next = a5
            sign.next = a5[11]

    return mux


@block
def test_mux32():
    z, a0, a1, a2, a3, a4, a5 = [Signal(intbv(0)[32:]) for i in range(7)]
    s = Signal(intbv(0)[3:])
    sign = Signal(intbv(0)[1:])
    mux_1 = mux32(a0, a1, a2, a3, a4, a5, s, z, sign)

    @instance
    def test():
        for i in range(12):
            a0.next, a1.next, a2.next, a3.next, a4.next, a5.next = [randrange(2 ** 32) for i in range(6)]
            s.next = randrange(2 ** 3)
            yield delay(10)
            print("%s  %s  %s  %s  %s  %s %s %s" % (a0, a1, a2, a3, a4, a5, s, z))

    return test, mux_1


# tp = test_mux32()
# tp.run_sim()

def conv_mux32():
    z, a0, a1, a2, a3, a4, a5 = [Signal(intbv(0)[32:]) for i in range(7)]
    sign = Signal(intbv(0)[1:])
    s = Signal(intbv(0)[3:])
    mux_1 = mux32(a0, a1, a2, a3, a4, a5, s, z, sign)
    mux_1.convert(hdl='Verilog')

# conv_mux32()
