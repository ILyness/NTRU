#ifndef POLYMOD_H
#define POLYMOD_H

#include <vector>
#include <string>
#include <iostream>

class ConvolutionPoly {
private:
    std::vector<int> coeffs;
    int N;
    int q;
    int d;

    void calculateDegree();
    int getCenterModulus(int n) const;
    void modCoefficients();
    void parseEquation(int degreeMod, const std::string& equation);
    int getIntegerInverse(int to_invert) const;
    std::pair<ConvolutionPoly, ConvolutionPoly> divide(const ConvolutionPoly& other) const;
    std::pair<int, std::vector<ConvolutionPoly>> getQuotients(ConvolutionPoly mod, ConvolutionPoly to_invert);


public:
    // Constructors
    ConvolutionPoly(int degreeMod);
    ConvolutionPoly(int degreeMod, int coeffMod);
    ConvolutionPoly(int degreeMod, int coeffMod, const std::vector<int>& vals);
    ConvolutionPoly(int degreeMod, int coeffMod, const std::string& equation);

    // Getters
    std::vector<int> get_coeffs() const;
    int get_N() const;
    int get_q() const;
    int get_d() const;
    int getCoeffAt(int i) const;

    // Operations
    void setModulus(int coeffMod);
    std::string toString() const;
    ConvolutionPoly inverse();
    
    // Operator Overloads
    ConvolutionPoly operator+(const ConvolutionPoly& other) const;
    ConvolutionPoly operator-(const ConvolutionPoly& other) const;
    ConvolutionPoly operator*(const ConvolutionPoly& other) const;
    ConvolutionPoly operator/(const ConvolutionPoly& other) const;
    ConvolutionPoly operator%(const ConvolutionPoly& other) const;
    bool operator==(const ConvolutionPoly& other) const;
};

#endif