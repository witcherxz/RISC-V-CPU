from myhdl import intbv, block, Signal, always, delay, instance, always_comb


@block
def imemory(din, address, we, clk, dout):
    instructions = open('instructions').read().splitlines()
    mem = [Signal(intbv(int(instructions[i], 2))[32:]) for i in range(len(instructions))]

    @always(clk.posedge)
    def write():
        if we:
            mem[address].next = din

    @always_comb
    def read():
        dout.next = mem[int(address // 4)]

    return write, read


@block
def mem_testbench():
    din, add = [Signal(intbv(0)[32:].signed()) for i in range(2)]
    dout = Signal(intbv(0)[32:])
    we, clk = [Signal(intbv(0)[1:]) for i in range(2)]
    # wsize = Signal(intbv(0)[2:])

    mem_1 = imemory(din, add, we, clk, dout)

    @always(delay(5))
    def clock():
        clk.next = not clk

    @instance
    def testbench():
        din.next = 9
        we.next = 1
        add.next = 0
        wsize.next = 0
        yield delay(6)
        yield delay(6)

    return testbench, mem_1, clock


# mem_testbench().run_sim(100)


def conv():
    din, add = [Signal(intbv(0)[32:].signed()) for i in range(2)]
    dout = Signal(intbv(0)[32:])
    we, clk = [Signal(intbv(0)[1:]) for i in range(2)]
    wsize = Signal(intbv(0)[2:])

    mem_1 = memory(din, add, wsize, we, clk, dout)
    mem_1.convert(hdl="verilog")

# conv()
