"""Static API usage checked by Pyright in CI (not a simulation script)."""
import numpy as np
from numpy.typing import NDArray
from pyphysx import Material, RigidDynamic, RigidBodyFlag, Scene, Shape, SolverType, cast_transformation


def check_bindings() -> None:
    material = Material(static_friction=.5, dynamic_friction=.25, restitution=0.)
    actor = RigidDynamic()
    actor.attach_shape(Shape.create_box([.01, .02, .03], material))
    actor.set_global_pose(([0., 0., .1], [1., 0., 0., 0.]))
    actor.set_rigid_body_flag(RigidBodyFlag.ENABLE_CCD, True)
    scene = Scene(solver_type=SolverType.TGS)
    scene.add_actor(actor)
    actors: list[RigidDynamic] = scene.get_dynamic_rigid_actors()
    velocity: NDArray[np.float32] = actors[0].get_linear_velocity()
    position, orientation = cast_transformation(([0., 0., .1], [1., 0., 0., 0.]))
    xyz: NDArray[np.float32] = position
    w: float = orientation.w
    components: NDArray[np.float64] = orientation.components
    assert components.shape == (4,)
    assert velocity.shape == xyz.shape and w == 1.
    scene.release()
