# pySLC
Python wrapper for the Soil-Leaf-Canopy (SLC) radiative transfer model

This folder contains the python wrappers to the SLC radiative transfer model developed by Verhoef et al. 
The Python code allows to run SLC in spectral mode, and in angular mode, similar to SLC_demo. However,
the function to write the angular output is onyl fully compatible with the default optical coefficients and
soil parameters files (OPTCOEFF.DAT and SOILPARAM.DAT).

The original wrapper code was written by Allard de Wit (allard.dewit@wur.nl) in August 2008.
Some modifications have been made by Valerie Laurent (valerie.laurent@wur.nl) until December 2009.
An update to make the code compatible with python3 was done in January 2017. Additionally, the code
was converted into a python package with the appropriate structure.

License:
*  The Python wrappers to SLC are licensed under the GPL v3, see:
   http://www.gnu.org/licenses/gpl.html
*  The SLC Fortran code is subject to restrictions put by its developers, please
   contact Wout Verhoef (wout.verhoef@itc.nl) before redistributing pySLC.

Some documentation about the model inputs is contained in /pyslc/lib/SLC2lib.for
For more documentation, refer to the the literature by Verhoef et al.

# Package contents

The package consists of the following structure:
pyslc/:
    * pyslc/
        *  lib/              contains the SLC Fortran code and the shared libraries for Python
        *  optcoeff_files/   contains the optical coefficients files for PROSPECT.
                             NB: those files also contain the water refraction index (H2O_abko) for the soil moisture model
        *  soilparam_files/  contains the files with the soil single scattering albedo values
        *  standparam_files/ contains the files with the leaf chemistry and canopy structure parameters values
        *  sensors_charac/   contains the spectral characteristics of the sensors (only CHRIS mode 4 is available now)
    * output/           contains reference output files, generated output from "run_example.py" is written here.
    * doc/              Documentation
    * examples/         Examples
        * example_run.py    An example for a spectral and angular run.
        * Tamarugo_loop_example/ Incomplete example, left here for

# Installing

pySLC behaves as a normal python package, though there is no setup.py file. It can be placed manually in your python path.
The only necessity is to manually compile the fortran code and python wrappers in pyslc/lib using f2py. Example scripts 
for several platforms are available in the pyslc/lib folder.

Notes:
*  It is necessary to have: a Fortran compiler (e.g. g95, www.g95.org),
   the GNU Compiler (GCC, http://gcc.gnu.org or http://www.mingw.org/ for Windows), and 
   the Python modules 'numpy' and 'spectral' (http://spectralpython.sourceforge.net/).
*  The scripts in the lib/ directory can be used to compile SLC for different
   platforms (unix, windows). You have to run the 'make_pyslc2lib_...' batch file for the corresponding platform
   in the command line.
*  Note that these scripts produce an output file that consists of py2_sl2lib_<pyversion>_<platform>.so (unix) or .pyd
   (windows).  This file has to be renamed or copied to py_sl2lib.so/.pyd
*  Examples are provided in 'example_run.py'


Valerie Laurent, 07/12/2011
Allard de Wit, 07/01/2017
