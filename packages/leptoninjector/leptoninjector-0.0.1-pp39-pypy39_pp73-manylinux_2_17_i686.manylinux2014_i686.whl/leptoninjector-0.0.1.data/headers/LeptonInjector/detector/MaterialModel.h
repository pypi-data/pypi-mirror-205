#pragma once
#ifndef LI_MaterialModel_H
#define LI_MaterialModel_H

#include <map>
#include <string>
#include <vector>

#include <cereal/cereal.hpp>
#include <cereal/archives/json.hpp>
#include <cereal/archives/binary.hpp>
#include <cereal/types/vector.hpp>
#include <cereal/types/array.hpp>
#include <cereal/types/set.hpp>
#include <cereal/types/map.hpp>
#include <cereal/types/polymorphic.hpp>
#include <cereal/types/base_class.hpp>
#include <cereal/types/utility.hpp>

#include "LeptonInjector/serialization/array.h"
#include "LeptonInjector/dataclasses/Particle.h"
#include "LeptonInjector/utilities/Constants.h"

namespace LI {
namespace detector {

class MaterialModel {
    static constexpr const int CHAR_BUF_SIZE = 8196;
    static constexpr const double electron_molar_mass = 5.4857990888e-4; // g per mol
public:
    static const std::map<std::tuple<int, int, int, int>, double> atomic_masses;
    struct Component {
        LI::dataclasses::Particle::ParticleType type = LI::dataclasses::Particle::ParticleType::unknown;
        int strange_count = 0;
        int neutron_count = 0;
        int nucleon_count = 0;
        int proton_count = 0;
        double molar_mass = 0;
        bool is_atom = true;
        Component() {}
        Component(LI::dataclasses::Particle::ParticleType type);
        bool operator==(Component const & component) const;
        template<class Archive>
        void serialize(Archive & archive, std::uint32_t const version) {
            if(version == 0) {
                archive(cereal::make_nvp("ParticleType", type));
                archive(cereal::make_nvp("StrangeCount", strange_count));
                archive(cereal::make_nvp("NeutronCount", neutron_count));
                archive(cereal::make_nvp("NucleonCount", nucleon_count));
                archive(cereal::make_nvp("ProtonCount", proton_count));
                archive(cereal::make_nvp("MolarMass", molar_mass));
                archive(cereal::make_nvp("IsAtom", is_atom));
            } else {
                throw std::runtime_error("Component only supports version <= 0!");
            }
        }
    };
    struct MaterialComponent {
        MaterialComponent() {}
        Component component;
        // Represents fraction of material mass that this consists of this component
        double mass_density_over_total_mass_density; // (g * cm^-3) / (g * cm^-3) --> dimensionless
        // Represents number of component particles per gram of material
        double particle_density_over_total_mass_density; // (#particles * cm^-3) / (g * cm^-3) --> (#particles * g^-1)
        bool operator==(MaterialComponent const & component) const;
        template<class Archive>
        void serialize(Archive & archive, std::uint32_t const version) {
            if(version == 0) {
                archive(cereal::make_nvp("Component", component));
                archive(cereal::make_nvp("MassFraction", mass_density_over_total_mass_density));
                archive(cereal::make_nvp("ParticleFraction", particle_density_over_total_mass_density));
            } else {
                throw std::runtime_error("MaterialComponent only supports version <= 0!");
            }
        }
    };
private:
    std::string path_;
    std::vector<std::string> model_files_;
    std::vector<std::string> material_names_;
    std::map<std::string, int> material_ids_;

    std::vector<std::vector<MaterialComponent>> material_components_;
    std::map<std::pair<int, LI::dataclasses::Particle::ParticleType>, MaterialComponent> material_components_by_id_;
    std::vector<double> material_radiation_length_;
    std::map<std::pair<int, LI::dataclasses::Particle::ParticleType>, double> component_radiation_length_;
public:
    bool operator==(MaterialModel const & component) const;
    template<class Archive>
    void serialize(Archive & archive, std::uint32_t const version) {
        if(version == 0) {
            archive(cereal::make_nvp("Path", path_));
            archive(cereal::make_nvp("ModelFiles", model_files_));
            archive(cereal::make_nvp("MaterialNames", material_names_));
            archive(cereal::make_nvp("MaterialIDs", material_ids_));
            archive(cereal::make_nvp("MaterialComponents", material_components_));
            archive(cereal::make_nvp("MaterialRadiationLength", material_radiation_length_));
            archive(cereal::make_nvp("ComponentRadiationLength", component_radiation_length_));
        } else {
            throw std::runtime_error("MaterialModel only supports version <= 0!");
        }
    }
    MaterialModel();
    MaterialModel(std::string const & file);
    MaterialModel(std::string const & path, std::string const & file);
    MaterialModel(std::vector<std::string> const & files);
    MaterialModel(std::string const & path, std::vector<std::string> const & files);

    void SetPath(std::string const & path);
    void AddMaterial(std::string const & name, std::map<int, double> const & matratios);
    void AddModelFiles(std::vector<std::string> const & matratios);
    void AddModelFile(std::string matratio);

    std::vector<LI::dataclasses::Particle::ParticleType> GetMaterialTargets(int material_id) const;
    double GetMaterialRadiationLength(int material_id) const;
    std::string GetMaterialName(int material_id) const;
    int GetMaterialId(std::string const & material_name) const;
    bool HasMaterial(std::string const & material_name) const;
    bool HasMaterial(int material_id) const;

    double GetTargetMassFraction(int material_id, LI::dataclasses::Particle::ParticleType) const;
    double GetTargetParticleFraction(int material_id, LI::dataclasses::Particle::ParticleType) const;
    std::vector<double> GetTargetMassFraction(int material_id, std::vector<LI::dataclasses::Particle::ParticleType> const &) const;
    std::vector<double> GetTargetParticleFraction(int material_id, std::vector<LI::dataclasses::Particle::ParticleType> const &) const;

    template<typename Iterator, typename = typename std::enable_if<std::is_same<LI::dataclasses::Particle::ParticleType, typename Iterator::value_type>::value, Iterator>::type>
    std::vector<double> GetTargetMassFraction(int material_id, Iterator begin, Iterator end) const;
    template<typename Iterator, typename = typename std::enable_if<std::is_same<LI::dataclasses::Particle::ParticleType, typename Iterator::value_type>::value, Iterator>::type>
    std::vector<double> GetTargetParticleFraction(int material_id, Iterator begin, Iterator end) const;

    std::vector<double> GetTargetRadiationFraction(int material_id, std::vector<LI::dataclasses::Particle::ParticleType> const &) const;
    template<typename Iterator, typename = typename std::enable_if<std::is_same<LI::dataclasses::Particle::ParticleType, typename Iterator::value_type>::value, Iterator>::type>
    std::vector<double> GetTargetRadiationFraction(int material_id, Iterator begin, Iterator end) const;

    std::vector<LI::dataclasses::Particle::ParticleType> GetMaterialConstituents(int material_id) const;
private:
    double ComputeMaterialRadiationLength(int id) const;
public:
    static int GetNucleonContent(int code, int & num_strange, int & num_neutrons, int & num_protons, int & num_nucleons);
    static double GetMolarMass(LI::dataclasses::Particle::ParticleType particle);
    static int GetStrangeCount(LI::dataclasses::Particle::ParticleType particle);
    static int GetNucleonCount(LI::dataclasses::Particle::ParticleType particle);
    static int GetNeutronCount(LI::dataclasses::Particle::ParticleType particle);
    static int GetProtonCount(LI::dataclasses::Particle::ParticleType particle);
    static int GetEmpericalNuclearBindingEnergy(int num_strange, int num_neutrons, int num_protons, int num_nucleons);
};

} // namespace detector
} // namespace LI

CEREAL_CLASS_VERSION(LI::detector::MaterialModel, 0);
CEREAL_CLASS_VERSION(LI::detector::MaterialModel::Component, 0);
CEREAL_CLASS_VERSION(LI::detector::MaterialModel::MaterialComponent, 0);

#include "LeptonInjector/detector/MaterialModel.tcc"

# endif // LI_MaterialModel_H

