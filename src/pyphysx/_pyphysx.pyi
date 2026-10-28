# Public native bindings. Seeded from pybind11-stubgen 2.5.5, then reviewed
# against src/pyphysx.cpp and include/transformation_utils.h. See doc/typing.md.
from __future__ import annotations
import collections.abc
import numpy
import numpy.typing
import typing
__all__: list[str] = ['ABP', 'ACCELERATION', 'ADAPTIVE_FORCE', 'Aggregate', 'BOX', 'BroadPhaseType', 'CAPSULE', 'CONVEXMESH', 'D6Axis', 'D6Drive', 'D6Joint', 'D6Motion', 'DISABLE_CCD_RESWEEP', 'DISABLE_CONTACT_CACHE', 'DISABLE_CONTACT_REPORT_BUFFER_RESIZE', 'ENABLE_AVERAGE_POINT', 'ENABLE_CCD', 'ENABLE_CCD_FRICTION', 'ENABLE_CCD_MAX_CONTACT_IMPULSE', 'ENABLE_ENHANCED_DETERMINISM', 'ENABLE_FRICTION_EVERY_ITERATION', 'ENABLE_GPU_DYNAMICS', 'ENABLE_PCM', 'ENABLE_POSE_INTEGRATION_PREVIEW', 'ENABLE_SPECULATIVE_CCD', 'ENABLE_STABILIZATION', 'EXCLUDE_KINEMATICS_FROM_ACTIVE_ACTORS', 'FORCE', 'FREE', 'ForceMode', 'FrictionType', 'GPU', 'GeometryType', 'HEIGHTFIELD', 'IMPULSE', 'KINEMATIC', 'LIMITED', 'LOCKED', 'LOCK_ANGULAR_X', 'LOCK_ANGULAR_Y', 'LOCK_ANGULAR_Z', 'LOCK_LINEAR_X', 'LOCK_LINEAR_Y', 'LOCK_LINEAR_Z', 'MBP', 'MUTABLE_FLAGS', 'Material', 'ONE_DIRECTIONAL', 'PATCH', 'PGS', 'PLANE', 'Physics', 'REQUIRE_RW_LOCK', 'RETAIN_ACCELERATIONS', 'RigidActor', 'RigidBodyFlag', 'RigidDynamic', 'RigidDynamicLockFlag', 'RigidStatic', 'SAP', 'SCENE_QUERY_SHAPE', 'SIMULATION_SHAPE', 'SLERP', 'SPHERE', 'SWING', 'SWING1', 'SWING2', 'Scene', 'SceneFlag', 'Shape', 'ShapeFlag', 'SolverType', 'TGS', 'TRIANGLEMESH', 'TRIGGER_SHAPE', 'TWIST', 'TWO_DIRECTIONAL', 'USE_KINEMATIC_TARGET_FOR_SCENE_QUERIES', 'VELOCITY_CHANGE', 'VISUALIZATION', 'X', 'Y', 'Z', 'cast_transformation']


# PxVec3 returns a length-3 float32 ndarray. Inputs accept convertible sequences.
_Vector = numpy.typing.NDArray[numpy.float32]

# The caster accepts objects with quaternion components (including numpy-quaternion).
# Its output is a numpy-quaternion scalar. Describe the component interface here
# rather than depending on that separate native package having its own stubs.
class _QuaternionLike(typing.Protocol):
    @property
    def w(self) -> float: ...
    @property
    def x(self) -> float: ...
    @property
    def y(self) -> float: ...
    @property
    def z(self) -> float: ...

# Positions have 3 elements; packed poses have 7: x,y,z,qw,qx,qy,qz.
# Tuple forms are (position,) or (position, quaternion). Matrices are not poses.
_PoseInput = numpy.typing.ArrayLike | tuple[numpy.typing.ArrayLike] | tuple[numpy.typing.ArrayLike, numpy.typing.ArrayLike | _QuaternionLike]
class _QuaternionResult(_QuaternionLike, typing.Protocol):
    @property
    def components(self) -> numpy.typing.NDArray[numpy.float64]: ...

_Pose = tuple[_Vector, _QuaternionResult]

class Aggregate:

    def __init__(self, max_size: typing.SupportsInt | typing.SupportsIndex=256, enable_self_collision: bool=False) -> None:
        ...

    def add_actor(self, actor: RigidActor) -> None:
        ...

    def get_actors(self) -> list[RigidActor]:
        ...

    def remove_actor(self, actor: RigidActor) -> None:
        ...

class BroadPhaseType:
    ABP: typing.ClassVar[BroadPhaseType]
    GPU: typing.ClassVar[BroadPhaseType]
    MBP: typing.ClassVar[BroadPhaseType]
    SAP: typing.ClassVar[BroadPhaseType]
    __members__: typing.ClassVar[dict[str, BroadPhaseType]]

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

class D6Axis:
    SWING1: typing.ClassVar[D6Axis]
    SWING2: typing.ClassVar[D6Axis]
    TWIST: typing.ClassVar[D6Axis]
    X: typing.ClassVar[D6Axis]
    Y: typing.ClassVar[D6Axis]
    Z: typing.ClassVar[D6Axis]
    __members__: typing.ClassVar[dict[str, D6Axis]]

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

class D6Drive:
    SLERP: typing.ClassVar[D6Drive]
    SWING: typing.ClassVar[D6Drive]
    TWIST: typing.ClassVar[D6Drive]
    X: typing.ClassVar[D6Drive]
    Y: typing.ClassVar[D6Drive]
    Z: typing.ClassVar[D6Drive]
    __members__: typing.ClassVar[dict[str, D6Drive]]

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

class D6Joint:

    def __init__(self, actor0: RigidActor, actor1: RigidActor, local_pose0: _PoseInput=..., local_pose1: _PoseInput=...) -> None:
        ...

    def get_drive_position(self) -> _Pose:
        ...

    def get_drive_velocity(self) -> tuple[_Vector, _Vector]:
        ...

    def get_force_torque(self) -> tuple[_Vector, _Vector]:
        ...

    def get_linear_limit(self, axis: D6Axis) -> tuple[float, float]:
        ...

    def get_local_pose(self, actor_id: typing.SupportsInt | typing.SupportsIndex=0) -> _Pose:
        ...

    def get_motion(self, axis: D6Axis) -> D6Motion:
        ...

    def get_relative_transform(self) -> _Pose:
        ...

    def get_swing_limit(self) -> tuple[float, float]:
        ...

    def get_twist_limit(self) -> tuple[float, float]:
        ...

    def is_broken(self) -> bool:
        ...

    def release(self) -> None:
        ...

    def set_break_force(self, force: typing.SupportsFloat | typing.SupportsIndex, torque: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

    def set_drive(self, axis: D6Drive, stiffness: typing.SupportsFloat | typing.SupportsIndex, damping: typing.SupportsFloat | typing.SupportsIndex, force_limit: typing.SupportsFloat | typing.SupportsIndex, is_acceleration: bool=False) -> None:
        ...

    def set_drive_position(self, pose: _PoseInput=...) -> None:
        ...

    def set_drive_velocity(self, linear: numpy.typing.ArrayLike=..., angular: numpy.typing.ArrayLike=...) -> None:
        ...

    def set_linear_limit(self, axis: D6Axis, lower_limit: typing.SupportsFloat | typing.SupportsIndex, upper_limit: typing.SupportsFloat | typing.SupportsIndex, contact_dist: typing.SupportsFloat | typing.SupportsIndex=-1) -> None:
        ...

    def set_linear_limit_soft(self, axis: D6Axis, lower_limit: typing.SupportsFloat | typing.SupportsIndex, upper_limit: typing.SupportsFloat | typing.SupportsIndex, spring_stiffness: typing.SupportsFloat | typing.SupportsIndex, spring_damping: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

    def set_motion(self, axis: D6Axis, motion: D6Motion) -> None:
        ...

    def set_swing_limit(self, y_limit_angle: typing.SupportsFloat | typing.SupportsIndex, z_limit_angle: typing.SupportsFloat | typing.SupportsIndex, contact_dist: typing.SupportsFloat | typing.SupportsIndex=-1) -> None:
        ...

    def set_swing_limit_soft(self, y_limit_angle: typing.SupportsFloat | typing.SupportsIndex, z_limit_angle: typing.SupportsFloat | typing.SupportsIndex, spring_stiffness: typing.SupportsFloat | typing.SupportsIndex, spring_damping: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

    def set_twist_limit(self, lower_limit: typing.SupportsFloat | typing.SupportsIndex, upper_limit: typing.SupportsFloat | typing.SupportsIndex, contact_dist: typing.SupportsFloat | typing.SupportsIndex=-1) -> None:
        ...

    def set_twist_limit_soft(self, lower_limit: typing.SupportsFloat | typing.SupportsIndex, upper_limit: typing.SupportsFloat | typing.SupportsIndex, spring_stiffness: typing.SupportsFloat | typing.SupportsIndex, spring_damping: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

class D6Motion:
    FREE: typing.ClassVar[D6Motion]
    LIMITED: typing.ClassVar[D6Motion]
    LOCKED: typing.ClassVar[D6Motion]
    __members__: typing.ClassVar[dict[str, D6Motion]]

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

class ForceMode:
    ACCELERATION: typing.ClassVar[ForceMode]
    FORCE: typing.ClassVar[ForceMode]
    IMPULSE: typing.ClassVar[ForceMode]
    VELOCITY_CHANGE: typing.ClassVar[ForceMode]
    __members__: typing.ClassVar[dict[str, ForceMode]]

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

class FrictionType:
    ONE_DIRECTIONAL: typing.ClassVar[FrictionType]
    PATCH: typing.ClassVar[FrictionType]
    TWO_DIRECTIONAL: typing.ClassVar[FrictionType]
    __members__: typing.ClassVar[dict[str, FrictionType]]

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

class GeometryType:
    BOX: typing.ClassVar[GeometryType]
    CAPSULE: typing.ClassVar[GeometryType]
    CONVEXMESH: typing.ClassVar[GeometryType]
    HEIGHTFIELD: typing.ClassVar[GeometryType]
    PLANE: typing.ClassVar[GeometryType]
    SPHERE: typing.ClassVar[GeometryType]
    TRIANGLEMESH: typing.ClassVar[GeometryType]
    __members__: typing.ClassVar[dict[str, GeometryType]]

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

class Material:

    def __init__(self, static_friction: typing.SupportsFloat | typing.SupportsIndex=0.0, dynamic_friction: typing.SupportsFloat | typing.SupportsIndex=0.0, restitution: typing.SupportsFloat | typing.SupportsIndex=0.0) -> None:
        ...

    def __repr__(self) -> str:
        ...

    def get_dynamic_friction(self) -> float:
        ...

    def get_restitution(self) -> float:
        ...

    def get_static_friction(self) -> float:
        ...

    def set_dynamic_friction(self, dynamic_friction: typing.SupportsFloat | typing.SupportsIndex=0.0) -> None:
        ...

    def set_restitution(self, restitution: typing.SupportsFloat | typing.SupportsIndex=0.0) -> None:
        ...

    def set_static_friction(self, static_friction: typing.SupportsFloat | typing.SupportsIndex=0.0) -> None:
        ...

class Physics:

    @staticmethod
    def init_gpu() -> None:
        ...

    @staticmethod
    def set_num_cpu(num_cpu: typing.SupportsInt | typing.SupportsIndex=0) -> None:
        ...

class RigidActor:

    def attach_shape(self, shape: Shape) -> None:
        ...

    def detach_shape(self, shape: Shape) -> None:
        ...

    def disable_gravity(self) -> None:
        ...

    def enable_gravity(self) -> None:
        ...

    def get_atached_shapes(self) -> list[Shape]:
        ...

    def get_global_pose(self) -> _Pose:
        ...

    def get_user_data(self) -> typing.Any:
        ...

    def overlaps(self, other_actor: RigidActor) -> bool:
        ...

    def set_global_pose(self, pose: _PoseInput=...) -> None:
        ...

    def set_user_data(self, o: typing.Any) -> None:
        ...

class RigidBodyFlag:
    ENABLE_CCD: typing.ClassVar[RigidBodyFlag]
    ENABLE_CCD_FRICTION: typing.ClassVar[RigidBodyFlag]
    ENABLE_CCD_MAX_CONTACT_IMPULSE: typing.ClassVar[RigidBodyFlag]
    ENABLE_POSE_INTEGRATION_PREVIEW: typing.ClassVar[RigidBodyFlag]
    ENABLE_SPECULATIVE_CCD: typing.ClassVar[RigidBodyFlag]
    KINEMATIC: typing.ClassVar[RigidBodyFlag]
    RETAIN_ACCELERATIONS: typing.ClassVar[RigidBodyFlag]
    USE_KINEMATIC_TARGET_FOR_SCENE_QUERIES: typing.ClassVar[RigidBodyFlag]
    __members__: typing.ClassVar[dict[str, RigidBodyFlag]]

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

class RigidDynamic(RigidActor):

    def __init__(self) -> None:
        ...

    def add_force(self, force: numpy.typing.ArrayLike, force_mode: ForceMode=...) -> None:
        ...

    def add_torque(self, torque: numpy.typing.ArrayLike, torque_mode: ForceMode=...) -> None:
        ...

    def get_angular_damping(self) -> float:
        ...

    def get_angular_velocity(self) -> _Vector:
        ...

    def get_linear_damping(self) -> float:
        ...

    def get_linear_velocity(self) -> _Vector:
        ...

    def get_mass(self) -> float:
        ...

    def get_rigid_dynamic_lock_flag_value(self, flag: RigidDynamicLockFlag) -> bool:
        ...

    def get_sleep_threshold(self) -> float:
        ...

    def get_stabilization_threshold(self) -> float:
        ...

    def get_wake_counter(self) -> float:
        ...

    def is_sleeping(self) -> bool:
        ...

    def set_angular_damping(self, damping: typing.SupportsFloat | typing.SupportsIndex=0.0) -> None:
        ...

    def set_angular_velocity(self, vel: numpy.typing.ArrayLike) -> None:
        ...

    def set_kinematic_target(self, pose: _PoseInput=...) -> None:
        ...

    def set_linear_damping(self, damping: typing.SupportsFloat | typing.SupportsIndex=0.0) -> None:
        ...

    def set_linear_velocity(self, vel: numpy.typing.ArrayLike) -> None:
        ...

    def set_mass(self, mass: typing.SupportsFloat | typing.SupportsIndex=1.0) -> None:
        ...

    def set_max_angular_velocity(self, max_vel: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

    def set_max_depenetration_velocity(self, max_vel: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

    def set_max_linear_velocity(self, max_vel: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

    def set_rigid_body_flag(self, flag: RigidBodyFlag, value: bool) -> None:
        ...

    def set_rigid_dynamic_lock_flag(self, flag: RigidDynamicLockFlag, value: bool) -> None:
        ...

    def set_sleep_threshold(self, threshold: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

    def set_solver_iteration_counts(self, position_iters: typing.SupportsInt | typing.SupportsIndex, velocity_iters: typing.SupportsInt | typing.SupportsIndex=1) -> None:
        ...

    def set_stabilization_threshold(self, threshold: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

class RigidDynamicLockFlag:
    LOCK_ANGULAR_X: typing.ClassVar[RigidDynamicLockFlag]
    LOCK_ANGULAR_Y: typing.ClassVar[RigidDynamicLockFlag]
    LOCK_ANGULAR_Z: typing.ClassVar[RigidDynamicLockFlag]
    LOCK_LINEAR_X: typing.ClassVar[RigidDynamicLockFlag]
    LOCK_LINEAR_Y: typing.ClassVar[RigidDynamicLockFlag]
    LOCK_LINEAR_Z: typing.ClassVar[RigidDynamicLockFlag]
    __members__: typing.ClassVar[dict[str, RigidDynamicLockFlag]]

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

class RigidStatic(RigidActor):

    @staticmethod
    def create_plane(material: Material, nx: typing.SupportsFloat | typing.SupportsIndex=0.0, ny: typing.SupportsFloat | typing.SupportsIndex=0.0, nz: typing.SupportsFloat | typing.SupportsIndex=1.0, distance: typing.SupportsFloat | typing.SupportsIndex=0.0) -> RigidStatic:
        ...

    def __init__(self) -> None:
        ...

class Scene:

    def __init__(self, friction_type: FrictionType=..., broad_phase_type: BroadPhaseType=..., scene_flags: collections.abc.Sequence[SceneFlag]=[], solver_type: SolverType=..., gpu_max_num_partitions: typing.SupportsInt | typing.SupportsIndex=8, gpu_dynamic_allocation_scale: typing.SupportsFloat | typing.SupportsIndex=1.0) -> None:
        ...

    def add_actor(self, actor: RigidActor) -> None:
        ...

    def add_aggregate(self, agg: Aggregate) -> None:
        ...

    def get_aggregates(self) -> list[Aggregate]:
        ...

    def get_bounce_threshold_velocity(self) -> float:
        ...

    def get_dynamic_rigid_actors(self) -> list[RigidDynamic]:
        ...

    def get_gravity(self) -> _Vector:
        ...

    def get_nb_sleeping_dynamic_actors(self) -> int:
        ...

    def get_static_rigid_actors(self) -> list[RigidActor]:
        ...

    def release(self) -> None:
        ...

    def set_bounce_threshold_velocity(self, velocity: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

    def set_gravity(self, gravity: numpy.typing.ArrayLike) -> None:
        ...

    def simulate(self, dt: typing.SupportsFloat | typing.SupportsIndex=0.016666666666666666, niters: typing.SupportsInt | typing.SupportsIndex=1) -> None:
        ...

    @property
    def simulation_time(self) -> float:
        ...

    @simulation_time.setter
    def simulation_time(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

class SceneFlag:
    ADAPTIVE_FORCE: typing.ClassVar[SceneFlag]
    DISABLE_CCD_RESWEEP: typing.ClassVar[SceneFlag]
    DISABLE_CONTACT_CACHE: typing.ClassVar[SceneFlag]
    DISABLE_CONTACT_REPORT_BUFFER_RESIZE: typing.ClassVar[SceneFlag]
    ENABLE_AVERAGE_POINT: typing.ClassVar[SceneFlag]
    ENABLE_CCD: typing.ClassVar[SceneFlag]
    ENABLE_ENHANCED_DETERMINISM: typing.ClassVar[SceneFlag]
    ENABLE_FRICTION_EVERY_ITERATION: typing.ClassVar[SceneFlag]
    ENABLE_GPU_DYNAMICS: typing.ClassVar[SceneFlag]
    ENABLE_PCM: typing.ClassVar[SceneFlag]
    ENABLE_STABILIZATION: typing.ClassVar[SceneFlag]
    EXCLUDE_KINEMATICS_FROM_ACTIVE_ACTORS: typing.ClassVar[SceneFlag]
    MUTABLE_FLAGS: typing.ClassVar[SceneFlag]
    REQUIRE_RW_LOCK: typing.ClassVar[SceneFlag]
    __members__: typing.ClassVar[dict[str, SceneFlag]]

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

class Shape:

    @staticmethod
    def create_box(size: numpy.typing.ArrayLike, material: Material, is_exclusive: bool=True) -> Shape:
        ...

    @staticmethod
    def create_convex_mesh_from_points(points: numpy.typing.ArrayLike, material: Material, is_exclusive: bool=True, scale: typing.SupportsFloat | typing.SupportsIndex=1.0, quantized_count: typing.SupportsInt | typing.SupportsIndex=255, vertex_limit: typing.SupportsInt | typing.SupportsIndex=255) -> Shape:
        ...

    @staticmethod
    def create_sphere(radius: typing.SupportsFloat | typing.SupportsIndex, material: Material, is_exclusive: bool=True) -> Shape:
        ...

    def get_box_half_extents(self) -> _Vector:
        ...

    def get_flag_value(self, flag: ShapeFlag) -> bool:
        ...

    def get_geometry_type(self) -> GeometryType:
        ...

    def get_local_pose(self) -> _Pose:
        ...

    def get_materials(self) -> list[Material]:
        ...

    def get_shape_data(self) -> numpy.typing.NDArray[numpy.float32]:
        ...

    def get_sphere_radius(self) -> float:
        ...

    def get_user_data(self) -> typing.Any:
        ...

    def overlaps(self, other_shape: Shape, global_pose: _PoseInput=..., global_pose_other: _PoseInput=...) -> bool:
        ...

    def set_contact_offset(self, offset: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

    def set_flag(self, flag: ShapeFlag, value: bool=True) -> None:
        ...

    def set_local_pose(self, pose: _PoseInput=...) -> None:
        ...

    def set_rest_offset(self, offset: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...

    def set_user_data(self, o: typing.Any) -> None:
        ...

class ShapeFlag:
    SCENE_QUERY_SHAPE: typing.ClassVar[ShapeFlag]
    SIMULATION_SHAPE: typing.ClassVar[ShapeFlag]
    TRIGGER_SHAPE: typing.ClassVar[ShapeFlag]
    VISUALIZATION: typing.ClassVar[ShapeFlag]
    __members__: typing.ClassVar[dict[str, ShapeFlag]]

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

class SolverType:
    PGS: typing.ClassVar[SolverType]
    TGS: typing.ClassVar[SolverType]
    __members__: typing.ClassVar[dict[str, SolverType]]

    def __getstate__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __int__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...

    def __str__(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

def cast_transformation(pose: _PoseInput=...) -> _Pose:
    ...
ABP: BroadPhaseType
ACCELERATION: ForceMode
ADAPTIVE_FORCE: SceneFlag
BOX: GeometryType
CAPSULE: GeometryType
CONVEXMESH: GeometryType
DISABLE_CCD_RESWEEP: SceneFlag
DISABLE_CONTACT_CACHE: SceneFlag
DISABLE_CONTACT_REPORT_BUFFER_RESIZE: SceneFlag
ENABLE_AVERAGE_POINT: SceneFlag
ENABLE_CCD: SceneFlag
ENABLE_CCD_FRICTION: RigidBodyFlag
ENABLE_CCD_MAX_CONTACT_IMPULSE: RigidBodyFlag
ENABLE_ENHANCED_DETERMINISM: SceneFlag
ENABLE_FRICTION_EVERY_ITERATION: SceneFlag
ENABLE_GPU_DYNAMICS: SceneFlag
ENABLE_PCM: SceneFlag
ENABLE_POSE_INTEGRATION_PREVIEW: RigidBodyFlag
ENABLE_SPECULATIVE_CCD: RigidBodyFlag
ENABLE_STABILIZATION: SceneFlag
EXCLUDE_KINEMATICS_FROM_ACTIVE_ACTORS: SceneFlag
FORCE: ForceMode
FREE: D6Motion
GPU: BroadPhaseType
HEIGHTFIELD: GeometryType
IMPULSE: ForceMode
KINEMATIC: RigidBodyFlag
LIMITED: D6Motion
LOCKED: D6Motion
LOCK_ANGULAR_X: RigidDynamicLockFlag
LOCK_ANGULAR_Y: RigidDynamicLockFlag
LOCK_ANGULAR_Z: RigidDynamicLockFlag
LOCK_LINEAR_X: RigidDynamicLockFlag
LOCK_LINEAR_Y: RigidDynamicLockFlag
LOCK_LINEAR_Z: RigidDynamicLockFlag
MBP: BroadPhaseType
MUTABLE_FLAGS: SceneFlag
ONE_DIRECTIONAL: FrictionType
PATCH: FrictionType
PGS: SolverType
PLANE: GeometryType
REQUIRE_RW_LOCK: SceneFlag
RETAIN_ACCELERATIONS: RigidBodyFlag
SAP: BroadPhaseType
SCENE_QUERY_SHAPE: ShapeFlag
SIMULATION_SHAPE: ShapeFlag
SLERP: D6Drive
SPHERE: GeometryType
SWING: D6Drive
SWING1: D6Axis
SWING2: D6Axis
TGS: SolverType
TRIANGLEMESH: GeometryType
TRIGGER_SHAPE: ShapeFlag
TWIST: D6Drive
TWO_DIRECTIONAL: FrictionType
USE_KINEMATIC_TARGET_FOR_SCENE_QUERIES: RigidBodyFlag
VELOCITY_CHANGE: ForceMode
VISUALIZATION: ShapeFlag
X: D6Drive
Y: D6Drive
Z: D6Drive
