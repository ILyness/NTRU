from itertools import batched
import time
import sys
from ntru import NTRU, getRandomPolynomialCoeffs
from polymod import ConvolutionPoly

def padValues(values, padding, mod):
    return values + (padding * (mod - (len(values) % mod)))


def encryptMessage(plaintext, N, p, q, d, h_str):
    h_coeffs = qnaryBlockToCoeffs(h_str)
    block_size = N // 8

    plaintext = padValues(plaintext, '\0', block_size)
    ciphertext = ''

    for block_plaintext in batched(plaintext, block_size):
        block_plaincoeffs = blockToBinaryCoeffs(block_plaintext, N)
        block_ciphercoeffs, m, r, e = encryptFromH(N, p, q, d, h_coeffs, block_plaincoeffs)
        ciphertext += qnaryCoeffsToBlock(block_ciphercoeffs, q)
    
    return (ciphertext, m, r, e)

def encryptFromH(N, p, q, d, h_coeffs, m_coeffs):
    h = ConvolutionPoly(rank=N, modulus=q, coeffs=h_coeffs)
    m = ConvolutionPoly(rank=N, modulus=q, coeffs=m_coeffs)
    r = ConvolutionPoly(rank=N, modulus=q, coeffs=getRandomPolynomialCoeffs(N, d, d))

    e = (r * p) * h + m
    return (e.coeffs, m, r, e)

def decryptMessage(ciphertext, ntru):
    plaintext = ''

    for block_ciphertext in batched(ciphertext, ntru.N):
        block_ciphercoeffs = qnaryBlockToCoeffs(block_ciphertext)
        block_plaincoeffs = ntru.decryptMessage(block_ciphercoeffs)
        plaintext += binaryCoeffsToBlock(block_plaincoeffs)
    
    return plaintext
        
def binaryCoeffsToBlock(coeffs):
    block = ''
    for block_plaincoeffs in batched(coeffs[:-(len(coeffs) % 8)], 8):
        binary = ''.join((str(c) for c in block_plaincoeffs))
        block += chr(int(binary, 2))
    
    return block


def blockToBinaryCoeffs(block, N):
    coeffs = []
    for char in block:
        bits = format(ord(char), '08b')
        coeffs += [int(bit) for bit in bits]
    return padValues(coeffs, [0], N)


def coefToCharNum(coef):
    if coef <= 93: return coef + 33
    return coef + 67

def charNumToCoef(char_num):
    if char_num >= 160: return char_num - 67
    return char_num - 33

def qnaryCoeffsToBlock(coeffs, q):
    return ''.join([chr(coefToCharNum(c % q)) for c in coeffs])
    


def qnaryBlockToCoeffs(block):
    return [charNumToCoef(ord(char)) for char in block]


def main():
    N, p, q, d = 17, 3, 101, 5
    ntru = NTRU(N, p, q, d)
    h_coeffs = ntru.createRandomKeys()
    h_str = qnaryCoeffsToBlock(h_coeffs, q)
    print(h_str)

    ciphertext, _, _, _ = encryptMessage('catdogdjfkj123123', N, p, q, d, h_str)
    print(ciphertext)
    plaintext = decryptMessage(ciphertext, ntru)
    print(plaintext)

if __name__ == '__main__':
    main()
