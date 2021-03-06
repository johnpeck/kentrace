#!/cygdrive/c/Python27/python
""" kentrace.py
    A collection of scripts that operate on Ken's debug traces """


#-------------------- Begin clint requirements -------------------------
from clint.textui import colored # Colored text output
from clint.textui import indent,puts # Allows indenting text
#-------------------- End clint requirements ---------------------------

#------------------- Begin text formatting requirements ----------------
import textwrap
wrapit = textwrap.TextWrapper()
wrapit.width = 70 # Wrap at 70 columns
wrapit.replace_whitespace = True
#------------------- End text formatting requirements ------------------

import sys

mymarker = "--jp--> " # What I'll put at the beginning of my comments
modmarker = "hasmods" # Added to output file if it has already been written

# Dictionary of <register> : <register name>
regnamedict = {'Reg 0x0002':'Register 0x2 is the signal generation board configuration register',
               'Reg 0x0005':'Register 0x5 is the AC switch control register',
               'Reg 0x0032':'Register 0x32 is the waveform generator bias DAC',
               'Reg 0x0080':'Register 0x80 is the buddy box configuration register',
               'Reg 0x00A1':'Register 0xa1 is the bandwidth configuration register',
               'Reg 0x00A2':'Register 0xa2 is the first quad DAC',
               'Reg 0x00A3':'Register 0xa3 is the second quad DAC',
               'Reg 0x00A4':'Register 0xa4 is the external input gain DAC',
               'Reg 0x00A5':'Register 0xa5 is the front panel I BNC gain DAC',
               'Reg 0x00A6':'Register 0xa6 is the I/V configuration register',
               'Reg 0x00A7':'Register 0xa7 is the voltmeter configuration register',
               'Reg 0x00A8':'Register 0xa8 is the front panel E BNC gain DAC',
               'Reg 0x00A9':'Register 0xa9 is the front panel E bias rejection DAC',
               'Reg 0x00AA':'Register 0xaa is the rear panel E BNC gain DAC',
               'Reg 0x00AB':'Register 0xab is the current interrupt boost DAC',
               'Reg 0x00AC':'Register 0xac is the positive feedback DAC',
               'Reg 0x00AD':'Register 0xad is the rear panel I BNC gain DAC',
               'Reg 0x0093':'Register 0x93 is the I ADC data',
               'Reg 0x0096':'Register 0x96 is the I ADC calibration value.',
               'Query 0x0092':'Register 0x92 is the E ADC data',
               'Query 0x0093':'Register 0x93 is the I ADC data',
               'Query 0x0094':'Register 0x94 is the Synchronous ADC data',
               'Reg 0x0000':'Last entry'
}

# Dictionary of <register> : <register notes>
regnotedict = {'Reg 0x0096':(wrapit.fill('For the I ADC, remember that the full-scale output in hex is range dependent.  0x20c49b is full-scale for the 1mA range (indicates that 1mA is flowing), while 0x2af31d is full-scale for the 10nA range.  These values are tabulated in the FPGA design document.'))
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
            # Write the register name
            for key in regnamedict:
                if (line.count(key) != 0):
                    linestring = makenote(regnamedict[key])
                    fot.write(linestring + '\n')
            # Write the register notes
            for key in regnotedict:
                if (line.count(key) != 0):
                    for noteline in regnotedict[key].splitlines():
                        fot.write(mymarker + noteline + '\n')



                    

""" linenumber (input file object, output file name)
    Adds line numbers """
def linenumber(infile,outfilename):
    fot = open(outfilename,'r')
    rawfile = fot.read()
    fot.close()
    fot = open(outfilename,'w') # Re-open the file for writing
    linecount = 1
    for line in rawfile.split('\n'):
        if not line.startswith(mymarker):
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

""" addheader(input file object, output file name)
    Adds a header to the beginning of the file. """
def addheader(infile,outfilename):
    fot = open(outfilename,'r')
    rawfile = fot.read()
    fot.close()
    fot = open(outfilename,'w') # Re-open the file for writing
    headstr = wrapit.fill("Worked-up output trace from EC301's debug port.  The ecscripts directory contains fcal.py, which has functions related to decomposing hex register settings into human-readable states:")
    for line in headstr.splitlines():
        fot.write(mymarker + line + '\n') # Write the long part of the header
    fot.write(mymarker + "bwbitview(integer) -- Bandwidth configuration register" + '\n')
    fot.write(mymarker + "ivbitview(integer) -- Internal I/V configuration register" + '\n')
    fot.write(mymarker + "bbbitview(integer) -- Buddy box configuration register" + '\n')
    fot.write(mymarker + "vmbitview(integer) -- Internal voltmeter configuration register" + '\n')
    for line in rawfile.split('\n'):
        fot.write(line + '\n') # Write the rest of the file
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
    addheader(fin,outfilename)
    regnames(fin,outfilename)
    print('Wrote file ' + outfilename)
    fin.close()

    




if __name__ == '__main__':
    main()
