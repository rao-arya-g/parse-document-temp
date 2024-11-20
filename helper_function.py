"""
CSCI-630 - Lab 2
Author: Arya Girisha Rao(ar1422@rit.edu)

This is a python file for Lab 2 to solve the problem - https://cs.rit.edu/~jro/courses/intelSys/labs/resolution/
"""


def debug_info(clause_1, clause_2, clause_3):
    print_string = "Input\n"
    for entry in clause_1.entries:
        if entry.negation:
            print_string += " " + entry.name
        else:
            print_string += " !" + entry.name

    print_string += "\n"
    for entry in clause_2.entries:
        if entry.negation:
            print_string += " " + entry.name
        else:
            print_string += " !" + entry.name

    print_string += "\nOutput - \n"
    for entry in clause_3.entries:
        if entry.negation:
            print_string += " " + entry.name
        else:
            print_string += " !" + entry.name

    print(print_string)
