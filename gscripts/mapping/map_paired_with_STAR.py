#!/usr/bin/env python

from glob import glob
from qtools import Submitter
# import sys
#
# species = sys.argv[1]

#!/usr/bin/env python

# Parse command line arguments
import argparse

'''
Author: Olga Botvinnik
Date created: 07/11/2013 14:12

The purpose of this program is to ...

Example run:
cd dir_with_sequencing_files
python map_paired_with_STAR.py
'''

#######################################################################
# Class: CommandLine
#######################################################################
class CommandLine(object):
    def __init__(self, inOpts=None):
        self.parser = argparse.ArgumentParser(
            description=''' Given a number of digits "n" and number of
            iterations "N", calculate .....
            ''',
            add_help=True, prefix_chars='-')
        self.parser.add_argument('--species', '-s', action='store',
                                 type=str, default='hg19', required=True,
                                 help="Which species' genome to map to")
        self.parser.add_argument('--read-number-prefix', action='store',
                                 type=str, default='R',
                                 help='The prefix before the read number in '
                                      'the .fastq filename, e.g. Sample1_R1'
                                      '.fastq and Sample1_R2.fastq')
        self.parser.add_argument('--file-extension', action='store',
                                 type=str, default='fastq.gz',
                                 help='File extension of the sequencing '
                                      'files'
                                      '. Most often, this is `fastq`, '
                                      '`fastq.gz`, `fq`, or `fq.gz`')
        self.parser.add_argument('--STAR', type=str, action='store',
                                 default='/home/yeo-lab/software/STAR_2.3'
                                         '.0e/STAR',
                                 help='Which installation of STAR to use.')
        self.parser.add_argument('--no-sam2bam-sort-index', type=bool,
                                 action='store_true', required=False,
                                 default=False,
                                 help='The default is to convert the SAM file'
                                      ' produced by STAR to BAM, '
                                      'then sort and index it using the '
                                      'sam_to_bam.py script from MISO. If you'
                                      ' do not wish to do so, turn off this '
                                      'functionality, specify this flag.')

        if inOpts is None:
            self.args = vars(self.parser.parse_args())
        else:
            self.args = vars(self.parser.parse_args(inOpts))

    def do_usage_and_die(self, str):
        '''
        If a critical error is encountered, where it is suspected that the
        program is not being called with consistent parameters or data, this
        method will write out an error string (str), then terminate execution
        of the program.
        '''
        import sys

        print >> sys.stderr, str
        self.parser.print_usage()
        return 2


#######################################################################
# Class: Usage
#######################################################################
class Usage(Exception):
    '''
    Used to signal a Usage error, evoking a usage statement and eventual
    exit when raised
    '''

    def __init__(self, msg):
        self.msg = msg


#######################################################################
# Function: main
#######################################################################
def main():
    '''
    This function is invoked when the program is run from the command line,
    i.e. as:
        python program.py
    or as:
        ./program.py
    If the user has executable permissions on the user (set by chmod ug+x
    program.py or by chmod 775 program py. Just need the 4th bit set to true)
    '''
    cl = CommandLine()
    try:
        read_number_prefix = cl.args['read_number_prefix']
        file_extension = cl.args['file_extension']
        species = cl.args['species']
        STAR = cl.args['STAR']

        # assume
        if file_extension.endswith('z'):
            zcat_command = '--readFilesCommand zcat'
        else:
            zcat_command = ''


        for read1 in glob('*%s1*%s' % (read_number_prefix, file_extension)):
            base_dir = os.path.dirname(read1)
            read2 = read1.replace('%s1' % read_number_prefix,
                             '%s2' % read_number_prefix)
            filename_prefix = read1 + '.'
            commands = []
            commands.append('%s \
        --runMode alignReads \
        --runThreadN 16 \
        --genomeDir /projects/ps-yeolab/genomes/%s/star/ \
        --genomeLoad LoadAndRemove \
        --outFileNamePrefix %s \
        --readFilesIn %s, %s \
        --outSAMunmapped Within \
        --outFilterMultimapNmax 1 %s'
                            % (STAR, species, read1, read2, filename_prefix,
                                         zcat_command))
            commands.append('sleep 500')

            sam = filename_prefix + '.Aligned.out.sam'
            commands.append('sam_to_bam.py --convert %s %s--ref '
                            '/projects/ps-yeolab/genomes/%s/chromosomes/all.fa'
                            '.fai'
                            % (sam, base_dir, species))

            sub = Submitter(queue_type='PBS', sh_file=read1+'_map.sh',
                            command_list=commands, job_name='map_'+read1)
            sub.write_sh(submit=True, nodes=16, ppn=4, queue='glean')


        # for file in glob('*Rd1*gz'):
        #     pair = file.replace('Rd1', 'Rd2')
        #     name = file.replace('_Rd1', '')
        #     cmd_list = []
        #     cmd_list.append('/home/yeo-lab/software/STAR_2.3.0e/STAR \
        # --runMode alignReads \
        # --runThreadN 16 \
        # --genomeDir /projects/ps-yeolab/genomes/{}/star/ \
        # --genomeLoad LoadAndRemove \
        # --readFilesCommand zcat \
        # --readFilesIn {},{} \
        # --outFileNamePrefix {}. \
        # --outSAMunmapped Within \
        # --outFilterMultimapNmax 1'.format(species, file, pair, name))
        #
        #     sub = Submitter(queue_type='PBS', sh_file='map_'+file+'.sh',
        #                     command_list=cmd_list, job_name='map_'+file)
        #     sub.write_sh(submit=True, nodes=1, ppn=16, queue='glean')
        #
        # pass
    # If not all the correct arguments are given, break the program and
    # show the usage information
    except Usage, err:
        cl.do_usage_and_die(err.msg)


if __name__ == '__main__':
    main()

