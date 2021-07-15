"""Test of bits of the parser."""
# pwfn
from pwfn._parser import fp, integer, real


def test_data_types() -> None:
    """Test parsers for various types."""
    result = fp.parseString("3.3")[0]
    assert float(result) == 3.3

    result = real.parseString("-6.20000000E+10")[0]
    assert float(result) == -6.2e10

    result = real.parseString("6.20000000D-10")[0]
    assert float(result) == 6.2e-10

    assert int(integer.parseString("4")[0]) == 4
    assert int(integer.parseString("0")[0]) == 0
    assert int(integer.parseString("-0")[0]) == 0
    assert int(integer.parseString("+08")[0]) == 8
    assert int(integer.parseString("-118")[0]) == -118
