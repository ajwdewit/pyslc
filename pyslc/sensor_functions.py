# -*- coding: utf-8 -*-
# Copyright (c) 2008-2017 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl), Valerie Laurent
# 23 October 2009, Valerie Laurent

import os, sys
from math import floor
dir = os.path.dirname(os.path.abspath(__file__)) #Get dir

##------------------------------------------------------------------------------
#def plot_CP_spec_resp_functions():
#    w_range = range(450, 851, 1)
#    F1 = plt.figure()
#    ax = F1.add_subplot(111)
#    for band in range(1,19):
#        (centre, fwhm) = get_band_centre_fwhm(band)
#        g_list = create_gaussian_list(centre, fwhm, w_range)
#        ax.plot(w_range, g_list)
#    F1.savefig('/home/laure007/Spectral_conv/CP_spec_resp_functions')
#    return

#-------------------------------------------------------------------------------
def read_AISA_wavelength_list():
    file = open(dir+'/sensors_charac/AISA_spectral_bands.txt')
    w = []
    file.readline()
    for i in range(40):
        line = file.readline()
        w.append(float(line))
    file.close()
    return w

#-------------------------------------------------------------------------------
def read_angles(DataCont, filename=None):
    d = DataCont
    if filename==None:
        filename = dir + '/sensors_charac/CHRIS_angles_CZ_2006.txt'
    
    # Read angles data
    file = open(filename)
    file.readline()
    geom_list = []
    for i in range(3*5):
        line = file.readline()
        list = line.split()
        geom_list.append(list)
    file.close()
    
    # Find the right angles
    di = '%s_%s' %(d.meta.date, d.meta.image)
    for list in geom_list:
        if list[0] == di:
            d.ang.sza = float(list[1])
            d.ang.saa = float(list[2])
            d.ang.vza = float(list[3])
            d.ang.vaa = float(list[4])
    return d

#-------------------------------------------------------------------------------
def check_sensor_bands(wdata, centre, fwhm):
    # check for bands shorter or longuer than
    # the available simulation wavelength range
    
    #truncate short wavelengths if needed
    i = 0
    while centre[i] - 2*fwhm[i] < min(wdata):
        i += 1
    imin = i

    #truncate long wavelengths if needed    
    i = len(centre) - 1
    while centre[i] + 2*fwhm[i] > max(wdata):
        i -= 1
    imax = i

    return centre[imin : imax+1], fwhm[imin : imax+1]

#-------------------------------------------------------------------------------
def read_band_centre_fwhm_data(sensor, wdata):
    file = open(dir + '/sensors_charac/' + sensor + '_spectral_bands.txt')
    centre = []
    fwhm   = []
    line = file.readline()
    
    if sensor=='CHRIS': (wcol, fcol) = (3, 4)
    elif sensor=='AISA': (wcol, fcol) = (1, 2)
    else: (wcol, fcol) = (1, 2)
    while line:
        line = file.readline()
        list = line.split()
        try:
            centre.append(float(list[wcol]))
            fwhm.append(  float(list[fcol]))
        except:
            pass
    file.close()

    if sensor=='CHRIS':
        b = 15 #band number to remove (oxygen feature)
        centre = centre[:b-1] + centre[b:]
        fwhm   = fwhm[:b-1]   + fwhm[b:]
    (centre, fwhm) = check_sensor_bands(wdata, centre, fwhm)
    
    return centre, fwhm

#-------------------------------------------------------------------------------
def get_w_wmin_wmax(sensor):
    wdata = range(400, 2401)
    try:
        (centre, fwhm) = read_band_centre_fwhm_data(sensor, wdata)
    except:
        centre = range(400, 2400)
        fwhm = [0 for w in centre]
    nb = len(centre)
    wmin = centre[0] - 2*fwhm[0]
    wmax = centre[nb-1] + 2*fwhm[nb-1]
    wmin = int(floor(wmin))
    wmax = int(floor(wmax) + 1)
    return centre, wmin, wmax

#-------------------------------------------------------------------------------
def prepare_sensor_data(DataCont):
    d = DataCont
    dic = d.meta.__dict__ #Dictionnary of instance attributes
    if dic.has_key('sensor')==False or d.meta.sensor=='':
        d.meta.sensor = ''
        d.worig = range(400, 2401)
    d.meta.wmin, d.meta.wmax = get_wmin_wmax(d.meta.sensor, d.worig)
    return d

#-------------------------------------------------------------------------------
def get_CP_band_info(b, wdata): #CHRIS / PROBA
    if b==1:
        color = 'Blue'
    if b==2:
        color = 'Green'
    if b>=3 and b<=6:
        color = 'Red'
    if b>=7 and b<=12:
        color = 'Red edge'
    if b>=13:
        color = 'NIR'
    (wlist, fwhmlist) = read_band_centre_fwhm_data('CHRIS', wdata)
    w = wlist[b-1]
    return color, int(w)

#-------------------------------------------------------------------------------
