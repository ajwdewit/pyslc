# -*- coding: utf-8 -*-
# Copyright (c) 2008-2017 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl), Valerie Laurent


def prepare_angles(sza, vza, saa, vaa):
    """This function is used to prepare the input angles for pyslc and MODTRAN.
    It calculates the angles as needed, that is in the range specified below:
        sza in [0, 90]
        vza in [0, 90]
        azi in [0, 180]
    If the angles do not comply with the above requirements, they are changed
    by this function.
    Rq: we don't use negative vza. The azimuth determines whether the observer
    is in the backward of forward direction. Negative vza values will only be
    used to make plotting the angular outputs more convenient."""
    
    # Take absolute values of the zenith angles
    sza2 = abs(sza)
    vza2 = abs(vza)
    
    # Calculate azimuth value in [0, 180]
    azi = (saa - vaa) % 360
    azi2 = 180. - abs(180. - abs(azi))
    
    return sza2, vza2, azi2


def prepare_angles_check(stand):
    a = stand.ang
    sza, vza, azi = prepare_angles(a.sza, a.vza, a.saa, a.vaa)
    stand.ang_check.sza = sza
    stand.ang_check.vza = vza
    stand.ang_check.azi = azi
    return stand


def prepare_angles_plot(DataCont):
    """This function prepares a new set of angles to be used for plotting.
    The plotting angles are defined as follows:
     - the azimuth angle stays the same
     - the zenitha angles are negative in the backward direction."""
    d = DataCont
    d.ang_plot.azi = d.ang_check.azi
    d.ang_plot.sza = - d.ang_check.sza
    if d.ang_check.azi>=0 and d.ang_check.azi<90: #backward
        d.ang_plot.vza = - d.ang_check.vza
    elif d.ang_check.azi>=90 and d.ang_check.azi<=180: #forward
        d.ang_plot.vza = d.ang_check.vza
    else:
        print('error: the azimuth angle (ang_check.azi) is supposed to be in [0, 180]')
    return d
