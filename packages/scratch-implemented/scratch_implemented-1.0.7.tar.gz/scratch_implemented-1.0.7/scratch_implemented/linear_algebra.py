class Linear_Algebra:

    @staticmethod
    def is_square(M):
        return len(M) == len(M[0])

    @staticmethod
    def multiply(A, B):  # https://www.youtube.com/watch?v=sZxjuT1kUd0
        return "Error A cols != B rows" if len(B) != len(A[0]) else [[sum(r_i * c_i for r_i, c_i in zip(row, col)) for col in zip(*B)] for row in A]

    @staticmethod
    def transpose(M):
        # return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
        return list(map(list, zip(*M)))

    @staticmethod
    def get_I(M):
        return "Error A cols != B rows" if len(M) != len(M[0]) else [[1 if i == j else 0 for j in range((len(M)))] for i in range((len(M)))]

    @staticmethod
    def is_invertable(M, M_i):
        return True if Linear_Algebra.multiply(M, M_i) == Linear_Algebra.multiply(M_i, M) == Linear_Algebra.get_I(M) else False

    @staticmethod
    def make_square(M):
        return Linear_Algebra.multiply(Linear_Algebra.transpose(M), M)

    # ======================================================= TO_DO =========================================================
    # https://www.mathsisfun.com/algebra/matrix-inverse-minors-cofactors-adjugate.html

    @staticmethod
    def get_determinant(M):
        if len(M) == 2:
            return M[0][0]*M[1][1]-M[0][1]*M[1][0]

        determinant = 0
        for c in range(len(M)):
            determinant += ((-1)**c)*M[0][c] * Linear_Algebra.get_determinant(Linear_Algebra.get_minor(M, 0, c))  # noqa
        return determinant

    @staticmethod
    def get_minor(M, i, j):
        return [row[:j] + row[j+1:] for row in (M[:i]+M[i+1:])]

    @staticmethod
    def inverse(M):  # https://www.youtube.com/watch?v=P3l7gGeHXC8
        determinant = Linear_Algebra.get_determinant(M)

        if determinant != 0 and Linear_Algebra.is_square(M):
            if len(M) == 2:
                return [[M[1][1]/determinant, -1*M[0][1]/determinant],
                        [-1*M[1][0]/determinant, M[0][0]/determinant]]

            cofactors = []
            for r in range(len(M)):
                cofactorRow = []
                for c in range(len(M)):
                    minor = Linear_Algebra.get_minor(M, r, c)
                    cofactorRow.append(((-1)**(r+c)) * Linear_Algebra.get_determinant(minor))  # noqa
                cofactors.append(cofactorRow)
            cofactors = Linear_Algebra.transpose(cofactors)
            for r in range(len(cofactors)):
                for c in range(len(cofactors)):
                    cofactors[r][c] = cofactors[r][c]/determinant
            return cofactors

        return "Error!Matrix is not square or it`s determinant = 0"
