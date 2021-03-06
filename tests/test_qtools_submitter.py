'''
Created on Aug 1, 2013

@author: Olga Botvinnik
'''
import unittest

from gscripts.qtools import Submitter
import subprocess
from subprocess import PIPE

import tests


class Test(unittest.TestCase):
    def test_main(self):
        commands = ['date', 'echo testing PBS']
        job_name = 'test_qtools_submitter'
        submit_sh = '%s/%s.sh' % (tests.get_test_dir(), job_name)
        sub = Submitter(queue_type='PBS', sh_file=submit_sh,
                        command_list=commands,
                        job_name=job_name)
        job_id = sub.write_sh(submit=True, nodes=1, ppn=16,
                                 queue='home-yeo', walltime='0:01:00')
        true_result_string = '''#!/bin/sh
#PBS -N test_qtools_submitter
#PBS -o %s/test_qtools_submitter.sh.out
#PBS -e %s/test_qtools_submitter.sh.err
#PBS -V
#PBS -l walltime=0:01:00
#PBS -l nodes=1:ppn=16
#PBS -A yeo-group
#PBS -q home-yeo

# Go to the directory from which the script was called
cd $PBS_O_WORKDIR
date
echo testing PBS
''' % (tests.get_test_dir(), tests.get_test_dir())
        true_result = true_result_string.split('\n')

        # with open(submit_sh) as f:
        #     for x in f.readlines():
        #         print x,

        for true, test in zip(true_result, open(submit_sh)):
            self.assertEqual(true.strip().split(), test.strip().split())

        # Make sure the job ID is a single (potentially multi-digit) integer
        self.assertRegexpMatches(job_id, '^\d+$')
        subprocess.Popen(["qdel", job_id],
                                 stdout=PIPE)

    def test_wait_for_pbs(self):
        commands = ['date', 'echo testing PBS']
        job_name = 'test_qtools_submitter_wait_for_pbs'
        submit_sh = '%s/%s.sh' % (tests.get_test_dir(), job_name)
        sub = Submitter(queue_type='PBS', sh_file= submit_sh,
                        command_list=commands,
                        job_name=job_name, wait_for=['11111'])
        job_id = sub.write_sh(submit=True, nodes=1, ppn=16,
                                 queue='home-yeo', walltime='0:01:00')
        true_result_string = '''#!/bin/sh
#PBS -N test_qtools_submitter_wait_for_pbs
#PBS -o %s/test_qtools_submitter_wait_for_pbs.sh.out
#PBS -e %s/test_qtools_submitter_wait_for_pbs.sh.err
#PBS -V
#PBS -l walltime=0:01:00
#PBS -l nodes=1:ppn=16
#PBS -A yeo-group
#PBS -q home-yeo
#PBS -W depend=afterok:11111

# Go to the directory from which the script was called
cd $PBS_O_WORKDIR
date
echo testing PBS
''' % (tests.get_test_dir(), tests.get_test_dir())
        true_result = true_result_string.split('\n')

        # with open(submit_sh) as f:
        #     for x in f.readlines():
        #         print x,

        for true, test in zip(true_result, open(submit_sh)):
            self.assertEqual(true.strip().split(), test.strip().split())

        # Make sure the job ID is a single (potentially multi-digit) integer
        self.assertRegexpMatches(job_id, '^\d+$')
        subprocess.Popen(["qdel", job_id],
                                 stdout=PIPE)

    def test_wait_for_array_pbs(self):
        commands = ['date', 'echo testing PBS']
        job_name = 'test_qtools_submitter_wait_for_pbs'
        submit_sh = '%s/%s.sh' % (tests.get_test_dir(), job_name)
        sub = Submitter(queue_type='PBS', sh_file= submit_sh,
                        command_list=commands,
                        job_name=job_name, wait_for_array=['11111'])
        job_id = sub.write_sh(submit=True, nodes=1, ppn=16,
                                 queue='home-yeo', walltime='0:01:00')
        true_result_string = '''#!/bin/sh
#PBS -N test_qtools_submitter_wait_for_pbs
#PBS -o %s/test_qtools_submitter_wait_for_pbs.sh.out
#PBS -e %s/test_qtools_submitter_wait_for_pbs.sh.err
#PBS -V
#PBS -l walltime=0:01:00
#PBS -l nodes=1:ppn=16
#PBS -A yeo-group
#PBS -q home-yeo
#PBS -W depend=afterokarray:11111

# Go to the directory from which the script was called
cd $PBS_O_WORKDIR
date
echo testing PBS
''' % (tests.get_test_dir(), tests.get_test_dir())
        true_result = true_result_string.split('\n')

        # with open(submit_sh) as f:
        #     for x in f.readlines():
        #         print x,

        for true, test in zip(true_result, open(submit_sh)):
            self.assertEqual(true.strip().split(), test.strip().split())

        # Make sure the job ID is a single (potentially multi-digit) integer
        self.assertRegexpMatches(job_id, '^\d+$')
        subprocess.Popen(["qdel", job_id],
                                 stdout=PIPE)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_main']
    unittest.main()