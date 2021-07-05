from py4hw import *


class ROM(Logic):
    def __init__(self, parent: Logic, name: str, address: Wire, data: Wire):
        super().__init__(parent, name)

        self.address = self.addIn("address", address)
        self.data = self.addOut("data", data)

        self.wcount = pow(2, address.getWidth())

        self.values = [0] * self.wcount

    def loadROM(self, filename: str, base: int = 10):
        """
        Load ROM contents from file.

        If content is smaller than ROM size, completes with 0.
        If content is larger than ROM size, excedent is ignored.
        """

        try:
            dump = []
            with open(filename) as f:
                dump = f.readlines()

                self.values = [int(x, base) for x in dump]

            ldump = len(dump)
            if ldump < self.wcount:
                self.values.extend([0 for i in range(self.wcount - ldump)])
            elif ldump > self.wcount:
                self.values = self.values[:self.wcount]

        except OSError as reason:
            print("Error loading ROM: " + str(reason))

    def write(self, address: int, value: int):
        self.values[address] = value

    def read(self, address: int) -> int:
        return self.values[address]

    def clock(self):
        self.data.prepare(self.values[self.address.get()])


sys = HWSystem()

addr = sys.wire("Address", 5)
data = sys.wire("Data", 8)

Scope(sys, "Data OUT", data)

rom = ROM(sys, "ROM", addr, data)
rom.loadROM("test.rom", 16)

sim = sys.getSimulator()

for i in range(32):
	addr.prepare(i)
	sim.clk(1)