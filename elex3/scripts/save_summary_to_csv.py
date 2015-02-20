#!/usr/bin/env python
"""
This script leverages re-usable bits of code in the lib/ directory to
generate a summary CSV of election results.

USAGE:

    python save_summary_results_to_csv.py


OUTPUT:

    summary_results.csv containing racewide totals for each race/candidate pair.


"""
from os.path import dirname, join
import csv

#TODO: MAKE SURE parent dir of elex3 is on module search path so that
# fully qualified imports (e.g. from elex3.lib.foo import foobar) will work!!!

# Initial wiring for our shell script
def main():
    # Path to the downloaded results
    path = join(dirname(dirname(__file__)), 'fake_va_elec_results.csv')
    #TODO: Insert your own AMAZIGINGLY readable functions,
    # imported from other libs and/or defined here

if __name__ == '__main__':
    main()
