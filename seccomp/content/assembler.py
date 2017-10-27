# MONTADOR PARA O INTERPRETADOR SECCOMP 2017 #

import os,sys
import re
import binascii

def trim(x):
	pat = re.compile(r'\s+')
	return pat.sub('',rest)

def match(exp,i,args):
	try:
		args[0] = (re.findall(exp, i))[0]
	except:
		args[0] = []
	return args[0]

filename = sys.argv[1]

f = open(filename,'r')
code = [x.strip('\n') for x in f.readlines()] #read lines
f.close()

code = [x.split('%')[0] for x in code] #remove comments

#remove empty lines
code = [x.strip() for x in code]
code = [x for x in code if (x != '')]

#everything in uppercase
code = [x.upper() for x in code]

#prepare labels and instructions
addr = 0
labels = {}
instr  = []
for line in code:
	if ':' in line: #it's a label
		label = line.split(':')[0]
		labels[label] = addr
	else: #it's a instruction
		op = line.split()[0] #mnemonic
		inst = ''
		try:
			rest = line.split(None,1)[1]
			inst = op + " " + trim(rest)
		except:
			inst = op
		instr.append(inst)
		addr = addr + 4 #each instruction has 4 bytes


bytesarray = bytearray()

hexaIndex = '([0-9A-F])'
hexaValue = '([0-9A-F]+)'
for i in instr:
	args = [0]
	#print(i)

	b1 = 0x00
	b2 = 0x00
	b3 = 0x00
	b4 = 0x00

	if i == "NOP":
		b1 = 0x00
	elif i == "CLS":
		b1 = 0x60
	elif i == "HALT":
		b1 = 0x70
	elif match("LD R" + hexaIndex + ",#" + hexaValue, i, args) != []:
		b1 = 0x10
		b2 = int(args[0][0],16)<<4
		b3 = (int(args[0][1],16)&(0xFF00))>>8
		b4 = (int(args[0][1],16)&(0x00FF))
	elif match("LD R" + hexaIndex + ",R" + hexaIndex, i, args) != []:
		b1 = 0x11
		b2 = int(args[0][0],16)<<4 | int(args[0][1],16)
	elif match("LD \(#" + hexaValue + "\),R" + hexaIndex, i, args) != []:
		b1 = 0x12
		b2 = int(args[0][1],16)<<4
		b3 = (int(args[0][0],16)&(0xFF00))>>8
		b4 = (int(args[0][0],16)&(0x00FF))
	elif match("LD R" + hexaIndex + ",\(#" + hexaValue + "\)", i, args) != []:
		b1 = 0x13
		b2 = int(args[0][0],16)<<4
		b3 = (int(args[0][1],16)&(0xFF00))>>8
		b4 = (int(args[0][1],16)&(0x00FF))
	elif match("LD R" + hexaIndex + ",'([A-Z]+)'", i, args) != []:
		key = int(ord(args[0][1]))
		b1 = 0x14
		b2 = int(args[0][0],16)<<4
		b3 = (key&(0xFF00))>>8
		b4 = (key&(0x00FF))
	elif match("JP (\w+)", i, args) != []:
		addr = labels[args[0]]
		b1 = 0x20
		b3 = (addr&(0xFF00))>>8
		b4 = (addr&(0x00FF))
	elif match("CALL (\w+)", i, args) != []:
		addr = labels[args[0]]
		b1 = 0x21
		b3 = (addr&(0xFF00))>>8
		b4 = (addr&(0x00FF))
	elif match("RET", i, args) != []:
		b1 = 0x22
	elif match("BEQ R" + hexaIndex + ",R" + hexaIndex + ",(\w+)", i, args) != []:
		addr = labels[args[0][2]]
		b1 = 0x30
		b2 = int(args[0][0],16)<<4 | int(args[0][1],16)
		b3 = (addr&(0xFF00))>>8
		b4 = (addr&(0x00FF))
	elif match("BGT R" + hexaIndex + ",R" + hexaIndex + ",(\w+)", i, args) != []:
		addr = labels[args[0][2]]
		b1 = 0x31
		b2 = int(args[0][0],16)<<4 | int(args[0][1],16)
		b3 = (addr&(0xFF00))>>8
		b4 = (addr&(0x00FF))
	elif match("BLT R" + hexaIndex + ",R" + hexaIndex + ",(\w+)", i, args) != []:
		addr = labels[args[0][2]]
		b1 = 0x32
		b2 = int(args[0][0],16)<<4 | int(args[0][1],16)
		b3 = (addr&(0xFF00))>>8
		b4 = (addr&(0x00FF))
	elif match("ADD R" + hexaIndex + ",R" + hexaIndex, i, args) != []:
		b1 = 0x40
		b2 = int(args[0][0],16)<<4 | int(args[0][1],16)
	elif match("SUB R" + hexaIndex + ",R" + hexaIndex, i, args) != []:
		b1 = 0x41
		b2 = int(args[0][0],16)<<4 | int(args[0][1],16)
	elif match("MUL R" + hexaIndex + ",R" + hexaIndex, i, args) != []:
		b1 = 0x42
		b2 = int(args[0][0],16)<<4 | int(args[0][1],16)
	elif match("DIV R" + hexaIndex + ",R" + hexaIndex, i, args) != []:
		b1 = 0x43
		b2 = int(args[0][0],16)<<4 | int(args[0][1],16)
	elif match("AND R" + hexaIndex + ",R" + hexaIndex, i, args) != []:
		b1 = 0x50
		b2 = int(args[0][0],16)<<4 | int(args[0][1],16)
	elif match("OR R" + hexaIndex + ",R" + hexaIndex, i, args) != []:
		b1 = 0x51
		b2 = int(args[0][0],16)<<4 | int(args[0][1],16)
	elif match("NOT R" + hexaIndex, i, args) != []:
		b1 = 0x52
		b2 = int(args[0][0],16)<<4
	elif match("DRW R" + hexaIndex + ",R" + hexaIndex + ",R" + hexaIndex + ",R" + hexaIndex + ",R" + hexaIndex, i, args) != []:
		b1 = 0x61
		b2 = int(args[0][0],16)<<4 | int(args[0][1],16)
		b3 = int(args[0][2],16)<<4 | int(args[0][3],16)
		b4 = int(args[0][4],16)<<4
	else:
		print("ERROR: ", i ," NOT IMPLEMENTED!")
		exit(1)

	bytesarray.append(b1)
	bytesarray.append(b2)
	bytesarray.append(b3)
	bytesarray.append(b4)

f = open(sys.argv[2],'wb')
f.write(bytesarray)
f.close()
