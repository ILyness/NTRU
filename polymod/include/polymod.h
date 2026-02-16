#ifndef POLYMOD_H
#define POLYMOD_H

#include <vector>
#include <string>
#include <iostream>

enum class Generator {SAMPLE_IID, SAMPLE_FIXED_TYPE};

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
    int getQBits() const;
    std::pair<ConvolutionPoly, ConvolutionPoly> divide(const ConvolutionPoly& other) const;
    std::pair<int, std::vector<ConvolutionPoly>> getQuotients(ConvolutionPoly mod, ConvolutionPoly to_invert);


public:
    // Constructors
    ConvolutionPoly();
    ConvolutionPoly(int degreeMod, int coeffMod, const Generator& generator);
    ConvolutionPoly(int degreeMod);
    ConvolutionPoly(int degreeMod, int coeffMod);
    ConvolutionPoly(int degreeMod, int coeffMod, const std::vector<int>& vals);
    ConvolutionPoly(int degreeMod, int coeffMod, const std::vector<unsigned char>& serialization);
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
    std::string serialize() const;
    ConvolutionPoly inverse();
    
    // Operator Overloads
    ConvolutionPoly operator+(const ConvolutionPoly& other) const;
    ConvolutionPoly operator-(const ConvolutionPoly& other) const;
    ConvolutionPoly operator*(const ConvolutionPoly& other) const;
    ConvolutionPoly operator+(int scalar) const;
    ConvolutionPoly operator-(int scalar) const;
    ConvolutionPoly operator*(int scalar) const;
    ConvolutionPoly operator-() const;
    friend ConvolutionPoly operator+(int scalar, const ConvolutionPoly& p);
    friend ConvolutionPoly operator-(int scalar, const ConvolutionPoly& p);
    friend ConvolutionPoly operator*(int scalar, const ConvolutionPoly& p);
    ConvolutionPoly operator/(const ConvolutionPoly& other) const;
    ConvolutionPoly operator%(const ConvolutionPoly& other) const;
    bool operator==(const ConvolutionPoly& other) const;
};

ConvolutionPoly operator+(int scalar, const ConvolutionPoly& p);
ConvolutionPoly operator-(int scalar, const ConvolutionPoly& p);
ConvolutionPoly operator*(int scalar, const ConvolutionPoly& p);

#endif