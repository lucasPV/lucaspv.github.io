# EMULADOR PARA O INTERPRETADOR SECCOMP 2017 #
# ATIVIDADE: COMPLETE AS INSTRUÇÕES QUE FALTAM!

import os, sys
import time
import pygame
from pygame.locals import *

#lê o caminho da rom fornecida como entrada
romPath = sys.argv[1]

#definições gerais da arquitetura
memorySize    = 0xFFFF
displayWidth  = 64
displayHeight = 64
nKeys         = 26
nRegisters    = 0xF

#memórias
memory  = [0 for x in range(memorySize+1)] #RAM
display = [[0 for x in range(displayWidth+1)] for y in range(displayHeight+1)] #Vídeo
keys    = [0 for x in range(nKeys+1)] #Keyboard
stack   = [] #pilha de chamadas

#registradores
R  = [0 for x in range(nRegisters+1)] #propósito geral
PC = 0 #contador de programa (program counter)
SP = 0 #ponteiro da pilha (stack pointer)

#leitura da ROM
file = open(romPath,'rb')
rom  = list(file.read())
file.close()

#copia a ROM para a memória RAM
for i in range(len(rom)):
	memory[i] = rom[i]

pygame.init()
window = pygame.display.set_mode((displayWidth*10,displayHeight*10))
pygame.display.set_caption('Emulador')

SP = 0
PC = 0
print("Address    ", end='\t')
print("Instruction", end='\t')
print("Mnemonic",    end='\n')
while True:
	instr = (memory[PC]<<24 | memory[PC+1]<<16 |  memory[PC+2]<<8 | memory[PC+3])
	print('#%.8X' % PC,    end='\t')
	print('#%.8X' % instr, end='\t')

	#extração dos campos (busca da instrução)
	op1  = (0xF0 & memory[PC])>>4
	op2  = (0x0F & memory[PC])
	x    = (0xF0 & memory[PC+1])>>4
	y    = (0x0F & memory[PC+1])
	nnnn = ((memory[PC+2])<<8 | (memory[PC+3]))

	PC = PC + 4 #cada instrução são 4 bytes (32 bits)

	#verifica teclado
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				keys[ord('Q')-ord('A')] = 1
			elif event.key == pygame.K_o:
				keys[ord('O')-ord('A')] = 1
			elif event.key == pygame.K_l:
				keys[ord('L')-ord('A')] = 1
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_q:
				keys[ord('Q')-ord('A')] = 0
			elif event.key == pygame.K_o:
				keys[ord('O')-ord('A')] = 0
			elif event.key == pygame.K_l:
				keys[ord('L')-ord('A')] = 0

	#decodifica a instrução
	if op1 == 0x0: #NOP
		print("NOP", end='')
	elif op1 == 0x1: #LD
		if op2 == 0x0:
			print("LD R", hex(x)[2:], ",(#", hex(nnnn)[2:], ")", sep='', end='')
			R[x] = nnnn
		else:
			print("ERRO: Não foi possível executar a instrução!")
			exit(1)
	elif op1 == 0x2: #JP
		if op2 == 0x0:
			PC = nnnn
	elif op1 == 0x7: #HALT
		print("HALTED!")
		pygame.quit()
		quit()
		exit(0)
	else:
		print("ERRO: Não foi possível executar a instrução!")
		exit(1)

	#desenha
	for curX in range(displayWidth):
		for curY in range(displayWidth):
			r = (((0xF00 & display[curX][curY])>>8)/0XF)*255
			g = (((0x0F0 & display[curX][curY])>>4)/0XF)*255
			b = (((0x00F & display[curX][curY]))/0XF)*255
			pygame.draw.rect(window, (r,g,b), Rect((curX*10,curY*10), (10,10)))
	pygame.display.update()

	print("")

	#time.sleep(0.002)
