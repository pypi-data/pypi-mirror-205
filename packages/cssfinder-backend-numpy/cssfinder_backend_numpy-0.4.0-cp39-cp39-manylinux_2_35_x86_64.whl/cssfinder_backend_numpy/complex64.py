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


"""Numpy backend with fixed precision of complex 128-bit."""

from __future__ import annotations

import logging
from typing import cast

import numpy as np

from cssfinder_backend_numpy.base import NumPyBase, NumPyJitBase
from cssfinder_backend_numpy.impl import Implementation
from cssfinder_backend_numpy.numpy import _complex64
from cssfinder_backend_numpy.numpy_debug import _complex64 as _complex64_debug
from cssfinder_backend_numpy.numpy_jit import _complex64 as _complex64_jit

try:
    from cssfinder_backend_numpy.cython import (  # type: ignore[attr-defined] # noqa: E501 I001 RUF100
        _complex64 as _complex64_cython,
    )

    HAS_CYTHON = True

except ImportError:
    logging.critical("Failed to import Cython compiled single precision NumPy backend.")
    HAS_CYTHON = False


class NumPyC64(NumPyBase[np.complex64, np.float32]):
    """Concrete numpy based backend for Gilbert algorithm using complex128 type."""

    impl: Implementation[np.complex64, np.float32] = cast(
        Implementation[np.complex64, np.float32],
        _complex64,
    )
    primary_t: type[np.complex64] = np.complex64
    secondary_t: type[np.float32] = np.float32


class NumPyC64Jit(NumPyJitBase[np.complex64, np.float32]):
    """Concrete numpy based backend for Gilbert algorithm using complex128 type."""

    impl: Implementation[np.complex64, np.float32] = cast(
        Implementation[np.complex64, np.float32],
        _complex64_jit,
    )
    primary_t: type[np.complex64] = np.complex64
    secondary_t: type[np.float32] = np.float32


class NumPyC64Debug(NumPyBase[np.complex64, np.float32]):
    """Concrete numpy based backend for Gilbert algorithm using complex128 type."""

    impl: Implementation[np.complex64, np.float32] = cast(
        Implementation[np.complex64, np.float32],
        _complex64_debug,
    )
    primary_t: type[np.complex64] = np.complex64
    secondary_t: type[np.float32] = np.float32


if HAS_CYTHON:

    class NumPyC64Cython(NumPyBase[np.complex64, np.float32]):
        """Concrete numpy based backend for Gilbert algorithm using complex128 type."""

        impl: Implementation[np.complex64, np.float32] = cast(
            Implementation[np.complex64, np.float32],
            _complex64_cython,
        )
        primary_t: type[np.complex64] = np.complex64
        secondary_t: type[np.float32] = np.float32
