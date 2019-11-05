import random
from collections import namedtuple
import time


def generate(deg):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 39, 83, 89,
              97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191,
              193, 197, 199]

    q = random.choice(primes)
    while True:
        even = random.randint(2 ** 1, 2 ** 2)
        if (even % 2) != 0:
            even += 1

        p = q * even + 1
        cond1 = (p < pow((2*q + 1), 2))
        cond2 = (pow(2, q * even, p) == 1)
        cond3 = (pow(2, even, p) != 1)
        cond4 = ((p > pow(2, deg - 1)) and (p < pow(2, deg)))
        if cond1 and cond2 and cond3 and cond4:
            break
        if p < pow(2, deg - 1):
            q = p
        else:
            q = random.choice(primes)

    return p


def fermat_test(n, k):
    for i in range(0, k):
        a = random.randint(2, n - 1)
        if pow(a, n - 1, n) != 1:
            return 0
    return (1 - 2 ** -k) * 100


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


def get_primes(start, stop):
    if start >= stop:
        return []

    primes = [2]

    for n in range(3, stop + 1, 2):
        for p in primes:
            if n % p == 0:
                break
        else:
            primes.append(n)

    while primes and primes[0] < start:
        del primes[0]

    return primes


def are_relatively_prime(a, b):
    for n in range(2, min(a, b) + 1):
        if a % n == b % n == 0:
            return False
    return True


def make_key_pair(p, q):
    stop = (p - 1) * (q - 1)
    for e in range(3, stop, 2):
        if are_relatively_prime(e, stop):
            break
    else:
        raise AssertionError("cannot find 'e' with p={!r} "
                             "and q={!r}".format(p, q))

    d = invmod(e, stop)
    return PublicKey(p * q, e), PrivateKey(p * q, d)


class PublicKey(namedtuple('PublicKey', 'n e')):
    __slots__ = ()

    def encrypt(self, x):
        return pow(x, self.e, self.n)


class PrivateKey(namedtuple('PrivateKey', 'n d')):
    __slots__ = ()

    def decrypt(self, x):
        return pow(x, self.d, self.n)


if __name__ == '__main__':
    r = 10                     # кол-во раундов для теста Ферма
    start_gen = time.time()
    deg = 512
    p = generate(deg)
    q = generate(deg)
    print("Время генерации p и q: ", time.time() - start_gen)
    print("Порядок сгенерированных чисел (2^deg) при deg: ", deg)
    print("p:\n", p)
    print('\t\tТест Ферма p:', fermat_test(p, r), '%')
    print("q:\n", q)
    print('\t\tТест Ферма q:', fermat_test(q, r), '%')

    # Тесты на простоту приведены только как доказательство, это рабочий алгоритм генерации больших чисел,
    # реализованный еще в первой лабораторной.

    start_crypt = time.time()
    public, private = make_key_pair(p, q)

    x = random.randrange(public.n - 2)
    y = public.encrypt(x)
    print("Время генерации открытого и закрытого ключа вместе с применением зашифрования и расшифрования: ",
          time.time() - start_crypt)
    print("x:\n", x)
    print("y = Ee(x):\n", y)
    print("Dd(Ee(x)):\n", private.decrypt(y))
    if(x == private.decrypt(y)):
        print("x = Dd(Ee(x)) = Ee(Dd(x))")


