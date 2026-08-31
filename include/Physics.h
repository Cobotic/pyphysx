/**
 * Copyright (c) CTU  - All Rights Reserved
 * Created on: 4/30/20
 *     Author: Vladimir Petrik <vladimir.petrik@cvut.cz>
 *
 *     Wrapper for physics, foundation, cooking, and dispatcher for scenes workload management.
 *     Implements singleton patterns and therefore ensures that physics is created only once.
 */

#ifndef SIM_PHYSX_PHYSICS_H
#define SIM_PHYSX_PHYSICS_H

#include <PxPhysicsAPI.h>
#include <cmath>
#include <cstdlib>
#include <iostream>
class Physics {

public:
    static Physics &get() {
        static Physics instance;
        return instance;
    }

    static auto get_physics() {
        return Physics::get().physics;
    }

    static auto init_gpu() {
#if !defined(__aarch64__) and !__APPLE__ and !defined(_WIN64) and !defined(_WIN32)
        physx::PxCudaContextManagerDesc desc;
        desc.interopMode = physx::PxCudaInteropMode::NO_INTEROP;
        Physics::get().cuda_context_manager = PxCreateCudaContextManager(*Physics::get().foundation, desc);
        if (Physics::get().cuda_context_manager) {
            if (!Physics::get().cuda_context_manager->contextIsValid()) {
                Physics::get().cuda_context_manager->release();
                Physics::get().cuda_context_manager = nullptr;
            }
        }
#endif
    }

    /** @brief Set number of CPU used for all scenes computation. */
    static void set_num_cpu(int num_cpu) {
        Physics::get().dispatcher = physx::PxDefaultCpuDispatcherCreate(num_cpu);
    }

    Physics(Physics const &) = delete;

    void operator=(Physics const &) = delete;

    virtual ~Physics() {
        std::cout << "DELETING PHYSX" << std::endl;
#define SAFE_RELEASE(x)    if(x)    { x->release(); x = nullptr;    }
        release_all_scenes();
        SAFE_RELEASE(dispatcher);
#if !defined(__aarch64__) and !__APPLE__
        SAFE_RELEASE(cuda_context_manager);
#endif
        SAFE_RELEASE(cooking);
        SAFE_RELEASE(physics);
        SAFE_RELEASE(foundation);
    }

private:
    static float scale_from_environment(const char *name, float fallback) {
        const char *value = std::getenv(name);
        if (value == nullptr || value[0] == '\0') {
            return fallback;
        }
        char *end = nullptr;
        const float parsed = std::strtof(value, &end);
        if (end == value || *end != '\0' || !std::isfinite(parsed) || parsed <= 0.0f) {
            std::cerr << "Ignoring invalid positive PhysX scale " << name
                      << "=" << value << std::endl;
            return fallback;
        }
        return parsed;
    }

    Physics() {
        using namespace physx;
        PxTolerancesScale scale;
        scale.length = scale_from_environment("DEEPOSE_PHYSX_TOLERANCE_LENGTH", scale.length);
        scale.speed = scale_from_environment("DEEPOSE_PHYSX_TOLERANCE_SPEED", scale.speed);
        foundation = PxCreateFoundation(PX_PHYSICS_VERSION, allocator, error_callback);
        physics = PxCreatePhysics(PX_PHYSICS_VERSION, *foundation, scale);
        auto params = PxCookingParams(scale);
        params.buildGPUData = true;
        cooking = PxCreateCooking(PX_PHYSICS_VERSION, *foundation, params);
        dispatcher = physx::PxDefaultCpuDispatcherCreate(0);
    }

    void release_all_scenes() {
        std::cout << "RELEASE ALL SCENES" << std::endl;
        std::vector<physx::PxScene *> scenes(physics->getNbScenes());
        physics->getScenes(&scenes[0], scenes.size());
        for (auto &scene : scenes) {
            scene->release();
        }
    }

public:
    physx::PxDefaultAllocator allocator;
    physx::PxDefaultErrorCallback error_callback;
    physx::PxFoundation *foundation = nullptr;
    physx::PxPhysics *physics = nullptr;
    physx::PxCooking *cooking = nullptr;

    physx::PxDefaultCpuDispatcher *dispatcher = nullptr;
    physx::PxCudaContextManager *cuda_context_manager = nullptr;

};

#endif //SIM_PHYSX_PHYSICS_H
