from polymod import ConvolutionPoly
from math import gcd
import random


class NTRU:
    def __init__(self):
        self.N = 7
        self.p = 3
        self.q = 41
        self.d = 2
        self.h = None

        if gcd(self.N, self.q) != 1 or gcd(self.p, self.q) != 1:
            print('Parameter error: we must have:\n     gcd(p, q) = gcd(N, q) = 1.')
            exit()
        
        if self.q <= (6*self.d+1) * self.p:
            print('Parameter warning:\n     q <= (6d+1)p.\nWill proceed.')

    def createKeys(self):
        self.f = ConvolutionPoly(rank=self.N, coeffs=[-1, 0, 1, 1, -1, 0, 1])
        self.g = ConvolutionPoly(rank=self.N, modulus=self.q, coeffs=[0, -1, -1, 0, 1, 0, 1])

        if self.f.coeffs.count(1) != self.d+1 or self.f.coeffs.count(-1) != self.d:
            print(f'Parameter error:\n     f has an incorrect number of 1 and -1 coefficients: should be {self.d+1} 1s and {self.d} -1s, is {f.coeffs.count(1)} 1s and {f.coeffs.count(-1)} -1s.')
            exit()
        
        if self.g.coeffs.count(1) != self.d or self.g.coeffs.count(-1) != self.d:
            print(f'Parameter error:\n     g has an incorrect number of 1 and -1 coefficients: should be {self.d} 1s and {self.d} -1s, is {g.coeffs.count(1)} 1s and {g.coeffs.count(-1)} -1s.')
            exit()
        
        self.f.set_modulus(self.q)
        self.F_q = self.f.inverse()

        self.f.set_modulus(self.p)
        self.F_p = self.f.inverse()

        self.h = self.F_q * self.g
        return self.h
    
    def getRandomPolynomial(self):
        coefs = [1 for _ in range(self.d)] + [-1 for _ in range(self.d)] + [0 for _ in range(self.N - 2*self.d)]
        random.shuffle(coefs)
        return coefs

    def encryptMessage(self, m_coeffs):
        m = ConvolutionPoly(self.N, self.q, m)
        r = self.getRandomPolynomial()

        m.set_modulus(self.q)
        self.h.set_modulus(self.q)
        e = ConvolutionPoly(self.N, self.q, self.p*r) * self.h + m
        
        return e

    def deryptMessage(self, e):
        m = ConvolutionPoly(self.N, self.q, m)
        # r = self.getRandomPolynomial()

        # m.set_modulus(self.q)
        # self.h.set_modulus(self.q)
        # e = ConvolutionPoly(self.N, self.q, self.p*r) * self.h + m
        
        # return e



def main():
    ntru = NTRU()
    h = ntru.createKeys()

    # m_coeffs = [1, 1, 2, 2, 0, 0, 1]
    # e = ntru.encryptMessage(m_coeffs)


    


if __name__ == '__main__':
    main()
