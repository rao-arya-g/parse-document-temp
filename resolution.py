import copy
from class_definitions import Clause, Variable, Constant, Function, Predicate


def check_equality_of_predicates(p_1, p_2):

    if p_1 == p_2:
        return False, None

    if p_1.name != p_2.name or p_1.negation == p_2.negation:
        return False, None

    substitution_dict = {}
    flag = unification(p_1.arguments, p_2.arguments, substitution_dict)

    if not flag:
        return False, {}
    else:
        return True, substitution_dict


def check_two_clauses_for_resolution(clause_1, clause_2):
    predicates_1 = clause_1.entries
    predicates_2 = clause_2.entries
    for p_1 in predicates_1:
        for p_2 in predicates_2:
            flag, substitution = check_equality_of_predicates(p_1, p_2)
            if flag:
                return resolve_two_clauses(clause_1, clause_2, p_1, p_2, substitution)

    return None


def resolve_two_clauses(clause_1, clause_2, predicate_1, predicate_2, substitution):
    all_predicates = list(clause_1.entries) + list(clause_2.entries)
    all_predicates.remove(predicate_1)
    all_predicates.remove(predicate_2)
    new_clause = Clause(frozenset(all_predicates))

    if len(substitution) > 0:
        return create_new_clause(new_clause, substitution)
    else:
        return new_clause


def generate_all_pair_of_clauses(clauses):
    all_clauses = list(clauses)
    list_of_pairs = []
    for i in range(len(all_clauses)):
        for j in range(len(all_clauses)):
            list_of_pairs.append((all_clauses[i], all_clauses[j]))

    return list_of_pairs


def pl_resolution(clauses):

    while True:
        pair_of_clauses = generate_all_pair_of_clauses(clauses)
        new_clauses = set()
        for pair in pair_of_clauses:

            resolved_clause = check_two_clauses_for_resolution(pair[0], pair[1])
            if resolved_clause:
                if len(resolved_clause.entries) == 0:
                    return False
                new_clauses.add(resolved_clause)

        if new_clauses.issubset(clauses):
            return True

        clauses.update(new_clauses)


def unification(e_1, e_2, substitution_dict):
    if e_1 == e_2:
        return True

    for (e1, e2) in zip(e_1, e_2):
        if isinstance(e1, Constant) and isinstance(e2, Constant):
            if e1 != e2:
                return False
            else:
                continue

        if isinstance(e1, Variable):
            if e1 in e_2:
                return False
            else:
                substitution_dict[e1] = e2
                continue

        if isinstance(e2, Variable):
            if e2 in e_1:
                return False
            else:
                substitution_dict[e2] = e1
                continue

        if isinstance(e1, Function) and isinstance(e2, Function):
            if e1.name != e2.name:
                return False
            else:
                function_substitution = {}
                unification(e1.terms, e2.terms, function_substitution)
                substitution_dict.update(function_substitution)
                continue
        else:
            return False

    return True


def create_new_function(function, substitution_dict):
    all_terms = []

    for entry in function.terms:
        if isinstance(entry, Variable):
            if entry in substitution_dict:
                all_terms.append(copy.copy(substitution_dict[entry]))
            else:
                all_terms.append(entry)

        elif isinstance(entry, Function):
            all_terms.append(create_new_function(entry, substitution_dict))
        else:
            all_terms.append(entry)

    return Function(function.name, frozenset(all_terms))


def create_new_predicate(predicate, substitution_dict):
    all_terms = []

    for entry in predicate.arguments:
        if isinstance(entry, Variable):
            if entry in substitution_dict:
                all_terms.append(copy.copy(substitution_dict[entry]))
            else:
                all_terms.append(entry)

        elif isinstance(entry, Function):
            all_terms.append(create_new_function(entry, substitution_dict))
        else:
            all_terms.append(entry)

    return Predicate(predicate.name, tuple(all_terms), predicate.negation)


def create_new_clause(clause, substitution_dict):
    all_predicates = []
    for predicate in clause.entries:
        all_predicates.append(create_new_predicate(predicate, substitution_dict))

    return Clause(frozenset(all_predicates))
