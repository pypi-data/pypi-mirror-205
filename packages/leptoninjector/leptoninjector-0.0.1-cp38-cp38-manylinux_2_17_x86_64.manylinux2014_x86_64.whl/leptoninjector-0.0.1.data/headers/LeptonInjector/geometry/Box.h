#pragma once
#ifndef LI_Box_H
#define LI_Box_H

#include <map>
#include <math.h>
#include <memory>
#include <vector>
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

class Box : public Geometry {
public:
    Box();
    Box(double x, double y, double z);
    Box(Placement const &);
    Box(Placement const &, double x, double y, double z);
    Box(const Box&);

    template<typename Archive>
    void serialize(Archive & archive, std::uint32_t const version) {
        if(version == 0) {
            archive(::cereal::make_nvp("XWidth", x_));
            archive(::cereal::make_nvp("YWidth", y_));
            archive(::cereal::make_nvp("ZWidth", z_));
            archive(cereal::virtual_base_class<Geometry>(this));
        } else {
            throw std::runtime_error("Box only supports version <= 0!");
        }
    }

    std::shared_ptr<const Geometry> create() const override { return std::shared_ptr<const Geometry>( new Box(*this) ); };
    void swap(Geometry&) override;

    virtual ~Box() {}

    // Operators
    Box& operator=(const Geometry&) override;

    // Methods
    std::pair<double, double> ComputeDistanceToBorder(const math::Vector3D& position, const math::Vector3D& direction) const override;
    std::vector<Intersection> ComputeIntersections(math::Vector3D const & position, math::Vector3D const & direction) const override;

    // Getter & Setter
    double GetX() const { return x_; }
    double GetY() const { return y_; }
    double GetZ() const { return z_; }

    void SetX(double x) { x_ = x; };
    void SetY(double y) { y_ = y; };
    void SetZ(double z) { z_ = z; };
protected:
    virtual bool equal(const Geometry&) const override;
    virtual bool less(const Geometry&) const override;
private:
    void print(std::ostream&) const override;

    double x_; //!< width of box in x-direction
    double y_; //!< width of box in y-direction
    double z_; //!< width of box in z-direction
};


} // namespace geometry
} // namespace LI

CEREAL_CLASS_VERSION(LI::geometry::Box, 0);
CEREAL_REGISTER_TYPE(LI::geometry::Box)
CEREAL_REGISTER_POLYMORPHIC_RELATION(LI::geometry::Geometry, LI::geometry::Box);

#endif // LI_Box_H
