import numpy as np
import matplotlib.pyplot as plt

from ..read_slc_inputs import read_optcoeff


# 10 nm data
optcoeff = read_optcoeff()
w = optcoeff.wavelength.reshape(1, len(optcoeff.wavelength))
opt10 = np.concatenate((w, optcoeff.optipar), axis=0)
print('10nm', len(opt10[0]), min(opt10[0]), max(opt10[0]))

# 1nm data
optcoeff = read_optcoeff('optcoeff_400-2400_P4.dat')
w = optcoeff.wavelength.reshape(1, len(optcoeff.wavelength))
opt1 = np.concatenate((w, optcoeff.optipar), axis=0)
print('1nm', len(opt1[0]), min(opt1[0]), max(opt1[0]))

# reduce res to 10nm ==> new_opt
new_opt = np.empty_like(opt10)
j = 0
for i in range(len(opt1[0])):
    if opt1[0][i] in opt10[0]: 
        new_opt[:,j]=opt1[:,i]
        j+=1

# compare
parnames = ['wavelength', 'nr', 'Kdm', 'Kab', 'Kw', 'Ks', 'n', 'H2Oabs']
for i in range(len(parnames)):
    par = parnames[i]
    F = plt.figure()
    ax = F.add_subplot(111)
    ax.plot(opt10[0], opt10[i], 'k', label=par+' OPTCOEFF')
#    ax.plot(opt10[0], new_opt[i], 'r--', label='my '+par)
    ax.plot(opt1[0], opt1[i], 'r--', label='my '+par)
    ax.legend()
    ax.set_xlabel('Wavelength (nm)')
    F.savefig(par)
