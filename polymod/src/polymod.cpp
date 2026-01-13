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

class ConvolutionPoly {
    private:
        std::vector<int> coeffs;
        int N;
        int q;

        int getCenterModulus(int n) const {
            if (q == 0) return n;
            int res = n % q;
            if (res > q/2) res -= q;
            return res;
        }

        void modCoefficients() {
            if (q == 0) return;
            for (size_t i = 0; i < coeffs.size(); i++) {
                coeffs[i] = getCenterModulus(coeffs[i]);
            }
        }

        void parseEquation(int degreeMod, const std::string& equation) {
            coeffs = std::vector<int>(degreeMod+1, 0);
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
        }

    public:
        ConvolutionPoly(int degreeMod) : N(degreeMod), q(0), coeffs(degreeMod, 0) {};
        ConvolutionPoly(int degreeMod, int coeffMod) : N(degreeMod), q(coeffMod) {
            if (q < 0) throw std::invalid_argument("Coefficient modulus q must be positive.");
            coeffs = std::vector<int>(degreeMod, 0);
        };
        ConvolutionPoly(int degreeMod, int coeffMod, const std::vector<int>& vals) : N(degreeMod), q(coeffMod), coeffs(vals) {
            if (q < 0) throw std::invalid_argument("Coefficient modulus q must be positive.");
            if (degreeMod != vals.size()) throw std::invalid_argument("Values provided must match specified polynomial degree.");
            modCoefficients();
        };
        ConvolutionPoly(int degreeMod, int coeffMod, const std::string& equation) : N(degreeMod), q(coeffMod) {
            if (q < 0) throw std::invalid_argument("Coefficient modulus q must be positive.");
            parseEquation(degreeMod, equation);
            modCoefficients(); 
        }

        std::vector<int> get_coeffs() const { return coeffs; }
        int get_N() const { return N; }
        int get_q() const { return q; }

        std::string toString() {
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
            if (first) return "0";
            return ss.str();
        }

        void setModulus(int coeffMod) {
            if (coeffMod < 0) throw std::invalid_argument("Coefficient modulus q must be positive.");
            q = coeffMod;
            modCoefficients();
        }

        ConvolutionPoly operator+(const ConvolutionPoly& other) const {
            if (N != other.N) throw std::invalid_argument("Polynomial Ranks must match.");
            if (q != other.q) throw std::invalid_argument("Polynomial moduli must match.");
            std::vector<int> result(N);
            for (size_t i = 0; i < N; i++) {
                result[i] = coeffs[i] + other.coeffs[i];
            }
            return ConvolutionPoly(N, q, result);
        }

        ConvolutionPoly operator*(const ConvolutionPoly& other) const {
            if (N != other.N) throw std::invalid_argument("Polynomial Ranks must match.");
            if (q != other.q) throw std::invalid_argument("Polynomial moduli must match.");
            std::vector<int> result(N);
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    result[i+j % N] += coeffs[i] * other.coeffs[j];
                }
            }
            return ConvolutionPoly(N, q, result);
        }


};

PYBIND11_MODULE(polymod, m) {
    py::options options;
    options.disable_function_signatures();
    m.doc() = "Convolution Polynomial Library designed to support necessary operations for the NTRU cryptosystem."; 
    py::class_<ConvolutionPoly>(m, "ConvolutionPoly", R"pbdoc(
        ConvolutionPoly(rank=10, modulus=0, coefficients=None, equation=None)

        A Convolution Polynomial.

        Supports addition and multiplication operations in a ring of convolution polynomials with
        specified rank and optional modulus.

        Parameters
        ----------
        rank : int
            The rank of the ring the polynomial belongs to.
        modulus : int, optional
            The modulus of the coefficients for the polynomial. If 0 (the default), no modulus will be used.
        coeffs : list of int, optional
            The coefficients for the polynomial in ascending degree. Must match the rank. If not in range, coefficients will
            be modified to fall in the center lift modulus if provided.
        equation : str, optional
            The math equation for the polynomial. Rank and modulus are not inferred, and not included terms are
            assumed to be 0. Must be in the form ax^n + bx^k - cx^m + ... 

        Attributes
        ----------
        coeffs : list of int
            The coefficents of the polynomial center-lifted modulo q (if provided).
        N : int
            The rank of the polynomial.
        q : int
            The modulus of the polynomial. If 0 (default), no modulus is used.

        Notes
        -----
        The following operators are supported:

        * **Addition (+):** Performs addition of coefficents modulo `q`.
        * **Multiplication (*):** Performs standard convolution polynomial multiplication with respect to rank ``N``.

        Examples
        --------
        >>> p = ConvolutionPoly()
        >>> p 
        0 (no modulus) [Rank 10]
        )pbdoc")
        .def(py::init([](std::optional<int> rank, 
                              std::optional<int> modulus, 
                              std::optional<std::vector<int>> coeffs,
                              std::optional<std::string> equation) {
            
            if (coeffs.has_value() && equation.has_value()) {
                throw py::value_error("Cannot provided both coefficients and equation.");
            }

            int N = (rank.has_value()) ? *rank : 10;
            int q = (modulus.has_value()) ? *modulus : 0;
            std::vector<int> vals;
            if (coeffs.has_value()) vals = *coeffs;
            std::string eq;
            if (equation.has_value()) eq = *equation;

            if (modulus.has_value()) {
                if (equation.has_value()) {
                    return new ConvolutionPoly(N, q, eq);
                } else if (coeffs.has_value()) {
                    return new ConvolutionPoly(N, q, vals);
                } else {
                    return new ConvolutionPoly(N, q);
                }
            } else {
                if (coeffs.has_value()) {
                    return new ConvolutionPoly(N, q, vals);
                }
                return new ConvolutionPoly(10);
            }                   
        }),
        py::arg("rank") = py::none(),
        py::arg("modulus") = py::none(),
        py::arg("coeffs") = py::none(),
        py::arg("equation") = py::none()
        )
        .def_property_readonly("coeffs", &ConvolutionPoly::get_coeffs)
        .def_property_readonly("N", &ConvolutionPoly::get_N)
        .def_property_readonly("q", &ConvolutionPoly::get_q)
        .def("set_modulus", &ConvolutionPoly::setModulus, R"pbdoc(
            Update the modulus of the polynomial.

            Parameters
            ----------
            q : int
                The new modulus. If 0, then no modulus will be used.

            Returns
            -------
            None

            Raises
            ------
            ValueError
                If ``q`` is negative.
            )pbdoc")
        .def(py::self + py::self)
        .def(py::self * py::self)
        .def("__repr__", &ConvolutionPoly::toString);
}