#pragma once
#ifndef LI_ExponentialDistribution1D_H
#define LI_ExponentialDistribution1D_H
#include <memory>
#include <string>
#include <exception>
#include <functional>

#include <cereal/cereal.hpp>
#include <cereal/archives/json.hpp>
#include <cereal/archives/binary.hpp>
#include <cereal/types/polymorphic.hpp>
#include <cereal/types/base_class.hpp>

#include "LeptonInjector/detector/Distribution1D.h"

namespace LI {
namespace detector {

class ExponentialDistribution1D : public Distribution1D {
friend cereal::access;
public:
    ExponentialDistribution1D();
    ExponentialDistribution1D(const ExponentialDistribution1D&);
    ExponentialDistribution1D(double sigma);
    bool compare(const Distribution1D& dist) const override;
    Distribution1D* clone() const override { return new ExponentialDistribution1D(*this); };
    std::shared_ptr<const Distribution1D> create() const override {
        return std::shared_ptr<const Distribution1D>(new ExponentialDistribution1D(*this));
    };
    double Derivative(double x) const override;
    double AntiDerivative(double x) const override;
    double Evaluate(double x) const override;
    template<class Archive>
        void serialize(Archive & archive, std::uint32_t const version) {
            if(version == 0) {
                archive(::cereal::make_nvp("Sigma", sigma_));
                archive(cereal::virtual_base_class<Distribution1D>(this));
            } else {
                throw std::runtime_error("ExponentialDistribution1D only supports version <= 0");
            }
        };
protected:
    double sigma_;
};

} // namespace detector
} // namespace LI

CEREAL_CLASS_VERSION(LI::detector::ExponentialDistribution1D, 0);
CEREAL_REGISTER_TYPE(LI::detector::ExponentialDistribution1D);
CEREAL_REGISTER_POLYMORPHIC_RELATION(LI::detector::Distribution1D, LI::detector::ExponentialDistribution1D);

#endif // LI_ExponentialDistribution1D_H
