# -*- coding: utf-8 -*-
# Copyright (c) 2008-2017 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl), Valerie Laurent

from copy import deepcopy


def calculate_uv(LIDFa, LIDFb):
    # These are dummy variables to make sure that:
    # |LIDFa| + |LIDFb| <= 1
    u = LIDFa + LIDFb
    v = LIDFa - LIDFb
    return u, v


def calculate_LIDFab(u, v):
    LIDFa = (u + v)/2.0
    LIDFb = (u - v)/2.0
    return LIDFa, LIDFb


def get_leaf_par(parstring):
    if parstring[:5] in ['green', 'brown']:
        leaf = parstring[:5]
        par = parstring[5:]
    else:
        leaf = None
        if parstring=='PAI': par = 'LAI'
        else: par = parstring
    return par, leaf


def get_leaf_container(s, leaf):
    if leaf=='green':   c = s.leafgreen
    elif leaf=='brown': c = s.leafbrown
    else: raise RuntimeError("Unknown leaf type: '%s'" %leaf)
    return c


def is_parameter_value_valid(parstring, val):
    par, leaf = get_leaf_par(parstring)

    # minimum values
    if par=='N':
        if val<1: raise RuntimeError('Value for N parameters cannot be <1')
    elif par in ['LIDFa', 'LIDFb', 'u', 'v']:
        if val<-1: raise RuntimeError('Value for %s cannot be <-1' %par)
    else: # all other parameters
        if val<0: raise RuntimeError('Value for %s cannot be <0!' %par)

    # maximum values
    if par in ['LIDFa', 'LIDFb', 'u', 'v', 'fB', 'Cv', 'hot', 'D', 'Zeta']:
        if val>1: raise RuntimeError('Value for %s cannot be >1!: value=%s' %(par, val))

    return True


def check_valid_input_values(s):
    #canopy
    s.canopy.u, s.canopy.v = calculate_uv(s.canopy.LIDFa, s.canopy.LIDFb)
    for parstring in ['greenCab', 'greenCw', 'greenCdm', 'greenN',\
                      'brownCab', 'brownCw', 'brownCdm', 'brownN',\
                      'LAI', 'Cv', 'fB', 'D', 'LIDFa', 'LIDFb', 'Zeta', 'hot',\
                      'u', 'v']:
        val = get_parameter_value(s, parstring)
        if is_parameter_value_valid(parstring, val)==True:
            if parstring=='fB' and val<0.0001: 
                s.canopy.fB = 0 #SLC bug, see email Wout of 01/07/2011
        else: raise RuntimeError('Wrong input value for parameter %s' %parstring)

    # atmosphere
    if 'atm' in s.__dict__:
        for parstring in ['vis', 'aer', 'H2O', 'O3', 'surfaceheight', 'stemp']:
            if parstring in s.atm.__dict__:
                val = get_parameter_value(s, parstring)
                if is_parameter_value_valid(parstring, val)==True: pass
                else: raise RuntimeError('Wrong input value for parameter %s' %parstring)

    return s


def set_parameter_value(s, parstring, val):
    r = deepcopy(s)
    par, leaf = get_leaf_par(parstring)

    # leaf parameters
    if par in ['Cab', 'Cw', 'Cdm', 'Cs', 'N']:
        c = get_leaf_container(r, leaf)
        if par=='Cab': c.Cab = val
        elif par=='Cw':  c.Cw = val
        elif par=='Cdm': c.Cdm = val
        elif par=='Cs':  c.Cs = val
        elif par=='N':   c.N = val
        else: raise RuntimeError("Unknown PROSPECT parameter: '%s'" %par)

    else:
        # Canopy parameters
        if par=='LAI':     r.canopy.LAI = val
        elif par=='hot':   r.canopy.hot = val
        elif par=='fB':    r.canopy.fB = val
        elif par=='D':     r.canopy.D = val
        elif par=='Cv':    r.canopy.Cv = val
        elif par=='Zeta':  r.canopy.Zeta = val
        elif par=='LIDFa': r.canopy.LIDFa = val
        elif par=='LIDFb': r.canopy.LIDFb = val
        elif par=='u':     r.canopy.u = val
        elif par=='v':     r.canopy.v = val

        # Atmospheric parameters
        elif par=='aer':           r.atm.aer = val
        elif par=='vis':           r.atm.vis = val
        elif par=='stemp':         r.atm.stemp = val
        elif par=='H2O':           r.atm.H2O = val
        elif par=='O3':            r.atm.O3 = val
        elif par=='surfaceheight': r.atm.surfaceheight = val

        else: raise RuntimeError("Unknown parameter: '%s'" %par)

    return r


def get_parameter_value(s, parstring):
    par, leaf = get_leaf_par(parstring)

    # leaf param
    if par in ['Cab', 'Cw', 'Cdm', 'Cs', 'N']:
        c = get_leaf_container(s, leaf)
        if par=='Cab':   val = c.Cab
        elif par=='Cw':  val = c.Cw
        elif par=='Cdm': val = c.Cdm
        elif par=='Cs':  val = c.Cs
        elif par=='N':   val = c.N
        else: raise RuntimeError("Unknown PROSPECT parameter: '%s'" %par)
    else:

        # Canopy param
        if par=='LAI':     val = s.canopy.LAI
        elif par=='hot':   val = s.canopy.hot
        elif par=='fB':    val = s.canopy.fB
        elif par=='D':     val = s.canopy.D
        elif par=='Cv':    val = s.canopy.Cv
        elif par=='Zeta':  val = s.canopy.Zeta
        elif par=='LIDFa': val = s.canopy.LIDFa
        elif par=='LIDFb': val = s.canopy.LIDFb
        elif par=='u':     val = s.canopy.u
        elif par=='v':     val = s.canopy.v
        
        # Atmospheric parameters
        elif par == 'aer':           val = s.atm.aer
        elif par == 'vis':           val = s.atm.vis
        elif par == 'stemp':         val = s.atm.stemp
        elif par == 'surfaceheight': val = s.atm.surfaceheight
        elif par == 'H2O':
            val = s.atm.H2O
            if val=='default': val = 1.835834 #g/cm2
        elif par == 'O3':   
            val = s.atm.O3
            if val=='default': val = 7.05 #g/m2 it is converted to g/cm2 in create_dcards

        # Other parameters
        elif par=='rmsd_TOA': val = s.rmsd_TOA
        elif par=='rmsd_TOC': val = s.rmsd_TOC
        elif par=='cost': val = s.cost
        elif par=='cost_model': val = s.cost_model
        elif par=='cost_apriori': val = s.cost_apriori
        elif par=="sza": val = s.ang.sza
        elif par=="saa": val = s.ang.saa
        elif par=="vza": val = s.ang.vza
        elif par=="vaa": val = s.ang.vaa
        elif par=="lmfac": val = s.lmfac

        else: raise RuntimeError("Unknown parameter: '%s'" %par)
    return val


def get_parameter_unit(par):
    # leaf parameters
    if par=='Cab': unit = 'microg/cm2'
    elif par=='Cw': unit = 'cm' 
    elif par=='Cdm': unit = 'g/cm2'
    # atmosphere parameters
    elif par=='vis':           unit = 'km'
    elif par=='stemp':         unit = 'degrees'
    elif par=='surfaceheight': unit = 'm'
    elif par=='H2O':           unit = 'g/cm2'
    elif par=='O3':            unit = 'g/m2'
    else: unit = ''
    return unit
