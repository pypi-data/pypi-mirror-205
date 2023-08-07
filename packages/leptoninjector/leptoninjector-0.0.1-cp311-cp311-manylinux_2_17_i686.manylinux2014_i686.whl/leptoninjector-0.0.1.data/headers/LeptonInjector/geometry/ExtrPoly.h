#pragma once
#ifndef LI_ExtrPoly_H
#define LI_ExtrPoly_H

#include <map>
#include <memory>
#include <vector>
#include <math.h>
#include <float.h>
#include <iostream>

#include <cereal/cereal.hpp>
#include <cereal/archives/json.hpp>
#include <cereal/archives/binary.hpp>
#include <cereal/types/polymorphic.hpp>
#include <cereal/types/base_class.hpp>
#include <cereal/types/utility.hpp>

#include "LeptonInjector/math/Vector3D.h"
#include "LeptonInjector/geometry/Placement.h"
#include "LeptonInjector/geometry/Geometry.h"

namespace LI {
namespace geometry {

class ExtrPoly : public Geometry {
public:
    struct ZSection {
        ZSection() {}
        ZSection(double zpos, double offset[2], double scale)
            : zpos(zpos), scale(scale), offset{offset[0],offset[1]} {}

        double zpos;
        double scale;
        std::array<double, 2> offset;
        void operator=(ZSection const & other) {
            zpos = other.zpos;
            scale = other.scale;
            offset[0] = other.offset[0];
            offset[1] = other.offset[1];
        }
        bool operator<(ZSection const & other) const {
            return (this != &other) and
                std::tie(zpos, scale, offset[0], offset[1])
                <
                std::tie(other.zpos, other.scale, other.offset[0], other.offset[1]);
        }
        friend bool operator==(ZSection const & l, ZSection const & r) {
            return (l.zpos == r.zpos &&
                    l.scale == r.scale &&
                    l.offset[0] == r.offset[0] &&
                    l.offset[1] == r.offset[1]);
        }
        template<typename Archive>
        void serialize(Archive & archive, std::uint32_t const version) {
            if(version == 0) {
                archive(::cereal::make_nvp("ZPosition", zpos));
                archive(::cereal::make_nvp("Scale", scale));
                archive(::cereal::make_nvp("Offset", offset));
            } else {
                throw std::runtime_error("ZSection only supports version <= 0!");
            }
        }
    };

    struct plane {
        double a,b,c,d; // a*x + b*y + c*z + d = 0
        template<typename Archive>
        void serialize(Archive & archive, std::uint32_t const version) {
            if(version == 0) {
                archive(::cereal::make_nvp("A", a));
                archive(::cereal::make_nvp("B", b));
                archive(::cereal::make_nvp("C", c));
                archive(::cereal::make_nvp("D", d));
            } else {
                throw std::runtime_error("Plane only supports version <= 0!");
            }
        }
    };

public:
    ExtrPoly();
    ExtrPoly(const std::vector<std::vector<double>>& polygon,
            const std::vector<ZSection>& zsections);
    ExtrPoly(Placement const &);
    ExtrPoly(Placement const &, const std::vector<std::vector<double>>& polygon,
            const std::vector<ZSection>& zsections);
    ExtrPoly(const ExtrPoly&);

    template<typename Archive>
    void serialize(Archive & archive, std::uint32_t const version) {
        if(version == 0) {
            archive(::cereal::make_nvp("Polygons", polygon_));
            archive(::cereal::make_nvp("ZSections", zsections_));
            archive(::cereal::make_nvp("Planes", planes_));
            archive(cereal::virtual_base_class<Geometry>(this));
        } else {
            throw std::runtime_error("Sphere only supports version <= 0!");
        }
    }

    /* Geometry* clone() const override{ return new ExtrPoly(*this); }; */
    std::shared_ptr<const Geometry> create() const override{ return std::shared_ptr<const Geometry>( new ExtrPoly(*this) ); }
    void swap(Geometry&) override;

    virtual ~ExtrPoly() {}

    // Operators
    ExtrPoly& operator=(const Geometry&) override;

    // Methods
    std::pair<double, double> ComputeDistanceToBorder(const math::Vector3D& position, const math::Vector3D& direction) const override;
    std::vector<Intersection> ComputeIntersections(math::Vector3D const & position, math::Vector3D const & direction) const override;

    // Getter & Setter
    std::vector<std::vector<double>> GetPolygon() const { return polygon_; }
    std::vector<ZSection> GetZSections() const { return zsections_; }

    void SetPolygon(std::vector<std::vector<double>> polygon ) { polygon_=polygon; }
    void SetZSections(std::vector<ZSection> zsections) { zsections_=zsections; }

    void ComputeLateralPlanes();

protected:
    virtual bool equal(const Geometry&) const override;
    virtual bool less(const Geometry&) const override;
private:
    void print(std::ostream&) const override;

    std::vector<std::vector<double>> polygon_; //!< vector of (x,y) pairs denoting vertices of polygon
    std::vector<ZSection> zsections_; //!< vector of z sections describing z extent of polygon
    std::vector<plane> planes_;
};

} // namespace geometry
} // namespace LI

CEREAL_CLASS_VERSION(LI::geometry::ExtrPoly, 0);
CEREAL_REGISTER_TYPE(LI::geometry::ExtrPoly)
CEREAL_REGISTER_POLYMORPHIC_RELATION(LI::geometry::Geometry, LI::geometry::ExtrPoly);

#endif // LI_ExtrPoly_H
