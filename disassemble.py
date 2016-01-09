# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 16:30:07 2016

@author: leonardojofre

descripcion: desensabla un archivo binario a codigo para mips 32 little-endian
man        : python disassemble.py -i <inputfile> -o <outputfile>
"""

import sys, getopt
import binascii
try:   
    from capstone import *
except:
    print("no se puede encontrar capstone, use pip install capstone")
    sys.exit(2)


def main(argv):
    inputfile = ''
    outputfile = ''
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'disassemble.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
         
    if inputfile == '' or outputfile == '':
        print 'python disassemble.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
   
    print 'Input file is "', inputfile
    print 'Output file is "', outputfile
    
    source  = open(inputfile, mode = 'rb')
    CODE = source.read()
    md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 + CS_MODE_BIG_ENDIAN)
    
    output_file = open(outputfile , mode = "w+")
    
    for i in md.disasm(CODE, 0x10000000):   
        print >> output_file, "0x%x:%s \t%s\t%s" %(i.address, binascii.hexlify(i.bytes) , i.mnemonic, i.op_str)
        
    output_file.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])