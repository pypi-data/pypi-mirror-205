#pragma once
#ifndef LI_RangedLeptonInjector_H
#define LI_RangedLeptonInjector_H

#include <map>
#include <memory>
#include <string>
#include <vector>
#include <utility>
#include <stdexcept>

#include <cereal/cereal.hpp>
#include <cereal/access.hpp>
#include <cereal/archives/json.hpp>
#include <cereal/archives/binary.hpp>
#include <cereal/types/vector.hpp>
#include <cereal/types/polymorphic.hpp>
#include <cereal/types/base_class.hpp>
#include <cereal/types/utility.hpp>

#include "LeptonInjector/detector/EarthModel.h"

#include "LeptonInjector/crosssections/CrossSection.h"

#include "LeptonInjector/dataclasses/InteractionRecord.h"

#include "LeptonInjector/distributions/Distributions.h"
#include "LeptonInjector/distributions/primary/type/PrimaryInjector.h"
#include "LeptonInjector/distributions/primary/energy/PrimaryEnergyDistribution.h"
#include "LeptonInjector/distributions/primary/direction/PrimaryDirectionDistribution.h"
#include "LeptonInjector/distributions/primary/helicity/PrimaryNeutrinoHelicityDistribution.h"
#include "LeptonInjector/distributions/primary/vertex/RangePositionDistribution.h"
#include "LeptonInjector/distributions/target/momentum/TargetMomentumDistribution.h"

#include "LeptonInjector/injection/InjectorBase.h"

namespace LI {
namespace math {
class Vector3D;
}

namespace utilities {
class LI_random;
}

namespace injection {

class RangedLeptonInjector : public InjectorBase {
friend cereal::access;
protected:
    std::shared_ptr<LI::distributions::RangeFunction> range_func;
    double disk_radius;
    double endcap_length;
    std::shared_ptr<LI::distributions::RangePositionDistribution> position_distribution;
    std::shared_ptr<LI::crosssections::CrossSectionCollection> cross_sections;
    RangedLeptonInjector();
public:
    RangedLeptonInjector(unsigned int events_to_inject, std::shared_ptr<LI::detector::EarthModel> earth_model, std::shared_ptr<injection::InjectionProcess> primary_process, std::vector<std::shared_ptr<injection::InjectionProcess>> secondary_processes, std::shared_ptr<LI::utilities::LI_random> random, std::shared_ptr<LI::distributions::RangeFunction> range_func, double disk_radius, double endcap_length);
    std::string Name() const override;
    virtual std::pair<LI::math::Vector3D, LI::math::Vector3D> InjectionBounds(LI::dataclasses::InteractionRecord const & interaction) const override;

    template<typename Archive>
    void save(Archive & archive, std::uint32_t const version) const {
        if(version == 0) {
            archive(::cereal::make_nvp("RangeFunction", range_func));
            archive(::cereal::make_nvp("DiskRadius", disk_radius));
            archive(::cereal::make_nvp("EndcapLength", endcap_length));
            archive(::cereal::make_nvp("PositionDistribution", position_distribution));
            archive(cereal::virtual_base_class<InjectorBase>(this));
        } else {
            throw std::runtime_error("RangedLeptonInjector only supports version <= 0!");
        }
    }

    template<typename Archive>
    void load(Archive & archive, std::uint32_t const version) {
        if(version == 0) {
            archive(::cereal::make_nvp("RangeFunction", range_func));
            archive(::cereal::make_nvp("DiskRadius", disk_radius));
            archive(::cereal::make_nvp("EndcapLength", endcap_length));
            archive(::cereal::make_nvp("PositionDistribution", position_distribution));
            archive(cereal::virtual_base_class<InjectorBase>(this));
        } else {
            throw std::runtime_error("RangedLeptonInjector only supports version <= 0!");
        }
    }
};

} // namespace injection
} // namespace LI

CEREAL_CLASS_VERSION(LI::injection::RangedLeptonInjector, 0);
CEREAL_REGISTER_TYPE(LI::injection::RangedLeptonInjector);
CEREAL_REGISTER_POLYMORPHIC_RELATION(LI::injection::InjectorBase, LI::injection::RangedLeptonInjector);

#endif // LI_RangedLeptonInjector_H
