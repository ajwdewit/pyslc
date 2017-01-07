REM Script to compile the fortran extension for pySLC on Windows systems
REM Compile options are for the GNU fortran compiler as provide by MinGW

REM Copyright (c) 2008-2017 Alterra, Wageningen-UR
REM Allard de Wit (allard.dewit@wur.nl), Valerie Laurent

REM Remove results from previous compilations
del *.o
del libslc.a
del *.pyd

REM Compile all fortran code but remove .o file for SLC2lib as that one has
REM to be processed by f2py
gfortran -O3 -c *.for
del SLC2lib.o

REM Pack in a static library
ar rv libslc.a *.o

REM Compile SLC2lib.for with the f2py python2fortran interface generator.
python3 f2py.py  -c --opt=-O3 -m py_slc2lib --fcompiler=gnu95 --compiler=mingw32  SLC2lib.for libslc.a