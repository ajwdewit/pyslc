# -*- coding: utf-8 -*-
# Copyright (c) 2008-2017 Alterra, Wageningen-UR
# Allard de Wit (allard.dewit@wur.nl), Valerie Laurent

def write_slc_header(rlist, file, type):
    if type=='spectral':
        r = rlist
    elif type=='angular':
        r = rlist[0]
    hlines = []
    hlines += ["Soil code".ljust(10)    + "%4.0f\n".rjust(13) % int(r.soil.code)]
                                        #+ "\t%s\n" %r.soil.filepath]
    hlines += ["Hapke_b".ljust(10)      + "%4.2f\n".rjust(13) % r.soil.Hapke_b]
    hlines += ["Hapke_c".ljust(10)      + "%4.2f\n".rjust(13) % r.soil.Hapke_c]
    hlines += ["Hapke_B0".ljust(10)     + "%4.2f\n".rjust(13) % r.soil.Hapke_b0]
    hlines += ["Hapke_h".ljust(10)      + "%4.2f\n".rjust(13) % r.soil.Hapke_h]
    hlines += ["SM%".ljust(10)          + "%4.1f\n".rjust(13) % (r.soil.moisture*100)]
    hlines += ["Cab_green".ljust(10)    + "%4.1f\n".rjust(13) % r.leafgreen.Cab]
    hlines += ["Cw_green".ljust(10)     + "%3.3f\n".rjust(12) % r.leafgreen.Cw]
    hlines += ["Cdm_green".ljust(10)    + "%4.3f\n".rjust(12) % r.leafgreen.Cdm]
    hlines += ["Cs_green".ljust(10)     + "%4.2f\n".rjust(13) % r.leafgreen.Cs]
    hlines += ["N_green".ljust(10)      + "%4.3f\n".rjust(12) % r.leafgreen.N]
    hlines += ["Cab_brown".ljust(10)    + "%4.1f\n".rjust(13) % r.leafbrown.Cab]
    hlines += ["Cw_brown".ljust(10)     + "%4.3f\n".rjust(12) % r.leafbrown.Cw]
    hlines += ["Cdm_brown".ljust(10)    + "%4.3f\n".rjust(12) % r.leafbrown.Cdm]
    hlines += ["Cs_brown".ljust(10)     + "%4.2f\n".rjust(13) % r.leafbrown.Cs]
    hlines += ["N_brown".ljust(10)      + "%4.3f\n".rjust(12) % r.leafbrown.N]
    hlines += ["LAI".ljust(10)          + "%4.2f\n".rjust(13) % r.canopy.LAI]
    hlines += ["LIDF a".ljust(10)       + "%4.2f\n".rjust(12) % r.canopy.LIDFa]
    hlines += ["LIDF b".ljust(10)       + "%4.2f\n".rjust(12) % r.canopy.LIDFb]
    hlines += ["hot".ljust(10)          + "%4.2f\n".rjust(13) % r.canopy.hot]
    hlines += ["fB".ljust(10)           + "%4.2f\n".rjust(13) % r.canopy.fB]
    hlines += ["D".ljust(10)            + "%4.2f\n".rjust(13) % r.canopy.D]
    hlines += ["Cv%".ljust(10)          + "%4.0f.\n".rjust(13) % (r.canopy.Cv*100)]
    hlines += ["zeta".ljust(10)         + "%4.2f\n".rjust(13) % r.canopy.Zeta]
    hlines += ["sza".ljust(10)          + "%4.1f\n".rjust(13) % r.ang_check.sza]
    if type == 'spectral':
        hlines += ["vza".ljust(10)      + "%4.1f\n".rjust(13) % r.ang_check.vza]
        hlines += ["azi".ljust(10)      + "%4.1f\n".rjust(13) % (r.ang.vaa - r.ang.saa)]
    elif type == 'angular':
        hlines += ["azi".ljust(10)      + "%4.1f\n".rjust(13) % (r.ang.vaa - r.ang.saa)]
    hlines += ["\n"]
    file.writelines(hlines)
    

def write_slc_spectral_output(r, file):
    """This function write the data for pyslc spectral output, equivalent to
    SLCdemo.
    Usage: write_slc_spectral_output(<file_object>, <SLC_result>)"""

    ofmt = "%4.0f.  %4.1f %4.1f %4.1f %4.1f   %5.1f %5.1f   %5.1f %5.1f   "+\
           "%4.1f %4.1f %4.1f %4.1f\n"
    lines = ["  WL           SOIL           LEAF green    LEAF brown      "+\
             "    CANOPY\n"]
    lines += [" (nm)   rso  rdo  rsd  rdd    refl  tran    refl  tran  "+\
              "  rso  rdo  rsd  rdd\n"]
    lines += ["\n"]
    for i in range(len(r.w)):
        t = (r.w[i],
             r.rsosoil[i]*100, r.rdosoil[i]*100, r.rsdsoil[i]*100, r.rddsoil[i]*100,
             r.rleafgreen[i]*100, r.tleafgreen[i]*100,
             r.rleafbrown[i]*100, r.tleafbrown[i]*100,
             r.rso[i]*100, r.rdo[i]*100, r.rsd[i]*100, r.rdd[i]*100)
        lines += [ofmt % t]
    file.writelines(lines)
    

def write_slc_spectral_output_file(r, filename):
    file = open(filename, 'w')
    write_slc_header(r, file, type='spectral')
    write_slc_spectral_output(r, file)
    file.close()


def write_slc_angular_output(rlist, fp, wlist):
    # Write title lines
    fp.write(''.ljust(10) + 'wavelengths in micron:\n')
    text1 = '   vza   '
    b = [] # list of indices corresponding to wavelengths in wlgth
    r = rlist[0]
    for w in wlist:
        index = int((w-400)/10)
        b.append(index)
        text1 = text1 + '%.3f\t' % (r.w[index]/1000.)
    fp.write(text1 + '\n')
    
    # Write the angular output data
    for r in rlist:
        #print r.ang.vza, r.ang_check.vza
        text = '%6.1f   ' %r.ang.vza #the original vza, with negative values
        for i in b:
            text += '%6.4f\t' %r.rso[i]
        fp.write(text + '\n')
    fp.write('\n')
    

def write_slc_angular_output_file(rlist, wlist, filename):
    file = open(filename, 'w')
    write_slc_header(rlist, file, type='angular')
    write_slc_angular_output(rlist, file, wlist)
    file.close()
