# -*- coding: utf-8 -*-
# Copyright (c) 2008-2017 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl), Valerie Laurent

class PyContainer(object):
    """Just a container """
    def __str__(self):
        if len(self.__dict__) == 0 :
            return "Empty container."
        else:
            lines = ["PyContainer contains items:\n"]
            for k, v in self.__dict__.items():
                lines.append("- %s: %s\n" % (k, v))
            return "".join(lines)


class DataContainer(object):
    """Container class for the data used and produced by the coupled model.
    It is used to contain and organize the input data, and the model output.
    The container contains the following tags:
        INPUTS              --> attributes, if any
            r.option        --> .Hapke, .moisture, .canopy, .atmosphere
            r.nwl
            r.optipar
            r.soilspec
            r.soil          --> .code, .filepath, .moisture, .Hapke_b, .Hapke_c,
                                .Hapke_b0, .Hapke_h
            r.leafgreen     --> .Cab, .Cw, .Cdm, .Cs, .N
            r.leafbrown     --> .Cab, .Cw, .Cdm, .Cs, .N
            r.canopy        --> .LAI, .LIDFa, .LIDFb, .hot, .fB, .D, .Cv, .Zeta, .u, .v
            r.ang           --> .sza, .saa, .vza, .vaa
            r.ang_check     --> .sza, .vza, .azi
            r.ang_plot      --> .sza, .vza, .azi
            r.worig         --> original 1nm resolution used for the runs
            r.w             --> after resampling
            r.atm           --> .aer, .vis, .stemp, .height, .H2O, .O3
            r.meta          --> .date, .image, .stand, .sensor, .wmin, .wmax,
                                .nwl, .band 
        SOIL OUTPUTS
            r.rddsoil
            r.rsdsoil
            r.rdosoil
            r.rsosoil
        GREEN LEAF OUTPUTS
            r.rleafgreen
            r.tleafgreen
        BROWN LEAF OUTPUTS
            r.rleafbrown
            r.tleafbrown
        CANOPY OUTPUTS
            r.rdd
            r.rsd
            r.rdo
            r.rso
            r.alfadt
            r.alfast
            r.fvc
        MODTRAN OUTPUTS
            r.a0            --> .w, .PATH, .GTOT, .GSUN, .LTOT, .Eso (albedo 0)
            r.a50           --> .w, .PATH, .GTOT, .GSUN, .LTOT, .Eso (albedo 0.5)
            r.a100          --> .w, .PATH, .GTOT, .GSUN, .LTOT, .Eso (albedo 1)
        MODTRAN GAIN FACTORS
            r.Lpo           This is the new way of preparing the 
            r.Gssoo         4-stream interaction
            r.rho_dd
            r.Gmult
            r.Gsdoo
            r.Gsddo
            r.Gssdo
        (MODTRAN EFFECTIVE PARAMETERS)
            r.w             This is the old way of preparing for the 
            r.tau_ss        4-stream interaction
            r.tau_oo        (kept for use in pyslc demo)
            r.rho_dd
            r.tau_sd
            r.tau_do
            r.ext_sol_ir
        TOA OUTPUT
            r.Lsim          TOA radiance simulation
            r.Rsim          TOA reflectance simulation
        CHRIS DATA
            r.Lmeas
            r.rmeas
        AISA DATA
            r.waisa
            r.raisa
        SVD
            r.svdTOC        --> .parlist, .S, .Vt, .U, .dpar, .dpar_norm
            r.svdTOA        --> .parlist, .S, .Vt, .U, .dpar, .dpar_norm"""

    def __init__(self):

        # Add subcontainers for the input/output data
        self.meta      = PyContainer()
        self.option    = PyContainer()
        self.soil      = PyContainer()
        self.leafgreen = PyContainer()
        self.leafbrown = PyContainer()
        self.canopy    = PyContainer()
        self.ang       = PyContainer()
        self.ang_check = PyContainer()
        self.ang_plot  = PyContainer()
        self.atm       = PyContainer()
        self.a0        = PyContainer()
        self.a50       = PyContainer()
        self.a100      = PyContainer()
        self.svdTOC    = PyContainer()
        self.svdTOA    = PyContainer()

    def __str__(self):
        if len(self.__dict__) == 0 :
            return "Empty container."
        else:
            lines = ["PyContainer contains items:\n"]
            for k, v in self.__dict__.items():
                lines.append("- %s\n" % k)
            return "".join(lines)
