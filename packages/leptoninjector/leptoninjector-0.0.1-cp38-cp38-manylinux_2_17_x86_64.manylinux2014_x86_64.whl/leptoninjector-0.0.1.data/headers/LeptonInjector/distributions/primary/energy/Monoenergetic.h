#pragma once
#ifndef LI_Monoenergetic_H
#define LI_Monoenergetic_H

#include <string>

#include <cereal/access.hpp>
#include <cereal/types/polymorphic.hpp>
#include <cereal/types/base_class.hpp>
#include <cereal/types/utility.hpp>

#include "LeptonInjector/distributions/Distributions.h"
#include "LeptonInjector/distributions/primary/energy/PrimaryEnergyDistribution.h"

namespace LI {
namespace distributions {

class Monoenergetic : virtual public PrimaryEnergyDistribution {
friend cereal::access;
protected:
    Monoenergetic() {};
private:
    double gen_energy;
public:
    Monoenergetic(double gen_energy);
    double pdf(double energy) const;
    double SampleEnergy(std::shared_ptr<LI::utilities::LI_random> rand, std::shared_ptr<LI::detector::EarthModel const> earth_model, std::shared_ptr<LI::crosssections::CrossSectionCollection const> cross_sections, LI::dataclasses::InteractionRecord const & record) const override;
    virtual double GenerationProbability(std::shared_ptr<LI::detector::EarthModel const> earth_model, std::shared_ptr<LI::crosssections::CrossSectionCollection const> cross_sections, LI::dataclasses::InteractionRecord const & record) const override;
    std::string Name() const override;
    virtual std::shared_ptr<InjectionDistribution> clone() const override;
    template<typename Archive>
    void save(Archive & archive, std::uint32_t const version) const {
        if(version == 0) {
            archive(::cereal::make_nvp("GenEnergy", gen_energy));
            archive(cereal::virtual_base_class<PrimaryEnergyDistribution>(this));
        } else {
            throw std::runtime_error("Monoenergetic only supports version <= 0!");
        }
    }
    template<typename Archive>
    static void load_and_construct(Archive & archive, cereal::construct<Monoenergetic> & construct, std::uint32_t const version) {
        if(version == 0) {
            double energy;
            archive(::cereal::make_nvp("GenEnergy", energy));
            construct(energy);
            archive(cereal::virtual_base_class<PrimaryEnergyDistribution>(construct.ptr()));
        } else {
            throw std::runtime_error("Monoenergetic only supports version <= 0!");
        }
    }
protected:
    virtual bool equal(WeightableDistribution const & distribution) const override;
    virtual bool less(WeightableDistribution const & distribution) const override;
};

} // namespace distributions
} // namespace LI

CEREAL_CLASS_VERSION(LI::distributions::Monoenergetic, 0);
CEREAL_REGISTER_TYPE(LI::distributions::Monoenergetic);
CEREAL_REGISTER_POLYMORPHIC_RELATION(LI::distributions::PrimaryEnergyDistribution, LI::distributions::Monoenergetic);

#endif // LI_Monoenergetic_H
