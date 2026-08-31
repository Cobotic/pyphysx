/**
 * Copyright (c) CTU  - All Rights Reserved
 * Created on: 4/30/20
 *     Author: Vladimir Petrik <vladimir.petrik@cvut.cz>
 */

#ifndef SIM_PHYSX_SCENE_H
#define SIM_PHYSX_SCENE_H

#include <algorithm>

#include <Physics.h>
#include <BasePhysxPointer.h>
#include <RigidDynamic.h>
#include "RigidStatic.h"
#include "Aggregate.h"

class Scene : public BasePhysxPointer<physx::PxScene> {
private:
    static physx::PxFilterFlags ccd_filter_shader(
            physx::PxFilterObjectAttributes attributes0,
            physx::PxFilterData filter_data0,
            physx::PxFilterObjectAttributes attributes1,
            physx::PxFilterData filter_data1,
            physx::PxPairFlags &pair_flags,
            const void *constant_block,
            physx::PxU32 constant_block_size) {
        auto filter_flags = physx::PxDefaultSimulationFilterShader(
                attributes0, filter_data0, attributes1, filter_data1,
                pair_flags, constant_block, constant_block_size);
        if (!physx::PxFilterObjectIsTrigger(attributes0)
                && !physx::PxFilterObjectIsTrigger(attributes1)) {
            pair_flags |= physx::PxPairFlag::eDETECT_CCD_CONTACT;
        }
        return filter_flags;
    }

public:
    Scene(const physx::PxFrictionType::Enum &friction_type,
          const physx::PxBroadPhaseType::Enum &broad_phase_type,
          const std::vector<physx::PxSceneFlag::Enum> &scene_flags,
          const physx::PxSolverType::Enum &solver_type,
          size_t gpu_max_num_partitions,
          float gpu_dynamic_allocation_scale
    ) : BasePhysxPointer() {
        physx::PxSceneDesc sceneDesc(Physics::get().physics->getTolerancesScale());
        sceneDesc.cpuDispatcher = Physics::get().dispatcher;
        sceneDesc.cudaContextManager = Physics::get().cuda_context_manager;
        const bool enable_ccd = std::find(
                scene_flags.begin(), scene_flags.end(),
                physx::PxSceneFlag::eENABLE_CCD) != scene_flags.end();
        sceneDesc.filterShader = enable_ccd
                ? ccd_filter_shader
                : physx::PxDefaultSimulationFilterShader;
        sceneDesc.gravity = physx::PxVec3(0.0f, 0.0f, -9.81f);
        sceneDesc.solverType = solver_type;
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

    void set_gravity(const physx::PxVec3 &gravity) {
        get_physx_ptr()->setGravity(gravity);
    }

    auto get_gravity() {
        return get_physx_ptr()->getGravity();
    }

    void set_bounce_threshold_velocity(float velocity) {
        get_physx_ptr()->setBounceThresholdVelocity(velocity);
    }

    auto get_bounce_threshold_velocity() {
        return get_physx_ptr()->getBounceThresholdVelocity();
    }

    /** @brief Simulate scene for given amount of time dt and fetch results with blocking. */
    void simulate(float dt, int niters=1) {
        for(int i=0; i<niters; i++) {            
            get_physx_ptr()->simulate(dt);        
            get_physx_ptr()->fetchResults(true);
            simulation_time += dt;
        }
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

    size_t get_nb_sleeping_dynamic_actors() {
        const auto n = get_physx_ptr()->getNbActors(physx::PxActorTypeFlag::eRIGID_DYNAMIC);
        std::vector<physx::PxActor *> actors(n);
        get_physx_ptr()->getActors(physx::PxActorTypeFlag::eRIGID_DYNAMIC, actors.data(), n);
        size_t sleeping = 0;
        for (auto *actor : actors) {
            auto *dynamic_actor = static_cast<physx::PxRigidDynamic *>(actor);
            sleeping += dynamic_actor->isSleeping() ? 1 : 0;
        }
        return sleeping;
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
