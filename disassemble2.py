# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 11:57:01 2016

@author: leonardojofre
"""

#segunda version
import binascii

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
        
bin_file = open("./alu_test.bin", mode = 'rb')

scale = 16

def instruction_generator(bin_file):
    while 1:
        try:
            yield bin(int(binascii.hexlify(bin_file.read(4)), scale))[2:].zfill(32)
        except:
            return

instructions = instruction_generator(bin_file = bin_file)
mem = hex(int('00000000',2))
for ins in instructions:
    # si fuera del tipo R
    opcode = ins[0:6]
    rs = ins[6:11]
    rt = ins[11:16]
    rd = ins[16:21]
    shamt = ins[21:26]
    funct = ins[26:32]
    
    #si fuera del tipo I
    address = ins[16:32]
    
    # si fuera del tipo J
    jump = ins[11:32]
    hexa_ins = hex(int(ins, 2))
    print 'direccion: ', mem 
    try:
        print operations[("R", '000000', funct)], registers[rs], registers[rt], registers[rd]
    except:
        try:
            print operations[("I", opcode, None)]
        except:
            try:
                operations[("J",opcode, None)]
            except:
                pass