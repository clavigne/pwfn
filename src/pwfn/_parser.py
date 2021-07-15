# external
from pyparsing import (
    Combine,
    Group,
    LineEnd,
    LineStart,
    Literal,
    nums,
    oneOf,
    OneOrMore,
    Optional,
    ParserElement,
    printables,
    Regex,
    SkipTo,
    StringEnd,
    StringStart,
    tokenMap,
    White,
    Word,
    ZeroOrMore,
)

ParserElement.enablePackrat()  # faster
ParserElement.setDefaultWhitespaceChars(" \t")  # use significant newlines

# Data types
# ------------------------------------------------------------------------------------------
# integer
integer = Regex(r"[+-]?\d+")

# floating point
fp = Regex(r"[+-]?(?:\d+\.\d*|\.\d+)")

# fortran real
real = Regex(
    r"[+-]?(?:\d+(?:[eEdD][+-]?\d+)|(?:\d+\.\d*|\.\d+)(?:[eEdD][+-]?\d+)?)"
).setParseAction(tokenMap(lambda x: x.replace("D", "e")))

# a line of text
textline = (... + LineEnd().suppress()).setParseAction("".join)

# the file header
header = (
    Literal("GAUSSIAN")
    + ...
    + integer("nmo")
    + ...
    + integer("norb")
    + ...
    + integer("natm")
    + ...
    + LineEnd().suppress()
)

# an atom line
atom = Group(
    Word(printables)("atom")
    + White()
    + integer("i")
    + ...
    + Literal("CENTRE")
    + White()
    + integer("icnt")
    + Literal(")")
    + White()
    + fp("x")
    + ...
    + fp("y")
    + ...
    + fp("z")
    + ...
    + fp("charge")
    + ...
    + LineEnd().suppress()
)

# the center assignment group
center_assignment = (
    Literal("CENTRE ASSIGNMENTS").suppress() + OneOrMore(integer) + LineEnd().suppress()
)

# the orbital type group
type_assignment = (
    Literal("TYPE ASSIGNMENTS").suppress() + OneOrMore(integer) + LineEnd().suppress()
)

# exponents
exponents = Literal("EXPONENTS").suppress() + OneOrMore(real) + LineEnd().suppress()

# molecular orbitals
mos = Group(
    Literal("MO")
    + integer("i")
    + ...
    + Literal("OCC NO =")
    + ...
    + fp("occ")
    + Literal("ORB. ENERGY")
    + ...
    + fp("energy")
    + LineEnd().suppress()
    + Group(OneOrMore(OneOrMore(real) + LineEnd().suppress()))("coeffs")
)

parser = (
    textline("title")
    + header
    + Group(OneOrMore(atom))("atoms")
    + Group(OneOrMore(center_assignment))("icnt")
    + Group(OneOrMore(type_assignment))("ityp")
    + Group(OneOrMore(exponents))("exps")
    + Group(OneOrMore(mos))("mos")
    + Literal("END DATA")
    + ...
    + LineEnd()
    + textline("end")
)
