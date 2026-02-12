from itertools import batched
from ntru import NTRU

def padValues(values, padding, mod):
    return values + (padding * (mod - (len(values) % mod)))


def encryptMessage(plaintext, ntru):
    block_size = ntru.N // 8

    plaintext = padValues(plaintext, '\0', block_size)
    ciphertext = ''

    for block_plaintext in batched(plaintext, block_size):
        block_plaincoeffs = blockToBinaryCoeffs(block_plaintext, ntru.N)
        block_ciphercoeffs = ntru.encryptMessage(block_plaincoeffs)
        ciphertext += qnaryCoeffsToBlock(block_ciphercoeffs, ntru.q)
    
    return ciphertext


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


def qnaryCoeffsToBlock(coeffs, q):
    return ''.join([chr(c % q) for c in coeffs])


def qnaryBlockToCoeffs(block):
    return [ord(char) for char in block]


def main():
    ntru = NTRU(17, 3, 101, 5)
    ntru.createRandomKeys()
    ciphertext = encryptMessage('catdogdjfkj123123', ntru)
    plaintext = decryptMessage(ciphertext, ntru)
    print(plaintext)

if __name__ == '__main__':
    main()
