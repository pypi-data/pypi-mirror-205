#pragma once
#ifndef LI_SecondaryPositionDistribution_H
#define LI_SecondaryPositionDistribution_H

#include <memory>
#include <string>

#include <cereal/access.hpp>
#include <cereal/types/set.hpp>
#include <cereal/types/polymorphic.hpp>
#include <cereal/types/base_class.hpp>
#include <cereal/types/utility.hpp>

#include "LeptonInjector/dataclasses/Particle.h"

#include "LeptonInjector/math/Vector3D.h"

#include "LeptonInjector/geometry/Geometry.h"

#include "LeptonInjector/distributions/Distributions.h"
#include "LeptonInjector/distributions/primary/vertex/VertexPositionDistribution.h"

namespace LI {
namespace utilities {
class LI_random;
} // namespace utilities

namespace detector {
class EarthModel;
} // namespace detector

namespace dataclasses {
struct InteractionRecord;
struct InteractionSignature;
}
namespace crosssections {
class CrossSectionCollection;
} // namespace crosssections
} // namespace LeptonInjector

namespace LI {
namespace distributions {

class SecondaryPositionDistribution : virtual public VertexPositionDistribution {
friend cereal::access;
private:
    double max_length = std::numeric_limits<double>::infinity();
    std::shared_ptr<const LI::geometry::Geometry> fiducial = NULL;


    LI::math::Vector3D SamplePosition(std::shared_ptr<LI::utilities::LI_random> rand, std::shared_ptr<LI::detector::EarthModel const> earth_model, std::shared_ptr<LI::crosssections::CrossSectionCollection const> cross_sections, LI::dataclasses::InteractionRecord & record) const override;
    LI::math::Vector3D SamplePosition(std::shared_ptr<LI::utilities::LI_random> rand, std::shared_ptr<LI::detector::EarthModel const> earth_model, std::shared_ptr<LI::crosssections::CrossSectionCollection const> cross_sections, LI::dataclasses::InteractionTreeDatum & datum) const override;
public:
    virtual void Sample(std::shared_ptr<LI::utilities::LI_random> rand, std::shared_ptr<LI::detector::EarthModel const> earth_model, std::shared_ptr<LI::crosssections::CrossSectionCollection const> cross_sections, LI::dataclasses::InteractionTreeDatum & datum) const override;
    virtual void Sample(std::shared_ptr<LI::utilities::LI_random> rand, std::shared_ptr<LI::detector::EarthModel const> earth_model, std::shared_ptr<LI::crosssections::CrossSectionCollection const> cross_sections, LI::dataclasses::InteractionRecord & record) const override;
    virtual double GenerationProbability(std::shared_ptr<LI::detector::EarthModel const> earth_model, std::shared_ptr<LI::crosssections::CrossSectionCollection const> cross_sections, LI::dataclasses::InteractionRecord const & record) const override;
    virtual double GenerationProbability(std::shared_ptr<LI::detector::EarthModel const> earth_model, std::shared_ptr<LI::crosssections::CrossSectionCollection const> cross_sections, LI::dataclasses::InteractionTreeDatum const & datum) const override;
    SecondaryPositionDistribution();
    SecondaryPositionDistribution(const SecondaryPositionDistribution &) = default;
    SecondaryPositionDistribution(double max_length);
    SecondaryPositionDistribution(double max_length, std::shared_ptr<LI::geometry::Geometry> fiducial);
    SecondaryPositionDistribution(std::shared_ptr<const LI::geometry::Geometry> fiducial);
    std::string Name() const override;
    virtual std::pair<LI::math::Vector3D, LI::math::Vector3D> InjectionBounds(std::shared_ptr<LI::detector::EarthModel const> earth_model, std::shared_ptr<LI::crosssections::CrossSectionCollection const> cross_sections, LI::dataclasses::InteractionRecord const & interaction) const override;
    virtual std::pair<LI::math::Vector3D, LI::math::Vector3D> InjectionBounds(std::shared_ptr<LI::detector::EarthModel const> earth_model, std::shared_ptr<LI::crosssections::CrossSectionCollection const> cross_sections, LI::dataclasses::InteractionTreeDatum const & datum) const override;
    virtual std::shared_ptr<InjectionDistribution> clone() const override;
    template<typename Archive>
    void save(Archive & archive, std::uint32_t const version) const {
        if(version == 0) {
            archive(::cereal::make_nvp("MaxLength", max_length));
            archive(cereal::virtual_base_class<VertexPositionDistribution>(this));
        } else {
            throw std::runtime_error("SecondaryPositionDistribution only supports version <= 0!");
        }
    }
    template<typename Archive>
    static void load_and_construct(Archive & archive, cereal::construct<SecondaryPositionDistribution> & construct, std::uint32_t const version) {
        if(version == 0) {
            double max_length;
            archive(::cereal::make_nvp("MaxLength", max_length));
            construct(max_length);
            archive(cereal::virtual_base_class<VertexPositionDistribution>(construct.ptr()));
        } else {
            throw std::runtime_error("SecondaryPositionDistribution only supports version <= 0!");
        }
    }
protected:
    virtual bool equal(WeightableDistribution const & distribution) const override;
    virtual bool less(WeightableDistribution const & distribution) const override;
};

} // namespace distributions
} // namespace LI

CEREAL_CLASS_VERSION(LI::distributions::SecondaryPositionDistribution, 0);
CEREAL_REGISTER_TYPE(LI::distributions::SecondaryPositionDistribution);
CEREAL_REGISTER_POLYMORPHIC_RELATION(LI::distributions::VertexPositionDistribution, LI::distributions::SecondaryPositionDistribution);

#endif // LI_SecondaryPositionDistribution_H
