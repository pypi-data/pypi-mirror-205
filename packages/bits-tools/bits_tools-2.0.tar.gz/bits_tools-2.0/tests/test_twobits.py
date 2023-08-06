import sys
import pytest

def test_twobits():
    import bits
    zero_one = bits.TwoBits(0,1)
    assert zero_one.bits == [0,1]
def test_twobits_and():
    import bits
    zero_one = bits.TwoBits(0,1)
    assert zero_one.andGate() == 0
def test_twobits_or():
    import bits
    zero_one = bits.TwoBits(0,1)
    assert zero_one.orGate() == 1
def test_twobits_not():
    import bits
    zero_one = bits.TwoBits(0,1)
    assert zero_one.notGate() == [1,0]
def test_twobits_nand():
    import bits
    zero_one = bits.TwoBits(0,1)
    assert zero_one.nandGate() == 1
def test_twobits_nor():
    import bits
    zero_one = bits.TwoBits(0,1)
    assert zero_one.norGate() == 0
def test_twobits_xor():
    import bits
    zero_one = bits.TwoBits(0,1)
    assert zero_one.xorGate() == 1
def test_twobits_xnor():
    import bits
    zero_one = bits.TwoBits(0,1)
    assert zero_one.xnorGate() == 0
def test_validate_good():
    import bits
    zero_one = bits.TwoBits(0,1)
    try:
        zero_one.validate([0,1])
        assert True
    except:
        assert False
def test_validate_bad():
    import bits
    zero_one = bits.TwoBits(0,1)
    try:
        zero_one.validate([0,2])
        assert False
    except:
        assert True
def test_setbits():
    import bits
    zero_one = bits.TwoBits(0,1)
    zero_one.set_bits([1,0])
    assert zero_one.bits == [1,0]
def test_getbits():
    import bits
    zero_one = bits.TwoBits(0,1)
    assert zero_one.get_bits() == [0,1]
