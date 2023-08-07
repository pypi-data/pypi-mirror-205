#ifndef LI_FixedDirection_H
#define LI_FixedDirection_H

#include <memory>
#include <string>
#include <vector>
#include <utility>
#include <stdexcept>

#include <cereal/access.hpp>
#include <cereal/types/polymorphic.hpp>
#include <cereal/types/base_class.hpp>
#include <cereal/types/utility.hpp>

#include "LeptonInjector/math/Vector3D.h"

#include "LeptonInjector/distributions/Distributions.h"
#include "LeptonInjector/distributions/primary/direction/PrimaryDirectionDistribution.h"

namespace LI {
namespace distributions {

class FixedDirection : virtual public PrimaryDirectionDistribution {
friend cereal::access;
protected:
    FixedDirection() {};
private:
    LI::math::Vector3D dir;
public:
    FixedDirection(LI::math::Vector3D dir) : dir(dir) {};
private:
    LI::math::Vector3D SampleDirection(std::shared_ptr<LI::utilities::LI_random> rand, std::shared_ptr<LI::detector::EarthModel const> earth_model, std::shared_ptr<LI::crosssections::CrossSectionCollection const> cross_sections, LI::dataclasses::InteractionRecord const & record) const override;
    virtual double GenerationProbability(std::shared_ptr<LI::detector::EarthModel const> earth_model, std::shared_ptr<LI::crosssections::CrossSectionCollection const> cross_sections, LI::dataclasses::InteractionRecord const & record) const override;
    virtual std::vector<std::string> DensityVariables() const override;
    virtual std::shared_ptr<InjectionDistribution> clone() const override;
    std::string Name() const override;
    template<typename Archive>
    void save(Archive & archive, std::uint32_t const version) const {
        if(version == 0) {
            archive(::cereal::make_nvp("Direction", dir));
            archive(cereal::virtual_base_class<PrimaryDirectionDistribution>(this));
        } else {
            throw std::runtime_error("FixedDirection only supports version <= 0!");
        }
    }
    template<typename Archive>
    static void load_and_construct(Archive & archive, cereal::construct<FixedDirection> & construct, std::uint32_t const version) {
        if(version == 0) {
            LI::math::Vector3D d;
            archive(::cereal::make_nvp("Direction", d));
            construct(d);
            archive(cereal::virtual_base_class<PrimaryDirectionDistribution>(construct.ptr()));
        } else {
            throw std::runtime_error("FixedDirection only supports version <= 0!");
        }
    }
protected:
    virtual bool equal(WeightableDistribution const & distribution) const override;
    virtual bool less(WeightableDistribution const & distribution) const override;
};

} // namespace distributions
} // namespace LI

CEREAL_CLASS_VERSION(LI::distributions::FixedDirection, 0);
CEREAL_REGISTER_TYPE(LI::distributions::FixedDirection);
CEREAL_REGISTER_POLYMORPHIC_RELATION(LI::distributions::PrimaryDirectionDistribution, LI::distributions::FixedDirection);

#endif // LI_FixedDirection_H
