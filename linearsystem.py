from fractions import Fraction
import pyperclip
import sys
import numpy


class matrix(object):
    def __init__(self, arr):
        self.arr = arr

    def get_row(self, row):
        return self.arr[row]

    def get_col(self, col):
        return [row[col] for row in self.arr]

    def swap(self, first, second):
        self.arr[first], self.arr[second] = self.arr[second], self.arr[first]

    def scale(self, row, factor):
        self.arr[row] = [x * factor for x in self.arr[row]]

    def add(self, target, source):
        new_arr = self.arr[:]
        new_arr[target] = [
            self.arr[target][i] + self.arr[source][i]
            for i in range(len(self.arr[0]))
        ]
        return matrix(new_arr)

    def add_row(self, target, source, scale=1):
        self.arr[target] = [
            self.arr[target][i] + scale * self.arr[source][i]
            for i in range(len(self.arr[target]))
        ]

    def print_tex(self):
        print(self.tex_str())

    def reduced(self):
        copy = matrix(self.arr[:])
        return copy.reduce()

    def reduce0(self, x, y):
        if self.arr[x][y] == 0:
            return
        elif self.arr[x][y] != 1:
            self.scale(x, Fraction(1, self.arr[x][y]))
        for j in range(x + 1, len(self.arr)):
            self.add_row(j, x, (-1) * self.arr[j][x])

    def reduce1(self, x, y):
        if y > 0 and self.arr[x][y - 1] != 0:
            self.reduce1(x, y - 1)
            return
        if self.arr[x][y] != 1:
            self.reduce0(x, y)
        for i in range(x):
            self.add_row(i, x, (-1) * self.arr[i][y])

    def reduce(self, v=False):
        self.rreduce0(0, 0, v)
        self.rreduce1(len(self.arr) - 1, len(self.arr[0]) - 1)

    def rreduce0(self, row, col, v=False):
        if row >= len(self.arr) or col >= len(self.arr[0]):
            return
        if self.arr[row][col] == 0:
            for i in range(row, len(self.arr)):
                if self.arr[i][col] != 0:
                    self.swap(row, i)
                    if v:
                        self.print_tex()
                    self.rreduce0(row, col, v)
                    return
            self.rreduce0(row, col + 1, v)
        self.reduce0(row, col)
        if v:
            self.print_tex()
        self.rreduce0(row + 1, col + 1, v)

    def rreduce1(self, row, col, v=False):
        if row < 0 or col < 0:
            return
        elif self.arr[row][col] == 0:
            self.rreduce1(row - 1, col, v)
        elif row > 0 and col > 0:
            self.reduce1(row, col)
            if v:
                self.print_tex()
            self.rreduce1(row - 1, col - 1, v)

    def tex_str(self):
        result = "\\begin{bmatrix}\n"
        for col in self.arr:
            result += "\t"
            for i, v in enumerate(col):
                if i != 0:
                    result += " &"
                result += str(v)
                if i == len(col) - 1:
                    result += "\\\\\n"
        result += "\\end{bmatrix}"
        return result

    def transposed(self):
        new_arr = []
        for col in range(len(self.arr[0])):
            new_arr.append([self.arr[i][col] for i, _ in enumerate(self.arr)])
        return matrix(new_arr)

    def transpose(self):
        self.arr = self.transposed()

    def to_clipboard(self):
        pyperclip.copy(self.tex_str())

    def cat(self, other):
        return matrix(
            [self.arr[i] + other.arr[i] for i in range(len(self.arr))]
        )

    def is_full_rank_rref(self):
        for i, row in enumerate(self.arr):
            for j, col in enumerate(row):
                if (j < i and col != 0) or (j == i and col != 1):
                    return False
        return True

    def __str__(self):
        res = ""
        for row in self.arr:
            res += "["
            res += " ".join(list(map(str, row)))
            res += "]\n"
        return res

    def __mul__(self, other):
        return matrix(numpy.matmul(self.arr, other.arr).tolist())


def regress(coords):
    A = matrix([[1, coords[x][0]] for x in range(len(coords))])
    b = matrix([[coords[y][1]] for y in range(len(coords))])
    AtA = A.transposed() * A
    Atb = A.transposed() * b
    xhat = AtA.cat(Atb)
    xhat.reduce()
    if xhat.is_full_rank_rref():
        slope = xhat.arr[1][len(xhat.arr[0]) - 1]
        intercept = xhat.arr[0][len(xhat.arr[0]) - 1]
        return f"y = {slope}x + {intercept}"
    return "something went wrong..." + str(xhat)


def dot(l, r):
    var = sum(l[i] * r[i] for i in range(len(l)))
    return var


def from_bmatrix(s):
    s = s.replace("\n", "")
    lines = s.split("\\")
    arr = []
    for line in lines:
        if line != "":
            arr.append(list(map(int, line.split(" &"))))
    return matrix(arr)


def from_clipboard():
    s = pyperclip.paste()
    return from_bmatrix(s)


if __name__ == "__main__":
    print(regress([(1, 4), (2, 10), (3, 3)]))
