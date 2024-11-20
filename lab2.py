import sys
from knowledge_base import KnowledgeBase
from resolution import pl_resolution

"""
CSCI-630 - Lab 2
Author: Arya Girisha Rao(ar1422@rit.edu)

This is a python file for Lab 2 to solve the problem - https://cs.rit.edu/~jro/courses/intelSys/labs/resolution/
"""


def input_validation():
    if len(sys.argv) != 2:
        raise ValueError("Please provide the filename. ")


def main():
    input_validation()
    kb = KnowledgeBase()

    if pl_resolution(kb.clauses):
        print("yes")
    else:
        print("no")


if __name__ == '__main__':
    main()
