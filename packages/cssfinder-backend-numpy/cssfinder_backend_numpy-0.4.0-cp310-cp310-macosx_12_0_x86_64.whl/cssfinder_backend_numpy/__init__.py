# Copyright 2023 Krzysztof Wiśniewski <argmaster.world@gmail.com>
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the “Software”), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""Implementation of CSSFinder backend using NumPy library."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cssfinder.cssfproject import Precision

from cssfinder_backend_numpy.complex64 import HAS_CYTHON as HAS_CYTHON_64
from cssfinder_backend_numpy.complex64 import NumPyC64, NumPyC64Debug, NumPyC64Jit
from cssfinder_backend_numpy.complex128 import HAS_CYTHON as HAS_CYTHON_128
from cssfinder_backend_numpy.complex128 import NumPyC128, NumPyC128Debug, NumPyC128Jit

if TYPE_CHECKING:
    from cssfinder.algorithm.backend import BackendBase

__version__ = "0.4.0"


def export_backend() -> dict[tuple[str, Precision], BackendBase]:
    """Export mapping of available backends in this package."""
    backends = {
        ("numpy_jit", Precision.SINGLE): NumPyC64Jit,
        ("numpy_jit", Precision.DOUBLE): NumPyC128Jit,
        ("numpy", Precision.SINGLE): NumPyC64,
        ("numpy", Precision.DOUBLE): NumPyC128,
        ("numpy_debug", Precision.SINGLE): NumPyC64Debug,
        ("numpy_debug", Precision.DOUBLE): NumPyC128Debug,
    }
    if HAS_CYTHON_64:
        from cssfinder_backend_numpy.complex64 import NumPyC64Cython

        backends[("numpy_cython", Precision.SINGLE)] = NumPyC64Cython

    if HAS_CYTHON_128:
        from cssfinder_backend_numpy.complex128 import NumPyC128Cython

        backends[("numpy_cython", Precision.DOUBLE)] = NumPyC128Cython

    return backends
