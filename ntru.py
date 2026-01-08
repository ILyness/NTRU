from polymod import ConvolutionPoly
from math import gcd



class NTRU:
    def __init__(self):
        self.N = 7
        self.p = 3
        self.q = 41
        self.d = 2

        if gcd(self.N, self.q) != 1 or gcd(self.p, self.q) != 1:
            print('Parameter error: we must have:\n     gcd(p, q) = gcd(N, q) = 1.')
            exit()
        
        if self.q <= (6*self.d+1) * self.p:
            print('Parameter warning:\n     q <= (6d+1)p.\nWill proceed.')

    def createKeys(self):
        # print(self.N)
        f = ConvolutionPoly(rank=self.N, modulus=self.p, coeffs=[-1, 0, 1, 1, -1, 0, 1, 1])
        # g = ConvolutionPoly(rank=self.N, modulus=self.p, coeffs=[0, -1, -1, 0, 1, 0, 1])

        print(f)
        print(f.coeffs)


def main():
    ntru = NTRU()
    ntru.createKeys()

if __name__ == '__main__':
    main()