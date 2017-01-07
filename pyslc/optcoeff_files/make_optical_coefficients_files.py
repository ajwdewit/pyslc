from copy import deepcopy

from ..sensor_functions import read_AISA_wavelength_list


def lin_interp(x, x0, x1, y0, y1):
    y = y0 + (x-x0)*(y1-y0)/(x1-x0)  # cf notebook 2 page 33
    return y


def interp_Ks_H2O_refr():

    with open('OPTCOEFF.DAT', 'r') as fp:
        all_lines = fp.readlines()

    # collect the 10 nm data from "OPTCOEFF.DAT"
    W_10        = []  # wavelength is in micrometers
    Ks_10       = []
    H2O_refr_10 = []
    for each_line in all_lines[11:]:
        list = each_line.split()
        W_10.append(float(list[0]))
        Ks_10.append(float(list[5]))
        H2O_refr_10.append(float(list[6]))

    # Create 1nm data lists
    Ks          = []
    H2O_refr    = []
    for i in range(len(W_10)-1):
        for j in range(10):
            Ks.append(lin_interp(W_10[i]+j*0.001, W_10[i], W_10[i+1], Ks_10[i], Ks_10[i+1]))
            H2O_refr.append(lin_interp(W_10[i]+j*0.001, W_10[i], W_10[i+1], H2O_refr_10[i], H2O_refr_10[i+1]))
    Ks.append(Ks_10[len(Ks_10)-1])
    H2O_refr.append(H2O_refr_10[len(H2O_refr_10)-1])

    return Ks, H2O_refr


class Optical_coefficients_container():
    """Container class for the optical coefficiens, calculate_all_coeffs
    will return this container with the following tags added:
    c.w
    c.Nr
    c.Kdm
    c.Kab
    c.Kw
    c.Ks
    c.H2O_refr
    c.H2O_abko"""


def calculate_all_coeffs(wmin, wmax, Pversion, res='1nm'):
    c = Optical_coefficients_container()
    # Define the lists
    c.w        = ['W']
    c.Nr       = ['Nr']
    c.Kdm      = ['Kdm']
    c.Kab      = ['Kab']
    c.Kw       = ['Kw']
    c.Ks       = ['Ks']
    c.H2O_refr = ['H2O_refr']
    c.H2O_abko = ['H2O_abko']
    d = deepcopy(c)  # for use if resolution is 10 nm

    # Fill what we can from "dataSpec_P5.m" (W, Nr, Kab, Kw, Kdm and H2O_abko = Kw)
    with open('dataSpec_%s.m' %Pversion, 'r') as fp:
        all_lines = fp.readlines()

    if Pversion == 'P5':
        lmin = wmin-400+18
        lmax = wmax-400+18+1
    if Pversion == 'P4':
        lmin = wmin-400+19
        lmax = wmax-400+19+1
    for each_line in all_lines[lmin:lmax]:
        list = each_line.split()
        c.w.append(int(list[0]))
        c.Nr.append(float(list[1]))
        c.Kab.append(float(list[2]))
        c.Kw.append(float(list[4]))
        c.H2O_abko.append(float(list[4]))
        c.Kdm.append(float(list[5]))
        
    # Interpolate the rest from "OPTCOEFF.DAT": Ks and H2O_refr
    (Ks, H2O_refr) = interp_Ks_H2O_refr()
    c.Ks       = c.Ks + Ks[wmin-400 : wmax-400+1]
    c.H2O_refr = c.H2O_refr + H2O_refr[wmin-400 : wmax-400+1]

    # keep only 10 nm data is required
    if res == '10nm':
        for i in range(1, len(c.w)):
            if c.w[i] in range(400, 2401, 10): 
                d.w.append(c.w[i])
                d.Nr.append(c.Nr[i])
                d.Kab.append(c.Kab[i])
                d.Kw.append(c.Kw[i])
                d.H2O_abko.append(c.H2O_abko[i])
                d.Kdm.append(c.Kdm[i])
                d.Ks.append(c.Ks[i])
                d.H2O_refr.append(c.H2O_refr[i])
        c = d

    return c


def write_optcoeff_file(wmin, wmax, Pversion, res='1nm'):
    c = calculate_all_coeffs(wmin, wmax, Pversion, res=res)
    
    # Write the data in format similar to "OPTCOEFF.DAT"
    filename = 'optcoeff_%s-%s_%s' %(wmin, wmax, Pversion)
    if res == '10nm':
        filename = filename + '_%s' %res
    with open(filename+'.dat', 'w') as fp:
        var = [c.w, c.Nr, c.Kdm, c.Kab, c.Kw, c.Ks, c.H2O_refr, c.H2O_abko]

        # Header
        if res == '10nm':
            fp.write('5  !number of header lines including this one\r\n')
            fp.write('This file contains 10 nm resolution data for use in SLC_demo\r\n')
            fp.write('The data for W, Nr, Kab, Kw, Kdm and H2O_abko were taken from "dataSpec_%s.m"\r\n' %Pversion)
            fp.write('The data for Ks and H2O_refr were taken from "OPTCOEFF.DAT"\r\n')
        else:
            fp.write('4  !number of header lines including this one\r\n')
            fp.write('The data for W, Nr, Kab, Kw, Kdm and H2O_abko were taken from "dataSpec_%s.m"\r\n' %Pversion)
            fp.write('The data for Ks and H2O_refr have been interpolated from "OPTCOEFF.DAT"\r\n')
        line = ''
        for v in var:
            line = line + '%s\t' %v[0]
        line += '\r\n'
        fp.write(line)
        fp.write('%s  !number of spectral bands\r\n' %(len(c.w)-1))

        # Write the contents of the Optical_coefficients_container
        for i in range(1, len(c.w)):
            line = '%.3f\t' %(c.w[i]*0.001) + '%f\t' %c.Nr[i]\
                   + '%.3E\t' %c.Kdm[i]     + '%.3E\t' %c.Kab[i]\
                   + '%.3E\t' %c.Kw[i]      + '%f\t' %c.Ks[i]\
                   + '%f\t' %c.H2O_refr[i]  + '%.3E\t' %c.Kw[i] + '\r\n'
            fp.write(line)

    return


def write_optcoeff_file_nbands(wlist, Pversion):
    c = calculate_all_coeffs(400, 2400, Pversion)
    
    # Write the data in format similar to "OPTCOEFF.DAT"
    filename = 'optcoeff_%s_%sbands' %(Pversion, len(wlist))
    file = open(filename+'.dat', 'w')
    var = [c.w, c.Nr, c.Kdm, c.Kab, c.Kw, c.Ks, c.H2O_refr, c.H2O_abko]
    
    # Header
    file.write('6  !number of header lines including this one\r\n')
    file.write('This file contains the data for the following wavelengths:\r\n')
    file.write('%s \r\n' %wlist)
    file.write('The data for W, Nr, Kab, Kw, Kdm and H2O_abko were taken from "dataSpec_%s.m"\r\n' %Pversion)
    file.write('The data for Ks and H2O_refr were taken from "OPTCOEFF.DAT"\r\n')

    line = ''
    for v in var:
        line = line + '%s\t' %v[0]
    line = line + '\r\n'
    file.write(line)
    file.write('%s  !number of spectral bands\r\n' %len(wlist))
    
    # Write the contents of the Optical_coefficients_container
    for i in range(1, len(c.w)):
        if c.w[i] in wlist:
            line = '%.3f\t' %(c.w[i]*0.001) + '%f\t' %c.Nr[i]\
                   + '%.3E\t' %c.Kdm[i]     + '%.3E\t' %c.Kab[i]\
                   + '%.3E\t' %c.Kw[i]      + '%f\t' %c.Ks[i]\
                   + '%f\t' %c.H2O_refr[i]  + '%.3E\t' %c.Kw[i] + '\r\n'
            file.write(line)
        
    file.close()
    return


def make_AISA_optcoeff_file(Pversion):

    optco_file = open('optcoeff_400-2400_%s.dat' %Pversion)
    with open('otpcoeff_AISA_%s.txt' %Pversion, 'w') as outfile:
        for i in range(4):
            outfile.write(optco_file.readline())
        line = optco_file.readline()
        outfile.write('40' + line[4:])

        wAISA = read_AISA_wavelength_list()
        j = 0
        for i in range(815-465+1):
            while j < 40:
                line = optco_file.readline()
                list = line.split()
                if int(float(list[0])*1000) == int(round(wAISA[j])):
                    outfile.write(line)
                    j += 1  # Go to next AISA wavelength
    
    optco_file.close()
    return


def main():
    wmin = 400
    wmax = 2400
    Pversion = 'P4'
    
    wlist = [550, 670, 850, 1600]
    write_optcoeff_file_nbands(wlist, Pversion)
    # write_optcoeff_file(wmin, wmax, Pversion, res='10nm')
    # make_AISA_optcoeff_file(Pversion)
    
    print('... Finished')
    

if __name__ == "__main__":
    main()
