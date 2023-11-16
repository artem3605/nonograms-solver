import pycosat
from itertools import combinations


class Function:
    def __init__(self):
        self.clauses = []

    def add(self, clause):

        if isinstance(clause[0], int):
            self.clauses.append(clause)
        else:
            for i in clause:
                self.clauses.append(i)


class DNF(Function):
    pass


class CNF(Function):
    def bcp(self):
        unit_clauses = []
        for clause in self.clauses:
            if len(clause) == 1:
                unit_clauses.append(clause[0])
        for i in range(len(self.clauses)):
            if len(self.clauses[i]) == 1:
                continue
            for var in unit_clauses:
                if var in self.clauses[i]:
                    self.clauses[i].pop(self.clauses[i].index(var))
                if -var in self.clauses[i]:
                    self.clauses[i].pop(self.clauses[i].index(-var))


def N(x, y, n):
    return x * n + y + 1


def check(array, lim):
    p = 0
    ptr = 0
    for j in range(len(array)):
        if ptr == len(lim):
            break
        if array[j] == 1:
            p += 1
        else:
            if 0 < p != lim[ptr]:
                return False
            elif p > 0:
                p = 0
                ptr += 1
    if ptr == len(lim) or ptr + (lim[ptr] == p) == len(lim):
        return True
    return False


def to_cnf(dnf):
    global cnt
    cnf = CNF()
    start = cnt
    for clause in dnf.clauses:
        for var in clause:
            cnf.add([var, -cnt])
        cnt += 1
    cnf.add([var for var in range(start, cnt)])
    return cnf


m, n = map(int, input().split())
lims = []
cnt = n * m + 1
cnf = CNF()
for i in range(m):
    a = list(map(int, input().split()))
    row = [j for j in range(n)]
    dnf = DNF()
    lims.append(a)
    to_add = CNF()
    for j in combinations(row, sum(a)):
        to_check = [0] * n
        for z in j:
            to_check[z] = 1
        if check(to_check, a):
            dnf.add([(-1) ** (to_check[j] + 1) * N(i, j, n) for j in range(n)])
    to_add = to_cnf(dnf)
    to_add.bcp()

    cnf.add(to_add.clauses)

for i in range(n):
    a = list(map(int, input().split()))
    column = [j for j in range(m)]
    dnf = DNF()
    lims.append(a)
    for j in combinations(column, sum(a)):
        to_check = [0] * m
        for z in j:
            to_check[z] = 1
        if check(to_check, a):
            dnf.add([(-1) ** (to_check[j] + 1) * N(j, i, n) for j in range(m)])
    to_add = to_cnf(dnf)
    to_add.bcp()
    cnf.add(to_add.clauses)

solution = pycosat.solve(cnf.clauses)
to_check = [[0] * n for i in range(m)]
for i in range(n * m):
    if solution[i] < 0:
        to_check[i // n][i % n] = 0
    else:
        to_check[i // n][i % n] = 1

for row in to_check:
    print(*row)
