# This script show examples of how to run SLC using the python wrapper in
# spectal and angular modes.
# Written by: Valerie Laurent, December 2009
# Contact: valerie.laurent@wur.nl

import os, sys

# IMPORT THE NECESSARY MODULES / FUNCTIONS
from pyslc.run_SLC import run_SLC
from pyslc.run_SLC_angular import run_SLC_angular
from pyslc.read_slc_inputs import read_standparam, read_soilparam, read_optcoeff
from pyslc.write_slc_output_file import write_slc_spectral_output_file,\
                                  write_slc_angular_output_file
top_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
package_dir = os.path.join(top_dir, "pyslc")
output_dir = os.path.join(top_dir, "output")

# SPECTRAL RUN
stand_fname = os.path.join(package_dir, "standparam_files", "SLCdemo_default.txt")
s = read_standparam(filename=stand_fname, type='SLCdemo')
soil_fname = os.path.join(package_dir, "soilparam_files", "SOILPARAM.DAT")
s = read_soilparam(s, soil_fname)
optcoeff_fname = os.path.join(package_dir, "optcoeff_files", "OPTCOEFF.DAT")
optcoeff = read_optcoeff(filename=optcoeff_fname)
s.worig = optcoeff.wavelength
s.optipar = optcoeff.optipar
s.option.Hapke    = 'N'
s.option.moisture = 'N'
s.option.canopy   = 'Y'
r = run_SLC(s)
output_fname = os.path.join(output_dir, "example_output.txt")
write_slc_spectral_output_file(r, output_fname)

# ANGULAR RUN ----
rlist = run_SLC_angular(s)
wlist = [450, 550, 650, 750, 850]  #list of wavelengths to output
output_fname = os.path.join(output_dir, "example_angular_output.txt")
write_slc_angular_output_file(rlist, wlist, output_fname)

print('... finished')

