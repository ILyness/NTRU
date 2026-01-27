#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>
#include "../include/polymod.h"

namespace py = pybind11;

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
        d : int
            The degree of the polynomial.

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
        .def_property_readonly("d", &ConvolutionPoly::get_d)
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
        .def("get_coeff", &ConvolutionPoly::getCoeffAt, R"pbdoc(
            Get coefficient of polynomial at specified index.

            Parameters
            ----------
            i : int
                Index of coefficient to access.

            Returns
            -------
            int
                Value at specified index.

            Raises
            ------
            ValueError
                If ``i`` is out of range.
            )pbdoc", py::arg("i"))
        .def("inverse", &ConvolutionPoly::inverse, R"pbdoc(
            Get the inverse of the polynomial.

            Returns
            -------
            ConvolutionPoly
                The inverse of the polynomial, if it exists. None otherwise.
            )pbdoc")
        .def(py::self + py::self)
        .def(py::self * py::self)
        .def(py::self / py::self)
        .def(py::self % py::self)
        .def("__repr__", &ConvolutionPoly::toString);
}