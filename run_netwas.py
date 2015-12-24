"""
(C) Casey Greene.

This python script runs netwas for every standard in the vegas_ad1 and
vegas_ad2 folders. After some of the first set of jobs failed because ppn=1,
set ppn=4 and make re-runnable.
"""

import os
from pbsjob import PBSJob

job = PBSJob(name="netwas", queue="largeq", walltime="02:00:00",
             addr="casey.s.greene@dartmouth.edu", command="echo $host", ppn=4)

if not os.path.exists('results'):
    os.mkdir('results')

if not os.path.exists('results/vegas_ad1'):
    os.mkdir('results/vegas_ad1')

for standard in os.listdir('standards/vegas_ad1'):
    labels = 'standards/vegas_ad1/' + standard
    results = 'results/vegas_ad1/' + standard
    if not os.path.exists(results):
        job.set_name_command('netwas-ad1-' + standard, 'SVMperfer -l ' +
                             labels + ' -o ' + results + ' -i ' +
                             'data/hippocampus.dab -a -k 0 -c 5 -e 2 -t 50')
        job.submit('jobs/netwas-ad1-' + standard + '.pbs')

if not os.path.exists('results/vegas_ad2'):
    os.mkdir('results/vegas_ad2')

for standard in os.listdir('standards/vegas_ad2'):
    labels = 'standards/vegas_ad2/' + standard
    results = 'results/vegas_ad2/' + standard
    if not os.path.exists(results):
        job.set_name_command('netwas-ad2-' + standard, 'SVMperfer -l ' +
                             labels + ' -o ' + results + ' -i ' +
                             'data/hippocampus.dab -a -k 0 -c 5 -e 2 -t 50')
        job.submit('jobs/netwas-ad2-' + standard + '.pbs')
