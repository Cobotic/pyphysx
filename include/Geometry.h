/**
 * Copyright (c) CTU  - All Rights Reserved
 * Created on: 5/1/20
 *     Author: Vladimir Petrik <vladimir.petrik@cvut.cz>
 */

 #ifndef PYPHYSX_GEOMETRY_H
 #define PYPHYSX_GEOMETRY_H
 
 #include <Eigen/Eigen>
 #include <PxPhysicsAPI.h>
 #include <BasePhysxPointer.h>
 #include <Material.h>
 #include <Physics.h>
 #include <transformation_utils.h>
 #include <array>
 
 #ifndef M_PI
 #define M_PI 3.14159265358979323846
 #endif
 
 class BoxGeometry : public BasePhysxPointer<physx::PxBoxGeometry> {
 
 public:
    BoxGeometry(float hx, float hy, float hz) :
        BasePhysxPointer(new physx::PxBoxGeometry(hx, hy, hz)) {
    }
    
    explicit BoxGeometry(physx::PxBoxGeometry *pref) : BasePhysxPointer<physx::PxBoxGeometry>(pref) {}
 };
#endif //PYPHYSX_GEOMETRY_H