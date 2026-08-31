#!/usr/bin/env python

# Copyright (c) CTU  - All Rights Reserved
# Created on: 5/1/20
#     Author: Vladimir Petrik <vladimir.petrik@cvut.cz>

import numpy as np
import unittest
import sys

sys.path.append('lib')

from pyphysx import *


class SceneTestCase(unittest.TestCase):

    def test_simulation_free_fall(self):
        actor = RigidDynamic()
        scene = Scene()
        scene.add_actor(actor)
        for _ in range(480):
            scene.simulate(dt=0.5 / 480)
        expected_distance = -0.5 * 9.81 * scene.simulation_time ** 2
        self.assertAlmostEqual(actor.get_global_pose()[0][2], expected_distance, places=2)

    def test_get_actors(self):
        scene = Scene()
        r1 = RigidDynamic()
        r2 = RigidDynamic()
        r3 = RigidDynamic()
        r1.set_mass(1.)
        r2.set_mass(2.)
        r3.set_mass(3.)
        scene.add_actor(r1)
        scene.add_actor(r2)
        scene.add_actor(r3)
        actors = scene.get_dynamic_rigid_actors()
        self.assertEqual(3, len(actors))
        self.assertAlmostEqual(1., actors[0].get_mass())
        self.assertAlmostEqual(2., actors[1].get_mass())
        self.assertAlmostEqual(3., actors[2].get_mass())

    def test_get_aggregates(self):
        scene = Scene()
        agg = Aggregate()
        agg.add_actor(RigidDynamic())
        agg.add_actor(RigidDynamic())
        agg.add_actor(RigidDynamic())
        scene.add_aggregate(agg)
        agg = Aggregate()
        agg.add_actor(RigidDynamic())
        agg.add_actor(RigidDynamic())
        agg.add_actor(RigidDynamic())
        scene.add_aggregate(agg)

        self.assertEqual(2, len(scene.get_aggregates()))

    def test_swept_ccd_filter_stops_fast_actor_at_thin_floor(self):
        material = Material(restitution=0)
        floor = RigidStatic()
        floor.attach_shape(Shape.create_box([1, 1, 0.01], material))
        floor.set_global_pose([0, 0, -0.005])

        actor = RigidDynamic()
        actor.attach_shape(Shape.create_box([0.01] * 3, material))
        actor.set_mass(0.01)
        actor.set_global_pose([0, 0, 0.1])
        actor.set_linear_velocity([0, 0, -10])
        actor.set_rigid_body_flag(RigidBodyFlag.ENABLE_CCD, True)

        scene = Scene(scene_flags=[SceneFlag.ENABLE_CCD])
        scene.add_actor(floor)
        scene.add_actor(actor)
        scene.simulate(0.02)

        self.assertGreater(actor.get_global_pose()[0][2], 0)

    def test_sleeping_dynamic_actor_count(self):
        scene = Scene()
        material = Material(restitution=0)
        floor = RigidStatic()
        floor.attach_shape(Shape.create_box([1, 1, 0.1], material))
        floor.set_global_pose([0, 0, -0.05])
        actor = RigidDynamic()
        actor.attach_shape(Shape.create_box([0.01] * 3, material))
        actor.set_mass(0.01)
        actor.set_global_pose([0, 0, 0.1])
        scene.add_actor(floor)
        scene.add_actor(actor)
        scene.simulate(dt=1 / 80, niters=80)

        self.assertEqual(scene.get_nb_sleeping_dynamic_actors(), 1)

    def test_tgs_solver_and_configurable_gravity(self):
        scene = Scene(solver_type=SolverType.TGS)
        scene.set_gravity([0, 0, -1.5])

        np.testing.assert_allclose(scene.get_gravity(), [0, 0, -1.5])

    def test_configurable_bounce_threshold_velocity(self):
        scene = Scene()
        scene.set_bounce_threshold_velocity(0.5)
        self.assertAlmostEqual(scene.get_bounce_threshold_velocity(), 0.5)


if __name__ == '__main__':
    unittest.main()
