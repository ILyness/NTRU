#include <iostream>
#include "polymod.cpp"

int main() {
    std::cout << "Testing Constructor 1..." << std::endl;
    ConvolutionPoly test = ConvolutionPoly(5);
    std::cout << test.toString() << std::endl;
    std::cout << "Testing Constructor 2..." << std::endl;
    test = ConvolutionPoly(5, 6);
    std::cout << test.toString() << std::endl;
    std::cout << "Testing Constructor 3..." << std::endl;
    std::vector<int> vals = {0, 1, 2, 3, 4, 5};
    test = ConvolutionPoly(5, 6, vals);
    std::cout << test.toString() << std::endl;
    std::cout << "Testing Constructor 4..." << std::endl;
    std::string eq = "x^2 + 5x - 2";
    std::cout << eq << std::endl;
    test = ConvolutionPoly(5, 6, eq);
    std::cout << test.toString() << std::endl;
    eq = "x^4 + 8x + 14";
    std::cout << eq << std::endl;
    test = ConvolutionPoly(5, 6, eq);
    std::cout << test.toString() << std::endl;
    eq = "x^3 - 5x - 1";
    std::cout << eq << std::endl;
    test = ConvolutionPoly(5, 6, eq);
    std::cout << test.toString() << std::endl;
    eq = "x^1 + 12x^2";
    std::cout << eq << std::endl;
    test = ConvolutionPoly(5, 6, eq);
    std::cout << test.toString() << std::endl;
    eq = "x^2 - 2";
    std::cout << eq << std::endl;
    test = ConvolutionPoly(5, 6, eq);
    std::cout << test.toString() << std::endl;
    eq = "x^5 +11x - 4";
    std::cout << eq << std::endl;
    test = ConvolutionPoly(5, 6, eq);
    std::cout << test.toString() << std::endl;
}