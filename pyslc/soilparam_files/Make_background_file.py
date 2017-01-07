#!/usr/bin/env python
import matplotlib.pyplot as plt


def get_col_nb(object):
    obj_list = ['Wavelength', 'Blackberry', 'Grass', 'Blueberry', 'Litter', 'Humus', 'Soil']
    col_list = [0, 1, 2, 3, 4, 5, 6]
    return col_list[obj_list.index(object)]
    

def get_refl_list(object, wmin, wmax):
    filename = 'Field_reflectance_data.txt'
    with open(filename) as fp:
        # Skip lines with too small wavelength
        for i in range(wmin-400+1):
            line = fp.readline()
        # Get the data
        col = get_col_nb(object)
        list = []
        for i in range(wmax - wmin+1):
            line = fp.readline()
            list.append(float(line.split()[col]))

    return list


class Field_reflectance_container(object):
    """Container class for the reflectance data of the understory/soil objects.
    It contains the following tags:
    c.items
    c.w
    c.Blackb
    c.Grass
    c.Blueb
    c.Litter
    c.Humus
    c.Soil"""
    pass


class Stand_background_reflectance_container(object):
    """Container class for the reflectance data of the understory/soil for
    the 3 stands. It contains the following tags:
    r.items
    r.w
    r.YOUNG
    r.OLD1
    r.OLD2"""
    pass


def read_refl_data(wmin, wmax):
    c = Field_reflectance_container()
    c.items = ['Wavelength', 'Blackberry', 'Grass', 'Blueberry', 'Litter', 'Humus', 'Soil']
    c.w = get_refl_list('Wavelength', wmin, wmax)
    c.Blackb = get_refl_list('Blackberry', wmin, wmax)
    c.Grass = get_refl_list('Grass', wmin, wmax)
    c.Blueb = get_refl_list('Blueberry', wmin, wmax)
    c.Litter = get_refl_list('Litter', wmin, wmax)
    c.Humus = get_refl_list('Humus', wmin, wmax)
    c.Soil = get_refl_list('Soil', wmin, wmax)
    return c


def compute_stand_background_sign(c):
    r = Stand_background_reflectance_container()
    r.items = ['Wavelength', 'YOUNG', 'OLD1', 'OLD2']
    r.w = c.w
    r.YOUNG = []
    r.OLD1 = []
    r.OLD2 = []
    for w in range(len(c.w)):
        r.YOUNG.append((c.Soil[w] + c.Litter[w] + c.Humus[w])/3)
        r.OLD1.append((20*r.YOUNG[w] + 35*c.Blueb[w] + 35*c.Blackb[w] + 10*c.Grass[w])/100)
        r.OLD2.append((40*r.YOUNG[w] + 50*c.Blackb[w] + 10*c.Grass[w])/100)
    return r


def plot_refl_data(c, plot_name):
    F1 = plt.figure()
    ax = F1.add_subplot(111)
    
    ax.plot(c.w, c.Blackb)
    ax.plot(c.w, c.Blueb)
    ax.plot(c.w, c.Grass)
    ax.plot(c.w, c.Humus)
    ax.plot(c.w, c.Litter)
    ax.plot(c.w, c.Soil)
    ax.legend(c.items[1:], loc='upper left')
    
    F1.savefig(plot_name)
    return


def plot_refl_stands(r, plot_name):
    F1 = plt.figure()
    ax = F1.add_subplot(111)
    
    ax.plot(r.w, r.YOUNG, 'g')
    ax.plot(r.w, r.OLD1, 'r')
    ax.plot(r.w, r.OLD2, 'b')
    ax.legend(r.items[1:], loc='upper left')
    
    F1.savefig(plot_name)
    return


def write_background_file(wmin, wmax):
    c = read_refl_data(wmin, wmax)
    r = compute_stand_background_sign(c)    
    
    filename = 'background_%s-%s.dat' %(wmin, wmax)
    with open(filename, 'w') as fp:
        # Header
        fp.write('2 !No of header lines including this one\r\n')
        nb = len(r.items[1:])
        nw = len(r.w)
        for i in range(nb):
            fp.write(r.items[i+1] + '\t')
        fp.write('\r\n')
        fp.write('%s %s !number of soils, number of bands\r\n' %(nb, nw))

        # Hapke parameters
        for i in range(nb):
            fp.write(str(i+1)+'\t')
        fp.write('!soilcode\r\n')
        fp.write('%s\t'*nb %(0.84, 0.84, 0.84) + '!b\r\n')
        fp.write('%s\t'*nb %(0.68, 0.68, 0.68) + '!c\r\n')
        fp.write('%s\t'*nb %(0.3, 0.3, 0.3) + '!bo\r\n')
        fp.write('%s\t'*nb %(0.23, 0.23, 0.23) + '!h\r\n')

        # Data
        for w in range(nw):
            fp.write('%s\t'*nb % (r.YOUNG[w], r.OLD1[w], r.OLD2[w]) + '\r\n')


def main():
    wmin = 400
    wmax = 1600
    
    # plot_refl_stands(r, plotpath + 'Background_sign')
    write_background_file(wmin, wmax)
    
    print('... Finished')
    

if __name__=='__main__':
    main()
