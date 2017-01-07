# Script to compile the fortran extension for pySLC on LINUX/BSD/MacOSX systems
# Compile options are for the INTEL fortran compiler

# Copyright (c) 2008-2017 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl), Valerie Laurent

# Remove results from previous compilations
rm *.o *.a *.so

# Compile all fortran code but remove .o file for SLC2lib as that one has
# to be processed by f2py
ifort -O3 -c *.for
rm SLC2lib.o

# Pack in a static library
ar rv libslc.a *.o

# Compile SLC2lib.for with the f2py python2fortran interface generator.
python3 f2py.py -c --opt=-O3 -m py_slc2lib --fcompiler=intel SLC2lib.for libslc.a
