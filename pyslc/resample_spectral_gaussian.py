# -*- coding: utf-8 -*-
# Copyright (c) 2008-2017 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl), Valerie Laurent
from .sensor_functions import read_band_centre_fwhm_data
import numpy as np
import spectral


def gaussian(centre, fwhm, w):
    from math import sqrt, log, pi, exp
    # The FWHM of the Gaussian curve is FWHM = 2*sigma*sqrt(2ln(2))
    # http://en.wikipedia.org/wiki/Gaussian_function
    # http://en.wikipedia.org/wiki/Normal_distribution
    # The ln() function is called 'log' in python (natural log., base e)
    sigma = fwhm / (2*sqrt(2*(log(2))))
    g = 1/(sigma*sqrt(2*pi)) * exp(-(w-centre)**2/(2*sigma**2))
    return g


def get_data_subset(data, wdata, centre, fwhm):
    wmin = centre - 2*fwhm
    wmax = centre + 2*fwhm
    
    #Get index min
    i = 0
    while wdata[i] < wmin:
        i = i+1
    imin = i         #TRY: imin = wdata.index(floor(wmin)+1)
    
    #Get index max
    i = len(wdata)-1
    while wdata[i] > wmax:
        i = i-1
    imax = i
    
    #Get the slice of the data list where wmin <= w <= wmax
    data_sub = data[imin:imax+1]

    return data_sub


def integrate(data_list, w_list, centre, fwhm):
    # Get data and wavelength list subsets for the integration
    data = get_data_subset(data_list, w_list, centre, fwhm)
    w = get_data_subset(w_list, w_list, centre, fwhm)
    sum = 0
    sum_weights = 0
    for i in range(len(data)):
        weight = gaussian(centre, fwhm, w[i])
        sum = sum + weight * data[i]
        sum_weights = sum_weights + weight
    return sum/sum_weights


def resample_variable_val(data, w, sensor):
    wdata = w.tolist() #trick. It is faster with list than array...?
    var = []
    band = 1
    (centre, fwhm) = read_band_centre_fwhm_data(sensor, wdata)
    for w in range(len(centre)):
        r_value = integrate(data, wdata, centre[band-1], fwhm[band-1])
        var.append(r_value)
        band += 1
    return np.array(var)


def resample_variable(data, w, sensor):
    # 08/07/2011: faster way, but gives slightly different results
    worig = range(400, 2401)
    (wsensor, fwhm) = read_band_centre_fwhm_data(sensor, worig)
    resample = spectral.BandResampler(w, wsensor, fwhm2=fwhm)
    return resample(data)
