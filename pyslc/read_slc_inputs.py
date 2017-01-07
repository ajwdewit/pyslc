# -*- coding: utf-8 -*-
# Copyright (c) 2008-2017 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl), Valerie Laurent

import os, sys
import numpy
import copy
import types

from .data_container_class import DataContainer, PyContainer


def read_standparam_SLCdemo(filename=None):
    """This function reads the stand parameters from SLCdemo files.
    s.ang.saa is set to 0, and s.ang.vaa to the azi specified in the file."""
    if filename==None:
        filename = dir + '/standparam_files/SLCdemo_default.txt'
    
    file = open(filename)
    values = []
    for i in range(27):
        line = file.readline()
        list = line.split()
        if i in [0, 17, 18]:
            values.append(float(list[2]))
            #if i==0: soilfile = list[3]
        else:
            values.append(float(list[1]))
    file.close()
    
    #Fill DataContainer
    s = DataContainer()
    #s.soil.filepath = soilfile
    s.soil.code     = values[0]
    s.soil.Hapke_b  = values[1]
    s.soil.Hapke_c  = values[2]
    s.soil.Hapke_b0 = values[3]
    s.soil.Hapke_h  = values[4]
    s.soil.moisture = values[5]*0.01 #from SM% to real SM value im [0,1]
    s.leafgreen.Cab = values[6]
    s.leafgreen.Cw  = values[7]
    s.leafgreen.Cdm = values[8]
    s.leafgreen.Cs  = values[9]
    s.leafgreen.N   = values[10]
    s.leafbrown.Cab = values[11]
    s.leafbrown.Cw  = values[12]
    s.leafbrown.Cdm = values[13]
    s.leafbrown.Cs  = values[14]
    s.leafbrown.N   = values[15]
    s.canopy.LAI    = values[16]
    s.canopy.LIDFa  = values[17]
    s.canopy.LIDFb  = values[18]
    s.canopy.hot    = values[19]
    s.canopy.fB     = values[20]
    s.canopy.D      = values[21]
    s.canopy.Cv     = values[22]*0.01 #from Cv% to real Cv value im [0,1]
    s.canopy.Zeta   = values[23]
    s.ang.sza       = values[24]
    s.ang.vza       = values[25]
    s.ang.saa       = 0 #Relative azimuth (azi) is provided --> saa=0, vaa=azi
    s.ang.vaa       = values[26]
    return s


def get_stand_column(stand, line):
    list = line.split()
    return list.index(stand)


def read_standparam_val(filename=None, stand=None):
    """This function reads the stand parameters from files with val formatting.
    This type for files contain more complete and detailed info.
    The option for each sub model are provided, but the angles are not
    provided here."""
    if filename==None:
        filename = dir+'/standparam_files/SLC_default_input_param_CZ.txt'
        
    file = open(filename)
    col = get_stand_column(stand, file.readline())
    values = []
    for i in range(1, 24):
        line = file.readline()
        list = line.split()
        if i <=3:
            values.append(list[col])
        else:
            values.append(float(list[col]))
    file.close()
    
    #Fill DataContainer
    s = DataContainer()
    s.meta.stand      = stand
    s.option.Hapke    = values[0]
    s.option.moisture = values[1]
    s.option.canopy   = values[2]
    s.soil.code       = values[3]   
    s.soil.moisture   = values[4]
    s.leafgreen.Cab   = values[5]
    s.leafgreen.Cw    = values[6]
    s.leafgreen.Cdm   = values[7]
    s.leafgreen.Cs    = values[8]
    s.leafgreen.N     = values[9]
    s.leafbrown.Cab   = values[10]
    s.leafbrown.Cw    = values[11]
    s.leafbrown.Cdm   = values[12]
    s.leafbrown.Cs    = values[13]
    s.leafbrown.N     = values[14]
    s.canopy.LAI      = values[15]
    s.canopy.LIDFa    = values[16]
    s.canopy.LIDFb    = values[17]
    s.canopy.hot      = values[18]
    s.canopy.fB       = values[19]
    s.canopy.D        = values[20]
    s.canopy.Cv       = values[21]
    s.canopy.Zeta     = values[22]
    return s    


def read_standparam(filename=None, stand=None, type='val'):
    # Later: adapt this function to recognise the format of the file and use
    # the corresponding function to read the data
    
    #----for SLCdemo files
    if type=='SLCdemo':
        s = read_standparam_SLCdemo(filename)
        #print '    No option is specified, using default configuration similar to SLCdemo:\n\
        #      - Using soil Hapke BRDF model\n\
        #      - Using soil moisture model\n\
        #      - Using PROSPECT leaf and SAIL canopy models activated\n\
        #      NB: You can deactivate the models by setting the corresponding option to "N"'
        s.option.Hapke    = 'Y'
        s.option.moisture = 'Y'
        s.option.canopy   = 'Y'
    
    #----for Valerie's files
    elif type=='val':
        s = read_standparam_val(filename, stand) 
    return s


class ReadSLCSoilParam:
    
    def __init__(self, SLCsoilfile):
        """Class for reading and providing pyslc soil parameters. This
        version reads from ASCII file as defined by Verhoef & Bach.

        Usage: SoilReader = ReadSLCSoilParam(soilparam_file)

        SoilReader is an object which contains all soil parameters for each
        soil defined in 'soilparam_file'. The appropriate soil must then
        be selected using:
        soil_param = SoilReader(<soil_code>)

        soil_param is a structure with the following tags:
           soilcode
           habke_b
           habke_c
           habke_h
           habke_B0
           soilspectrum

        Definitions of these variables can be found in SCL2lib.for"""
        if not os.path.exists(SLCsoilfile):
            print("pyslc soil file not found at: %s" % SLCsoilfile)
            return

        with open(SLCsoilfile) as fp:
            line = fp.readline()
            nr_headerlines = int(line.split()[0])
            # Skip nr_headerlines-1 in ASCII file
            for i in range(nr_headerlines-1):
                line = fp.readline()

            # read nr of soils, nr of bands
            line = fp.readline()
            nrsoils, nrbands = line.split()[0:2]
            nrsoils = int(nrsoils)
            nrbands = int(nrbands)

            # Read soil codes
            line = fp.readline()
            soilcodes = line.split()[0:nrsoils]
            try:
                assert len(soilcodes) == nrsoils
            except AssertionError:
                raise RuntimeError("Nr of soils in header does not match nr "+\
                                   "of columns in soil definition")

            # Read Habke parameters
            habke_par = ['b', 'c', 'B0', 'h']
            habke_parvalues = {}
            for parname in habke_par:
                line = fp.readline()
                tmp = [float(t) for t in line.split()[:-1]]
                try:
                    assert len(tmp) == nrsoils
                except AssertionError:
                    raise RuntimeError("Read error for parameter %s" % parname)
                habke_parvalues[parname] = tmp

            # Read remaining columnar data
            lines = fp.readlines()
            soilspec = numpy.zeros((1, nrsoils))

            for line in lines:
                #tmp = numpy.fromstring(line, dtype='f', sep=" ")
                tmp = line.split()
                tmp = numpy.array([float(t) for t in tmp])
                tmp = tmp.reshape((1, nrsoils))
                soilspec = numpy.concatenate([soilspec, tmp], axis=0)
            soilspec = soilspec[1:,:]

            # Convert soil parameters in a format easier to access.
            self._wrap_SLC_soil_params(soilcodes, habke_parvalues, soilspec)


    def _wrap_SLC_soil_params(self, soilcodes, habke_parvalues, soilspec):
        "Wraps the pyslc soil parameters into a useful structure"
        self.SLC_soil_params = {}
        for i in range(len(soilcodes)):
            tmp = PyContainer()
            tmp.soilcode = soilcodes[i]
            tmp.habke_b = habke_parvalues['b'][i]
            tmp.habke_c = habke_parvalues['c'][i]
            tmp.habke_h = habke_parvalues['h'][i]
            tmp.habke_B0 = habke_parvalues['B0'][i]
            tmp.soilspectrum = soilspec[:,i]
            tmp.soilmoisture  = None
            self.SLC_soil_params[tmp.soilcode] = copy.deepcopy(tmp)
            
    def __call__(self, soilcode):
        try:
            return self.SLC_soil_params[str(soilcode)]
        except KeyError:
            print("Unknown soil code!")
            return None


class ReadSLCOptCoeff(object):
    """Class for reading and providing pyslc optical coefficients. This
    version reads from ASCII file as defined by Verhoef & Bach.
    
    Usage: r = ReadSLCOptCoeff(optcoeff_file)
    
    Return object r has the following attributes as float32 arrays:
        self.wavelength 
        self.nr
        self.Kdm
        self.Kab
        self.Kw
        self.Ks
        self.nrW
        self.H2Oabs
    Definitions of these variables can be found in SCL2lib.for 
    """
    
    def __init__(self, optcoeff_file):
        "Reads and processes the optcoeff_file for pyslc."
        try:
            if os.path.exists(optcoeff_file):
                fp = open(optcoeff_file)
            else:
                raise RuntimeError("Opt. Coefficients file '%s' does not exist!" % optcoeff_file)
                
            # Read nr of header lines
            line = fp.readline()
            nr_headerlines = int(line.split()[0])
            
            # skip nr of header lines
            for i in range(nr_headerlines-1):
                line = fp.readline()
            
            # read nr of spectral bands
            line = fp.readline()
            nr_bands = int(line.split()[0])
            
            # read remaining columnar data
            abs_coeffs = numpy.zeros((1,8), dtype='f')
            lines = fp.readlines()
            for line in lines:
                #tmp = numpy.fromstring(line, dtype='f', sep="\t")
                tmp = line.split()
                tmp = numpy.array([float(t) for t in tmp])
                tmp = tmp.reshape((1,8))
                abs_coeffs = numpy.concatenate([abs_coeffs, tmp], axis=0)
            # Remove first line from array
            abs_coeffs = abs_coeffs[1:,:]
            
            # Check if nr of bands eq first dimension of abs_coeffs
            try:
                assert(nr_bands == abs_coeffs.shape[0])
            except AssertionError:
                msg = "Specified nr of bands does not match file length"
                raise RuntimeError(msg)
            
            # Process abs_coeffs array into a more usefull structure
            self._process_SLC_abscoeffs(abs_coeffs)
            self._construct_optipar()
        except Exception as e:
            print(e)
            raise
        
    def _process_SLC_abscoeffs(self, abs_coeffs):
        self.wavelength = abs_coeffs[:,0].squeeze() *1000
        self.nr = abs_coeffs[:,1].squeeze()
        self.Kdm = abs_coeffs[:,2].squeeze()
        self.Kab = abs_coeffs[:,3].squeeze()
        self.Kw = abs_coeffs[:,4].squeeze()
        self.Ks = abs_coeffs[:,5].squeeze()
        self.nrW = abs_coeffs[:,6].squeeze()
        self.H2Oabs = abs_coeffs[:,7].squeeze()
        
    def _construct_optipar(self):
        n = len(self.Kdm)
        optipar_lst = [self.nr.reshape((1,n)), self.Kdm.reshape((1,n)),
                       self.Kab.reshape((1,n)), self.Kw.reshape((1,n)),
                       self.Ks.reshape((1,n)), self.nrW.reshape((1,n)),
                       self.H2Oabs.reshape((1,n))]
        self.optipar = numpy.concatenate(optipar_lst, axis=0)


def read_soilparam(s, filename='SOILPARAM.dat'):
    # Read the soil parameters and use soil_code=1 for input into SLC
    # Manually set soil moisture value.
    soil_reader = ReadSLCSoilParam(filename)
    soilparam = soil_reader(int(s.soil.code))
    if s.soil.moisture is None:
        raise RuntimeError("Soil moisture should be specified in s.soil.moisture")
    else:
        s.soilspec = soilparam.soilspectrum
        s.soilpar  = [soilparam.habke_b, soilparam.habke_c, soilparam.habke_B0,
                      soilparam.habke_h, soilparam.soilmoisture] 
    return s
    

def read_optcoeff(filename='OPTCOEFF.DAT'):
    # Read the optical coefficients for SLC
    opt_param = ReadSLCOptCoeff(filename)
    return opt_param


def get_optcoeff_soilparam(s, res="1nm"):
    # Define paths
    optcoeff_path  = dir + '/optcoeff_files/'
    
    # Define files
    if 'wmin' not in s.meta.__dict__: (wmin, wmax) = (400, 2400)
    else: (wmin, wmax) = (s.meta.wmin, s.meta.wmax)
    try:
        if wmin<400 or wmax>2400:
            raise RuntimeError('can only run pyslc for the 400-2400 nm range')
        else:
            if res=="1nm":
                optcoeff_file  = 'optcoeff_400-2400_P4.dat'
                soilparam_file = s.soil.filepath
            elif res=='10nm':
                optcoeff_file  = 'OPTCOEFF.DAT'
                soilparam_file = dir + '/soilparam_files/SOILPARAM.DAT'
            else: raise RuntimeError('check code resolution')
    except:
        raise RuntimeError('You have to specify s.meta.wmin and s.meta.wmax')
    
    # Read optcoeff and soilparam
    optcoeff = read_optcoeff(optcoeff_path + optcoeff_file)
    if 'filepath' in s.soil.__dict__: soilparam_file = s.soil.filepath
    soilparam = read_soilparam(s.soil.code, s.soil.moisture, soilparam_file)
    
    # Restrict to wmin - wmax range
    imin = wmin-400
    imax = (2400-400+1)-(2400-wmax)
    
    newoptipar = []
    for par in optcoeff.optipar:
        newoptipar.append(par[imin : imax])
    newoptipar = numpy.array(newoptipar)
    optcoeff.wavelength    = optcoeff.wavelength[imin : imax]
    #optcoeff.nr            = optcoeff.nr[imin : imax]
    #optcoeff.Kdm           = optcoeff.Kdm[imin : imax]
    #optcoeff.Kab           = optcoeff.Kab[imin : imax]
    #optcoeff.Kw            = optcoeff.Kw[imin : imax]
    #optcoeff.Ks            = optcoeff.Ks[imin : imax]
    #optcoeff.nrW           = optcoeff.nrW[imin : imax]
    #optcoeff.H2Oabs        = optcoeff.H2Oabs[imin : imax]
    soilparam.soilspec = soilparam.soilspectrum[imin : imax]
    
    # Prepare optcoeff and soilparam for the SLC2lib fortran module
    s.optipar  = newoptipar
    s.worig    = optcoeff.wavelength

    return s
