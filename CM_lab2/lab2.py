import time

import numpy as np
from numpy import linalg as la
import random

import matplotlib.pyplot as plt


def generate_matrix_with_dimension(n):
    m = np.array([[random.randint(1, 10) for _ in range(n)] for _ in range(n)], dtype=float)
    return m


def generate_vector_with_dimension(n):
    v = np.array([random.randint(1, 10) for _ in range(n)], dtype=float)
    return v


def gauss_row_choice(A, b, with_output=True):
    n = len(b)
    x = np.empty(n)
    Ar = A.copy(n)
    br = b.copy(n)
    rn = 0
    R = np.eye(n, n)

    for k in range(n - 1):
        m1 = max(A[k, k:n])
        m2 = min(A[k, k:n])
        if abs(m2) > abs(m1):
            m1 = m2

        idx = np.where(A[k] == m1)[0][-1]
        if idx >= k:
            for t in range(n):
                temp = A[t, k]
                A[t, k] = A[t, idx]
                A[t, idx] = temp
                R[t][idx], R[t][k] = R[t][k], R[t][idx]
            rn += 1

        for i in range(k + 1, n):
            q = A[i, k] / A[k, k]
            for j in range(k, n):
                A[i][j] -= q * A[k][j]
            b[i] -= q * b[k]

    x[-1] = b[-1] / A[-1][-1]
    for i in range(n - 2, -1, -1):
        summ = 0.
        for j in range(i + 1, n):
            summ += A[i][j] * x[j]
        x[i] = (b[i] - summ) / A[i][i]

    rx = np.dot(R, x)

    if with_output:
        print('\n ====================== DECISION ======================== ')
        print('Calculated x:\n', rx)
        print('X from numpy decision:\n', la.solve(Ar, br))
        # print(Ar)
        print('\ndet(A) from linalg: ', la.det(A))
        detA = 1.
        for i in range(n):
            detA *= A[i, i]

        print('det(A): ', detA)


def condition_number(A):
    max = 0
    n = len(A)
    for i in range(n):
        sum = 0
        for j in range(n):
            sum += abs(A[i][j])
        if sum > max:
            max = sum

    AI = la.inv(A)
    maxI = 0
    for i in range(n):
        sum = 0
        for j in range(n):
            sum += abs(AI[i][j])
        if sum > maxI:
            maxI = sum
    return max * maxI   # ||A|| * ||A^-1||


def max_norm(v):
    n = len(v)
    max = 0
    for i in range(n):
        if max < abs(v[i]):
            max = abs(v[i])
    return max


def prove(A, b, cond_num):
    n = len(b)
    x = la.solve(A, b)
    bc = b.copy(n)
    a = 0
    for i in range(5):
        bc[0] += 0.001
        a += 0.001
        xc = la.solve(A, bc)
        left = max_norm(xc - x) / max_norm(x)
        right = max_norm(bc - b) / max_norm(b) * cond_num
        print('The introduced perturbation in the vector component: ', a)
        print('Check the inequality: ')
        print(left, ' <= ', right)
        print(f"\t-- {left <= right}")


def profile():
    x, y = [], []
    dim, exec_time = 1, 0
    # in seconds
    while exec_time < 3:
        A = generate_matrix_with_dimension(dim)
        b = generate_vector_with_dimension(dim)
        start = time.time()
        gauss_row_choice(A, b, with_output=False)
        exec_time = time.time() - start
        x.append(dim)
        y.append(exec_time)
        print(f'Calculated for dimension {dim}')
        dim += 10

    print(f'Dimension with working time more than minute: {x[-1]}')
    with plt.xkcd():
        plt.plot(x, y, 'r')
        plt.title('Performance')
        plt.xlabel('Dimension')
        plt.ylabel('Calculation time (sec)')
        plt.show()
    # TODO: Save in picture with 'savefig'


if __name__ == '__main__':
    A0 = np.array([[1., 3.],
                   [4., -1.]])

    b0 = np.array([2., -1.])

    A1 = np.array([[-1., -2., -3., 3., 5., -4., -5., 2.],
                   [-1., -2., 0., 5., 1., 4., -1., -5.],
                   [-2., -4., -3., 4., -1., -5., 3., 5.],
                   [-4., -8., -6., 12., 1., 3., 2., 0.],
                   [-8., -16., -12., 24., 6., -3., -4., 1.],
                   [-16., -32., -24., 48., 12., -5., 5., 3.],
                   [-32., -64., -48., 96., 24., -10., 0., 2.],
                   [-4., 3., -2., 1., -3., -1., -2., 2.]])

    b1 = np.array([-8., 2., -1., 4., -4., 7., 0., -2.])

    A2 = np.array([[1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
                   [1., 2., 4., 8., 16., 32., 64., 128., 256., 512., 1024.],
                   [1., 3., 9., 27., 81., 243., 729., 2187., 6561., 19683., 59049.],
                   [1., 4., 16., 64., 256., 1024., 4096., 16384., 65536., 262144., 1048576.],
                   [1., 5., 25., 125., 625., 3125., 15625., 78125., 390625., 1953125., 9765625.],
                   [1., 6., 36., 216., 1296., 7776., 46656., 279936., 1679616., 10077696., 60466176.],
                   [1., 7., 49., 343., 2401., 16807., 117649., 823543., 5764801., 40353607., 282475249.],
                   [1., 8., 64., 512., 4096., 32768., 262144., 2097152., 16777216., 134217728., 1073741824.],
                   [1., 9., 81., 729., 6561., 59049., 531441., 4782969., 43046721., 387420489., 3486784401.],
                   [1., 10., 100., 1000., 10000., 100000., 1000000., 10000000., 100000000., 1000000000., 10000000000.],
                   [1., 11., 121., 1331., 14641., 161051., 1771561., 19487171., 214358881., 2357947691., 25937424601.]])

    b2 = np.array(
        [11., 2047., 88573., 1398101., 12207031., 72559411., 329554457., 1227133513., 3922632451., 11111111111.,
         28531167061.])

    A3 = np.array([[5., -3., 5., 3., -4., 3., -3., 4.],
                   [5., -3., -2., 0., 1., 4., 1., -2.],
                   [10., -6., 3., 5., 4., -2., 5., 2.],
                   [20., -12., 6., 8., -1., -1., 0., 2.],
                   [40., -24., 12., 16., 0., 5., 3., -4.],
                   [80., -48., 24., 32., 0., 9., 1., 5.],
                   [160., -96., 48., 64., 0., 18., 7., 4.],
                   [4., -2., -3., -1., -2., 4., -3., 0.]])

    b3 = np.array([5., -1., 11., 2., 8., 23., 45., -7.])

    # Решения СЛАУ и сравнение с их решениями с помощью numpy:
    gauss_row_choice(A0, b0)  # тестовая матрица
    gauss_row_choice(A1, b1)
    gauss_row_choice(A2, b2)
    gauss_row_choice(A3, b3)

    # Вычисление числа обусловленности в максимум-норме оператора А2:
    # Подтверждение связи числа обусловленности и относительными погрешностями
    # начальных данных и решения:
    print('\n ============= CONDITION NUMBER OF 2nd MATRIX ============= ')
    cn = condition_number(A2)
    print('Condition number: ', cn)
    prove(A2, b2, cn)

    # Тест на время:
    profile()

