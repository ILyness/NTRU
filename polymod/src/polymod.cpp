#include <vector>
#include <cmath>
#include <algorithm>
#include <string>
#include <sstream>
#include <stdexcept>
#include <iostream>
#include <bitset>
#include <bit>
#include <random>
#include <cstdint>
#include "../include/polymod.h"


void ConvolutionPoly::calculateDegree() {
    for (int i = N-1; i > 0; i--) {
        if (coeffs[i]) {
            d = i;
            return;
        }
    }
    d = 0;
};

int ConvolutionPoly::getCenterModulus(int n) const {
    if (q == 0) return n;
    int res = n % q;
    if (res > (q>>1)) res -= q;
    if (res < -(q>>1)) res += q;
    return res;
};

void ConvolutionPoly::modCoefficients() {
    if (q == 0) return;
    for (size_t i = 0; i < coeffs.size(); i++) {
        coeffs[i] = getCenterModulus(coeffs[i]);
    }
};

int ConvolutionPoly::getQBits() const {
    int qbits = 0;
    for (int mod=q-1; mod; mod>>=1) qbits++;
    return qbits;
}

void ConvolutionPoly::parseEquation(int degreeMod, const std::string& equation) {
    coeffs = std::vector<int>(degreeMod, 0);
    int a;
    size_t b;
    int sign = 1;
    size_t i = 0;
    while (i < equation.size()) {
        switch (equation[i]) {
            case ' ':
                i++; continue;
            case '+':
                sign = 1; i++; break;
            case '-':
                sign = -1; i++; break;
            default:
                size_t j = 0;
                while (!(equation[i+j] == 'x' || equation[i+j] == '+' || equation[i+j] == '-') && i+j < equation.size()) j++;
                if (j) a = std::stoi(equation.substr(i, i+j)); else a = 1;
                i += j;
                if (i >= equation.size()) b = 0;
                else {
                    if (equation[i] == 'x') {
                        i++;
                        if (equation[i] == '^') {
                            i++;
                            j = 0;
                            while (!(equation[i+j] == 'x' || equation[i+j] == '+' || equation[i+j] == '-') && i+j < equation.size()) j++;
                            b = std::stoi(equation.substr(i, i+j));
                            i += j;
                        } else b = 1;
                    } else b = 0;
                }
                if (coeffs.at(b) != 0) {
                    throw std::invalid_argument("Duplicate tokens with the same degree will not be processed.");
                } else {
                    coeffs.at(b) = a * sign;
                }
        }
    }
};

int ConvolutionPoly::getIntegerInverse(int to_invert) const {
    if (to_invert < 0) to_invert += q;
    if (to_invert == 0) throw std::invalid_argument("Cannot get inverse of 0.");
    if (to_invert == 1) return 1;
    
    int dividend = q;
    int divisor = to_invert;

    int quotient;
    int remainder = 1000;
    std::vector<int> quotients;

    while (remainder != 0) {
        quotient = dividend / divisor;
        remainder = dividend % divisor;

        quotients.push_back(quotient);

        dividend = divisor;
        divisor = remainder;
    }
    if (dividend != 1) throw std::invalid_argument("Coefficient divisor and dividend must be coprime.");

    int large_num_coef = 0;
    int small_num_coef = 1;
    int temp;
    
    for (int i = quotients.size() - 2; i >= 0; i--) {
        temp = large_num_coef;
        large_num_coef = small_num_coef;
        small_num_coef = temp - (quotients[i]*small_num_coef);
    }
    return small_num_coef;
}

std::pair<ConvolutionPoly, ConvolutionPoly> ConvolutionPoly::divide(const ConvolutionPoly& other) const {
    std::vector<int> multiple(N);
    std::vector<int> remainder = coeffs;
    int n = get_d();
    int k = other.get_d();
    int l = other.getCoeffAt(k);
    int inv = getIntegerInverse(l);
    int idx;
    // exit(1);
    while (n >= k) {
        multiple[n-k] = (remainder[n] * inv) % q;
        for (int i = n-k; i <= n; i++) {
            idx = (N + i - (n - k)) % N;
            remainder[i] = getCenterModulus(remainder[i] - multiple[n-k] * other.getCoeffAt(idx));
        }
        while ((n >= 0) && (remainder[n] == 0)) {
            n--;
        }
    }
    return std::pair<ConvolutionPoly, ConvolutionPoly>(ConvolutionPoly(N, q, multiple), ConvolutionPoly(N, q, remainder));
};

std::pair<int, std::vector<ConvolutionPoly>> ConvolutionPoly::getQuotients(ConvolutionPoly mod, ConvolutionPoly to_invert) {
    std::vector<int> ones(N, 1);

    ConvolutionPoly dividend = mod;
    ConvolutionPoly divisor = to_invert;

    ConvolutionPoly quotient = ConvolutionPoly(N, q, ones);
    ConvolutionPoly remainder = ConvolutionPoly(N, q, ones);

    std::vector<ConvolutionPoly> quotients;

    int num_zeros_in_remainder = 1;

    while (num_zeros_in_remainder != 0) {
        std::pair<ConvolutionPoly, ConvolutionPoly> divided = dividend.divide(divisor);

        quotient = divided.first;
        remainder = divided.second;

        quotients.push_back(quotient);

        dividend = divisor;
        divisor = remainder;

        num_zeros_in_remainder = 0;
        for (size_t i = 0; i < N; i++) {
            if (remainder.coeffs[i] != 0) {
                num_zeros_in_remainder++;
            }
        }
    }

    for (size_t i = 1; i < N; i++) {
        if (dividend.coeffs[i] != 0) throw std::invalid_argument("ConvolutionPoly not invertible.");
    }

    return std::pair<int, std::vector<ConvolutionPoly>>(dividend.coeffs[0], quotients);
};

ConvolutionPoly::ConvolutionPoly() : N(3), q(0), coeffs(3, 0) {};
ConvolutionPoly::ConvolutionPoly(int degreeMod, int coeffMod, const std::vector<unsigned char>& serialization) : N(degreeMod), q(coeffMod) {
    if (!q) throw std::invalid_argument("Polynomial must have coefficient modulus to serialize.");
    int qbits = getQBits();
    unsigned long long buffer;
    coeffs = std::vector<int>(N);
    int buf_size = 0;
    int idx = 0;
    for (unsigned char c : serialization) {
        buffer = (buffer << 8) | c;
        buf_size += 8;
        while (buf_size > qbits) {
            if (idx >= N) throw std::invalid_argument("Serialization does not match specified degree.");
            coeffs[idx] = (buffer >> (buf_size - qbits)) & ((1 << qbits) - 1);
            buf_size -= qbits;
            idx++;
        }
    }
    modCoefficients();
}
ConvolutionPoly::ConvolutionPoly(int degreeMod, int coeffMod, const Generator& generator) : N(degreeMod), q(coeffMod) {
    std::random_device rd;
    std::mt19937 engine(rd());
    coeffs = std::vector<int>(N, 0);
    switch (generator) {
        case Generator::SAMPLE_IID: {
            std::independent_bits_engine<std::mt19937, 8, uint8_t> rbe(engine);
            for (int i=0; i<N-1; i++) {
                uint8_t random_byte = rbe();
                coeffs[i] = (int)random_byte % 3;
            }
            break;
        }
        case Generator::SAMPLE_FIXED_TYPE: {
            std::vector<std::pair<int, int>> rand_vals(N);
            std::uniform_int_distribution<> distrib(1, N);
            int d = q / 16 - 1;
            if (d <= 0) throw std::invalid_argument("Coefficient modulus q is too small for sample_fixed_type generation.");
            for (size_t i=0; i<N-1; i++) {
                rand_vals[i].first = distrib(engine);
                if (i < d) rand_vals[i].second = 1;
                else if (i < 2*d) rand_vals[i].second = -1;
                else rand_vals[i].second = 0;
            }
            std::sort(rand_vals.begin(), rand_vals.end());
            for (size_t i=0; i<N-1; i++) {
                coeffs[i] = rand_vals[i].second;
            }
            break;
        }
    }
    calculateDegree();
};
ConvolutionPoly::ConvolutionPoly(int degreeMod) : N(degreeMod), q(0), coeffs(degreeMod, 0), d(0) {};
ConvolutionPoly::ConvolutionPoly(int degreeMod, int coeffMod) : N(degreeMod), q(coeffMod) {
    if (q < 0) throw std::invalid_argument("Coefficient modulus q must be positive.");
    coeffs = std::vector<int>(degreeMod, 0);
};
ConvolutionPoly::ConvolutionPoly(int degreeMod, int coeffMod, const std::vector<int>& vals) : N(degreeMod), q(coeffMod), coeffs(vals) {
    if (q < 0) throw std::invalid_argument("Coefficient modulus q must be positive.");
    if (degreeMod != vals.size()) throw std::invalid_argument("Values provided must match specified polynomial degree.");
    modCoefficients();
    calculateDegree();
};
ConvolutionPoly::ConvolutionPoly(int degreeMod, int coeffMod, const std::string& equation) : N(degreeMod), q(coeffMod) {
    if (q < 0) throw std::invalid_argument("Coefficient modulus q must be positive.");
    parseEquation(degreeMod, equation);
    modCoefficients(); 
    calculateDegree();
};

std::vector<int> ConvolutionPoly::get_coeffs() const { return coeffs; }
int ConvolutionPoly::get_N() const { return N; }
int ConvolutionPoly::get_q() const { return q; }
int ConvolutionPoly::get_d() const { return d; }

int ConvolutionPoly::getCoeffAt(int i) const {
    if (i >= N) throw std::invalid_argument("Index must be at most N.");
    return coeffs[i];
};

std::string ConvolutionPoly::toString() const {
    std::stringstream ss;
    bool first = true;
    for (int i = coeffs.size()-1; i >= 0; i--) {
        if (coeffs[i] == 0) continue;
        if (!first && coeffs[i] > 0) ss << " + ";
        if (coeffs[i] < 0) {
            if (first) ss << '-'; else ss << " - ";
        }
        if (i == 0 || std::abs(coeffs[i]) != 1) ss << std::abs(coeffs[i]);
        if (i > 0) ss << 'x';
        if (i > 1) ss << '^' << i; 
        first = false; 
    }
    if (q) ss << " (modulo " << q << ") "; else ss << "(no modulus) ";
    ss << "[Rank " << N << ']';
    if (first) return "0 " + ss.str();
    return ss.str();
};

std::string ConvolutionPoly::serialize() const {
    if (!q) throw std::invalid_argument("Polynomial must have coefficient modulus to serialize.");
    int qbits = getQBits();
    unsigned long long buffer = 0;
    int buf_size = 0;
    std::vector<unsigned char> bytes;
    for (int coeff : coeffs) {
        buffer = (buffer << qbits) | coeff;
        buf_size += qbits;
        while (buf_size > 8) {
            bytes.push_back((buffer >> (buf_size-8)) & 0xFF);
            buf_size -= 8;
        }
    }
    if (buf_size) bytes.push_back((buffer & ((1 << buf_size) - 1)) << (8 - buf_size));
    return std::string(bytes.begin(), bytes.end());
};

void ConvolutionPoly::setModulus(int coeffMod) {
    if (coeffMod < 0) throw std::invalid_argument("Coefficient modulus q must be positive.");
    q = coeffMod;
    modCoefficients();
};

ConvolutionPoly ConvolutionPoly::inverse() {
    if (q > 3) {
        // std::cout << "q: " << q << std::endl;
        // std::cout << "q binary:  " << std::bitset<sizeof(int) * __CHAR_BIT__>(q) << std::endl;
        int qbits = 0;
        int mod = q;
        for (mod; ~mod & 1; mod>>=1) qbits++;
        mod >>= 1;
        // std::cout << "qbits: " << qbits << std::endl;
        // std::cout << "mod binary:  " << std::bitset<sizeof(int) * __CHAR_BIT__>(mod) << std::endl;
        if (mod == 1) {
            ConvolutionPoly f2 = ConvolutionPoly(N, q, coeffs);
            f2.setModulus(2);
            ConvolutionPoly G = f2.inverse();
            for (int bit=qbits; bit; bit>>=1) {
                G.setModulus(G.get_q() << 1);
                G = G * (-(*this * G) + 2);
            }
            G.setModulus(1 << qbits);
            return G;
        }
    }

    N++;
    coeffs.push_back(0);

    std::vector<int> mod_coeffs(N, 0);
    mod_coeffs[0] = -1;
    mod_coeffs[N-1] = 1;
    ConvolutionPoly mod_poly = ConvolutionPoly(N, q, mod_coeffs);
    
    std::pair<int, std::vector<ConvolutionPoly>> quotient_info = getQuotients(mod_poly, *this);
    int coef_to_change_unit = getIntegerInverse(quotient_info.first);
    std::vector<ConvolutionPoly> quotients = quotient_info.second;

    N--;
    coeffs.pop_back();

    std::vector<int> all_zeros(N, 0);
    ConvolutionPoly large_poly_coef = ConvolutionPoly(N, q, all_zeros);
    
    std::vector<int> small_poly_coef_coeffs(N, 0);
    small_poly_coef_coeffs[0] = coef_to_change_unit;
    ConvolutionPoly small_poly_coef = ConvolutionPoly(N, q, small_poly_coef_coeffs);
    
    for (int i = quotients.size()-2; i >= 0; i--) {
        ConvolutionPoly curr_quotient = quotients[i];
        curr_quotient.N--;
        curr_quotient.coeffs.pop_back();

        ConvolutionPoly temp = large_poly_coef;
        large_poly_coef = small_poly_coef;
        small_poly_coef = temp - (curr_quotient * small_poly_coef);
    }

    return small_poly_coef;
};

ConvolutionPoly ConvolutionPoly::operator+(int scalar) const {
    std::vector<int> result(N);
    for (int i=0; i<N; i++) {
        result[i] = coeffs[i] + scalar;
    }
    return ConvolutionPoly(N, q, result);
};
ConvolutionPoly ConvolutionPoly::operator-(int scalar) const {
    std::vector<int> result(N);
    for (int i=0; i<N; i++) {
        result[i] = coeffs[i] - scalar;
    }
    return ConvolutionPoly(N, q, result);

};
ConvolutionPoly ConvolutionPoly::operator*(int scalar) const {
    std::vector<int> result(N);
    for (int i=0; i<N; i++) {
        result[i] = coeffs[i] * scalar;
    }
    return ConvolutionPoly(N, q, result);

};

ConvolutionPoly ConvolutionPoly::operator-() const {
    std::vector<int> result(N);
    for (int i=0; i<N; i++) {
        result[i] = coeffs[i] * -1;
    }
    return ConvolutionPoly(N, q, result);
};

ConvolutionPoly operator+(int scalar, const ConvolutionPoly& p) {
    int N = p.get_N();
    std::vector<int> result(N);
    for (int i=0; i<N; i++) {
        result[i] = scalar + p.getCoeffAt(i);
    }
    return ConvolutionPoly(N, p.get_q(), result);
};

ConvolutionPoly operator-(int scalar, const ConvolutionPoly& p) {
    int N = p.get_N();
    std::vector<int> result(N);
    for (int i=0; i<N; i++) {
        result[i] = scalar - p.getCoeffAt(i);
    }
    return ConvolutionPoly(N, p.get_q(), result);
};

ConvolutionPoly operator*(int scalar, const ConvolutionPoly& p) {
    int N = p.get_N();
    std::vector<int> result(N);
    for (int i=0; i<N; i++) {
        result[i] = scalar * p.getCoeffAt(i);
    }
    return ConvolutionPoly(N, p.get_q(), result);
};

ConvolutionPoly ConvolutionPoly::operator+(const ConvolutionPoly& other) const {
    if (N != other.N) throw std::invalid_argument("Polynomial Ranks must match.");
    if (q != other.q) throw std::invalid_argument("Polynomial moduli must match.");
    std::vector<int> result(N);
    for (size_t i = 0; i < N; i++) {
        result[i] = coeffs[i] + other.coeffs[i];
    }
    return ConvolutionPoly(N, q, result);
};

ConvolutionPoly ConvolutionPoly::operator-(const ConvolutionPoly& other) const {
    if (N != other.N) throw std::invalid_argument("Polynomial Ranks must match.");
    if (q != other.q) throw std::invalid_argument("Polynomial moduli must match.");
    std::vector<int> result(N);
    for (size_t i = 0; i < N; i++) {
        result[i] = coeffs[i] - other.coeffs[i];
    }
    return ConvolutionPoly(N, q, result);
};

ConvolutionPoly ConvolutionPoly::operator*(const ConvolutionPoly& other) const {
    if (N != other.N) throw std::invalid_argument("Polynomial Ranks must match.");
    if (q != other.q) throw std::invalid_argument("Polynomial moduli must match.");
    std::vector<int> result(N);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            result[(i+j) % N] += coeffs[i] * other.coeffs[j];
        }
    }
    return ConvolutionPoly(N, q, result);
};

ConvolutionPoly ConvolutionPoly::operator/(const ConvolutionPoly& other) const {
    std::pair<ConvolutionPoly, ConvolutionPoly> result = divide(other);
    return result.first;
};

ConvolutionPoly ConvolutionPoly::operator%(const ConvolutionPoly& other) const {
    std::pair<ConvolutionPoly, ConvolutionPoly> result = divide(other);
    return result.second;
};

bool ConvolutionPoly::operator==(const ConvolutionPoly& other) const {
    return (N == other.N) && (q == other.q) && (coeffs == other.coeffs);
};