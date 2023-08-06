"""Build native extension with cython."""

from __future__ import annotations

import shutil
from pathlib import Path

from Cython.Build import build_ext, cythonize
from setuptools import Distribution, Extension

for so_path in Path("cssfinder_backend_numpy/cython").rglob("*.so"):
    so_path.unlink(missing_ok=True)

source = Path("cssfinder_backend_numpy/_cython")
extensions = [
    Extension(
        name=f"cssfinder_backend_numpy.cython.{name}",
        sources=[(source / name).with_suffix(".py").as_posix()],
        language="c++",
        extra_compile_args=["-O3", "-std=c++17"],
    )
    for name in ("_complex64", "_complex128")
]

ext_modules = cythonize(
    extensions, include_path=[source], compiler_directives={"language_level": "3"}
)
dist = Distribution({"ext_modules": ext_modules})
cmd = build_ext(dist)
cmd.ensure_finalized()
cmd.run()

for output in cmd.get_outputs():
    extension_dest_so_path = Path(output).relative_to(cmd.build_lib)
    extension_dest_so_path.parent.mkdir(0o777, exist_ok=True, parents=True)
    shutil.copyfile(output, extension_dest_so_path.as_posix())
