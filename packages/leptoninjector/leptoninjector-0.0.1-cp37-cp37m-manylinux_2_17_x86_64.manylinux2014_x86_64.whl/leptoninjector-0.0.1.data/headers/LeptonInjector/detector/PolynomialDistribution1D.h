#pragma once
#ifndef LI_PolynomialDistribution1D_H
#define LI_PolynomialDistribution1D_H
#include <memory>
#include <string>
#include <exception>
#include <functional>

#include <cereal/cereal.hpp>
#include <cereal/archives/json.hpp>
#include <cereal/archives/binary.hpp>
#include <cereal/types/polymorphic.hpp>
#include <cereal/types/base_class.hpp>

#include "LeptonInjector/math/Polynomial.h"

#include "LeptonInjector/detector/Distribution1D.h"

namespace LI {
namespace detector {

class PolynomialDistribution1D : public Distribution1D {
friend cereal::access;
protected:
public:
    PolynomialDistribution1D();
    PolynomialDistribution1D(const PolynomialDistribution1D&);
    PolynomialDistribution1D(const math::Polynom&);
    PolynomialDistribution1D(const std::vector<double>&);
    bool compare(const Distribution1D& dist) const override;
    Distribution1D* clone() const override { return new PolynomialDistribution1D(*this); };
    std::shared_ptr<const Distribution1D> create() const override {
        return std::shared_ptr<const Distribution1D>(new PolynomialDistribution1D(*this));
    };
    double Derivative(double x) const override;
    double AntiDerivative(double x) const override;
    double Evaluate(double x) const override;
    template<class Archive>
        void serialize(Archive & archive, std::uint32_t const version) {
            if(version == 0) {
                archive(::cereal::make_nvp("Polynomial", polynom_));
                archive(::cereal::make_nvp("PolynomialIntegral", Ipolynom_));
                archive(::cereal::make_nvp("PolynomialDerivative", dpolynom_));
                archive(cereal::virtual_base_class<Distribution1D>(this));
            } else {
                throw std::runtime_error("PolynomialDistribution1D only supports version <= 0");
            }
        };
protected:
    math::Polynom polynom_;
    math::Polynom Ipolynom_;
    math::Polynom dpolynom_;
};

} // namespace detector
} // namespace LI

CEREAL_CLASS_VERSION(LI::detector::PolynomialDistribution1D, 0);
CEREAL_REGISTER_TYPE(LI::detector::PolynomialDistribution1D);
CEREAL_REGISTER_POLYMORPHIC_RELATION(LI::detector::Distribution1D, LI::detector::PolynomialDistribution1D);

#endif // LI_PolynomialDistribution1D_H
