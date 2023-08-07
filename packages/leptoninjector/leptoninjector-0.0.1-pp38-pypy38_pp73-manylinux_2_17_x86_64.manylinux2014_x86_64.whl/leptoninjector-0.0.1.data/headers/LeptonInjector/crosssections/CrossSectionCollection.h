#pragma once
#ifndef LI_CrossSectionCollection_H
#define LI_CrossSectionCollection_H

#include <map>
#include <set>
#include <memory>
#include <string>
#include <stdexcept>

#include <cereal/cereal.hpp>
#include <cereal/archives/json.hpp>
#include <cereal/archives/binary.hpp>
#include <cereal/types/vector.hpp>
#include <cereal/types/polymorphic.hpp>
#include <cereal/types/base_class.hpp>
#include <cereal/types/utility.hpp>

#include "LeptonInjector/dataclasses/Particle.h"
#include "LeptonInjector/dataclasses/InteractionSignature.h"
#include "LeptonInjector/dataclasses/InteractionRecord.h"

#include "LeptonInjector/crosssections/CrossSection.h"
#include "LeptonInjector/crosssections/Decay.h"

namespace LI {
namespace crosssections {

class CrossSectionCollection{
private:
    LI::dataclasses::Particle::ParticleType primary_type;
    std::vector<std::shared_ptr<CrossSection>> cross_sections;
    std::vector<std::shared_ptr<Decay>> decays;
    std::map<LI::dataclasses::Particle::ParticleType, std::vector<std::shared_ptr<CrossSection>>> cross_sections_by_target;
    std::set<LI::dataclasses::Particle::ParticleType> target_types;
    static const std::vector<std::shared_ptr<CrossSection>> empty;
    void InitializeTargetTypes();
public:
    CrossSectionCollection();
    virtual ~CrossSectionCollection() {};
    CrossSectionCollection(LI::dataclasses::Particle::ParticleType primary_type, std::vector<std::shared_ptr<CrossSection>> cross_sections);
    CrossSectionCollection(LI::dataclasses::Particle::ParticleType primary_type, std::vector<std::shared_ptr<Decay>> decays);
    CrossSectionCollection(LI::dataclasses::Particle::ParticleType primary_type, std::vector<std::shared_ptr<CrossSection>> cross_sections, std::vector<std::shared_ptr<Decay>> decays);
    bool operator==(CrossSectionCollection const & other) const;
    std::vector<std::shared_ptr<CrossSection>> const & GetCrossSections() const {return cross_sections;}
    std::vector<std::shared_ptr<Decay>> const & GetDecays() const {return decays;}
    bool const HasCrossSections() const {return cross_sections.size() > 0;}
    bool const HasDecays() const {return decays.size() > 0;}
    std::vector<std::shared_ptr<CrossSection>> const & GetCrossSectionsForTarget(LI::dataclasses::Particle::ParticleType p) const;
    std::map<LI::dataclasses::Particle::ParticleType, std::vector<std::shared_ptr<CrossSection>>> const & GetCrossSectionsByTarget() const {
        return cross_sections_by_target;
    };
    std::set<LI::dataclasses::Particle::ParticleType> const & TargetTypes() const {
        return target_types;
    };
    double TotalDecayWidth(LI::dataclasses::InteractionRecord const & record) const;
    double TotalDecayLength(LI::dataclasses::InteractionRecord const & record) const;
    virtual bool MatchesPrimary(dataclasses::InteractionRecord const & record) const;
public:
    template<class Archive>
    void save(Archive & archive, std::uint32_t const version) const {
        if(version == 0) {
            archive(cereal::make_nvp("PrimaryType", primary_type));
            archive(cereal::make_nvp("CrossSections", cross_sections));
            archive(cereal::make_nvp("Decays", decays));
        } else {
            throw std::runtime_error("CrossSectionCollection only supports version <= 0!");
        }
    }

    template<class Archive>
    void load(Archive & archive, std::uint32_t const version) {
        if(version == 0) {
            archive(cereal::make_nvp("PrimaryType", primary_type));
            archive(cereal::make_nvp("CrossSections", cross_sections));
            archive(cereal::make_nvp("Decays", decays));
        } else {
            throw std::runtime_error("CrossSectionCollection only supports version <= 0!");
        }
    }
};

} // namespace crosssections
} // namespace LI

CEREAL_CLASS_VERSION(LI::crosssections::CrossSectionCollection, 0);

#endif // LI_CrossSectionCollection_H
