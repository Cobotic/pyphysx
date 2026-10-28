# Native binding typing contracts

The wheel ships `pyphysx/_pyphysx.pyi` and `pyphysx/py.typed`. The package explicitly
re-exports the native symbols. No physics code or numerical conversion is changed.

The initial declaration was extracted with pybind11-stubgen 2.5.5, then reviewed
against `src/pyphysx.cpp` and `include/transformation_utils.h`. Do not overwrite it
with unreviewed generated output: custom casters report placeholder names `pose`
and `pxvec3`, and generated pybind enum declarations need cleanup.

- Vector inputs accept NumPy-convertible sequences; vector outputs are length-3
  float32 arrays. Shape/dimension validity is checked by native code, not typing.
- Pose inputs accept 3-element positions, packed 7-element poses (xyz, **wxyz**),
  `(position,)`, or `(position, quaternion)`. They do not accept 4x4 matrices.
- Pose outputs are `(float32 position, numpy-quaternion scalar)`. The stub uses a
  private component protocol for the latter because numpy-quaternion is another
  native dependency without complete typing. This covers w/x/y/z and the output components array, not its entire
  arithmetic API. Quaternion inputs are normalized by the existing caster.
- Arbitrary user metadata remains `Any`, matching the native Python-object API.
- pybind enums are described as their actual classes, not as Python `IntEnum`.
  Preserve the existing module-level aliases, including overlapping enum names.

When changing bindings, update declarations in the same commit. Build/install the
wheel, run `pytest tests/test_typing_contract.py` and the native numerical tests,
then run `pyright --project pyrightconfig.json`. The contract test checks packaged
metadata, exports, public members and callable parameter names against the loaded
extension. Behavioral tests check conversions and returned values. These are
complementary: signatures cannot prove numerical correctness.

To regenerate an inspection copy (not a replacement):

```sh
python -m pybind11_stubgen pyphysx._pyphysx -o /tmp/pyphysx-stub-review
```

PoseStream's parent CI also runs a small installed-package contract test so the
pinned wheel and renderer's expectations are tested together.
