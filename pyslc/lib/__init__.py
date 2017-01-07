# Check OS for correct import of SLC fortran library
try:
    from .py_slc2lib import slc2lib
except ImportError as e:
    msg = "Failed to import the SLC2LIB FORTRAN extension, please compile the fortran code with f2py, see readme."
    print(msg)
    raise
