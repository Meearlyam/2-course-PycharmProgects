import string
import re

table = string.ascii_uppercase


def Vigener_cipher(text):
    fkey = open('vigenerkey.txt', 'w')
    fres = open('vigenerres.txt', 'w')
    text = re.sub(' ', '', text)
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
    key_ln = 0
    indices = [0] * ln

    for i in range(1, ln):
        coindex = 0
        e_ind = 0
        for k in range(26):
            f = 0
            size = 0
            for j in range(i - 1, ln, i):
                if text[j] == table[k]:
                    f += 1
                size += 1
            if size != 0 and size != 1:
                coindex += f * (f - 1) / size / (size - 1)

        indices[i] = coindex

    for i in range(1, 13):
        isBetterKey = True
        for j in range(1, 13):
            if i == j:
                continue
            if 1.065 * indices[i] <= indices[j]:
                isBetterKey = False
                break
        if isBetterKey:
            key_ln = i
            break

    print('Key length: ', key_ln)
    lalphabet = [0] * key_ln

    key_word = [0] * key_ln
    res_word = ''

    for i in range(key_ln):
        alph_frec = [0] * 26
        max_f = -1
        max_i = 0

        for j in range(i, ln, key_ln):
            ind = table.index(text[j])
            alph_frec[ind] += 1
            if alph_frec[ind] >= max_f:
                max_i = ind
                max_f = alph_frec[ind]

        # 4 - index of E in table(alphabet) - the most frequent letter in english language
        key_word[i] = max_i - 4
        print('max_f: ', max_f, ' SHIFT: ', key_word[i])
        res_word += table[key_word[i] % 26]

    print(key_word)
    print('Obtained key: ', res_word)

    size = len(res_word)
    break_key = ''
    for i in range(ln):
        break_key += res_word[i % size]
    breaked = ''
    decrypt = ''
    for i in range(ln):
        c = table.index(text[i])
        k = table.index(key[i])
        m = (c - k) % len(table)
        decrypt += table[m]
        k = table.index(break_key[i])
        m = (c - k) % len(table)
        breaked += table[m]
    print('Decryption:\n', decrypt)
    print('Breaked:\n', breaked)
    fkey.close()
    ftext.close()


ftext = open('text.txt', 'r')
text = ftext.read()
text = text.upper()

result = ''
print('Plaintext:\n', text)
Vigener_cipher(text)
decrypt_Vigener()
ftext.close()
