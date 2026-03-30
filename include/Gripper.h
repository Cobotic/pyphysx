/**
 * Copyright (c) CTU  - All Rights Reserved
 * Created on: 4/30/20
 *     Author: Vladimir Petrik <vladimir.petrik@cvut.cz>
 */

 #ifndef SIM_PHYSX_GRIPPER_H
 #define SIM_PHYSX_GRIPPER_H
 
 #include <Physics.h>
 #include <BasePhysxPointer.h>
 #include <RigidDynamic.h>
 #include "RigidStatic.h"
 #include "Aggregate.h"
 
 
 #include <iostream>

 std::vector<std::vector<float>> compute_gripper_collisions(
    const std::vector<physx::PxRigidActor*> &pieces, // npieces
    const std::vector<physx::PxBoxGeometry *> &bboxes, // nparts
    const std::vector<std::vector<std::vector<physx::PxTransform>>> &world2bboxes, // npieces x ngrips x nparts
    const std::vector<physx::PxRigidActor *> &extras // nothers
    ) {

    // for (size_t i = 0; i < world2bboxes.size(); ++i) {
    //     std::cout << "world2bboxes[" << i << "]:" << std::endl;
    //     for (size_t j = 0; j < world2bboxes[i].size(); ++j) {
    //         std::cout << "  Grip " << j << ":" << std::endl;
    //         for (size_t k = 0; k < world2bboxes[i][j].size(); ++k) {
    //             const auto& transform = world2bboxes[i][j][k];
    //             std::cout << "    Part " << k << ": Position(" 
    //                       << transform.p.x << ", " 
    //                       << transform.p.y << ", " 
    //                       << transform.p.z << "), Rotation("
    //                       << transform.q.x << ", " 
    //                       << transform.q.y << ", " 
    //                       << transform.q.z << ", " 
    //                       << transform.q.w << ")" << std::endl;
    //         }
    //     }
    // }
    // for (size_t i = 0; i < pieces.size(); ++i) {
    //     const auto& piece = pieces[i];
    //     physx::PxTransform transform = piece->getGlobalPose();
    //     std::cout << "Piece " << i << ": Position(" 
    //               << transform.p.x << ", " 
    //               << transform.p.y << ", " 
    //               << transform.p.z << "), Rotation("
    //               << transform.q.x << ", " 
    //               << transform.q.y << ", " 
    //               << transform.q.z << ", " 
    //               << transform.q.w << ")" << std::endl;
    // }

    // for (size_t i = 0; i < bboxes.size(); ++i) {
    //     std::cout << "BBox " << i << " dimensions: (" 
    //               << bboxes[i]->halfExtents.x * 2 << ", " 
    //               << bboxes[i]->halfExtents.y * 2 << ", " 
    //               << bboxes[i]->halfExtents.z * 2 << ")" << std::endl;
    // }
        // std::cout << "here" << std::endl;
    // std::cout << "Number of pieces: " << pieces.size() << std::endl;
    // for (size_t i = 0; i < pieces.size(); ++i) {
    //     std::cout << "Piece " << i << ": " << pieces[i] << std::endl;
    // }

    // std::cout << "Number of bboxes: " << bboxes.size() << std::endl;
    // for (size_t i = 0; i < bboxes.size(); ++i) {
    //     std::cout << "BBox " << i << ": " << bboxes[i] << std::endl;
    // }

    // std::cout << "Number of world2bboxes entries: " << world2bboxes.size() << std::endl;
    // for (size_t i = 0; i < world2bboxes.size(); ++i) {
    //     std::cout << "world2bboxes[" << i << "] size: " << world2bboxes[i].size() << std::endl;
    //     for (size_t j = 0; j < world2bboxes[i].size(); ++j) {
    //         std::cout << "  world2bboxes[" << i << "][" << j << "] size: " << world2bboxes[i][j].size() << std::endl;
    //     }
    // }

    // std::cout << "Number of extras: " << extras.size() << std::endl;
    // for (size_t i = 0; i < extras.size(); ++i) {
    //     std::cout << "Extra " << i << ": " << extras[i] << std::endl;
    // }
    size_t ngrips = world2bboxes[0].size();
    size_t npieces = pieces.size();
    size_t nparts = bboxes.size();
    std::cout << "ngrips: " << ngrips << ", npieces: " << npieces << ", nparts: " << nparts << std::endl;
    std::vector<std::vector<float>> collisions(npieces, std::vector<float>(ngrips, 0));
    
    std::vector<physx::PxRigidActor *> others;
    others.reserve(pieces.size() + others.size());
    others.insert(others.end(), pieces.begin(), pieces.end());
    others.insert(others.end(), extras.begin(), extras.end());

    std::vector<physx::PxBounds3> precomputedOthers;
    for (const auto &otherActor : others) {
        precomputedOthers.emplace_back(otherActor->getWorldBounds());
    }
    // for (const auto &otherActor : others) {
    //     physx::PxShape* shape;
    //     otherActor->getShapes(&shape, 1);
    //     physx::PxGeometryHolder holder = shape->getGeometry();
    //     physx::PxGeometry otherGeometry = holder.any();
    //     physx::PxBounds3 otherBounds = otherActor->getWorldBounds();
    //     precomputedOthers.emplace_back(otherGeometry, otherBounds);
    // }

    std::cout << "Precomputed others size: " << precomputedOthers.size() << std::endl;
    for (size_t ipiece = 0; ipiece < npieces; ++ipiece) {
        auto piece = pieces[ipiece];
        for (size_t igrip = 0; igrip < ngrips; ++igrip) {
            for (size_t ipart = 0; ipart < nparts; ++ipart) {
                // std::cout << "p: " << p << ", g: " << g << ", part: " << part << std::endl;
                physx::PxTransform bboxTransform = world2bboxes[ipiece][igrip][ipart]; // * pieces2bboxes[p][part];
                auto bbox = bboxes[ipart];
                physx::PxBounds3 bboxBounds = physx::PxGeometryQuery::getWorldBounds(*bbox, bboxTransform);
                for (size_t iother = 0; iother < pieces.size(); ++iother) {
                    // if (other_p == ipiece) continue;
                    auto otherActor = pieces[iother];
                    if (otherActor == piece) continue;
                    
                    // physx::PxBounds3 otherBounds = otherActor->getWorldBounds();
                    // std::cout << "Nect Actor: " << std::endl;
                    // auto other = precomputedOthers[other_p];
                    // const physx::PxGeometry& otherGeometry = other.first;
                    const physx::PxBounds3& otherBounds = precomputedOthers[iother];
                    // std::cout << "Other Geometry: " << typeid(otherGeometry).name() << std::endl;
                    // std::cout << "Other Bounds: " << otherBounds.minimum.x << ", " << otherBounds.minimum.y << ", " << otherBounds.minimum.z
                    //           << " to " << otherBounds.maximum.x << ", " << otherBounds.maximum.y << ", " << otherBounds.maximum.z << std::endl;
                    if (bboxBounds.intersects(otherBounds)){
                        physx::PxShape* shape;
                        otherActor->getShapes(&shape, 1);
                        // std::cout << "INTERSECTS" << ipiece << ", " << iother << std::endl;
                        // if (physx::PxGeometryQuery::overlap(bbox, bboxTransform, otherGeometry, otherActor->getGlobalPose())) {
                        if (physx::PxShapeExt::overlap(*shape, *otherActor, *bbox, bboxTransform)) {
                            physx::PxVec3 direction;
                            float depth;
                            
                            physx::PxGeometryHolder holder = shape->getGeometry();
                            physx::PxGeometry& otherGeometry = holder.any();
                            if (physx::PxGeometryQuery::computePenetration(direction, depth, *bbox, bboxTransform, otherGeometry, otherActor->getGlobalPose())) {
                                if (depth > collisions[ipiece][igrip]) {
                                    collisions[ipiece][igrip] = depth;
                                    // std::cout << "Penetration depth: " << depth << ", Direction: (" 
                                    //         << direction.x << ", " << direction.y << ", " << direction.z << ")" << std::endl;
                                }
                                // break;
                                // std::cout << "Penetration depth: " << depth << ", Direction: (" 
                                //         << direction.x << ", " << direction.y << ", " << direction.z << ")" << std::endl;
                            }
                            // std::cout << "Collision detected between piece " << ipiece << " and grip " << igrip << std::endl;
                        }
                    }
                    
                }

 

                // if (collisions[ipiece][igrip]) break;
            }
        }
    }

    return collisions;
}


class Gripper {
    public:
        std::vector<physx::PxBoxGeometry *> bboxes;
        Gripper(const std::vector<std::tuple<float, float, float>>& extents)
        : bboxes(extents.size()) {
            for (size_t i = 0; i < extents.size(); ++i) {
                const auto& extent = extents[i];
                bboxes[i] = new physx::PxBoxGeometry(std::get<0>(extent)/2, std::get<1>(extent)/2, std::get<2>(extent)/2);
            }
        }
        ~Gripper() {
            for (auto& bbox : bboxes) {
                delete bbox;
            }
        }
        
        std::vector<std::vector<float>> compute_collisions(
            const std::vector<RigidActor*> &pieces, // npieces
            const std::vector<std::vector<std::vector<physx::PxTransform>>> &world2bboxes, // npieces x ngrips x nparts
            const std::vector<RigidActor*> &extras // nothers
        ) {
            // auto physx_pieces = to_vector_of_physx_ptr<physx::PxRigidActor>(pieces);
            std::vector<physx::PxRigidActor *> physx_pieces;
            std::vector<physx::PxRigidActor *> physx_extras;
            for (const auto& piece : pieces) {                
                physx_pieces.push_back(piece->get_physx_ptr());                
            }
            for (const auto& extra : extras) {
                physx_extras.push_back(extra->get_physx_ptr());
            }
            std::cout << "Number of bboxes: " << bboxes.size() << std::endl;
            for (size_t i = 0; i < bboxes.size(); ++i) {
                std::cout << "BBox " << i << " extents: (" 
                          << bboxes[i]->halfExtents.x << ", " 
                          << bboxes[i]->halfExtents.y << ", " 
                          << bboxes[i]->halfExtents.z << ")" << std::endl;
            }
            // return std::vector<std::vector<bool>>(); // Placeholder for the actual implementation
            return compute_gripper_collisions(physx_pieces, bboxes, world2bboxes, physx_extras);
        }
};
 
 
 #endif //SIM_PHYSX_GRIPPER_H
 