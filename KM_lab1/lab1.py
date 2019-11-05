import random as rnd
import os
from math import gcd


def generate(deg):
	primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 39, 83, 89,
			  97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191,
			  193, 197, 199]

	q = rnd.choice(primes)
	while True:
		even = rnd.randint(2 ** 1, 2 ** 2)
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
			q = rnd.choice(primes)

	return p


def jacobi_symbol(a, b):
	if gcd(a, b) != 1:
		return 0
	r = 1
	if a < 0:
		a = -a
		if b % 4 == 3:
			r = -r
	while a != 0:
		t = 0
		while a % 2 == 0:
			t += 1
			a //= 2
		if t % 2 == 1:
			if b % 8 == 3 or b % 8 == 5:
				r = -r
		if a % 4 == b % 4 == 3:
			r = -r
		c = a
		a = b % c
		b = c
	return r


def fermat_test(n, k):
	for i in range(0, k):
		a = rnd.randint(2, n - 1)
		if pow(a, n - 1, n) != 1:
			return 0
	return (1 - 2 ** -k) * 100


def miller_rabin_test(n, k):
	s = 0
	t = n - 1
	while t % 2 == 0:
		s += 1
		t //= 2
	for i in range(0, k):
		a = rnd.randint(2, n - 2)
		x = pow(a, t, n)
		if x == 1 or x == n - 1:
			continue
		flag = True
		for j in range(0, s - 1):
			x = pow(x, 2, n)
			if x == 1:
				return 0
			if x == n - 1:
				flag = False
				break;
		if (flag):
			return 0
	return (1 - 4 ** -k) * 100


def solovey_strassen_test(n, k):
	for i in range(0, k):
		a = rnd.randint(2, n - 1)
		if gcd(a, n) > 1:
			return 0
		symbol = jacobi_symbol(a, n);
		if symbol == 0:
			return 0
		if pow(a, (n - 1) // 2, n) != symbol % n:
			return 0
	return (1 - 2 ** -k) * 100


os.system('cls')
print('Введите число сгенерированных чисел:')
count = int(input())
print('Введите число раундов для каждого числа:')
k = int(input())
print()
print('Введите порядок для генерации чисел:')
deg = int(input())

for i in range(1, count + 1):

	n = 115
	print('Число №', i, ':\n\t', n)

	print('\tВероятности простоты:')
	print('\t\tТест Ферма:', fermat_test(n, k), '%')
	print('\t\tТест Миллера-Рабина:', miller_rabin_test(n, k), '%')
	print('\t\tТест Соловея-Штрассена:', solovey_strassen_test(n, k), '%')
	input()
print('Генерация чисел завершена')
input()
os.system('cls')
