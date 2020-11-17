import unittest
import linearsystem


class TestLinearSystem(unittest.TestCase):
    def test_can_make_new_matrix(self):
        m = linearsystem.matrix([[0], [0]])

    def test_get_row(self):
        m = linearsystem.matrix([[0], [0]])
        self.assertEqual([0], m.get_row(0))

    def test_get_col(self):
        m = linearsystem.matrix([[0, 2], [1, 3]])
        self.assertEqual([0, 1], m.get_col(0))

    def test_swap(self):
        m = linearsystem.matrix([[0, 2], [1, 3]])
        m.swap(0, 1)
        self.assertEqual([[1, 3], [0, 2]], m.arr)

    def test_add_whole_numbers(self):
        m = linearsystem.matrix([[1, 2], [3, 4]])
        m = m.add(0, 1)
        self.assertEqual([[4, 6], [3, 4]], m.arr)

    def test_to_string(self):
        m = linearsystem.matrix([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
        self.assertEqual([[1, 2, 3], [2, 3, 4], [3, 4, 5]], m.arr)

    def test_dot0(self):
        self.assertEqual(11, linearsystem.dot([2, 1], [4, 3]))

    def test_reduceI2(self):
        m = linearsystem.matrix([[3, 0], [1, 2]])
        m.reduce()
        self.assertEqual("[1 0]\n[0 1]\n", str(m))

    def test_reduce3by2(self):
        m = linearsystem.matrix([[1, 0], [2, 1], [3, 2]])
        m.reduce()
        self.assertEqual("[1 0]\n[0 1]\n[0 0]\n", str(m))

    def test_reduce4by4(self):
        m = linearsystem.matrix(
            [[1, 0, 0, 1], [2, 1, 1, 2], [3, 2, 2, 3], [4, 3, 3, 4]]
        )
        m.reduce()
        self.assertEqual("[1 0 0 1]\n[0 1 1 0]\n[0 0 0 0]\n[0 0 0 0]\n", str(m))

    def test_reduce_depedent(self):
        m = linearsystem.matrix(
            [
                [0, 0, 1, 3],
                [0, 0, 9, 4],
                [0, 0, 0, 5],
                [0, 0, 0, 0],
            ]
        )
        m.reduce()
        self.assertEqual("[0 0 0 0]\n[0 0 1 0]\n[0 0 0 1]\n[0 0 0 0]\n", str(m))

    def test_parse_row_vec_bmatrix(self):
        s = "2 &2 &2\\\\\n"
        self.assertEqual([[2, 2, 2]], linearsystem.from_bmatrix(s).arr)

    def test_parse_two_rows(self):
        s = "2 &2 &2\\\\\n" + "1 &1 &1\\\\\n"
        self.assertEqual(
            [[2, 2, 2], [1, 1, 1]], linearsystem.from_bmatrix(s).arr
        )

    #  def test_mult_2x2(self):
    #  m1 = linearsystem.matrix([[1, 0], [0, 1]])
    #  m2 = linearsystem.matrix([[1, 1], [0, 1]])
    #  self.assertEqual([[1, 1], [0, 1]], (m1 * m2).arr)

    def test_broken_example_from_lec(self):
        m = linearsystem.matrix(
            [[1, -3, -4, 3], [0, -6, -18, 15], [0, -2, -6, 5]]
        )
        m.reduce()
        want = (
            "\\begin{bmatrix}\n"
            + "\t1 &0 &5 &-9/2\\\\\n"
            + "\t0 &1 &3 &-5/2\\\\\n"
            + "\t0 &0 &0 &0\\\\\n"
            + "\\end{bmatrix}"
        )
        self.assertEqual(want, m.tex_str())

    def test_transpose_single(self):
        m = linearsystem.matrix([[1]])
        m.transpose()
        self.assertEqual([[1]], m.arr)

    def test_transpose_row(self):
        m = linearsystem.matrix([[1, 2, 3]])
        m.transpose()
        self.assertEqual([[1], [2], [3]], m.arr)

    def test_transpose_col(self):
        m = linearsystem.matrix([[1], [2], [3]])
        m.transpose()
        self.assertEqual([[1, 2, 3]], m.arr)

    def test_transpose_3x2(self):
        m = linearsystem.matrix([[1, 2], [2, 3], [3, 4]])
        m.transpose()
        self.assertEqual([[1, 2, 3], [2, 3, 4]], m.arr)

    def test_transpose_3x4(self):
        m = linearsystem.matrix([[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]])
        m.transpose()
        self.assertEqual([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]], m.arr)


if __name__ == "__main__":
    unittest.main()
