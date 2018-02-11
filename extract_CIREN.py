import sys
import os
from sas7bdat import SAS7BDAT


files = os.listdir(os.getcwd())
sasfiles = [x for x in files if 'sas7bdat' in x]


for infilename in sasfiles:
    outfilename = infilename.split(".")[0] + ".csv"
    print("reading {} and writing to {}".format(infilename, outfilename))
    with SAS7BDAT(infilename) as infile:
        with open(outfilename, "w+") as outfile:
            for linelist in infile:
                line = ",".join(list(map(str, linelist))) ## some lines contain numeric values
                outfile.write(line + "\n")
sys.exit(0)
