# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 16:30:07 2016

@author: leonardojofre

descripcion: segunda version para desensabla un archivo binario a codigo para mips 32 big-endian
man        : python disassemble2.py -i <inputfile> -o <outputfile>
"""

import sys, getopt
import binascii
from registers import *

try:   
    from capstone import *
except:
    print("no se puede encontrar capstone, use pip install capstone")
    sys.exit(2)
    
def instruction_generator(bin_file):
    scale = 16 #hexadecimal
    while 1:
        try:
            yield bin(int(binascii.hexlify(bin_file.read(4)), scale))[2:].zfill(32)
        except:
            return

def padhexa(s):
    #add padding to hex number
    return '0x' + s[2:].zfill(8)

def jump_address(binaty_str):
    return hex(int(binaty_str.zfill(32-2)+'00',2))


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
    
        # test bin file
    bin_file = open(inputfile, mode = 'rb')
    output_file = open(outputfile , mode = "w+")
        
    instructions = instruction_generator(bin_file = bin_file)
    hexa_dir = padhexa(hex(int('000000',2)))
    
    
    for ins in instructions:
        # si fuera del tipo R
        opcode = ins[0:6]; rs = ins[6:11]; rt = ins[11:16]; rd = ins[16:21]; shamt = ins[21:26]; funct = ins[26:32]
        
        #si fuera del tipo I
        address = ins[16:32]
        
        # si fuera del tipo J
        jump = ins[6:32]
        
        #instruccion en hexadecimal
        hexa_ins = padhexa(hex(int(ins, 2)))
        
        print >> output_file,"%s:%s"%(hexa_dir, hexa_ins),
        try:
            # si encuentra del tipo R
            if funct == '000000':
                mnemonic = operations[("R", opcode, funct)], reg[rd], reg[rs], int(rt)
                print >> output_file,"\t%s %s, %s, %s" %mnemonic
            else:
                mnemonic = operations[("R", opcode, funct)], reg[rd], reg[rs], reg[rt]
                print >> output_file, "\t%s %s, %s, %s" %mnemonic
        except KeyError:
            try:
            # si encuentra del tipo I
                if opcode == '101011': #sw
                    mnemonic = operations[("I", opcode, None)], reg[rt], hex(int(address, 2)), reg[rs]
                    print >> output_file, "\t%s, %s, %s(%s)" %mnemonic
                
                else:
                    mnemonic = operations[("I", opcode, None)], reg[rt], reg[rs], hex(int(address, 2))
                    print  >> output_file, "\t%s %s, %s, %s" %mnemonic
            except KeyError:
                
                try:
                    # si encuentra del tipo J
                    mnemonic = operations[("J",opcode, None)], padhexa(jump_address(jump))
                    print >> output_file, "\t%s %s" %mnemonic
                except KeyError:
                    mnemonic = "unknown"
                    print >> output_file, "\t%s" %mnemonic
        #inc the address
        hexa_dir = padhexa(hex(int(hexa_dir, 16) + 4))
        
        
    output_file.close()
    
   
if __name__ == "__main__":
    main(sys.argv[1:])