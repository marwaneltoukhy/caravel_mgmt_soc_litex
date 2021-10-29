from migen import *
from litex.soc.cores.gpio import GPIOTristate
from litex.soc.interconnect.csr_eventmanager import *
from migen.genlib.cdc import MultiReg

class GPIOASIC(GPIOTristate):
    def __init__(self, pads):
        assert isinstance(pads, Signal) or isinstance(pads, Record)
        nbits = len(pads) if isinstance(pads, Signal) else len(pads.o)

        self._oe  = CSRStorage(nbits, description="GPIO Tristate(s) Control.")
        self._in  = CSRStatus(nbits,  description="GPIO Input(s) Status.")
        self._out = CSRStorage(nbits, description="GPIO Ouptut(s) Control.")

        # # #
        # Tristate inout IOs (For external tristate IO chips or simulation).
        for i in range(nbits):
            self.comb += pads.oe[i].eq(~self._oe.storage[i])
            self.comb += pads.o[i].eq(self._out.storage[i])
            self.specials += MultiReg(pads.i[i], self._in.status[i])

class LogicAnalyzer(GPIOTristate):
    def __init__(self, pads):
        assert isinstance(pads, Signal) or isinstance(pads, Record)
        nbits = len(pads) if isinstance(pads, Signal) else len(pads.output)

        self._ien  = CSRStorage(nbits, description="LA Input Enable")
        self._oe  = CSRStorage(nbits, description="LA Output Enable")
        self._in  = CSRStatus(nbits,  description="LA Input(s) Status.")
        self._out = CSRStorage(nbits, description="LA Ouptut(s) Control.")

        # # #
        # Tristate inout IOs (For external tristate IO chips or simulation).
        for i in range(nbits):
            self.comb += pads.iena[i].eq(~self._ien.storage[i])
            self.comb += pads.oenb[i].eq(~self._oe.storage[i])
            self.comb += pads.output[i].eq(self._out.storage[i])
            self.specials += MultiReg(pads.input[i], self._in.status[i])