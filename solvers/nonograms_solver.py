import pycosat
from itertools import combinations
from logical_functions import CNF, DNF, to_cnf


def num(x, y, columns):
    """
    cell -> number
    :param x:
    :param y:
    :param columns:
    :return: the number of the variable responsible for the cell [x, y]
    """
    return x * columns + y + 1


def check(array, lim):
    """
    Checks whether the string can be colored as an array considering the lim
    :param array:
    :param lim:
    :return: True if it can, otherwise False
    """
    p, ptr = 0, 0
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


file = open('../examples/nonogram.txt', 'r')
m, n = map(int, file.readline().split())
lims = []
cnt = n * m + 1
cnf = CNF()
for i in range(m):
    a = list(map(int, file.readline().split()))
    row = [j for j in range(n)]
    dnf = DNF()
    lims.append(a)
    to_add = CNF()
    for combination in combinations(row, sum(a)):
        to_check = [0] * n
        for el in combination:
            to_check[el] = 1
        if check(to_check, a):
            dnf.add([(-1) ** (to_check[j] + 1) * num(i, j, n) for j in range(n)])
    to_add, cnt = to_cnf(dnf, cnt)
    cnf.add(to_add.clauses)

for i in range(n):
    a = list(map(int, file.readline().split()))
    column = [j for j in range(m)]
    dnf = DNF()
    lims.append(a)
    for combination in combinations(column, sum(a)):
        to_check = [0] * m
        for el in combination:
            to_check[el] = 1
        if check(to_check, a):
            dnf.add([(-1) ** (to_check[j] + 1) * num(j, i, n) for j in range(m)])
    to_add, cnt = to_cnf(dnf, cnt)
    cnf.add(to_add.clauses)

file.close()

solution = pycosat.solve(cnf.clauses)
if isinstance(solution, str):
    print('No solutions')
else:
    to_check = [[''] * n for i in range(m)]
    for i in range(n * m):
        if solution[i] < 0:
            to_check[i // n][i % n] = ' '
        else:
            to_check[i // n][i % n] = '▇'

    for row in to_check:
        print(*row)
