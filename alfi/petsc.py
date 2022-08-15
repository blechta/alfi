from pyop2.utils import get_petsc_dir

import ctypes
import os
import sys


def import_petsc():
    petsc_dir = get_petsc_dir()[1]
    ext = {'linux': '.so', 'darwin': '.dylib'}[sys.platform]
    libpetsc_path = os.path.join(petsc_dir, 'lib', 'libpetsc' + ext)
    libpetsc = ctypes.CDLL(libpetsc_path)
    return libpetsc


libpetsc = import_petsc()
del import_petsc


def MatNestSetVecType(mat, vtype):
    mat = ctypes.c_void_p(mat.handle)
    vtype = ctypes.c_char_p(vtype.encode('ascii'))
    ierr = libpetsc.MatNestSetVecType(mat, vtype)
    if ierr != 0:
        raise RuntimeError(f"MatNestSetVecType failed with error {ierr}")
