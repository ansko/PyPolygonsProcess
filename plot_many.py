# python plot_many.py

import matplotlib
import matplotlib.pyplot as plt
import os


MIN_PTS_NUMBER = 3

""" --- settings --- """
Ei = '30'
Em = '4'


def main_plot():
    fig = plt.figure()
    plt.xlabel('fi')
    plt.ylabel('E')
    plt.title('Ef = 232, Ei = {0}. , Em = {1}'.format(Ei, Em))
    lines_no_perc = []
    lines_perc = []
    legends_no_perc = []
    legends_perc = []

    ordered_ar = set()
    ordered_tau = set()
    for fname in os.listdir('.'):
        if not fname.startswith('rawdata'):
            continue
        ordered_ar.add(float(fname.split('_')[4]))
        ordered_tau.add(float(fname.split('_')[2]))

    for ar in sorted(ordered_ar):
        for tau in sorted(ordered_tau):
            fname = 'rawdata_tau_{0}_ar_{1}'.format(tau, ar)
            if not fname in os.listdir('.'):
                continue
            line_legend = '_'.join(['tau', str(tau), 'ar', str(ar)])
            xs_perc = []
            xs_no_perc = []
            ys_perc = []
            ys_no_perc = []
            fis = set()
            with open(fname) as f:
                for idx, line in enumerate(f):
                    if idx == 0:
                        continue
                    fis.add(float(line.split()[0]))
            if len(fis) < MIN_PTS_NUMBER:
                continue
            with open(fname) as f:
                for idx, line in enumerate(f):
                    if idx == 0:
                        continue
                    if int(line.split()[2]) == 1:
                        xs_perc.append(float(line.split()[0]))
                        ys_perc.append(float(line.split()[1]))
                    else:
                        xs_no_perc.append(float(line.split()[0]))
                        ys_no_perc.append(float(line.split()[1]))
            if xs_no_perc:
                plottables = {fi: [] for fi in sorted(set(xs_no_perc))}
                for idx in range(len(xs_no_perc)):
                    fi = xs_no_perc[idx]
                    E = ys_no_perc[idx]
                    plottables[fi].append(E)
                for fi in plottables.keys():
                    plottables[fi] = reduce(
                        lambda x, y: x + y, plottables[fi]) / len(plottables[fi])
                x = []
                y = []
                for fi in sorted(plottables.keys()):
                    x.append(fi)
                    y.append(plottables[fi])
                if len(x) < MIN_PTS_NUMBER:
                    print(line_legend, 'few_data no_perc', len(x))
                    continue
                tmp, = plt.plot(x, y, marker='o')
                lines_no_perc.append(tmp)
                legends_no_perc.append('n_' + line_legend)
            if xs_perc:
                plottables = {fi: [] for fi in sorted(set(xs_perc))}
                for idx in range(len(xs_perc)):
                    fi = xs_perc[idx]
                    E = ys_perc[idx]
                    plottables[fi].append(E)
                for fi in plottalles.keys():
                    plottables[fi] = reduce(
                        lambda x, y: x + y, plottables[fi]) / len(plottables[fi])
                x = []
                y = []
                for fi in sorted(plottables.keys()):
                    x.append(fi)
                    y.append(plottables[fi])
                if len(x) < MIN_PTS_NUMBER:
                    print(line_legend, 'few_data perc', len(x))
                    continue
                tmp, = plt.plot(x, y, marker='o')
                lines_perc.append(tmp)
                legends_perc.append('p_' + line_legend)
    for idx in range(len(lines_perc)):
        matplotlib.pyplot.legend(lines_perc, legends_perc, loc="upper left")
    for idx in range(len(lines_no_perc)):
        matplotlib.pyplot.legend(lines_no_perc, legends_no_perc, loc="upper left")
    fig.savefig('plot_many.png')


if __name__ == '__main__':
    main_plot()
