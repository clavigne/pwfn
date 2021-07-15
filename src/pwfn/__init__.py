"""pwfn is a single-page parser library for .wfn files."""
from __future__ import annotations

# std
from dataclasses import dataclass
from typing import Any, cast, List

# external
import numpy as np
from numpy.typing import NDArray

# module
from ._orbpowers import PATDATA


def _format(x: NDArray[Any]) -> str:
    s = np.array2string(
        x, precision=4, separator=",", suppress_small=True, threshold=10
    )
    return "\n    ".join(s.splitlines())


class ParserError(Exception):
    """An parsing logic error."""

    pass


@dataclass
class Wavefunction:
    """A container for a parsed .wfn file."""

    natm: int
    norb: int
    nmo: int
    at_name: list[str]
    at_charge: NDArray[np.float64]
    at_position: NDArray[np.float64]
    orb_center: NDArray[np.int32]
    orb_type: NDArray[np.int32]
    orb_exponent: NDArray[np.float64]
    mo_energy: NDArray[np.float64]
    mo_occupation: NDArray[np.float64]
    mo_coeffs: NDArray[np.float64]

    def __repr__(self: Wavefunction) -> str:
        """Pretty-print Wavefunction."""
        return (
            f"Wavefunction(natm={self.natm}, norb={self.norb}, nmo={self.nmo}\n"
            + f"  at_name={self.at_name}\n"
            + f"  at_charge={_format(self.at_charge)}\n"
            + f"  at_position=\n    {_format(self.at_position)}\n"
            + f"  orb_center={_format(self.orb_center)}\n"
            + f"  orb_type={_format(self.orb_type)}\n"
            + f"  orb_exponent={_format(self.orb_exponent)}\n"
            + f"  mo_energy={_format(self.mo_energy)}\n"
            + f"  mo_occupation={_format(self.mo_occupation)}\n"
            + f"  mo_coeffs=\n    {_format(self.mo_coeffs)}"
            + ")"
        )

    @property
    def cartesian_powers(self: Wavefunction) -> NDArray[np.int32]:
        """Return the cartesian powers for primitive orbitals."""
        return np.array([PATDATA[i - 1] for i in self.orb_type])


def loads(data: str) -> Wavefunction:
    """Parse a string that contains a .wfn file."""
    # module
    from ._parser import parser

    dat = parser.parseString(data)

    nmo = int(dat["nmo"])
    natm = int(dat["natm"])
    norb = int(dat["norb"])

    # load atom centers
    atom_xyz = np.zeros((natm, 3))
    atom_charge = np.zeros((natm))
    atom_names = [None for i in range(natm)]
    for i in range(natm):
        atom = dat["atoms"][i]
        iat = int(atom["icnt"]) - 1  # zero indexed
        if atom_names[iat] is not None:
            raise ParserError(f"Repeated center with index {iat+1}")

        atom_names[iat] = atom["atom"].strip()
        atom_xyz[iat, 0] = float(atom["x"])
        atom_xyz[iat, 1] = float(atom["y"])
        atom_xyz[iat, 2] = float(atom["z"])
        atom_charge[iat] = float(atom["charge"])

    for i in range(natm):
        if atom_names[i] is None:
            raise ParserError(f"Missing atom with index {i+1}")
    atom_names = cast(List[str], atom_names)  # verified no None are present

    icnt = np.array([int(i) - 1 for i in dat["icnt"]])
    if len(icnt) != norb:
        raise ParserError(f"found {len(icnt)} center assignments != {norb} orbitals")

    ityp = np.array([int(i) for i in dat["ityp"]])
    if len(ityp) != norb:
        raise ParserError(f"found {len(ityp)} orbital types != {norb} orbitals")

    exps = np.array([float(e) for e in dat["exps"]])
    if len(exps) != norb:
        raise ParserError(f"found {len(exps)} orbital exponents != {norb} orbitals")

    mo_coeffs = np.zeros((norb, nmo))
    mo_occ = np.zeros((nmo,))
    mo_energy = np.zeros((nmo,))
    found = [False] * nmo

    for i in range(nmo):
        mo = dat["mos"][i]
        imo = int(mo["i"]) - 1
        if found[imo]:
            raise ParserError(f"Repeated MO with index {imo+1}")

        found[imo] = True
        mo_occ[imo] = float(mo["occ"])
        mo_energy[imo] = float(mo["energy"])
        mo_coeffs[:, imo] = np.array([float(e) for e in mo["coeffs"]])

    for i in range(nmo):
        if not found[imo]:
            raise ParserError(f"Missing MO with index {i+1}")

    return Wavefunction(
        nmo=nmo,
        natm=natm,
        norb=norb,
        at_name=atom_names,
        at_position=atom_xyz,
        at_charge=atom_charge,
        orb_center=icnt,
        orb_type=ityp,
        orb_exponent=exps,
        mo_energy=mo_energy,
        mo_occupation=mo_occ,
        mo_coeffs=mo_coeffs,
    )
