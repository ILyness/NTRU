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
        f = ConvolutionPoly(rank=self.N, coeffs=[-1, 0, 1, 1, -1, 0, 1])
        g = ConvolutionPoly(rank=self.N, modulus=self.q, coeffs=[0, -1, -1, 0, 1, 0, 1])

        if f.coeffs.count(1) != self.d+1 or f.coeffs.count(-1) != self.d:
            print(f'Parameter error:\n     f has an incorrect number of 1 and -1 coefficients: should be {self.d+1} 1s and {self.d} -1s, is {f.coeffs.count(1)} 1s and {f.coeffs.count(-1)} -1s.')
            exit()
        
        if g.coeffs.count(1) != self.d or g.coeffs.count(-1) != self.d:
            print(f'Parameter error:\n     g has an incorrect number of 1 and -1 coefficients: should be {self.d} 1s and {self.d} -1s, is {g.coeffs.count(1)} 1s and {g.coeffs.count(-1)} -1s.')
            exit()
        
        
        f.set_modulus(self.q)
        inverse = f.inverse()
        print(inverse)
        print(f * inverse)
        exit()
        # f_p = f.set_modulus(self.p)

        F_q = ConvolutionPoly(rank=self.N, modulus=self.q, coeffs=[37, 2, 40, 21, 32, 26, 8]) # Should be inverse of f_q, hard-coded for now
        # F_p = ConvolutionPoly(rank=self.N, modulus=self.q, coeffs=[1, 1, 1, 1, 0, 1, 1]) # Should be inverse of f_p

        # Multiplying to check is unhappy bc "Values provided must match specified polynomial degree."
        # print(F_q * f) # checking bc should be id

        h = F_q * g # I got a segmentation fault, I am so sorry
        print(h)


def main():
    ntru = NTRU()
    ntru.createKeys()
    # invert(130)

if __name__ == '__main__':
    main()
