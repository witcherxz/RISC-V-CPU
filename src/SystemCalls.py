import math

from myhdl import intbv, block, Signal, concat, always_comb
from tabulate import tabulate

from Registerfile import register_file
from memory import mem0, mem1, mem2, mem3


@block
def system(is_ecall):
    @always_comb
    def system_calls():
        a0 = register_file[10]
        a1 = register_file[11]
        a2 = register_file[12]
        a7 = register_file[17]

        # write call
        if is_ecall and a7 == 64 and a0 == 1:
            string = ''
            address = int(a1) // 4
            for i in range(math.ceil(a2 / 4)):
                data_pnt = concat(mem3[(address + i)], mem2[(address + i)], mem1[(address + i)], mem0[(address + i)])
                string += ''.join(chr(data_pnt[8 + byte * 8:0 + byte * 8]) for byte in range(4))

            print(string)

        # exit call
        if is_ecall and a7 == 93:
            mem = [Signal(intbv(0)[32:]) for i in range(len(mem0))]
            for i in range(len(mem0)):
                mem[i] = concat(mem3[i], mem2[i], mem1[i], mem0[i])
            table = [[int(m) for m in mem]]
            print("Memory : ")
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

            s = ["x" + str(i) for i in range(32)]
            table = s, [int(reg) for reg in register_file]
            print("Register File : ")
            print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
            quit()

    return system_calls
