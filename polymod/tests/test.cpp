#include <iostream>
#include "../include/polymod.h"
#include "../src/polymod.cpp"

int main() {
    // Some basic test cases - need assertions and more egde cases.
    std::cout << "Testing constructors..." << std::endl;
    std::cout << "ConvolutionPoly(N)" << std::endl;
    ConvolutionPoly p(10);
    std::cout << p.toString() << std::endl;
    std::cout << "ConvolutionPoly(N, q)" << std::endl;
    p = ConvolutionPoly(10, 5);
    std::cout << p.toString() << std::endl;
    std::cout << "ConvolutionPoly(N, q, coeffs)" << std::endl;
    p = ConvolutionPoly(7, 32, std::vector({-1, 0, 1, 0, 1, -1, 0}));
    std::cout << p.toString() << std::endl;
    std::cout << "ConvolutionPoly(N, q, equation)" << std::endl;
    p = ConvolutionPoly(7, 32, "x^3-4x^2-3");
    std::cout << p.toString() << std::endl;
    std::cout << std::endl;

    std::cout << "Testing getters..." << std::endl;
    std::cout << "p: " << p.toString() << std::endl;
    std::cout << "p.get_N(): " << p.get_N() << std::endl;
    std::cout << "p.get_q(): " << p.get_q() << std::endl;
    std::cout << "p.get_d(): " << p.get_d() << std::endl;
    std::cout << "p.get_coeffs(): ";
    std::vector<int> coeffs = p.get_coeffs();
    for (size_t i=0; i<coeffs.size(); i++) std::cout << coeffs[i] << ' ';
    std::cout << std::endl;
    std::cout << "p.getCoeffAt(i) for i in range(N): ";
    for (int i=0; i<p.get_N(); i++) std::cout << p.getCoeffAt(i) << ' ';
    std::cout << '\n' << std::endl;

    std::cout << "Testing operators..." << std::endl;
    p = ConvolutionPoly(10, 10, std::vector({1,2,3,4,5,6,7,8,9,10}));
    ConvolutionPoly q = ConvolutionPoly(10, 10, std::vector({2,3,5,7,11,13,17,19,23,29}));
    int k = -3;
    std::cout << "p: " << p.toString() << std::endl;
    std::cout << "q: " << q.toString() << std::endl;
    std::cout << "k: " << k << std::endl;
    std::cout << "p + q: " << (p+q).toString() << std::endl;
    std::cout << "p - q: " << (p-q).toString() << std::endl;
    std::cout << "p * q: " << (p*q).toString() << std::endl;
    std::cout << "-p: " << (-p).toString() << std::endl;
    std::cout << "p + k: " << (p+k).toString() << std::endl;
    std::cout << "p - k: " << (p-k).toString() << std::endl;
    std::cout << "p * k: " << (p*k).toString() << std::endl;
    std::cout << "k + p: " << (k+p).toString() << std::endl;
    std::cout << "k - p: " << (k-p).toString() << std::endl;
    std::cout << "k * p: " << (p*q).toString() << std::endl;
    std::cout << std::endl;

    std::cout << "Testing modulus..." << std::endl;
    std::cout << "p: " << p.toString() << std::endl;
    std::cout << "p.setModulus(5)" << std::endl;
    p.setModulus(5);
    std::cout << "p: " << p.toString() << std::endl;
    std::cout << "p.setModulus(3)" << std::endl;
    p.setModulus(3);
    std::cout << "p: " << p.toString() << std::endl;
    std::cout << "p.setModulus(1)" << std::endl;
    p.setModulus(1);
    std::cout << "p: " << p.toString() << std::endl;
    std::cout << "p.setModulus(0)" << std::endl;
    p.setModulus(0);
    std::cout << "p: " << p.toString() << std::endl;
    std::cout << std::endl;

    std::cout << "Testing generation..." << std::endl;
    std::cout << "SAMPLE_IID:" << std::endl;
    ConvolutionPoly r = ConvolutionPoly(11, 41, Generator::SAMPLE_IID);
    std::cout << r.toString() << std::endl;
    std::cout << "SAMPLE_FIXED_TYPE:" << std::endl;
    r = ConvolutionPoly(11, 41, Generator::SAMPLE_FIXED_TYPE);
    std::cout << r.toString() << std::endl;
    std::cout << std::endl;

    std::cout << "Testing serialization..." << std::endl;
    ConvolutionPoly g = ConvolutionPoly(7, 32, Generator::SAMPLE_IID);
    std::cout << "g:" << std::endl;
    std::cout << g.toString() << std::endl;
    std::cout << "Serialization:" << std::endl;
    std::string serialization = g.serialize();
    // std::cout << serialization << std::endl;
    for (char c : serialization) std::cout << std::bitset<8>(c) << std::endl;
    std::vector<unsigned char> bytes(serialization.size());
    for (int i=0; i<bytes.size(); i++) bytes[i] = serialization[i];
    g = ConvolutionPoly(7, 32, bytes);
    std::cout << "Recovered g:" << std::endl;
    std::cout << g.toString() << std::endl;



    std::cout << "Testing inverses..." << std::endl;
    ConvolutionPoly f = ConvolutionPoly(11, 41, Generator::SAMPLE_IID);
    std::cout << "f: " << f.toString() << std::endl;
    std::cout << "f.inverse(): " << f.inverse().toString() << std::endl;
    f.setModulus(64);
    std::cout << "f: " << f.toString() << std::endl;
    std::cout << "f.inverse(): " << f.inverse().toString() << std::endl;
    std::cout << std::endl;


    return 0;
}




