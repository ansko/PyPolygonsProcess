"""
    1. Make ternary structures (by running CppPolygons/)
    2, Perform FEM test by runnnig gen_mesh, processMesh, FEMmain

    Usage:
        python3 task.py TASK_NAME
            TASK_NAME == mc - Monte-Carlo
            TASK_NAME == mix - mixing

    ONLY CUBIC CELL NOW !!!
"""

# ORDER: cpp_polygons -> gen_mesh -> process_mesh -> FEMmain3(x3)

######################################################
###                                                ###
### Performance with 3 FEMmain tasks (i7 8gb RAM): ###
###   (N, tau, ar) = ( Ndes = 3000  ar = 20 )      ###
###        iteration_time = 1000 sec.              ###
###                                                ###
######################################################


import math
import os
import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint
import random
import shutil
import sys
import subprocess
import time

year_month_day = '_'.join([
    time.asctime().split()[4],
    time.asctime().split()[1],
    time.asctime().split()[2]
])
py_main_log = 'py_main_log_' + year_month_day
avaliable_tasks = ['mc', 'mix']
required_settungs = {
    'any': {'Lx', 'thickness', 'shell_thickness', 'outer_radius',
            'vertices_number', 'disks_number', 'LOG'},
    'mc':  {'max_attempts', },
    'mix': {'mixing_steps', }
}
fem_dir = '/home/anton/FEMFolder/'
gen_mesh = fem_dir + 'gen_mesh.x'
processMesh = fem_dir + 'processMesh.x'
FEMmain = fem_dir + 'FEManton3.o'
cpp_dir = 'profiling/'
Ef = 232
Ei = 4
Em = 1.5
L_div_outer_r = 10


#def main(Nmax, taus, ars):
def main(N, tau, ar):
    clean(py_main_log)
    if len(sys.argv) < 2:
        print('usage: python3 task.py TASK_NAME')
        return 0
    task_name = sys.argv[1]
    if task_name not in avaliable_tasks:
        print('error: unavaliable task')
        return 0
    settings = { 
        'mc':{
            'Lx': 5,
            'thickness': 0.1,
            'shell_thickness': 0.1,
            'outer_radius': 0.5,
            'vertices_number': 6,
            'disks_number': 1,
            'LOG': 'from_py',
            'max_attempts': 1000,
            'shape': 'pc'
        },
        'mix': {
            'Lx': 5,
            'thickness': 0.1,
            'shell_thickness': 0.1,
            'outer_radius': 0.5,
            'vertices_number': 6,
            'disks_number': 1,
            'LOG': 'from_py',
            'mixing_steps': 1000,
            'shape': 'pc'
        }
    }
    cpp_polygons_executables = {
        'mc': 'MC_exfoliation',
        'mix': 'mixing'
    }
    settings = dict()
    #for N in range(1, Nmax+1):
    #    for tau in taus:
    #        for ar in ars:
    start_time = time.time()
    if True:
        if True:
            if True:
                #clean(py_main_log)
                seconds = str(int(time.time()))
                geo_fname = '.'.join(['_'.join([seconds, 'N', str(N),
                                                         'tau', str(tau),
                                                         'Lr', str(L_div_outer_r),
                                                         'ar', str(ar)]), 'geo'])
                cpp_out_log_name = '_'.join(['py_cpp_log', str(task_name),
                                              str(seconds)])
                settings['thickness'] = 0.1     # basic
                settings['vertices_number'] = 6 # basic
                settings['mixing_steps'] = 1000 # basic for mix
                settings['max_attempts'] = 1000 # basic for mc
                settings['outer_radius'] = settings['thickness'] * ar/2
                settings['Lx'] = settings['outer_radius'] * L_div_outer_r
                settings['shell_thickness'] = settings['thickness'] * tau
                settings['disks_number'] = N
                settings['LOG'] = cpp_out_log_name
                settings['geo_fname'] = os.getcwd() + '/geo/' + geo_fname
                create_cpp_settings(task_name, settings)
                # run my cpp code
                cpp_start_time = time.time()
                cpp_returned = subprocess.call(
                    cpp_dir +
                    cpp_polygons_executables[task_name],
                    stdout=open('logs/cpp_log_{0}'.format(year_month_day), 'a'),
                    stderr=open('logs/all_errors_{0}'.format(year_month_day), 'a'))
                print('\tcpp_returned', cpp_returned)
                if cpp_returned != 0:
                    return cpp_returned
                parsed_log = process_cpp_log(cpp_out_log_name)
                fi = (parsed_log['fillers_real_number'] *
                          settings['vertices_number'] *
                          0.5 *
                          settings['outer_radius']**2 *
                          math.sin(2 * math.pi / settings['vertices_number']) *
                          settings['thickness'] /
                      settings['Lx']**3)
                perc_str = ''
                perc_str += ('1' if parsed_log['percolation_x'] else '0')
                perc_str += ('1' if parsed_log['percolation_y'] else '0')
                perc_str += ('1' if parsed_log['percolation_z'] else '0')
                new_geo_fname = '_'.join([perc_str, geo_fname])
                os.rename('geo/{0}'.format(geo_fname),
                          'geo/{0}'.format(new_geo_fname))
                geo_fname = new_geo_fname
                # run all fem codes
                create_fem_input_returned = create_fem_input(settings)
                print('\tcreate_fem_input_returned', create_fem_input_returned)
                if create_fem_input_returned != 0:
                    return create_fem_input_returned
                fem_env = os.environ
                fem_env['LD_LIBRARY_PATH'] = (fem_dir + 'libs' + ':' +
                                              fem_dir + 'my_libs')
                gen_mesh_start_time = time.time()
                gen_mesh_returned = subprocess.call(
                    [gen_mesh, 'geo/' + geo_fname, '0.15', '2', '2'],
                    env=fem_env,
                    stdout=open('logs/gen_mesh_log_{0}'.format(year_month_day),
                                 'a'),
                    stderr=open('logs/all_errors_{0}'.format(year_month_day), 'a'))
                print('\tgen_mesh_returned', gen_mesh_returned)
                if gen_mesh_returned != 0:
                    return gen_mesh_returned
                shutil.move('generated.vol', 'out.mesh')
                process_mesh_start_time = time.time()
                processMesh_returned = subprocess.call(
                     processMesh,
                     env=fem_env,
                     stdout=open('logs/process_mesh_log_{0}'.format(
                         year_month_day), 'a'),
                     stderr=open('logs/all_errors_{0}'.format(year_month_day),
                         'a'))
                print('\tprocessMesh_returned', processMesh_returned)
                if processMesh_returned != 0:
                    return processMesh_returned
                fem_main_x_start_time = time.time()
                FEMmain_x_returned = subprocess.call(
                    [FEMmain, 'input_XX.txt'],
                     env=fem_env,
                     stdout=open('logs/fem_main_log_{0}'.format(year_month_day),
                         'a'),
                     stderr=open('logs/all_errors_{0}'.format(year_month_day),
                         'a'))
                print('\tFEMmain_x_returned', FEMmain_x_returned)
                if FEMmain_x_returned != 0:
                    return FEMmain_x_returned
                fem_main_y_start_time = time.time()
                FEMmain_y_returned = subprocess.call(
                    [FEMmain, 'input_YY.txt'],
                     env=fem_env,
                     stdout=open('logs/fem_main_log_{0}'.format(year_month_day),
                         'a'),
                     stderr=open('logs/all_errors_{0}'.format(year_month_day),
                         'a'))
                print('\tFEMmain_y_returned', FEMmain_y_returned)
                if FEMmain_y_returned != 0:
                    return FEMmain_y_returned
                fem_main_z_start_time = time.time()
                FEMmain_z_returned = subprocess.call(
                    [FEMmain, 'input_ZZ.txt'],
                     env=fem_env,
                     stdout=open('logs/fem_main_log_{0}'.format(year_month_day),
                         'a'),
                     stderr=open('logs/all_errors_{0}'.format(year_month_day),
                         'a'))
                fem_main_end_time = time.time()
                print('\tFEMmain_z_returned', FEMmain_z_returned)
                if FEMmain_z_returned != 0:
                    return FEMmain_z_returned
                moduli = get_pseudo_moduli(['XX', 'YY', 'ZZ'])
                # logging
                with open(py_main_log, 'a') as main_log:
                    main_log.write('# ' + seconds + ' ' + time.asctime() + '#'*50 + '\n')
                    main_log.write('# ' + task_name + ' N ' + str(N) +
                                                      ' tau ' + str(tau) +
                                                      ' ar ' + str(ar) + '\n')
                    main_log.write('!fi {0}\n'.format(fi))
                    main_log.write('!Ef {0}\n'.format(Ef))
                    main_log.write('!Ei {0}\n'.format(Ei))
                    main_log.write('!Em {0}\n'.format(Em))
                    main_log.write('!Lr {0}\n'.format(L_div_outer_r))
                    for k, v in settings.items():
                        main_log.write('\t' + str(k) + ' ' + str(v) + '\n')
                    for k, v in parsed_log.items():
                        main_log.write('\t' + str(k) + ' ' + str(v) + '\n')
                    for k, v in moduli.items():
                        main_log.write('\tE_' + str(k) + ' ' + str(v) + '\n')
                    iteration_time = time.time() - start_time
                    main_log.write('! all took {0}\n'.format(iteration_time))
                    main_log.write('!     cpp took {0}\n'.format(
                        gen_mesh_start_time - cpp_start_time))
                    main_log.write('!     gen_mesh took {0}\n'.format(
                        process_mesh_start_time - gen_mesh_start_time))
                    main_log.write('!     process_mesh took {0}\n'.format(
                        fem_main_x_start_time - process_mesh_start_time))
                    main_log.write('!     fem_x took {0}\n'.format(
                        fem_main_y_start_time - fem_main_x_start_time))
                    main_log.write('!     fem_y took {0}\n'.format(
                        fem_main_z_start_time - fem_main_y_start_time))
                    main_log.write('!     fem_z took {0}\n'.format(
                        fem_main_end_time - fem_main_z_start_time))

    #clean(py_main_log)
    print('\tfi', fi)
    print('\titeration took', iteration_time)
    return 0


def clean(py_main_log=None):
    names_to_leave = set([
        # FEM_RELEASE
        'RELEASE_GeoManipulation',
        'RELEASE_CppPolygons',
        'profiling',
        'geo',
        'task.py',
        'readme',
        'logs',
        'materials.txt',
        'matrices.txt',
        # FEMFolder
        'libs',
        'my_libs',
        'FEManton2.o',
        'FEManton3.o',
        'gen_mesh.x',
        'processMesh.x',
        # others
        py_main_log
    ])
    for fname in set(os.listdir()) - names_to_leave:
        if fname.endswith('.py'):
            continue
        if os.path.isdir(fname):
            shutil.rmtree(fname)
        else:
            os.remove(fname)
    for fname in set(os.listdir(fem_dir)) - names_to_leave:
        if os.path.isdir(fem_dir + fname):
            shutil.rmtree(fem_dir + fname)
        else:
            os.remove(fem_dir + fname)


def create_cpp_settings(task_name, settings, fname='settings'):
    with open(fname, 'w') as f:
        for required_setting in required_settungs['any']:
            if not required_setting in settings.keys():
                print('error: required general setting is not set')
                return 0
        for required_setting in required_settungs[task_name]:
            if not required_setting in settings.keys():
                print('error: required specific setting is not set')
                print(required_setting)
                return 0

        for (setting_name, setting_value) in settings.items():
            f.write(' '.join([str(setting_name), str(setting_value), '\n']))


def process_cpp_log(cpp_out_log_name):
    parsed_log = dict()
    with open(cpp_out_log_name) as f:
        for line in f:
            value, other = line.split(maxsplit=1)
            if other == '(algorithm used)\n':
                parsed_log['algorithm'] = value
            elif other == '(status of system formation)\n':
                parsed_log['system_reation_state'] = bool(value)
            elif other == '(number of fillers prepared)\n':
                parsed_log['fillers_real_number'] = int(value)
            elif other == '(possible max attempts number)\n':
                parsed_log['max attempts'] = int(value)
            elif other == '(real attempts number)\n':
                parsed_log['made attempts'] = int(value)
            elif other == '(flag_testing)\n':
                parsed_log['flag_testing'] = bool(value)
            elif other == '(number of intersections in system)\n':
                parsed_log['intersections_number'] = int(value)
            elif other == '(percolation flag along x: )\n':
                parsed_log['percolation_x'] = bool(int(value))
            elif other == '(percolation flag along y: )\n':
                parsed_log['percolation_y'] = bool(int(value))
            elif other == '(percolation flag along z: )\n':
                parsed_log['percolation_z'] = bool(int(value))
    return parsed_log


def create_fem_input(settings):
    if 'Lx' not in settings.keys():
        print('error: no Lx specified')
        return -1
    Lx = settings['Lx']
    if 'Ly' not in settings.keys():
        Ly = Lx
    if 'Lz' not in settings.keys():
        Lz = Lx
    for axe in ['XX', 'YY', 'ZZ']:
        with open('input_{0}.txt'.format(axe), 'w') as fem_input:
            fem_input.write('SizeX {0}\nSizeY {1}\nSizeZ {2}\n'.format(
                Lx, Ly, Lz))
            fem_input.write('MeshFileName mesh.xdr\n')
            fem_input.write('MaterialsGlobalFileName materials.bin\n')
            fem_input.write('TaskName test_elas_E{0}\n'.format(axe))
            fem_input.write('G_filler {0}\n'.format(Ef))
            fem_input.write('G_interface {0}\n'.format(Ei))
            fem_input.write('G_matrix {0}\n'.format(Em))
            fem_input.write('Strain\n')
            if axe == 'XX':
                fem_input.write('0.01 0 0\n0 0 0\n0 0 0\n')
            if axe == 'YY':
                fem_input.write('0 0 0\n0 0.01 0\n0 0 0\n')
            if axe == 'ZZ':
                fem_input.write('0 0 0\n0 0 0\n0 0 0.01\n')
            fem_input.write('\n')
    return 0


def get_pseudo_moduli(axis):
    """
        "Pseudo" means that these are not modui but stress_axe / strain_axe ratios
    """
    moduli = {axe: None for axe in  axis}
    for axe in axis:
        stress = None
        strain = None
        with open('test_elas_E{0}_results.txt'.format(axe)) as f:
            for idx, line in enumerate(f):
                if idx == 14:
                    if axe == 'XX':
                        strain = float(line.split()[0])
                        stress = float(line.split()[9])
                    elif axe == 'YY':
                        strain = float(line.split()[4])
                        stress = float(line.split()[13])
                    elif axe == 'ZZ':
                        strain = float(line.split()[8])
                        stress = float(line.split()[17])
                    else:
                        print('error in fem results parsing!')
                        return -1
        # for some unknown reason fem task may result in zero results
        try:
            moduli[axe] = stress / strain
        except:
            pass
    # comment
    return moduli


if __name__ == '__main__':
    print('starting at', time.asctime(), '#' *50)
    print('*** py_main_log:', py_main_log, '***')
    if 'logs' not in os.listdir():
        os.mkdir('logs')
    if 'geo' not in os.listdir():
        os.mkdir('geo')
    Nmax = 100 # N = 500*ar/math.pi * fi
               #     when r = ar/2 * th and L = L_div_outer_r * r and ar = 25
               #     for adequate fi==0.025 Nmax==100
    taus = [0.5, 1, 1.5, 2, 2.5, 3]
    ars = [10,]# х5, 10, 15, 20, 25]
    productive_runs = 0
    attempts_made = 0
    while(True):
        tau = random.choice(taus)
        ar = random.choice(ars)
        Nmax = int(500*ar/math.pi * 0.05)
        Nmax = min(100, Nmax) # Let us get results for big concentrations
                              #  with small ar for the begginning; bigger ar-s will
                              #  be checked later separately.
        fi = math.pi/500 * Nmax/ar
        N = random.choice(range(1, Nmax+1))
        print('productive_runs', productive_runs, 'attempts_made', attempts_made,
              'current (Nmax, N, tau, ar, fi_max_pos) = (',
               Nmax, N, tau, ar, fi, ')')
        return_code = main(N, tau, ar)
        if return_code == 0:
            productive_runs += 1
        attempts_made += 1
