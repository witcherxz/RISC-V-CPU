from myhdl import intbv, block, Signal, always, delay, instances, ResetSignal

from Adder import Adder
from And import and_gate
from Control import control
from FINALALU import ALU
from InstructionMemory import imemory
from LoadSlicer import load_slicer
from Registerfile import Registerfile
from SystemCalls import system
from decode import decoder
from memory import memory
from mux import mux2x1
from pcRegister import pcRegister


@block
def CPU():
    clk = Signal(intbv(0)[1:])
    reset = ResetSignal(0, active=1, isasync=True)
    pcout, memdin, memdout, instruction, \
    mem_out, load, regf_input, pc1 = [Signal(intbv(0)[32:]) for i in range(8)]
    pc2, pcin, PC_add_value, ALUSrc1, regfOut1, regfOut2, ALUSrc2, ALU_output, regfin, imm = [
        Signal(intbv(0)[32:].signed()) for i in range(10)]
    rd, rs1, rs2 = [Signal(intbv(0)[6:]) for i in range(3)]
    RegWE, ALUSrcSel1, ALUSrcSel2, branch_flag, MEMWE, RegWriteSrc, Branch, \
    BranchAddSrc, is_branch, MEMEN, callOS = [Signal(intbv(0)[1:]) for i in range(11)]
    funct3 = Signal(intbv(0)[3:])
    ALUSel = Signal(intbv(0)[5:])
    opcode = Signal(intbv(0)[5:])
    funct7 = Signal(intbv(0)[2:])
    imm_sel = Signal(intbv(0)[3:])
    PC = pcRegister(pcin, pcout, Signal(intbv(1)[1:]), clk)
    instuctionMemory = imemory(Signal(intbv(0)[32:]), pcout, Signal(intbv(0)[1:]), clk, instruction)
    decoder_1 = decoder(instruction, imm_sel, opcode, rd, rs1, rs2, funct3, funct7, imm)
    regester_file = Registerfile(regfin, rd, rs1, rs2, RegWE, regfOut1, regfOut2, clk)
    ALUSrc1Mux = mux2x1(regfOut1, pcout, ALUSrcSel1, ALUSrc1)
    ALUSrc2Mux = mux2x1(regfOut2, imm, ALUSrcSel2, ALUSrc2)
    ALU_1 = ALU(ALUSrc1, ALUSrc2, ALUSel, ALU_output, branch_flag)
    data_memory = memory(regfOut2, ALU_output, funct3, MEMWE, clk, mem_out, MEMEN)
    load_slicer_1 = load_slicer(mem_out, funct3, load)
    regf_input_mux = mux2x1(ALU_output, load, RegWriteSrc, regfin)
    controler = control(opcode, funct3, funct7, imm_sel, RegWE, MEMWE, ALUSel, ALUSrcSel1, ALUSrcSel2, BranchAddSrc,
                        RegWriteSrc,
                        Branch, MEMEN, callOS)
    And = and_gate(Branch, branch_flag, is_branch)
    PCplus4 = Adder(pcout, 4, pc1)
    PC_adder_mux = mux2x1(pcout, regfOut1, BranchAddSrc, PC_add_value)
    PCAdder = Adder(imm, PC_add_value, pc2)
    PC_mux = mux2x1(pc1, pc2, is_branch, pcin)
    sys = system(callOS)

    @always(delay(1))
    def clock():
        clk.next = not clk

    return instances()


print("CPU start processing...")
CPU().run_sim()
