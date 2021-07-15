"""Test of the various bits of the parser."""
# external
import numpy as np

# pwfn
import pwfn


def test_read_string() -> None:
    """Test reading a fchk file."""
    with open("tests/data/benzene.wfn") as f:
        result = pwfn.loads(f.read())

    assert result.natm == 12
    a = str(result)
    assert isinstance(a, str)
    powers = result.cartesian_powers
    assert np.allclose(powers[0], [0, 0, 0])
