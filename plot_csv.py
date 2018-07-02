# python plot_many.py

import matplotlib
import matplotlib.pyplot as plt
import os
import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint


MIN_PTS_NUMBER = 3

""" --- settings --- """
Ei = '30'
Em = '4'

csv_name = 'all.csv'


def plot_special(ars, taus, fixed_variable, fixed_variable_value):
    if fixed_variable == 'ar':
        for ar in ars:
            if ar != fixed_variable_value:
                continue
            fname = '_'.join(['const_ar', str(ar)])
            lines_perc = dict()
            lines_no_perc = dict() # {tau: {fi: [E1, E2, ..]}}
            with open(csv_name) as f:
                for line in f:
                    if ar != float(line.split()[5]):
                        continue
                    tau = float(line.split()[7])
                    perc = line.split()[10]
                    fi = float(line.split()[3])
                    E = float(line.split()[9])
                    if perc == 'True':
                        if tau in lines_perc.keys():
                            if fi in lines_perc[tau].keys():
                                lines_perc[tau][fi].append(E)
                            else:
                                lines_perc[tau][fi] = [E,]
                        else:
                            lines_perc[tau] = dict()
                            lines_perc[tau][fi] = [E,]
                    else:
                        if tau in lines_no_perc.keys():
                            if fi in lines_no_perc[tau].keys():
                                lines_no_perc[tau][fi].append(E)
                            else:
                                lines_no_perc[tau][fi] = [E,]
                        else:
                            lines_no_perc[tau] = dict()
                            lines_no_perc[tau][fi] = [E,]
            print('---', ar, '---')
            pprint(lines_perc)
    elif fixed_variable == 'tau':
        for tau in taus:
            if tau != fixed_variable_value:
                continue
            fname = '_'.join(['const_tau', str(tau)])
            lines_perc = dict()
            lines_no_perc = dict() # {ar: {fi: [E1, E2, ..]}}
            with open(csv_name) as f:
                for line in f:
                    if tau != float(line.split()[7]):
                        continue
                    ar = float(line.split()[5])
                    perc = line.split()[10]
                    fi = float(line.split()[3])
                    E = float(line.split()[9])
                    if perc == 'True':
                        if ar in lines_perc.keys():
                            if fi in lines_perc[ar].keys():
                                lines_perc[ar][fi].append(E)
                            else:
                                lines_perc[ar][fi] = [E,]
                        else:
                            lines_perc[ar] = dict()
                            lines_perc[ar][fi] = [E,]
                    else:
                        if ar in lines_no_perc.keys():
                            if fi in lines_no_perc[ar].keys():
                                lines_no_perc[ar][fi].append(E)
                            else:
                                lines_no_perc[ar][fi] = [E,]
                        else:
                            lines_no_perc[ar] = dict()
                            lines_no_perc[ar][fi] = [E,]
    else:
        print('unknown fixed variable!')
"""
plottables[fi] = reduce(lambda x, y: x + y, plottables[fi]) / len(plottables[fi])
"""

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
    with open(csv_name) as f:
        for line in f:
            ordered_ar.add(float(line.split()[5]))
            ordered_tau.add(float(line.split()[7]))
    ordered_ar = list(sorted(ordered_ar))
    ordered_tau = list(sorted(ordered_tau))
    for ar in ordered_ar:
        plot_special(ordered_ar, ordered_tau, 'ar', ar)

if __name__ == '__main__':
    main_plot()
