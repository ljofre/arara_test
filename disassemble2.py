#segunda version sin biblotecas
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
    ('I', '001001', None)     :'addiu',
    ('R', '000000', '100001') :'addu',
    ('R', '000000', '100100') :'and',
    ('I', '000100', None)     :'beq',
    ('J', '000010', None)     :'j',
    ('J', '000011', None)     :'jal',
    ('R', '000000', '001000') :'jr',
    ('I', '100011', None)     :'lw',
    ('R', '000000', '100101') :'or',
    ('R', '000000', '101010') :'slt',
    ('R', '000000', '000010') : 'srl',
    ('R', '000000', '000011') : 'sra',
    ('R', '000000', '000100') : 'sllv',
    ('R', '000000', '000000') :'sll',
    ('I', '101011', None)     :'sw',
    ('I', '001101', None)     :'ori',
    ('I', '001010', None)     :'slti',
    ('I', '001100', None)     :'andi',
    ('R', '000000', '100010') :'sub',
    ('I', '001110', None)     :'xori',
    ('R', '000000','100110')  :'xor',
    ('R', '000000','100111')  :'nor',
    ('R', '000000','000110')  :'srlv',
    ('R', '000000','000111')  :'srav',   
}

# test bin file
bin_file = open("./alu_test.bin", mode = 'rb')

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

instructions = instruction_generator(bin_file = bin_file)
hexa_dir = padhexa(hex(int('000000',2)))


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
    jump = ins[6:32]
    hexa_ins = padhexa(hex(int(ins, 2)))
    
    try:
        mnemonic = hexa_dir, hexa_ins, operations[("R", opcode, funct)], registers[rd], registers[rs], registers[rt]
        print("%s:%s\t%s %s %s %s" %mnemonic)
    except:
        try:
            if opcode == '101011':
                nmenomic = hexa_dir, hexa_ins, operations[("I", opcode, None)], hex(int(address, 2)), registers[rs]
                print(mnemonic)
            else:
                mnemonic = hexa_dir, hexa_ins, operations[("I", opcode, None)], registers[rt], registers[rs], hex(int(address, 2))
                print("%s:%s\t%s %s %s %s" %mnemonic)
        except:
            try:
                mnemonic = hexa_dir, hexa_ins, operations[("J",opcode, None)], jump
                print("%s:%s\t%s %s" %mnemonic)
            except:
                mnemonic = hexa_dir,hexa_ins, "unknown"
                print("%s:%s\t%s" %mnemonic)
    #inc the address
    hexa_dir = padhexa(hex(int(hexa_dir, 16) + 4))