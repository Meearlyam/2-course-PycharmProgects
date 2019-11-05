import numpy as np
from numpy import linalg as la
import random as rnd
from math import gcd, pow

table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .,!?'


def Hill_cipher(text):
    fkey = open('hillkey.txt', 'w')
    fres = open('hillres.txt', 'w')
    ln = len(text)
    while True:
        K = np.random.randint(1, 3, (3, 3))
        if la.det(K) != 0 and int(la.det(la.inv(K))) and gcd(int(la.det(K)), 31) == 1 \
                and hasInv(la.det(K), 31) and gcd(int(la.det(invMatrix(K))), 31) == 1:
            if la.det(invMatrix(K)) != 0:
                break

    key = ''
    for i in range(3):
        for j in range(3):
            key += str(K[i][j]) + ' '
        key += '\n'
    fkey.write(key)

    if ln % 3 != 0:
        if ln % 3 == 1:
            text += '  '
        if ln % 3 == 2:
            text += ' '
    ln = len(text)

    result = ''
    k = 0
    while True:
        if k == ln:
            break
        P = []
        for i in range(3):
            P.append(table.index(text[k + i].upper()))
        C = list(K.dot(P) % 31)
        for i in range(3):
            result += str(table[C[i]])
        k += 3

    print('Ciphertext:\n', result)
    fres.write(result)
    fkey.close()
    fres.close()


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def invmod(a, m):
    g, x, y = egcd(a, m)
    if hasInv(a, m):
        return x % m


def hasInv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return False
    else:
        return True


def invMatrix(A):
    RK = np.ones((3, 3))
    # RK[0][0] = K[2][2]
    # RK[1][1] = K[1][1]
    # RK[2][2] = K[0][0]
    # for i in range(3):
    #     for j in range(3):
    #         RK[i][j] = -K[i][j]
    m_shape = A.shape[0] - 1
    for i in range(3):
        for j in range(3):
            M = np.eye(m_shape, dtype=int)
            M[:i, :j] = A[:i, :j]
            M[:i, j:] = A[:i, j+1:]
            M[i:, :j] = A[i+1:, :j]
            M[i:, j:] = A[i+1:, j+1:]
            print(M)
            RK[i][j] = pow(-1, i+j) * la.det(M) % 31
    RK *= invmod(la.det(A), 31)
    RK = RK.transpose()
    return RK


def decrypt_Hill():
    fkey = open('hillkey.txt', 'r')
    ftext = open('hillres.txt', 'r')
    text = ftext.read()
    ln = len(text)
    decrypt = ''
    K = []
    RK = [0] * 3
    for line in fkey:
        K.append([int(x) for x in line.split()])
    # print(K)

    K = np.matrix(K, int)

    RK = invMatrix(K)
    print(RK)
    # RK = (1 / la.det(la.inv(K)) * la.inv(K)) % 31

    k = 0
    while True:
        if k == ln:
            break
        C = []
        for i in range(3):
            C.append(table.index(text[k + i]))
        P = np.array(RK.dot(C) % 31)
        # print(P)

        for i in range(3):
            t = int(round(P[i]))
            if t >= 31:
                t -= 1
            decrypt += str(table[t])
        k += 3
    print('Decryption:\n', decrypt)
    fkey.close()
    ftext.close()


def shift_cipher(text):
    fkey = open('shiftkey.txt', 'w')
    fres = open('shiftresult.txt', 'w')
    ln = len(text)
    key = rnd.sample(range(ln), ln)
    mkey = ''
    for i in range(ln):
        mkey += str(key[i]) + ' '
    fkey.write(mkey)
    result = ''
    for i in key:
        result += text[i]
    fres.write(result)
    print('Ciphertext:\n', result)
    fkey.close()
    fres.close()


def decrypt_shift():
    fkey = open('shiftkey.txt', 'r')
    ftext = open('shiftresult.txt', 'r')
    text = ftext.read()
    ln = len(text)
    decrypt = ''
    file_keys = []
    for line in fkey:
        file_keys.append([int(x) for x in line.split()])

    for i in range(ln):
        k = 0
        for j in range(ln):
            if(file_keys[0][j] == i):
                k = j

        decrypt += text[k]
    print('Decryption:\n', decrypt)
    fkey.close()
    ftext.close()


def Vigener_cipher(text):
    fkey = open('vigenerkey.txt', 'w')
    fres = open('vigenerres.txt', 'w')
    ln = len(text)
    print('Enter keyword for Vigener cipher:')
    key = input().upper()
    result = ''
    tkey = ''
    kln = len(key)
    for i in range(ln):
        tkey += key[i % kln]
    fkey.write(tkey)
    for i in range(ln):
        m = table.index(text[i].upper())
        k = table.index(tkey[i].upper())
        c = (k + m) % len(table)
        result += table[c]
    print('Ciphertext:\n', result)
    fres.write(result)
    fkey.close()
    fres.close()


def decrypt_Vigener():
    fkey = open('vigenerkey.txt', 'r')
    ftext = open('vigenerres.txt', 'r')
    text = ftext.read()
    key = fkey.read()
    ln = len(text)

    decrypt = ''
    for i in range(ln):
        c = table.index(text[i])
        k = table.index(key[i])
        m = (c - k) % len(table)
        decrypt += table[m]
    print('Decryption:\n', decrypt)
    fkey.close()
    ftext.close()


while True:
    ftext = open('text.txt', 'r')
    text = ftext.read()
    print('Choose a cipher for encrypting plaintext:')
    print('\t(1) Shift cipher')
    print('\t(2) Vigener cipher')
    print('\t(3) Hill cipher')
    print('\t(4) Decrypt shift cipher')
    print('\t(5) Decrypt Vigener cipher')
    print('\t(6) Decrypt Hill cipher')
    print('\t(7) Quit')
    choice = int(input())
    result = ''
    print('Plaintext:\n', text)
    if choice == 7:
        print('Application finished.')
        break
    elif choice == 1:
        shift_cipher(text)
    elif choice == 2:
        Vigener_cipher(text)
    elif choice == 3:
        Hill_cipher(text)
    elif choice == 4:
        decrypt_shift()
    elif choice == 5:
        decrypt_Vigener()
    elif choice == 6:
        decrypt_Hill()
    else:
        print('Invalid input!')
    input()
