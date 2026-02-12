from polymod import ConvolutionPoly
from math import gcd
import random


class NTRU:
    def __init__(self, N=8, p=3, q=41, d=2):
        self.N = N
        self.p = p
        self.q = q
        self.d = d

        if gcd(self.N, self.q) != 1 or gcd(self.p, self.q) != 1:
            print('Parameter error: we must have:\n     gcd(p, q) = gcd(N, q) = 1.')
            exit()
        
        if self.q <= (6*self.d+1) * self.p:
            print('Parameter warning:\n     q <= (6d+1)p.\nWill proceed.')


    def createKeys(self, f_coeffs, g_coeffs):
        if f_coeffs.count(1) != self.d+1 or f_coeffs.count(-1) != self.d:
            print(f'Parameter error:\n     f has an incorrect number of 1 and -1 coefficients: should be {self.d+1} 1s and {self.d} -1s, is {f_coeffs.coeffs.count(1)} 1s and {f_coeffs.coeffs.count(-1)} -1s.')
            exit()
        
        if g_coeffs.count(1) != self.d or g_coeffs.count(-1) != self.d:
            print(f'Parameter error:\n     g has an incorrect number of 1 and -1 coefficients: should be {self.d} 1s and {self.d} -1s, is {g_coeffs.count(1)} 1s and {g_coeffs.count(-1)} -1s.')
            exit()

        self.f = ConvolutionPoly(rank=self.N, modulus=self.p, coeffs=f_coeffs)
        self.g = ConvolutionPoly(rank=self.N, modulus=self.q, coeffs=g_coeffs)

        try:
            self.f.inverse()
            self.f.set_modulus(self.q)
            F_q = self.f.inverse()
        except:
            print(f'Parameter error:\n     f is uninvertible in q or p.')
            exit()

        self.h = F_q * self.g
    
    def getRandomPolynomial(self):
        coefs = [1 for _ in range(self.d)] + [-1 for _ in range(self.d)] + [0 for _ in range(self.N - 2*self.d)]
        random.shuffle(coefs)
        return coefs

    def encryptMessage(self, m_coeffs):
        m = ConvolutionPoly(rank=self.N, modulus=self.q, coeffs=m_coeffs)
        r = ConvolutionPoly(rank=self.N, modulus=self.q, coeffs=self.getRandomPolynomial())
        self.h.set_modulus(self.q)

        e = (r * self.p) * self.h + m
        return e

    def decryptMessage(self, e):
        self.f.set_modulus(self.q)
        e.set_modulus(self.q)
        a = self.f * e

        self.f.set_modulus(self.p)
        a.set_modulus(self.p)
        m = self.f.inverse() * a
        return m


def main():
    ntru = NTRU()
    f_coeffs = [-1, 0, 1, 1, -1, 0, 1]
    g_coeffs = [0, -1, -1, 0, 1, 0, 1]
    ntru.createKeys(f_coeffs, g_coeffs)

    m_coeffs = [1, -1, 1, 1, 0, -1, 0]
    e = ntru.encryptMessage(m_coeffs)
    m = ntru.decryptMessage(e)

    print(m_coeffs)
    print(m.coeffs)


if __name__ == '__main__':
    main()
