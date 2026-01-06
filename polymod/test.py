import ntru_math

# Define parameters (N=5, q=17)
# Note: NTRU typically uses N=509 or similar primes, 
# and q is often a power of 2 or a small prime like 2048.
N = 5
q = 17

# Create two polynomials: 
# A = 1 + 2x + 3x^2
# B = 2 + 1x
p1 = ntru_math.ConvolutionPoly([1, 2, 3, 0, 0], N, q)
p2 = ntru_math.ConvolutionPoly([2, 1, 0, 0, 0], N, q)

print(f"P1: {p1}")
print(f"P2: {p2}")

# Addition
p_sum = p1 + p2
print(f"Sum: {p_sum}")

# Multiplication (Cyclic Convolution)
# (1 + 2x + 3x^2) * (2 + x) 
# = 2 + x + 4x + 2x^2 + 6x^2 + 3x^3
# = 2 + 5x + 8x^2 + 3x^3
p_prod = p1 * p2
print(f"Product: {p_prod}")

# Center Lift (Mod 17: maps > 8 to negative)
p_lift_example = ntru_math.ConvolutionPoly([16, 15, 1, 2, 8], N, q)
print(f"Original: {p_lift_example}")
print(f"Center Lifted: {p_lift_example.center_lift()}")