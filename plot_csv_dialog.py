# python plot_many.py

import matplotlib
import matplotlib.pyplot as plt
import os
import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint


MIN_PTS_NUMBER = 3


answers = {
    'csv_name': '/home/anton/AspALL/Projects/FEM_RELEASE_BACKUP/logs/all.csv',
    'fi': None,
    'ar': None,
    'tau': None,
    'axe': None
}


def main_plot(pic_name, data):
    return 0


def select_from_csv(csv_name, fi=None, ar=None, tau=None, axe=None):
    data = []
    with open(csv_name) as f:
        for line in f:
            ls = line.split()
            time_csv = int(ls[1])
            fi_csv = float(ls[3])
            ar_csv = float(ls[5])
            tau_csv = float(ls[7])
            axe_csv = ls[8]
            E_csv = float(ls[9])
            if fi is not None and fi != fi_csv:
                continue
            if ar is not None and ar != ar_csv:
                continue
            if tau is not None and tau != tau_csv:
                continue
            if axe is not None and axe != axe_csv:
                continue
            data.append({
                'csv_name': csv_name,
                'fi': fi_csv,
                'ar': ar_csv,
                'tau': tau_csv,
                'axe': axe_csv,
                'E': E_csv
            })
    return data


def dialog():
    csv_name = raw_input('enter csv name ')
    ar = raw_input('enter ar or press enter ')
    ar = None if not ar else float(ar)
    tau = raw_input('enter tau or press enter ')
    tau = None if not tau else float(tau)
    axe = raw_input('enter axe or press enter ')
    if not axe:
        axe = None
    return {
        'csv_name': csv_name,
        'ar': ar,
        'tau': tau,
        'axe': axe
    }


def plot_data(data):
    """
        Plots every graph into a new file
    """
    csv_names = set()
    ars = set()
    taus = set()
    axis = set()
    data_dict = dict()
    for entry in data:
        csv_names.add(entry['csv_name'])
        ars.add(entry['ar'])
        taus.add(entry['tau'])
        axis.add(entry['axe'])
    for csv_name in csv_names:
        for ar in ars:
            for tau in taus:
                values = select(data, csv_name, ar, tau)
                x = []
                y = []
                for fi in sorted(values.keys()):
                    x.append(fi)
                    y.append(reduce(
                        lambda x, y: x + y, values[fi]) / len(values[fi]))
                if len(x) < MIN_PTS_NUMBER:
                    continue
                fig = plt.figure()
                plt.ylabel('E')
                plt.title('moduli = [232, 4, 1.5] ar = {0} tau = {1}'.format( 
                              ar, tau))
                tmp, = plt.plot(x, y, marker='o')
                legend = 'ar = {0} tau = {1}'.format(
                    csv_name.split('/')[-1][:-4], ar, tau)
                figname = 'figs/csv_{0}_ar_{1}_tau_{2}.png'.format(
                    csv_name.split('/')[-1][:-4], ar, tau)
                matplotlib.pyplot.legend([tmp], [legend], loc="upper left")
                if 'figs' not in os.listdir(os.getcwd()):
                    os.mkdir('figs')
                fig.savefig(figname)
    return 0


def plot_data_with_fixed(data, fixed_ar=False, fixed_tau=False):
    """
        Plots all graphs with fixed_ar or fixed_tau into a single file
    """
    if (fixed_ar and fixed_tau) or (not fixed_ar and not fixed_tau):
        print('bad number of fixes')
        return 0
    csv_names = set()
    ars = set()
    taus = set()
    axis = set()
    data_dict = dict()
    for entry in data:
        csv_names.add(entry['csv_name'])
        ars.add(entry['ar'])
        taus.add(entry['tau'])
        axis.add(entry['axe'])
    if ((fixed_ar == True and not len(ars) == 1) or
        (fixed_tau == True and not len(taus) == 1)):
        print('fix is ok, but data is bad')
        print('fixed_ar:', fixed_ar)
        print('fixed_tau:', fixed_tau)
        return 0
    if fixed_ar:
        figname = 'const_ar_{}.png'.format(sorted(ars)[0])
    if fixed_tau:
        figname = 'const_tau_{}.png'.format(sorted(taus)[0])
    for csv_name in csv_names:
        fig = plt.figure()
        plt.ylabel('E')
        lines = []
        legends = []
        if fixed_ar:
            figname = 'figs/csv_{0}_fixed_ar_{1}.png'.format(
                csv_name.split('/')[-1][:-4], fixed_ar)
            title = 'moduli = [232, 4, 1.5] fixed_ar = {0}'.format(fixed_ar)
            for tau in sorted(taus):
                values = select(data, csv_name, fixed_ar, tau)
                x = []
                y = []
                for fi in sorted(values.keys()):
                    x.append(fi)
                    y.append(reduce(
                        lambda x, y: x + y, values[fi]) / len(values[fi]))
                if len(x) < MIN_PTS_NUMBER:
                    continue
                legends.append('tau = {0}'.format(tau))
                line, = plt.plot(x, y, marker='o')
                lines.append(line)
            if lines:
                plt.title(title)
                matplotlib.pyplot.legend(lines, legends, loc="upper left")
                fig.savefig(figname)
        elif fixed_tau:
            figname = 'figs/csv_{0}_fixed_tau_{1}.png'.format(
                csv_name.split('/')[-1][:-4], fixed_tau)
            title = 'moduli = [232, 4, 1.5] fixed_tau = {0}'.format(fixed_tau)
            for ar in sorted(ars):
                values = select(data, csv_name, ar, fixed_tau)
                x = []
                y = []
                for fi in sorted(values.keys()):
                    x.append(fi)
                    y.append(reduce(
                        lambda x, y: x + y, values[fi]) / len(values[fi]))
                if len(x) < MIN_PTS_NUMBER:
                    continue
                legends.append('ar = {0}'.format(ar))
                line, = plt.plot(x, y, marker='o')
                lines.append(line)
            if lines:
                plt.title(title)
                matplotlib.pyplot.legend(lines, legends, loc="upper left")
                fig.savefig(figname)


def util_plot(x, y, title, legend, figname):
    matplotlib.pyplot.legend([tmp], [legend], loc="upper left")
    print(figname)
    fig.savefig(figname)
    return 0


def select(data, csv_name, ar, tau):
    values = dict()
    for entry in data:
        if (csv_name == entry['csv_name'] and
            ar == entry['ar'] and
            tau == entry['tau']):
            if entry['fi'] in values.keys():
                values[entry['fi']].append(entry['E'])
            else:
                values[entry['fi']] = [entry['E'],]
            x = []
            y = []
            for fi in sorted(values.keys()):
                x.append(fi)
                y.append(reduce(lambda x, y: x + y, values[fi]) / len(values[fi]))
    return values


def main_all_fixes(data):
    if 'figs' not in os.listdir(os.getcwd()):
        os.mkdir('figs')
    ars = set()
    taus = set()
    for entry in data:
        ars.add(entry['ar'])
        taus.add(entry['tau'])
    for ar in ars:
        plot_data_with_fixed(data, fixed_ar=ar)
    for tau in taus:
        plot_data_with_fixed(data, fixed_tau=tau)


if __name__ == '__main__':
    #answers = dialog()
    data = select_from_csv(answers['csv_name'], ar=answers['ar'],
        tau=answers['tau'], axe=answers['axe'])
    #plot_data(data)
    #plot_data_with_fixed(data, fixed_ar=5.0)
    main_all_fixes(data)
