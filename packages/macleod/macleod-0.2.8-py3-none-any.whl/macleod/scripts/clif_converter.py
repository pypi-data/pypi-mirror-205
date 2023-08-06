'''
Created on 2019-03-07

@author: Torsten Hahmann
'''

import os, sys, argparse, logging

import Macleod.scripts.licence

#print(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../")


import Macleod.Filemgt as Filemgt
import Macleod.parsing.parser as Parser
#from Macleod.Filemgt import Filemgt

# defaults for the ontology directory and basepath
default_dir = Filemgt.read_config('system', 'path')
default_prefix = Filemgt.read_config('cl', 'prefix')
tptp_output = 'tptp'
ladr_output = 'ladr'


def deprec():
    print("This script is no longer supported, please use the scripts clif_to_tptp, clif_to_owl, clif_to_ladr, or clif_to_owl instead.")

def convert_single_clif_file(ontology, output, resolve, loc=default_dir, prefix=default_prefix):

    logging.getLogger(__name__).info("Converting " + ontology.name + " to " + output + " format")

    if (output == tptp_output):
        results = ontology.to_tptp(resolve)
    elif (output == ladr_output):
        results = ontology.to_ladr(resolve)

    # the following assumes that the names of the configuration sections are the same as the names of the output (tptp/ladr)
    if resolve:
        ending = Filemgt.read_config(output, 'all_ending')
    else:
        ending = ""

    ending = ending + Filemgt.read_config(output, 'ending')

    output_file_name = Filemgt.get_full_path(ontology.name,
                                           folder=Filemgt.read_config('tptp','folder'),
                                           ending=ending)
    #ontology.get_all_modules()

    with open(output_file_name, "w") as f:
        for sentence in results:
            print(sentence)
            f.write(sentence + "\n")
        f.close()

    return output_file_name



def convert_all_clif_files(folder, output, resolve, loc=default_dir, prefix=default_prefix):

    # TODO move this functionality to the new check_consistency script
    tempfolder = Filemgt.read_config('converters', 'tempfolder')
    ignores = [tempfolder]
    cl_ending = Filemgt.read_config('cl', 'ending')
    logging.getLogger(__name__).info("Traversing folder " + folder)

    for directory, subdirs, files in os.walk(folder):
        if any(ignore in directory for ignore in ignores):
            pass
        else:
            for single_file in files:
                if single_file.endswith(cl_ending):
                    file = os.path.join(directory, single_file)
                    logging.getLogger(__name__).info("Found CL file " + file)
                    ontology = Parser.parse_file(file, prefix, loc, resolve)
                    convert_single_clif_file(ontology, output, resolve, loc, prefix)



def main():
    deprec()

if __name__ == '__main__':
    sys.exit(main())

