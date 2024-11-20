import sys
import re
from class_definitions import Clause, Predicate, Function, Variable, Constant

"""
CSCI-630 - Lab 2
Author: Arya Girisha Rao(ar1422@rit.edu)

This is a python file for Lab 2 to solve the problem - https://cs.rit.edu/~jro/courses/intelSys/labs/resolution/
"""


class KnowledgeBase(object):

    def initialize_kb(self):
        return

    def __init__(self):
        self.filename = sys.argv[1]
        self.predicate_names = set()
        self.variable_names = set()
        self.constant_names = set()
        self.function_names = set()
        self.clauses = set()
        self.process_inputs()

    @staticmethod
    def read_all_lines(filename):
        with open(filename) as f:
            lines = [line.rstrip() for line in f]
        return lines

    @staticmethod
    def pattern_match_function(input_string):
        start_index = input_string.find("(")
        end_index = input_string.rfind(")")
        return input_string[:start_index], input_string[start_index+1: end_index]

    def create_term(self, input_string):
        if input_string in self.variable_names:
            return Variable(input_string)
        elif input_string in self.constant_names:
            return Constant(input_string)
        else:
            name, terms_string = self.pattern_match_function(input_string)
            function_terms = terms_string.split(",")
            function_terms = [x.strip() for x in function_terms]
            terms_list = []
            for term_string in function_terms:
                terms_list.append(self.create_term(term_string))

            return Function(name, frozenset(terms_list))

    def construct_non_empty_predicate(self, input_string, negation):
        predicate_pattern = r"([\w]+)\((.*?)(?:, (.*?))*\)$"
        match = re.match(predicate_pattern, input_string)
        if match is None:
            raise ValueError("Predicate %s is not in required format".format(input_string))

        predicate_name = match.group(1)
        predicate_arguments = match.group(2).split(",")
        predicate_arguments = [x.strip() for x in predicate_arguments]
        all_terms = []
        for term in predicate_arguments:
            term_obj = self.create_term(term)
            all_terms.append(term_obj)
        predicate_obj = Predicate(predicate_name, tuple(all_terms), negation)
        return predicate_obj

    @staticmethod
    def construct_empty_predicate(input_string, negation):
        predicate_obj = Predicate(input_string, tuple(), negation)
        return predicate_obj

    def construct_predicate(self, input_string):
        if not input_string:
            raise ValueError("Predicate %s is not in required format".format(input_string))

        negation = False
        if input_string[0] == "!":
            negation = True
            input_string = input_string[1:]

        if "(" in input_string:
            predicate_obj = self.construct_non_empty_predicate(input_string, negation)
        else:
            predicate_obj = self.construct_empty_predicate(input_string, negation)

        return predicate_obj

    def construct_clause(self, input_string):
        predicate_strings = input_string.split()
        predicate_strings = [x.strip() for x in predicate_strings]
        all_predicates = []
        for predicate_string in predicate_strings:
            predicate_obj = self.construct_predicate(predicate_string)
            all_predicates.append(predicate_obj)

        return Clause(frozenset(all_predicates))

    def process_inputs(self):
        all_lines = self.read_all_lines(self.filename)
        self.predicate_names = set(all_lines[0].split()[1:])
        self.variable_names = set(all_lines[1].split()[1:])
        self.constant_names = set(all_lines[2].split()[1:])
        self.function_names = set(all_lines[3].split()[1:])

        for line in all_lines[5:]:
            clause = self.construct_clause(line)
            self.clauses.add(clause)
