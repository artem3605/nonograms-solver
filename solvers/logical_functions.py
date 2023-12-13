class Function:
    def __init__(self):
        self.clauses = []

    def add(self, clause):
        if not clause:
            return
        if isinstance(clause[0], int):
            self.clauses.append(clause)
        else:
            for clause in clause:
                self.clauses.append(clause)


class DNF(Function):
    pass


class CNF(Function):
    pass


def to_cnf(dnf, cnt):
    """
    converts dnf to cnf
    :param dnf:
    :param cnt:
    :return: cnf
    """
    cnf = CNF()
    start = cnt
    for clause in dnf.clauses:
        for var in clause:
            cnf.add([var, -cnt])
        cnt += 1
    cnf.add([var for var in range(start, cnt)])
    return cnf, cnt
