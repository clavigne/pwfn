# pwfn

**pwfn** is a tiny library for parsing [AIMPAC
format](https://github.com/ecbrown/aimpac/) `.wfn` files from quantum
chemistry programs and [Molden2Aim](https://github.com/zorkzou/Molden2AIM/)
into a Python data structure. This can be used to do ML on electronic
wavefunctions. 

This library does not do anything besides parsing! It is basically a single
page [pyparsing](https://github.com/pyparsing/pyparsing/) grammar. You'll need
to do your own data processing from its outputs.


## Usage

**pwfn** consists of a single string parser `pwfn.loads(s)`,

```python
import pwfn

with open("benzene.wfn", "r") as f:
    wavefunction = pwfn.loads(f.read())
```

This returns a `Wavefunction` container with the extracted data in its
attributes. All quantities are in Hartree units (unchanged from the `.wfn`
format).


## Installation

**pwfn** is available from pip,

```shell
pip install pwfn
```

It depends on the excellent
[pyparsing](https://github.com/pyparsing/pyparsing/) library as well as
[numpy](https://numpy.org/).

## Notes

If you want a similarly minimalist library to parse formatted checkpoint
files, consider my other library [fchic](https://github.com/clavigne/fchic).
If you are looking for a full feature solution for wavefunction data analysis,
consider using the excellent [Multiwfn program](http://sobereva.com/multiwfn/)
or [orbkit](https://github.com/orbkit/orbkit).


## License

**pwfn** is free software provided under the MIT license.


