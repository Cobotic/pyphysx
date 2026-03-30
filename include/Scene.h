/**
 * Copyright (c) CTU  - All Rights Reserved
 * Created on: 4/30/20
 *     Author: Vladimir Petrik <vladimir.petrik@cvut.cz>
 */

#ifndef SIM_PHYSX_SCENE_H
#define SIM_PHYSX_SCENE_H

#include <Physics.h>
#include <BasePhysxPointer.h>
#include <RigidDynamic.h>
#include "RigidStatic.h"
#include "Aggregate.h"

#include "Gripper.h"
#include "Geometry.h"
#include <iostream>

class Scene : public BasePhysxPointer<physx::PxScene> {
public:
    Scene(const physx::PxFrictionType::Enum &friction_type,
          const physx::PxBroadPhaseType::Enum &broad_phase_type,
          const std::vector<physx::PxSceneFlag::Enum> &scene_flags,
          size_t gpu_max_num_partitions,
          float gpu_dynamic_allocation_scale
    ) : BasePhysxPointer() {
        physx::PxSceneDesc sceneDesc(Physics::get().physics->getTolerancesScale());
        sceneDesc.cpuDispatcher = Physics::get().dispatcher;
        sceneDesc.cudaContextManager = Physics::get().cuda_context_manager;
        sceneDesc.filterShader = physx::PxDefaultSimulationFilterShader;
        sceneDesc.gravity = physx::PxVec3(0.0f, 0.0f, -9.81f);
        for (const auto &flag : scene_flags) {
            sceneDesc.flags |= flag;
        }
        sceneDesc.frictionType = friction_type;
        sceneDesc.broadPhaseType = broad_phase_type;
        sceneDesc.gpuMaxNumPartitions = gpu_max_num_partitions;
        sceneDesc.gpuDynamicsConfig.patchStreamSize *= gpu_dynamic_allocation_scale;
        sceneDesc.gpuDynamicsConfig.forceStreamCapacity *= gpu_dynamic_allocation_scale;
        sceneDesc.gpuDynamicsConfig.contactBufferCapacity *= gpu_dynamic_allocation_scale;
        sceneDesc.gpuDynamicsConfig.contactStreamSize *= gpu_dynamic_allocation_scale;
        sceneDesc.gpuDynamicsConfig.foundLostPairsCapacity *= gpu_dynamic_allocation_scale;
        sceneDesc.gpuDynamicsConfig.constraintBufferCapacity *= gpu_dynamic_allocation_scale;
        sceneDesc.gpuDynamicsConfig.heapCapacity *= gpu_dynamic_allocation_scale;
        sceneDesc.gpuDynamicsConfig.tempBufferCapacity *= gpu_dynamic_allocation_scale;

        set_physx_ptr(Physics::get().physics->createScene(sceneDesc));
    }

    /** @brief Simulate scene for given amount of time dt and fetch results with blocking. */
    void simulate(float dt, int niters=1) {
        for(int i=0; i<niters; i++) {            
            get_physx_ptr()->simulate(dt);        
            get_physx_ptr()->fetchResults(true);
        }
        
        simulation_time += dt*niters;
        
    }

    void simbin(float dt, int niters=1) {
        // std::cout << "Simulating scene for " << dt*niters << " seconds." << std::endl;
        int i = 0;
        // for(int i=0; i<niters; i++) {            
        const auto n = get_physx_ptr()->getNbActors(physx::PxActorTypeFlag::eRIGID_DYNAMIC);
        std::vector<physx::PxRigidDynamic *> actors(n);
        get_physx_ptr()->getActors(physx::PxActorTypeFlag::eRIGID_DYNAMIC,
            reinterpret_cast<physx::PxActor **>(&actors[0]), n);
        while (true) {
            i++;
            get_physx_ptr()->simulate(dt);        
            get_physx_ptr()->fetchResults(true);
            // auto dynamic_actors = get_dynamic_rigid_actors();
            // std::cout << i <<": " << "Number of dynamic actors: " << n << std::endl;
                
            int nMoving = 0;
            int xyoutside = 0;
            int zoutside = 0;
            for (const auto &actor : actors) {
                physx::PxTransform pose = actor->getGlobalPose();
                if (pose.p.x < -.3 && pose.p.x > .3 || pose.p.y < -.3 && pose.p.y > .3) {
                    xyoutside++;
                    actor->setLinearVelocity(physx::PxVec3(0, 0, 0));
                    actor->setGlobalPose(physx::PxTransform(physx::PxVec3(0, 0, 0.1f)));
                }
                if (pose.p.z < 0 || pose.p.z > 1) {
                    zoutside++;
                    actor->setLinearVelocity(physx::PxVec3(0, 0, 0));
                    actor->setGlobalPose(physx::PxTransform(physx::PxVec3(pose.p.x, pose.p.y, 0.1f)));
                }
                if (pose.p.x > -1 && pose.p.x < 1 &&
                    pose.p.y > -1 && pose.p.y < 1 &&
                    pose.p.z > 0 && pose.p.z < 1) {
                    // std::cout << "Actor is within the specified bounds." << std::endl;
                    physx::PxVec3 velocity = actor->getLinearVelocity();
                    float speed = velocity.magnitude();
                    if (speed > 0.1) {
                        // std::cout << "Actor is moving." << std::endl;
                        nMoving++;
                    } else {
                        // std::cout << "Actor is not moving." << std::endl;
                    }
                    
                }
               
            }
            if (xyoutside > 0) {
                // std::cout << "Warning: " << xyoutside << " actors are outside the XY bounds." << std::endl;
            }
            if (zoutside > 0) {
                // std::cout << "Warning: " << zoutside << " actors are outside the Z bounds." << std::endl;
            }
            // std::cout << "Number of moving actors: " << nMoving << std::endl;
            if (nMoving == 0) {
                break;
            }
        }
        // std::cout << "Simulation finished after " << i << " iterations." << std::endl;
        // std::cout << "Simulation time: " << dt*i << " seconds." << std::endl;
        simulation_time += dt*niters;
    }

    
    
    // std::vector<std::vector<bool>>  all_collisions(std::vector<BoxGeometry> bboxes) {
    //     std::vector<physx::PxBoxGeometry *> bboxes_physx;
    //     for (const auto &bbox : bboxes) {
    //         bboxes_physx.emplace_back(bbox.get_physx_ptr());
    //     }
    //     return all_collisions(bboxes_physx);
    // }
    std::vector<std::vector<float>>  all_collisions() {
        const auto n = get_physx_ptr()->getNbActors(physx::PxActorTypeFlag::eRIGID_DYNAMIC);
        std::vector<physx::PxRigidActor *> pieces(n);
        get_physx_ptr()->getActors(physx::PxActorTypeFlag::eRIGID_DYNAMIC,
            reinterpret_cast<physx::PxActor **>(&pieces[0]), n);
        // std::vector<physx::PxRigidActor*> test_pieces; // Test pieces
        std::vector<physx::PxBoxGeometry *> bboxes; // Test bounding boxes
        std::vector<std::vector<std::vector<physx::PxTransform>>> test_world2bboxes; // Test transforms
        std::vector<physx::PxRigidActor*> extras; // Test other actors

        // Initialize test arguments
        // test_pieces = actors; // Use all dynamic actors as test pieces

        // Create test bounding boxes
        int ngrips = 14;
        int nparts = 1;
        for (int i = 0; i < nparts; ++i) {
            // Create a box geometry for each part
            // bboxes.push_back(new physx::PxBoxGeometry(0.1f, 0.1f, 0.1f)); // Example bounding box size
            bboxes.push_back(new physx::PxBoxGeometry(0.1f, 0.1f, 0.1f)); // Example bounding box size
        }
        // bboxes.push_back(new physx::PxBoxGeometry(0.1f, 0.1f, 0.1f)); // Example bounding box size
        // bboxes.push_back(new physx::PxBoxGeometry(0.1f, 0.1f, 0.1f)); // Example bounding box size
        // bboxes.push_back(new physx::PxBoxGeometry(0.1f, 0.1f, 0.1f)); // Example bounding box size
        
        // Create test transforms
        for (size_t i = 0; i < pieces.size(); ++i) {
            std::vector<std::vector<physx::PxTransform>> transforms;
            for (size_t j = 0; j < ngrips; ++j) { // Example: one transform per piece
                std::vector<physx::PxTransform> sub;
                for (size_t k = 0; k < bboxes.size(); ++k) {
                    // Create a transform for each bounding box
                    sub.emplace_back(pieces[i]->getGlobalPose()); // * physx::PxTransform(physx::PxVec3(0.1f * j, 0.0f, 0.0f)));
                }
                transforms.push_back(sub);
            }
            test_world2bboxes.push_back(transforms);
        }

        // Add other actors (e.g., static actors) to test_others
        const auto static_n = get_physx_ptr()->getNbActors(physx::PxActorTypeFlag::eRIGID_STATIC);
        std::vector<physx::PxRigidStatic *> static_actors(static_n);
        get_physx_ptr()->getActors(physx::PxActorTypeFlag::eRIGID_STATIC,
            reinterpret_cast<physx::PxActor **>(&static_actors[0]), static_n);
        // extras.insert(extras.end(), static_actors.begin(), static_actors.end());
        // Call compute_collisions with test arguments
        std::cout << "Calling compute_collisions..." << std::endl;
        auto start_time = std::chrono::high_resolution_clock::now();
        std::vector<std::vector<float>> test_collisions = compute_gripper_collisions(pieces, bboxes, test_world2bboxes, extras);
        auto end_time = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> delta_time = end_time - start_time;
        std::cout << "Delta time: " << delta_time.count() << " seconds." << std::endl;
        std::cout << "Collisions computed." << std::endl;
        for (size_t i = 0; i < test_collisions.size(); ++i) {
            for (size_t j = 0; j < test_collisions[i].size(); ++j) {
                // std::cout << "Collision[" << i << "][" << j << "] = " << (test_collisions[i][j] ? "true" : "false") << std::endl;
            }
        }
        // Return the test collisions
        return test_collisions;
    }
    void release() {
        get_physx_ptr()->release();
    }
    void add_actor(RigidActor actor) {
        get_physx_ptr()->addActor(*actor.get_physx_ptr());
    }

    auto get_static_rigid_actors() {
        const auto n = get_physx_ptr()->getNbActors(physx::PxActorTypeFlag::eRIGID_STATIC);
        std::vector<physx::PxRigidActor *> actors(n);
        get_physx_ptr()->getActors(physx::PxActorTypeFlag::eRIGID_STATIC,
                                   reinterpret_cast<physx::PxActor **>(&actors[0]), n);
        return from_vector_of_physx_ptr<RigidActor>(actors);
    }

    auto get_dynamic_rigid_actors() {
        const auto n = get_physx_ptr()->getNbActors(physx::PxActorTypeFlag::eRIGID_DYNAMIC);
        std::vector<physx::PxRigidDynamic *> actors(n);
        get_physx_ptr()->getActors(physx::PxActorTypeFlag::eRIGID_DYNAMIC,
                                   reinterpret_cast<physx::PxActor **>(&actors[0]), n);
        return from_vector_of_physx_ptr<RigidDynamic, physx::PxRigidDynamic>(actors);
    }

    void add_aggregate(Aggregate agg) {
        get_physx_ptr()->addAggregate(*agg.get_physx_ptr());
    }

    auto get_aggregates() {
        const auto n = get_physx_ptr()->getNbAggregates();
        std::vector<physx::PxAggregate *> aggs(n);
        get_physx_ptr()->getAggregates(&aggs[0], n);
        return from_vector_of_physx_ptr<Aggregate>(aggs);
    }


    
public:
    double simulation_time = 0.;
};

#endif //SIM_PHYSX_SCENE_H
