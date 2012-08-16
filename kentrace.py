""" kentrace.py
    A collection of scripts that operate on Ken's debug traces """

#-------------------- Begin gnuplot requirements -----------------------
from numpy import *
import Gnuplot, Gnuplot.funcutils # For plotting with gnuplot
#-------------------- End gnuplot requirements -------------------------

#-------------------- Begin clint requirements -------------------------
from clint.textui import colored # Colored text output
from clint.textui import indent,puts # Allows indenting text
#-------------------- End clint requirements ---------------------------

import sys

mymarker = "--jp--> " # What I'll put at the beginning of my comments
modmarker = "hasmods" # Added to output file if it has already been written

regdict = {'Reg 0x00A1':'Register 0xa1 is the bandwidth configuration register',
           'Reg 0x00A7':'Register 0xa7 is the voltmeter configuration register',
           'Reg 0x00A5':'Register 0xa5 is the AC switch',
           'Reg 0x00A6':'Register 0xa6 is the I/V configuration register',
           'Reg 0x00A9':'Register 0xa9 is the front panel E bias rejection DAC',
           'Reg 0x0080':'Register 0x80 is the buddy box configuration register',
           'Reg 0x0032':'Register 0x32 is the waveform generator bias DAC',
           'Reg 0x0002':'Register 0x2 is the signal generation board configuration register',
           'Reg 0x0005':'Register 0x5 is the AC switch control register',
           'Reg 0x00A4':'Register 0xa4 is the external input gain DAC',
           'Reg 0x00A5':'Register 0xa5 is the front panel I BNC gain DAC',
           'Reg 0x00AD':'Register 0xad is the rear panel I BNC gain DAC',
           'Reg 0x0093':'Register 0x93 is the I ADC data',
           'Reg 0x0096':'Register 0x96 is the I ADC calibration value',
           'Reg 0x0000':'Last entry'
          }


""" makenote(note string)
    Formats note string into a note that will be inserted into the markup
    file.  Returns the full string. """
def makenote(note):
    notestring = (mymarker + note) 
    return notestring


""" regnames (input file object, output file name)
    Adds the name of the register immediately below the line referencing it. """
def regnames(infile,outfilename):
    fot = open(outfilename,'r')
    rawfile = fot.read()
    fot.close()
    fot = open(outfilename,'w') # Re-open the file for writing
    for line in rawfile.split('\n'):
        fot.write(line + '\n')
        if not line.startswith(mymarker):
            for key in regdict:
                if (line.count(key) != 0):
                    linestring = makenote(regdict[key])
                    fot.write(linestring + '\n')
                    

""" linenumber (input file object, output file name)
    Adds line numbers """
def linenumber(infile,outfilename):
    fot = open(outfilename,'r')
    rawfile = fot.read()
    fot.close()
    fot = open(outfilename,'w') # Re-open the file for writing
    linecount = 1
    for line in rawfile.split('\n'):
        fot.write(str(linecount) + ' ' +line + '\n')
        linecount += 1
    fot.close()
    
    
""" cleanfile(input file object, output file name)
    Cleans up the input file by making sure every line ends in a newline """
def cleanfile(infile,outfilename):
    fot = open(outfilename,'w')
    rawfile = infile.read()
    for line in rawfile.split('\r'):
        fot.write(line + '\n')
    fot.close()
 

        
    
    



def main():
    try:
        infile = sys.argv[1]
        fin = open(infile,'r')
        print ("Opened file " + sys.argv[1] + ".")
    except:
        print ("Failed to open input file " + sys.argv[1] + ".")
        return
    outfilename = infile.split(".")[0] + ".mrk"
    cleanfile(fin,outfilename)
    linenumber(fin,outfilename)
    regnames(fin,outfilename)
    print('Wrote file ' + outfilename)
    fin.close()

    




if __name__ == '__main__':
    main()
