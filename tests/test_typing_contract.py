"""Check the shipped declarations against native exports and numerical contracts."""
import ast
from pathlib import Path
import re

import numpy as np
import pytest
import quaternion

import pyphysx
from pyphysx import _pyphysx as native


def test_wheel_contains_typing_and_all_native_exports():
    package = Path(pyphysx.__file__).parent
    assert (package / 'py.typed').is_file()
    stub = ast.parse((package / '_pyphysx.pyi').read_text())
    exported = next(node.value for node in stub.body
                    if isinstance(node, ast.AnnAssign)
                    and isinstance(node.target, ast.Name)
                    and node.target.id == '__all__')
    names = set(ast.literal_eval(exported))
    assert names == {name for name in dir(native) if not name.startswith('_')}
    for name in names:
        assert getattr(pyphysx, name) is getattr(native, name)

    # Check every declared public native member and its parameter names. pybind11
    # signatures are in docstrings; inspect.signature is unavailable for these.
    for node in stub.body:
        if not isinstance(node, ast.ClassDef) or node.name.startswith('_'):
            continue
        cls = getattr(native, node.name)
        members = {name for name in vars(cls) if not name.startswith('_')}
        declared = {member.name if isinstance(member, ast.FunctionDef) else member.target.id
                    for member in node.body
                    if isinstance(member, ast.FunctionDef)
                    or isinstance(member, ast.AnnAssign) and isinstance(member.target, ast.Name)}
        assert members <= declared, (node.name, members - declared)
        for member in node.body:
            if isinstance(member, ast.AnnAssign) and isinstance(member.target, ast.Name):
                assert hasattr(cls, member.target.id)
            if not isinstance(member, ast.FunctionDef):
                continue
            if member.name.startswith('_') and member.name != '__init__':
                continue
            obj = getattr(cls, member.name)
            if isinstance(obj, property):
                continue
            signature = (obj.__doc__ or '').splitlines()[0]
            actual_args = re.findall(r'(?:\(|, )([a-zA-Z_][a-zA-Z_0-9]*):', signature)
            expected_args = [arg.arg for arg in member.args.args]
            assert actual_args == expected_args, (node.name, member.name, signature, expected_args)


@pytest.mark.parametrize('pose', [
    [1., 2., 3.],
    (1., 2., 3.),
    np.array([1., 2., 3.]),
    ([1., 2., 3.],),
    [1., 2., 3., 2., 0., 0., 0.],
    ([1., 2., 3.], [2., 0., 0., 0.]),
    ([1., 2., 3.], quaternion.quaternion(2., 0., 0., 0.)),
])
def test_pose_input_forms_return_position_and_normalized_quaternion(pose):
    position, rotation = pyphysx.cast_transformation(pose)
    assert isinstance(position, np.ndarray)
    assert position.shape == (3,) and position.dtype == np.float32
    np.testing.assert_array_equal(position, [1., 2., 3.])
    assert isinstance(rotation, quaternion.quaternion)
    assert rotation.components.shape == (4,) and rotation.components.dtype == np.float64
    np.testing.assert_allclose([rotation.w, rotation.x, rotation.y, rotation.z], [1., 0., 0., 0.])


def test_native_vector_and_actor_list_contracts():
    scene = pyphysx.Scene(solver_type=pyphysx.SolverType.TGS)
    try:
        scene.set_gravity([0., 0., -1.5])
        gravity = scene.get_gravity()
        assert gravity.shape == (3,) and gravity.dtype == np.float32
        np.testing.assert_array_equal(gravity, [0., 0., -1.5])
        actor = pyphysx.RigidDynamic()
        actor.set_global_pose(([.1, .2, .3], [1., 0., 0., 0.]))
        actor.set_linear_velocity([.25, .5, .75])
        velocity = actor.get_linear_velocity()
        assert velocity.dtype == np.float32 and velocity.shape == (3,)
        np.testing.assert_array_equal(velocity, [.25, .5, .75])
        scene.add_actor(actor)
        actors = scene.get_dynamic_rigid_actors()
        assert isinstance(actors, list) and len(actors) == 1
        assert isinstance(actors[0], pyphysx.RigidDynamic)
        np.testing.assert_allclose(actors[0].get_global_pose()[0], [.1, .2, .3])
    finally:
        scene.release()
