# -*- coding: utf-8 -*-
# Copyright (c) 2008-2017 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl), Valerie Laurent

from copy import deepcopy
from .run_SLC import run_SLC

##-------------------------------------------------------------------------------
#def prepare_viewangles_angular_Wout(saa, vaa):
#    """This function prepares the list of viewing angles to input in SLC for a
#    complete angular run, according to Wout:
#        VZA from -89 to +89 degrees, regardless of the value of the azimuth
#                                            (backward or forward direction)."""
#    
#    # Prepare start AZI
#    azi = (vaa - saa) % 360           # Take value in [0, 360] using modulo 360
#    azi = 180. - abs(180. - abs(azi)) # Take AZI value in  [0, 180]
#    
#    # Prepare VZA list
#    vza = numpy.arange(-89,90,1)
#    # Fill in and AZI lists
#    azi2 = []
#    for x in vza:
#        if x<0:
#            azi2.append(azi)
#        if x>=0:  # Switch to other side of nadir: azi+180
#            azi2.append(azi+180)
#    
#    # pack viewangles
#    viewangles = [[v, a] for v, a in zip(vza, azi2)]
#    return viewangles


def run_SLC_angular(DataCont):
    """This function makes an angular run of pyslc, with angles according to Wout:
    VZA from -89 to +89 degrees, regardless of the value of the starting azimuth
    (backward or forward direction)."""
    s = DataCont
    rlist = []  # list to collect the results DataContainers
    # Prepare vza and azi
    vaa = s.ang.vaa
    for vza in range(-89, 90, 1): # vza range
        s = deepcopy(DataCont)
        s.ang.vza = vza # the sign will be checked when running SLC
        if vza<0:
            pass # Keep the original vaa value
        else: # (vza>=0)
            s.ang.vaa = vaa + 180 # Jump to other side of nadir
        # Run SLC
        r = run_SLC(s)
        rlist.append(r)
    
    return rlist