% SIMPLE PONG GAME
% AUTHOR: LUCAS PASCOTTI VALEM

%globals used:
%R0 = #0
%R1 = #1
%R5 = y pad
%R6 = x ball
%R7 = y ball
%R8 = vx ball
%R9 = vy ball

main:
	CLS

	CALL setup

	loop:
		CALL check_quit

		CALL check_pad_move

		CALL ball_move

		CALL draw_ball

		CALL draw_pad

		JP loop


setup:
	LD R0,#0
	LD R1,#1
	LD R5,#5 %y pad
	LD R6,#1F %x ball
	LD R7,#A %y ball
	LD R8,#5 %vx ball
	LD R9,#1 %vy ball
	NOT R8
	RET

check_quit:
	LD  RF,'Q'
	BEQ RF,R1,quit
	RET

draw_pad: 
	%globals used: R5 = y pad

	LD RA,#000 %x pad
	LD RB,#002 %width
	LD RC,#007 %height
	LD RD,#F00 %color

	DRW RA,R5,RB,RC,RD
	RET

draw_ball:
	LD RD,#00F %color
	DRW R6,R7,R1,R1,RD
	RET

erase_pad: 
	%globals used: R5 = y pad

	LD RA,#000 %x pad
	LD RB,#002 %width
	LD RC,#007 %height

	DRW RA,R5,RB,RC,R0
	RET

erase_ball:
	DRW R6,R7,R1,R1,R0
	RET

check_pad_move:
	LD  RF,'O'
	BEQ RF,R1,move_pad_up

	LD  RF,'L'
	BEQ RF,R1,move_pad_down

	RET

move_pad_up:
	%globals used: R5 = y pad

	%CALL erase_pad
	CLS

	LD RF,#6 %increment

	SUB R5,RF

	BLT R5,R0,collision_pad_top

	RET

move_pad_down:
	%globals used: R5 = y pad

	CALL erase_pad

	LD RF,#6 %increment

	ADD R5,RF

	LD RF,#40 %display height
	LD RB,#007 %height
	SUB RF,RB
	BGT R5,RF,collision_pad_bottom

	RET

collision_pad_top:
	LD R5,R0
	RET

collision_pad_bottom:
	LD R5,RF
	RET

ball_move:
	CALL erase_ball

	ADD R6,R8 %update x

	ADD R7,R9 %update y

	CALL collision_pad_ball

	CALL check_ball_x

	CALL check_ball_y

	RET

check_ball_x:
	BLT R6,R0,collision_ball_right

	LD RF,#40 %display height
	SUB RF,R1
	BGT R6,RF,collision_ball_left

	RET

collision_ball_right:
	LD R6,R0
	NOT R8 %change direction
	SUB R7,R9 %do not update y
	RET

collision_ball_left:
	LD R6,RF
	NOT R8 %change direction
	SUB R7,R9 %do not update y
	RET

check_ball_y:
	BLT R7,R0,collision_ball_top

	LD RF,#40 %display height
	SUB RF,R1
	BGT R7,RF,collision_ball_bottom

	RET

collision_ball_top:
	LD R7,R0
	NOT R9 %change direction
	SUB R6,R8 %do not update x
	RET

collision_ball_bottom:
	LD R7,RF
	NOT R9 %change direction
	SUB R6,R8 %do not update x
	RET

collision_pad_ball:
	LD  RA,#002 %width pad
	BLT R6,RA,collision_pad_ball_y
	RET

collision_pad_ball_y:
	BLT R7,R5,game_over
	LD  RA,#6
	ADD RA,R5
	BGT R7,RA,game_over
	NOT R8
	LD  R6,#2

	%increase ball speed
	ADD R8,R1
	ADD R9,R1

	RET

game_over:
	CLS
	LD	RA,#40
	LD  RB,#0F
	DRW R0,R0,RA,RA,RB
game_over_loop:
	LD RF,'O'
	BEQ RF,R1, main
	JP game_over_loop

quit:
	HALT

