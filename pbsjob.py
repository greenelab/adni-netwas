import sys
from subprocess import Popen, PIPE

class PBSJob:
    """
    Job for working with Torque at Dartmouth
    If you use job-arrays, the dartmouth-defined limit is 100, for more
    you have to submit jobs individually
    """
    def __init__(self, name='', queue='default', nodes=1, ppn=1,
                 walltime = '01:00:00', mail='a', addr=None,
                 cwd = True, command = None, array=None, depends=None):
        self.name = name
        self.queue = queue
        self.nodes = nodes
        self.ppn = ppn
        self.walltime = walltime
        self.mail = mail
        self.array = array
        self.depends = depends
        if addr is None:
            sys.stderr.write('An email address is REQUIRED')
            return None
        self.addr = addr
        self.cwd = cwd
        if command is None:
            sys.stderr.write('A command is REQUIRED')
            return None
        self.command = command

    def set_command(self, command):
        self.command = command

    def set_name_command(self, name, command):
        self.name = name
        self.command = command

    #depends should be a list of jobs, uses afterok rule by default
    def set_depends(self, depends):
        self.depends = depends

    def submit(self, filename):
        self.write(filename)
        stdout = Popen('qsub ' + filename, shell=True, stdout=PIPE).stdout.read()
        return stdout.strip()

    def write(self, filename):
        ofile = open(filename, 'w')
        ofile.write('#!/bin/bash -l\n')
        ofile.write('#PBS -N ' + str(self.name) + '\n')
        ofile.write('#PBS -q ' + str(self.queue) + '\n')
        ofile.write('#PBS -l nodes=' + str(self.nodes) + ':ppn=' + str(self.ppn) + '\n')
        ofile.write('#PBS -l walltime=' + str(self.walltime) + '\n')
        ofile.write('#PBS -m ' + str(self.mail) + '\n')
        ofile.write('#PBS -M ' + str(self.addr) + '\n')
        if self.depends is not None:
            ofile.write('#PBS -W depend=afterok:' + ':'.join(self.depends) + '\n')
        if self.array is not None:
            ofile.write('#PBS -t 1-' + str(self.array) + '\n')
        ofile.write('export TERM=xterm\n')
        if self.cwd:
            ofile.write('cd $PBS_O_WORKDIR\n')
        ofile.write(str(self.command) + '\n')
        ofile.write('exit 0\n')
        ofile.close()
