from polymod import ConvolutionPoly
from math import gcd
import random

def getRandomPolynomialCoeffs(N, d1=None, d2=None):
    if d1 and d2:
        coefs = [1]*d1 + [-1]*d2 + [0]*(N-d1-d2)
    else:
        coefs = [random.randint(-1, 1) for _ in range(N)]
    random.shuffle(coefs)
    return coefs

class NTRU:
    def __init__(self, N, p, q, d, show_work=False):
        self.N = N
        self.p = p
        self.q = q
        self.d = d
        self.show_work = show_work

        if gcd(self.N, self.q) != 1 or gcd(self.p, self.q) != 1:
            print('Parameter error: we must have:\n     gcd(p, q) = gcd(N, q) = 1.')
            exit()
        
        if self.q <= (6*self.d+1) * self.p:
            print('Parameter warning:\n     q <= (6d+1)p.\nWill proceed.')
        
        self.printWork('(N, p, q, d)', (N,p,q,d))
    

    def printWork(self, name, value):
        num_spaces_before_equal = max(1, 4 - len(name))
        spaces_before_equal = ' ' * num_spaces_before_equal
        if self.show_work: print(f'     {name}{spaces_before_equal}= {value}')
    

    def createRandomKeys(self):
        g_coeffs = getRandomPolynomialCoeffs(self.N, self.d, self.d)

        successful = False
        i = 0
        while not successful and i <20:
            f_coeffs = getRandomPolynomialCoeffs(self.N, self.d+1, self.d)
            try:
                self.createKeys(f_coeffs, g_coeffs)
                successful = True
            except:
                i += 1
            

    def createKeys(self, f_coeffs=None, g_coeffs=None):
        if self.show_work: print('Creating keys.')

        if f_coeffs.count(1) != self.d+1 or f_coeffs.count(-1) != self.d:
            print(f'Parameter error:\n     f has an incorrect number of 1 and -1 coefficients: should be {self.d+1} 1s and {self.d} -1s, is {f_coeffs.coeffs.count(1)} 1s and {f_coeffs.coeffs.count(-1)} -1s.')
            exit()
        
        if g_coeffs.count(1) != self.d or g_coeffs.count(-1) != self.d:
            print(f'Parameter error:\n     g has an incorrect number of 1 and -1 coefficients: should be {self.d} 1s and {self.d} -1s, is {g_coeffs.count(1)} 1s and {g_coeffs.count(-1)} -1s.')
            exit()

        self.f = ConvolutionPoly(rank=self.N, modulus=self.p, coeffs=f_coeffs)
        self.g = ConvolutionPoly(rank=self.N, modulus=self.q, coeffs=g_coeffs)
        self.printWork('f', self.f)

        try:
            F_p = self.f.inverse()
            self.f.set_modulus(self.q)
            F_q = self.f.inverse()

            self.printWork('F_p', F_p)
            self.printWork('F_q', F_q)
        except:
            print(f'Parameter error:\n     f is uninvertible in q or p.')
            exit()
        
        self.printWork('g', self.g)

        self.h = F_q * self.g
        self.printWork('h', self.h)

    def encryptMessage(self, m_coeffs):
        if self.show_work: print(f'Encrypting message.')

        m = ConvolutionPoly(rank=self.N, modulus=self.q, coeffs=m_coeffs)
        r = ConvolutionPoly(rank=self.N, modulus=self.q, coeffs=getRandomPolynomialCoeffs(self.N, self.d, self.d))
        self.h.set_modulus(self.q)

        e = (r * self.p) * self.h + m
        return e

    def decryptMessage(self, e):
        if self.show_work: print(f'Decrypting message.')

        self.f.set_modulus(self.q)
        e.set_modulus(self.q)
        a = self.f * e

        self.f.set_modulus(self.p)
        a.set_modulus(self.p)
        m = self.f.inverse() * a

        self.printWork('a', a)
        self.printWork('m\'', m)

        return m

def textbookExample():
    ntru = NTRU(7, 3, 41, 2)
    f_coeffs = [-1, 0, 1, 1, -1, 0, 1]
    g_coeffs = [0, -1, -1, 0, 1, 0, 1]
    ntru.createKeys(f_coeffs, g_coeffs)

    m_coeffs = [1, -1, 1, 1, 0, -1, 0]
    e = ntru.encryptMessage(m_coeffs)
    m = ntru.decryptMessage(e)

    print(m_coeffs)
    print(m.coeffs)


def randomExample(N, p, q, d):
    ntru = NTRU(N, p, q, d, False)
    ntru.createRandomKeys()

    m_coeffs = getRandomPolynomialCoeffs(N)
    e = ntru.encryptMessage(m_coeffs)
    m_new = ntru.decryptMessage(e)

    print(ntru.f.coeffs)
    print(ntru.g.coeffs)

    print(m_coeffs == m_new.coeffs)

# Special parameters = (509, 3, 2048, 250)
def main():
    textbookExample()
    randomExample(13, 3, 101, 5)
    # randomExample(7, 3, 53, 2)

if __name__ == '__main__':
    main()
