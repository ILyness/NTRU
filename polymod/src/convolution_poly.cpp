#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>
#include <vector>
#include <cmath>
#include <algorithm>
#include <string>
#include <sstream>
#include <stdexcept>
#include <iostream>

namespace py = pybind11;

// ==========================================
// Global Math Helpers
// ==========================================

// Integer Extended Euclidean Algorithm to find inverse mod generic m
// Returns {gcd, x, y} such that ax + by = gcd
struct EGCDResult { long long gcd; long long x; long long y; };

EGCDResult integer_egcd(long long a, long long b) {
    if (a == 0) return {b, 0, 1};
    EGCDResult res = integer_egcd(b % a, a);
    return {res.gcd, res.y - (b / a) * res.x, res.x};
}

// Generic modular inverse for any q (prime or not)
int get_mod_inverse(int a, int m) {
    int val = (a % m + m) % m;
    EGCDResult res = integer_egcd(val, m);
    if (res.gcd != 1) {
        throw std::invalid_argument("Element is not invertible modulo q (GCD != 1)");
    }
    return (int)((res.x % m + m) % m);
}

// NTT Constants
constexpr long long NTT_MOD = 998244353;
constexpr long long NTT_G = 3;

long long power(long long base, long long exp) {
    long long res = 1;
    base %= NTT_MOD;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % NTT_MOD;
        base = (base * base) % NTT_MOD;
        exp /= 2;
    }
    return res;
}

long long ntt_mod_inverse(long long n) {
    return power(n, NTT_MOD - 2);
}

void ntt(std::vector<long long>& a, bool invert) {
    size_t n = a.size();
    for (size_t i = 1, j = 0; i < n; i++) {
        size_t bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) std::swap(a[i], a[j]);
    }
    for (size_t len = 2; len <= n; len <<= 1) {
        long long wlen = power(NTT_G, (NTT_MOD - 1) / len);
        if (invert) wlen = ntt_mod_inverse(wlen);
        for (size_t i = 0; i < n; i += len) {
            long long w = 1;
            for (size_t j = 0; j < len / 2; j++) {
                long long u = a[i + j];
                long long v = (a[i + j + len / 2] * w) % NTT_MOD;
                a[i + j] = (u + v) % NTT_MOD;
                a[i + j + len / 2] = (u - v + NTT_MOD) % NTT_MOD;
                w = (w * wlen) % NTT_MOD;
            }
        }
    }
    if (invert) {
        long long n_inv = ntt_mod_inverse(n);
        for (long long& x : a) x = (x * n_inv) % NTT_MOD;
    }
}

// ==========================================
// Class Definition
// ==========================================

class ConvolutionPoly {
private:
    std::vector<int> coeffs;
    int N; 
    int q; 

    // Helper: Modulo [0, n)
    int positive_modulo(long long i, int n) const {
        return (int)((i % n + n) % n);
    }

    // ==========================================
    // Internal Helpers for Polynomial EEA
    // ==========================================
    // These operate on raw vectors (no cyclic wrapping) because
    // the EEA requires standard polynomial division logic.

    // 1. Get Degree (index of last non-zero coeff)
    int get_degree(const std::vector<int>& p) const {
        for (int i = p.size() - 1; i >= 0; --i) {
            if (p[i] != 0) return i;
        }
        return -1; // Zero polynomial
    }

    // 2. Trim trailing zeros (helper for division)
    void trim(std::vector<int>& p) const {
        while (p.size() > 1 && p.back() == 0) {
            p.pop_back();
        }
    }

    // 3. Standard Polynomial Subtraction
    std::vector<int> raw_sub(const std::vector<int>& a, const std::vector<int>& b) const {
        size_t len = std::max(a.size(), b.size());
        std::vector<int> res(len);
        for(size_t i=0; i<len; ++i) {
            int v_a = (i < a.size()) ? a[i] : 0;
            int v_b = (i < b.size()) ? b[i] : 0;
            res[i] = positive_modulo(v_a - v_b, q);
        }
        trim(res);
        return res;
    }

    // 4. Standard Polynomial Multiplication (Naive O(N^2) is fine for EEA steps)
    std::vector<int> raw_mul(const std::vector<int>& a, const std::vector<int>& b) const {
        if (a.empty() || b.empty()) return {0};
        std::vector<int> res(a.size() + b.size() - 1, 0);
        for (size_t i = 0; i < a.size(); ++i) {
            for (size_t j = 0; j < b.size(); ++j) {
                long long val = (long long)a[i] * b[j];
                res[i+j] = positive_modulo(res[i+j] + val, q);
            }
        }
        trim(res);
        return res;
    }

    // 5. Polynomial Division: returns {Quotient, Remainder}
    // A(x) = B(x)Q(x) + R(x)
    std::pair<std::vector<int>, std::vector<int>> raw_div_mod(
        std::vector<int> num, std::vector<int> den) const 
    {
        // Denominator must not be zero
        int den_deg = get_degree(den);
        if (den_deg < 0) throw std::invalid_argument("Division by zero polynomial");

        // Leading coefficient inverse
        int lead_inv = get_mod_inverse(den[den_deg], q);

        std::vector<int> quot; 
        int num_deg = get_degree(num);

        // Standard long division algorithm
        // Note: We pre-allocate quotient but it's sparse; we'll fix size later or push back
        // Actually, easiest is to reduce num in place.
        std::vector<int> result_quot(std::max(0, num_deg - den_deg + 1), 0);

        while (num_deg >= den_deg && num_deg >= 0) {
            // Calculate scale factor for next term
            int lead_num = num[num_deg];
            int scale = positive_modulo((long long)lead_num * lead_inv, q);
            
            int diff_deg = num_deg - den_deg;
            result_quot[diff_deg] = scale;

            // Subtract (scale * x^diff * den) from num
            for (int i = 0; i <= den_deg; ++i) {
                long long subtrahend = (long long)scale * den[i];
                int target_idx = i + diff_deg;
                num[target_idx] = positive_modulo(num[target_idx] - subtrahend, q);
            }
            
            // Re-check degree
            num_deg = get_degree(num);
            // Manually trim num to ensure degree check is accurate next loop
            while(num.size() > (size_t)num_deg + 1 && num.size() > 0) num.pop_back();
        }
        
        trim(num); // num is now remainder
        return {result_quot, num};
    }

public:
    ConvolutionPoly(const std::vector<int>& c, int degree_mod, int coeff_mod) 
        : N(degree_mod), q(coeff_mod) {
        coeffs.resize(N, 0);
        for (size_t i = 0; i < c.size() && i < (size_t)N; ++i) {
            coeffs[i] = positive_modulo(c[i], q);
        }
    }

    std::vector<int> get_coeffs() const { return coeffs; }
    int get_N() const { return N; }
    int get_q() const { return q; }

    ConvolutionPoly operator+(const ConvolutionPoly& other) const {
        if (N != other.N || q != other.q) throw std::invalid_argument("Mismatch N or q");
        std::vector<int> new_coeffs(N);
        for(int i = 0; i < N; ++i) {
            new_coeffs[i] = positive_modulo(coeffs[i] + other.coeffs[i], q);
        }
        return ConvolutionPoly(new_coeffs, N, q);
    }

    ConvolutionPoly operator*(const ConvolutionPoly& other) const {
        if (N != other.N || q != other.q) throw std::invalid_argument("Mismatch N or q");
        
        size_t ntt_size = 1;
        while (ntt_size < (size_t)(2 * N)) ntt_size *= 2;

        std::vector<long long> fa(ntt_size, 0), fb(ntt_size, 0);
        for (size_t i = 0; i < (size_t)N; ++i) {
            fa[i] = coeffs[i];
            fb[i] = other.coeffs[i];
        }

        ntt(fa, false); ntt(fb, false);
        for (size_t i = 0; i < ntt_size; ++i) fa[i] = (fa[i] * fb[i]) % NTT_MOD;
        ntt(fa, true);

        std::vector<int> result_coeffs(N, 0);
        for (size_t i = 0; i < ntt_size; ++i) {
            size_t dest_index = i % N;
            long long current = result_coeffs[dest_index];
            result_coeffs[dest_index] = positive_modulo(current + fa[i], q);
        }
        return ConvolutionPoly(result_coeffs, N, q);
    }

    // ==========================================
    // INVERSE METHOD (Extended Euclidean)
    // ==========================================
    ConvolutionPoly inverse() const {
        // Algorithm: Solve A(x)S(x) + M(x)T(x) = gcd(A, M)
        // where A(x) = this, M(x) = x^N - 1
        // If gcd == 1, S(x) is the inverse.

        // 1. Setup R0 = x^N - 1
        std::vector<int> r0(N + 1, 0);
        r0[0] = positive_modulo(-1, q); // constant term -1
        r0[N] = 1;                      // x^N term 1
        
        // 2. Setup R1 = this
        std::vector<int> r1 = coeffs;
        trim(r1);

        // 3. Setup Bezout coefficients
        // t stores the coefficient for 'this' (the one we want as inverse)
        std::vector<int> t0 = {0};
        std::vector<int> t1 = {1};

        // 4. EEA Loop
        // r0_new = r1
        // r1_new = r0 % r1
        // t0_new = t1
        // t1_new = t0 - Q * t1
        while (get_degree(r1) >= 0 && !(r1.size() == 1 && r1[0] == 0)) {
            auto div_res = raw_div_mod(r0, r1);
            std::vector<int> Q = div_res.first;
            std::vector<int> remainder = div_res.second;

            r0 = r1;
            r1 = remainder;

            std::vector<int> t_temp = raw_sub(t0, raw_mul(Q, t1));
            t0 = t1;
            t1 = t_temp;
        }

        // 5. Check GCD
        // r0 holds the GCD. It must be a constant (degree 0).
        if (get_degree(r0) > 0) {
            throw std::runtime_error("Polynomial is not invertible (GCD is not constant)");
        }
        
        // 6. Normalize
        // If gcd = C, we have A*t0 = C (mod M). We need A * (t0 * C^-1) = 1.
        int gcd_val = r0[0];
        if (gcd_val == 0) throw std::runtime_error("Polynomial is not invertible (Zero GCD)");

        int scale = get_mod_inverse(gcd_val, q);
        
        // Multiply t0 by scale
        std::vector<int> result_vec(N, 0);
        for(size_t i=0; i<t0.size() && i<(size_t)N; ++i) {
            long long val = (long long)t0[i] * scale;
            result_vec[i] = positive_modulo(val, q);
        }

        return ConvolutionPoly(result_vec, N, q);
    }

    void change_modulus(int new_q) {
        q = new_q;
        for(auto &c : coeffs) c = positive_modulo(c, q);
    }

    std::vector<int> center_lift() const {
        std::vector<int> lifted(N);
        for(int i = 0; i < N; ++i) {
            if (coeffs[i] > q / 2) lifted[i] = coeffs[i] - q;
            else lifted[i] = coeffs[i];
        }
        return lifted;
    }

    std::string to_string() const {
        std::stringstream ss;
        bool first = true;
        for (int i = N - 1; i >= 0; --i) {
            int c = coeffs[i];
            if (c == 0) continue;
            if (!first) ss << " + ";
            if (c != 1 || i == 0) ss << c;
            if (i > 0) ss << "x";
            if (i > 1) ss << "^" << i;
            first = false;
        }
        if (first) return "0";
        ss << " (mod " << q << ")";
        return ss.str();
    }
};

PYBIND11_MODULE(ntru_math, m) {
    m.doc() = "NTRU Math Library with EEA Inverse"; 
    py::class_<ConvolutionPoly>(m, "ConvolutionPoly")
        .def(py::init<const std::vector<int>&, int, int>(), py::arg("coeffs"), py::arg("degree_mod"), py::arg("coeff_mod"))
        .def_property_readonly("coeffs", &ConvolutionPoly::get_coeffs)
        .def_property_readonly("N", &ConvolutionPoly::get_N)
        .def_property_readonly("q", &ConvolutionPoly::get_q)
        .def("change_modulus", &ConvolutionPoly::change_modulus)
        .def("center_lift", &ConvolutionPoly::center_lift)
        .def("inverse", &ConvolutionPoly::inverse, "Calculate inverse mod (x^N - 1) using EEA.")
        .def(py::self + py::self)
        .def(py::self * py::self)
        .def("__repr__", &ConvolutionPoly::to_string);
}