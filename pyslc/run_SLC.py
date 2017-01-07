# -*- coding: utf-8 -*-
# Copyright (c) 2008-2017 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl), Valerie Laurent

import os, sys
from copy import deepcopy

from .read_slc_inputs import read_optcoeff, read_soilparam
from .prepare_angles import prepare_angles_check
from .resample_spectral_gaussian import resample_variable
from .sensor_functions import prepare_sensor_data
from .input_parameters import check_valid_input_values

from .lib import slc2lib


def YN_to_option_digit(YN):
    """This function converts the Y/N options into Wout's boolean option.
    IMPORTANT: Wout's code is 0 for Yes, and 1 for No..."""
    if YN == 'Y':
        bool = 0
    elif YN == 'N':
        bool = 1
    else:
        raise('All options in the DataContainer have to be in Y/N format')
    return str(bool) #string to be able to concatenate in make_option


def make_option(option):
    digit1 = YN_to_option_digit(option.Hapke)
    digit2 = YN_to_option_digit(option.moisture)
    digit3 = YN_to_option_digit(option.canopy)
    #Digit1 is the rightmost digit. See comments in SLC2lib.for
    option = digit3 + digit2 + digit1 
    return option


def prepare_input_data(s):
    # option
    option = make_option(s.option)
    # soil
    soil = s.soil
    soilpar = [soil.Hapke_b, soil.Hapke_c, soil.Hapke_b0, soil.Hapke_h, soil.moisture]
    #soilspec
    soilspec = s.soilspec
    #optipar
    optipar = s.optipar
    # leafgreen
    lg = s.leafgreen
    leafgreen = [lg.Cab, lg.Cw, lg.Cdm, lg.Cs, lg.N]
    # leafbrown
    lb = s.leafbrown
    leafbrown = [lb.Cab, lb.Cw, lb.Cdm, lb.Cs, lb.N]
    # canopy
    c = s.canopy
    canopy = [c.LAI, c.LIDFa, c.LIDFb, c.hot, c.fB, c.D, c.Cv, c.Zeta]
    # angles
    s = prepare_angles_check(s) # Check angles
    a = s.ang_check
    ang = [a.sza, a.vza, a.azi]
    
    return option, soilpar, soilspec, optipar, leafgreen, leafbrown, canopy, ang


def resample_slc_output(r):

    if not hasattr(r.meta, "slcres"):
        r.meta.slcres = ""

    do_resample = True
    if not hasattr(r.meta, "sensor"):
        do_resample = False
    elif r.meta.sensor in ['', 'default']:
        do_resample = False
    elif r.meta.slcres == "N":
        do_resample = False

    if do_resample is False:
        r.w = r.worig  # Do not resample
    else:
        #r.rsosoil    = resample_variable(r.rsosoil,    r.worig, r.meta.sensor)
        #r.rsdsoil    = resample_variable(r.rsdsoil,    r.worig, r.meta.sensor)
        #r.rdosoil    = resample_variable(r.rdosoil,    r.worig, r.meta.sensor)
        #r.rddsoil    = resample_variable(r.rddsoil,    r.worig, r.meta.sensor)
        #r.rleafgreen = resample_variable(r.rleafgreen, r.worig, r.meta.sensor)
        #r.tleafgreen = resample_variable(r.tleafgreen, r.worig, r.meta.sensor)
        #r.rleafbrown = resample_variable(r.rleafbrown, r.worig, r.meta.sensor)
        #r.tleafbrown = resample_variable(r.tleafbrown, r.worig, r.meta.sensor)
        r.rso        = resample_variable(r.rso,        r.worig, r.meta.sensor)
        r.rsd        = resample_variable(r.rsd,        r.worig, r.meta.sensor)
        r.rdo        = resample_variable(r.rdo,        r.worig, r.meta.sensor)
        r.rdd        = resample_variable(r.rdd,        r.worig, r.meta.sensor)
        #r.alfadt     = resample_variable(r.alfadt,     r.worig, r.meta.sensor)
        #r.alfast     = resample_variable(r.alfast,     r.worig, r.meta.sensor)
        r.w          = resample_variable(r.worig,      r.worig, r.meta.sensor)

    return r


def run_SLC(DataCont):
    """Main routine for running SCL. (Reorganized by VL on 21 Oct 2009)
    run_slc2lib returns a DataContainer object.
    Angles:
    - The angles are checked and put in [0, 90] for the zenith angles and
      in [0, 180] for the azimuth angle. This is done by the 'check_angles'
      function --> DataContainer.ang_check"""
    
    s = check_valid_input_values(DataCont)
    
    # Prepare stand data for input in pyslc
    option, soilpar, soilspec, optipar,\
    leafgreen, leafbrown, canopy, ang = prepare_input_data(s)
    
    # Run pyslc fortran routine
    (rsoil, rtleaf, rcan, fvc) = slc2lib(option, optipar, soilspec, soilpar,
                                         leafgreen, leafbrown, canopy, ang)
    
    # Add results to the DataContainer (stand)
    s.rddsoil    = rsoil[0,:].squeeze()
    s.rsdsoil    = rsoil[1,:].squeeze()
    s.rdosoil    = rsoil[2,:].squeeze()
    s.rsosoil    = rsoil[3,:].squeeze()
    s.rleafgreen = rtleaf[0,:].squeeze()
    s.tleafgreen = rtleaf[1,:].squeeze()
    s.rleafbrown = rtleaf[2,:].squeeze()
    s.tleafbrown = rtleaf[3,:].squeeze()
    s.rdd        = rcan[0,:].squeeze()
    s.rsd        = rcan[1,:].squeeze()
    s.rdo        = rcan[2,:].squeeze()
    s.rso        = rcan[3,:].squeeze()
    s.alfadt     = rcan[4,:].squeeze()
    s.alfast     = rcan[5,:].squeeze()
    s.fvc        = fvc

    # Make a deepcopy of the results to be sure that variables in lists 
    # are not changed during next runs (may not be necessary though).
    slc_results = deepcopy(s)

    # Resample the results if needed
    r = resample_slc_output(slc_results)

    return r


