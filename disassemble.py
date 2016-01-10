# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 16:30:07 2016

@author: leonardojofre

descripcion: desensabla un archivo binario a codigo para mips 32 big-endian
man        : python disassemble.py -i <inputfile> -o <outputfile>
"""

import sys, getopt
import binascii
import mipsy

try:   
    from capstone import *
except:
    print("no se puede encontrar capstone, use pip install capstone")
    sys.exit(2)

registers = {
    '00000': '$zero','01000':'$t0','10000':'$s0','11000':'$t8',
    '00001': '$at'  ,'01001':'$t1','10001':'$s1','11001':'$t9',
    '00010': '$v0'  ,'01010':'$t2','10010':'$s2','11010':'$k0',
    '00011': '$v1'  ,'01011':'$t3','10011':'$s3','11011':'$k1',
    '00100': '$a0'  ,'01100':'$t4','10100':'$s4','11100':'$gp',
    '00101': '$a1'  ,'01101':'$t5','10101':'$s5','11101':'$sp',
    '00110': '$a2'  ,'01110':'$t6','10110':'$s6','11110':'$fp',
    '00111': '$a3'  ,'01111':'$t7','10111':'$s7','11111':'$ra',
}
    

# format \times opcode \times funct
operations = {
    ('R', '000000', '000000') :'nop',
    ('R', '000000', '100000') :'add',
    ('I', '001000', None)     :'addi',
    ('R', '000000', '100100') :'and',
    ('I', '000100', None)     :'beq',
    ('J', '000010', None)     :'j',
    ('J', '000011', None)     :'jal',
    ('R', '000000', '001000') :'jr',
    ('I', '100011', '100011') :'lw',
    ('R', '000000', '100101') :'or',
    ('R', '000000', '101010') :'slt',
    ('R', '000000', '000000') :'sll',
    ('I', '101011', None)     :'sw',
    ('R', '000000', '100010') :'sub',
}

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
    
    scale = 16 ## equals to hexadecimal
    for i in md.disasm(CODE, 0x10000000):
        ins = bin(int(binascii.hexlify(i.bytes), scale))[2:].zfill(32)
        
        print >> output_file, "0x%x:%s \t%s \t%s\t%s" %(i.address, binascii.hexlify(i.bytes), ins , i.mnemonic, i.op_str)
        
    output_file.close()
    
   
if __name__ == "__main__":
    main(sys.argv[1:])