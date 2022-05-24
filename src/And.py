from myhdl import block, always_comb


@block
def and_gate(in1, in2, out):
    @always_comb
    def gate():
        out.next = in1 & in2

    return gate
