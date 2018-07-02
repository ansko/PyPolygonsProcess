# ps -ef | grep python # display all python processes
# OUT:   UID        PID  PPID  C STIME TTY          TIME CMD


import os
import psutil
import signal
import time


limits = {
    'MC_exfoliation': 1000,
    'FEManton3.o': 1000,
    'gen_mesh.x': 1000,
    'processMesh.x': 100
}


def check_long(just_watch):
    for proc in psutil.process_iter():
        if proc.name() in ['MC_exfoliation',
                           'gen_mesh.x', 'processMesh.x', 'FEManton3.o']:
            running_time = int(time.time() - proc.create_time())
            #if not just_watch:
            #    continue
            if running_time > limits[proc.name()]:
                print('killing', proc.name(),
                      'with pid', proc.pid,
                      'running for', running_time, 'seconds')
                proc.terminate()
                return 1
            else:
                print('waiting for', proc.name(),
                      'with pid', proc.pid,
                      'running for', running_time,
                      'of max', limits[proc.name()], 'seconds')
            if proc.name() == 'MC_exfoliation':
                with open('/home/anton/AspALL/Projects/FEM_RELEASE/logs/' +
                          'cpp_log_2018_Jun_26') as f:
                    prev_line = False
                    for line in f:
                        pass
                    if line[-1] =='\n':
                        print('  cpp running, last line in log: ' + line[:-1])
                    else:
                        print('  cpp running, last line in log: ' + line)

if __name__ == '__main__':
    t = 3 # check for long processes for every t seconds
    just_watch = True
    while True:
        print('my pid =', os.getpid(), '--just_watch =', just_watch,
              end=' ... ')
        try:
            value = check_long(just_watch)
            if value == 1:
                print('killed')
            else:
                time.sleep(t)
        except:
            pass
