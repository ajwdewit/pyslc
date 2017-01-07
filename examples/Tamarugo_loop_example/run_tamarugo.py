#!/usr/bin/env python
import sys, os
import numpy as np

p = os.path.join(os.path.normpath(".."))
sys.path.append(p)
from pyslc.read_slc_inputs import *
from pyslc.run_SLC import run_SLC
from pyslc.write_slc_output_file import write_slc_spectral_output_file
from pyslc.input_parameters import get_parameter_value


#--------------------------------------------------------------------
def read_lab_spectrum(filename):
    file = open(filename)
    file.readline()
    line = file.readline()
    sign = []
    while line:
        sign.append(float(line.split()[3])/100.0)
        line = file.readline()
    file.close()
    return np.array(sign)

#--------------------------------------------------------------------
def read_SLC_output(filename):
    file = open(filename)
    for i in range(31):
        file.readline()
    line = file.readline()
    w = []
    sign = []
    while line:
        w.append(float(line.split()[0]))
        sign.append(float(line.split()[9])/100.)
        line = file.readline()
    file.close()
    return np.array(w), np.array(sign)

#--------------------------------------------------------------------
def write_sensitivity_textfile(rlist, filename, parlist):
    file = open(filename, 'w')

    #header
    for parstring in parlist:
        line = parstring
        for r in rlist:
            line += '\t%f' %get_parameter_value(r, parstring)
        file.write(line + '\r\n')

    #data
    for i in range(len(rlist[0].w)):
        line = '%s' %rlist[0].w[i]
        for r in rlist:
            line += '\t%f' %r.rso[i]
        file.write(line + '\r\n')

    file.close()
    return

#--------------------------------------------------------------------
infile = 'Out_SLCdemo_DAY1-800_10nm.txt'

# 4 runs
s = read_standparam(filename=infile, type='SLCdemo')
s = read_soilparam(s, 'Lab_background_smooth_10nm.dat')
optcoeff = read_optcoeff(filename='..\\pyslc\\optcoeff_files\\OPTCOEFF.DAT')
s.worig = optcoeff.wavelength
s.optipar = optcoeff.optipar
s.option.Hapke    = 'N'
s.option.moisture = 'N'
s.option.canopy   = 'Y'
rlist = []
for [Cw, PAI, LIDFa, fB] in [[0.023, 1.27, -0.30, 0.21],\
                                [0.023, 1.27, -0.45, 0.21],\
                                [0.013, 1.12, 0.10, 0.24],\
                                [0.013, 1.12, 0.02, 0.24]]:
    s.leafgreen.Cw = Cw
    s.canopy.LAI = PAI
    s.canopy.LIDFa = LIDFa
    s.canopy.fB = fB
    r = run_SLC(s)
    rlist.append(r)

print('Number of runs:', len(rlist))
parlist = ['LAI', 'fB', 'LIDFa', 'greenCw']
write_sensitivity_textfile(rlist, '4runs_10nm.txt', parlist)

#sensitivity runs
rlist = []
for Cw in np.arange(0.005, 0.031, 0.005):
    s.leafgreen.Cw = Cw
    for PAI in np.arange(0.27, 1.271, 0.1):
        s.canopy.LAI = PAI
        s.canopy.fB = 0.27/PAI
        for LIDFa in np.arange(-0.5, 0.21, 0.1):
            s.canopy.LIDFa = LIDFa
            r = run_SLC(s)
            rlist.append(r)

print('Number of runs:', len(rlist))
write_sensitivity_textfile(rlist, 'sensitivity_data_10nm.txt', parlist)

print('...finished')
