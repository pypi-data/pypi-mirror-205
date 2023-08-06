import random
from exceptions import InvalidBitsError
class TwoBits(object):
    def __init__(self, bit1, bit2):
        self.bits = []
        self.bit = bit1
        self.bits.append(bit1)
        self.bits.append(bit2)

    def get_bits(self):
        return self.bits

    def set_bits(self, newbits):
        self.validate(newbits)
        self.bits = newbits

    @staticmethod
    def validate(bits):
        if len(bits) != 2:
            raise InvalidBitsError("The number of bits must be 2")
        for bit in bits:
            if bit not in [0, 1]:
                raise InvalidBitsError("Bits must be either 0 or 1")

    def andGate(self):
        """Implements a basic AND gate.
        Takes no arguments."""
        if self.bits[0] and self.bits[1]:
            return 1
        return 0

    def orGate(self):
        """Implements a basic OR gate.
        Takes no arguments."""
        if self.bits[0] or self.bits[1]:
            return 1
        return 0

    def notGate(self):
        """Implements a basic NOT gate.
        Takes no arguments."""
        results = []
        for i in range(len(self.bits)):
            if self.bits[i] == 0:
                results.append(1)
            else:
                results.append(0)
        return results

    def nandGate(self):
        """Implements a basic NAND gate.
        Takes no arguments."""
        if self.notGate() and self.notGate():
            return 1
        return 0

    def norGate(self):
        if self.bits[0] or self.bits[1]:
            return 0
        return 1

    def xorGate(self):
        if self.bits[0] and not self.bits[1]:
            return 1
        elif not self.bits[0] and self.bits[1]:
            return 1
        return 0

    def xnorGate(self):
        if self.bits[0] and self.bits[1]:
            return 1
        elif not self.bits[0] and not self.bits[1]:
            return 1
        return 0


class RandomBits(object):
    def __init__(self, num_of_bits):
        self.bits = [random.randrange(0, 2) for _ in range(num_of_bits)]

    def get_bits(self):
        return self.bits

    def set_bits(self, newbits):
        self.validate(newbits)
        self.bits = newbits

    def validate(self, bits):
        if len(self.bits) != len(bits):
            raise InvalidBitsError("The number of bits must be " + str(len(self.bits)))
        for bit in bits:
            if bit not in [0, 1]:
                raise InvalidBitsError("Bits must be either 0 or 1")
            return True

    def andGate(self, otherBits):
        """Implements a basic AND gate.
        Takes one argument (otherBits), which is a list of bits."""
        results = []
        for i in range(len(self.bits)):
            if self.bits[i] and otherBits[i]:
                results.append(1)
            else:
                results.append(0)
        return results

    def orGate(self, otherBits):
        """Implements a basic OR gate.
        Takes one argument (otherBits), which is a list of bits."""
        results = []
        for i in range(len(self.bits)):
            if self.bits[i] or otherBits[i]:
                results.append(1)
            else:
                results.append(0)
        return results

    def nandGate(self, otherBits):
        """Implements a basic NAND gate.
        Takes one argument (otherBit), which is a list of bits."""
        results = []
        for i in range(len(self.bits)):
            if self.bits[i] and otherBits[i]:
                results.append(0)
            else:
                results.append(1)
        return results

    def notGate(self):
        """Implements a basic NOT gate.
        Takes no arguments. (It operates on the RandomBits instance it was called from.)"""
        results = []
        for i in range(len(self.bits)):
            if self.bits[i]:
                results.append(0)
            else:
                results.append(1)
        return results

    def norGate(self,otherBits):
        """Implements a NOR gate.
        Takes one argument (otherBits), a list of bits."""
        results = []
        for i in range(len(self.bits)):
            if self.bits[i] or otherBits[i]:
                results.append(0)
            else:
                results.append(1)
        return results
    
    def xorGate(self,otherBits):
        """Implements an XOR gate.
        Takes one argument (otherBits), a list of bits."""
        results = []
        for i in range(len(self.bits)):
            if self.bits[i] and otherBits[i]:
                results.append(0)
            elif self.bits[i] and not otherBits[i]:
                results.append(1)
            elif not self.bits[i] and otherBits[i]:
                results.append(1)
            else:
                results.append(0)
        return results
    
    def xnorGate(self, otherBits):
        """Implements an XNOR gate.
        Takes one argument (otherBits), a list of bits."""
        results = []
        for i in range(len(self.bits)):
            if self.bits[i] and otherBits[i]:
                results.append(1)
            elif not self.bits[i] and not otherBits[i]:
                results.append(1)
            else:
                results.append(0)
        return results

