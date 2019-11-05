import math
import random as rnd
import hashlib


class Elgamal:
    def __init__(self):
        self.hasher = hashlib.sha256()
        while True:
            self.q = rnd.getrandbits(192)
            if not self.millerTest(self.q):
                continue
            for k in range(2, 5):
                self.p = self.q * k + 1
                if self.millerTest(self.p):
                    break
            else:
                continue
            break
        # self.p = 0x3ade02996c6a146aa1c4fe016c295cfaeea6b7cbe234c4e41489e76484faf7d01ba7e8bb5ae18754e5c9bbacf6b9bff67467739eba900874802b0014cb6f4ec8e7fd1ca5adc081b10728dc64b734cead23637207e79e5fd2301f6739bddf8853a7cabb9b69c6661412aaf580f566f5708554bea53a398330c842a70208e181541eef5f087c8a480a685360698028877eed8cda8bb680d2a54d5d505417862ca6b48b947
        # self.q = 0x62a9bbf614e02a4e768924637817eae83c1ef3e65f434506
        while True:
            alpha = rnd.randint(2, self.p - 1)
            self.g = pow(alpha, (self.p - 1) // self.q, self.p)
            if self.g != 1:
                break
        self.g = 0x17712ab8487b90fb86152f8437edc213c97e6045669cacd16819992f7afc0d22e7c1ad32c24d7582d7ba1de2135fe8aedaea725a6be616c3f75a0f507285ae5abe131c58150ebf5cf94c4922cbbe2c092d29f82f1e16b55aab85cb45cd9344cf57d4e1611480d0121774703426660ee741112de263f0b2ac542ed7239251e1cb013b3ede4e19120468e1c64755d5050a397979a556fda82bfc9d21949599842bed436dc

        # self.x = rnd.randint(2, self.p - 1)
        self.x = 0x2c42742056274ad77ab4e0d79f611cb5f4ae02b30c09f55c
        # self.y = pow(self.g, self.x, self.p)
        self.y = 0x3ab9d2301c777c4f6c5092eb3f897b342195db121184c37f9862456b92adc4224a4acb2979c8252ee1edb6ca28b0c0c729701e393b8cf64da58e11417a22f4986e9cac7cae84d6c528cd87375dced0e46d25048a294d34560d108395f7f67501702bf109d707104e5dfc6bad6b4bc00edd5c61058a484751a3492da52ae31d09eac2d4054446debb1ba49c9177af203a49305e14b3fac9be60464e7b2e168c79b556e27

    def millerTest(self, num):
        s = 0
        d = num - 1
        while d & 1 == 0:
            s += 1
            d >>= 1

        for i in range(0, 48):
            a = rnd.randint(2, num - 1)
            a = pow(a, d, num)
            if a == 1 or a == num - 1:
                continue
            for i in range(1, s):
                a = pow(a, 2, num)
                if a == num - 1:
                    break
            else:
                return False
            return True

    def signature(self, msg):
        k = rnd.randint(1, self.q - 1)
        # k = 0x103e6c3843acd6f24cc6c9b1c213b45c3395d01a6da2d8f2
        r = pow(self.g, k, self.p)
        # r = 0x3a30f13f061344d27551cacb61081119737dc41b28630cb4c3bd1da427ee0b57231749a318505de7a688ff81459c7dff1400cc57670a44d910f80f41fe0ed40f5ae4b545ecca5a0dbed80815bda76ce85ba6c91642b86a9dc0065ca7054a9bb6918ca2d4bdc6a14b137ff8bc52ece958d454de309330d4eb95451c7fd303c699ca03105b3b3ba1f2d92ada6928405b8432608e98964d954ef9d0420d3ea0232c5b0082
        print('  ===== r ===== :\n', hex(r))
        # self.hasher.update(msg)
        #
        h = msg
        kinv = pow(k, self.q - 2, self.q)
        s = kinv * (h - self.x * r) % self.q
        # s = 0x5c76118758ed4d3ef2801bf5e78459f0f01ae57e42f81d2
        print('  ===== s ===== :\n', hex(s))
        return (r, s)

    def verifySignature(self, msg, rs):
        r, s = rs
        if not (0 < r < self.p and 0 < s < self.p - 1):
            return False
        # h = int(self.hasher.hexdigest(), 16)
        h = msg
        print('(y^r * r^s)(mod p): ')
        print(pow(self.y, r, self.p) * pow(r, s, self.p) % self.p)
        print('g^h(mod p):')
        print(pow(self.g, h, self.p))
        return pow(self.y, r, self.p) * pow(r, s, self.p) % self.p == pow(self.g, h, self.p)


if __name__ == '__main__':
    message = 0x43e7a9163484db603b6f0e49d21e34a6365055eb7bcb7805
    elgamal = Elgamal()
    rs = elgamal.signature(message)
    if elgamal.verifySignature(message, rs):
        print('\nThe given digital signature corresponds to original.')
