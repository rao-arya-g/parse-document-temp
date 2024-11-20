from dataclasses import dataclass

"""
CSCI-630 - Lab 2
Author: Arya Girisha Rao(ar1422@rit.edu)

This is a python file for Lab 2 to solve the problem - https://cs.rit.edu/~jro/courses/intelSys/labs/resolution/
"""


@dataclass(frozen=True)
class Clause:
    entries: frozenset


@dataclass(frozen=True)
class Constant:
    name: str


@dataclass(frozen=True)
class Function:
    name: str
    terms: frozenset


@dataclass(frozen=True)
class Predicate:
    name: str
    arguments: tuple
    negation: bool


@dataclass(frozen=True)
class Variable:
    name: str
