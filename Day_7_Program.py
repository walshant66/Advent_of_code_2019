from pynput.mouse import Button,Controller
import time
import pyautogui
import random
import numpy as np 
import unittest
import os

def run2_max_setting(filename_1,feedback):
	input_signal=0
	output_signal=-100
	if feedback==1:
		phases_list=factorial_complete_min_max(5,9)
	if feedback==0:
		phases_list=factorial_complete_min_max(0,4)
	for phases in phases_list:
		output_signal_new=int(test_amplifier_object(filename_1,input_signal,phases,feedback))
		if output_signal_new>output_signal:output_signal=output_signal_new
	return output_signal

def str_val(str_ori,mode_1,position):
	if mode_1==0:
		val_1=int(str_ori[int(str_ori[position])])
	else:
		val_1=int(str_ori[position])
	return val_1

def operation_run(str_ori,input_1,input_2,input_3,input_0,opcode,position,mode_2,code_output):
	if opcode==1:
		new_location=int(str_ori[position+3])
		str_ori[new_location]=str(input_1+input_2)
		position=position+4
	elif opcode==2:
		new_location=int(str_ori[position+3])
		str_ori[new_location]=str(input_1*input_2)
		position=position+4
	elif opcode==3:
		new_location=int(str_ori[position+1])
		str_ori[new_location]=str(input_0)
		position=position+2
	elif opcode==4:
		if mode_2==0:
			code_output=str_ori[int(str_ori[position+1])]
		if mode_2==1:
			code_output=(str_ori[position+1])
		position=position+2
	elif opcode==5:
		if input_1!=0:
			position=input_2
		else:
			position=position+3
	elif opcode==6:
		if input_1==0:
			position=input_2
		else:
			position=position+3
	elif opcode==7:
		if input_1<input_2:
			str_ori[input_3]="1"
		else:
			str_ori[input_3]="0"
		position=position+4
	elif opcode==8:
		if input_1==input_2:
			str_ori[input_3]="1"
		else:
			str_ori[input_3]="0"
		position=position+4
	return [str_ori,position,code_output]

def rotate(l, n):
    return l[n:] + l[:n]		
	
def factorial_run(a_in,new_addition):
	for i in range(0,len(a_in)):
		for j in range(0,(len(a_in[i])+1)):
			if j==0 and i==0:
				a_out=[rotate(rotate(a_in[i],j)+new_addition,-j)]
			else:
				a_out=a_out+[(rotate(rotate(a_in[i],j)+new_addition,-j))]
	return a_out

def factorial_complete_min_max(N_min,N_max):
	a_out1=[[N_min,N_min+1],[N_min+1,N_min]]
	for i in range(N_min+2,N_max+1):
		a_out1=factorial_run(a_out1,[i])
	return a_out1
	
class object_amplifier_state(object):
	def __init__(self,str=[],p1=0,ph1=0,s_in=-10,s_out=-20,op=-1,phase_input_complete_1=0):
		self.str_state=str
		self.position=p1
		self.phase=ph1
		self.input_signal=s_in
		self.code_output=s_out
		self.opcode=op
		self.phase_input_complete=phase_input_complete_1
	def next_state(self):
		[mode_1,mode_2,mode_3,input_1,input_2,input_3]=[0,0,1,0,0,0]
		if self.phase_input_complete==0:
			input_0=self.phase
			self.phase_input_complete=1
		else:
			input_0=self.input_signal
		self.opcode=int(((self.str_state[self.position]).rstrip())[-2:])
		if not(self.opcode>0 and self.opcode<9) and self.opcode!=99:
			print("wrong opcode")
			halt_here123
		if len(self.str_state[self.position])==5:
			halt_here123
			mode_2=int((self.str_state[self.position])[1])
			mode_1=int((self.str_state[self.position])[2])
		if len(self.str_state[self.position])==4:
			mode_2=int((self.str_state[self.position])[0])
			mode_1=int((self.str_state[self.position])[1])
		if len(self.str_state[self.position])==3:
			mode_1=int((self.str_state[self.position])[0])
		if self.opcode==1 or self.opcode==2 or (self.opcode>4 and self.opcode<9):
			input_1=str_val(self.str_state,mode_1,self.position+1)
			input_2=str_val(self.str_state,mode_2,self.position+2)
			if self.opcode==7 or self.opcode==8:
				input_3=str_val(self.str_state,mode_3,self.position+3)
		if self.opcode!=99:
			[self.str_state,self.position,self.code_output]=operation_run(self.str_state,input_1,input_2,input_3,input_0,self.opcode,self.position,mode_1,self.code_output)

def cycle_amp(AmpX):
	x=0
	while AmpX.opcode!=99 and (AmpX.opcode!=4 or x==0):
		AmpX.next_state()
		x=1

def test_amplifier_object(filename_1,input_signal,phases,feedback):
	with open(filename_1) as f:
		for line in f:
			str_state = line.split(',')
	f.close()
	position=0
	AmpA=object_amplifier_state(list(str_state),position,phases[0],input_signal)
	AmpB=object_amplifier_state(list(str_state),position,phases[1],input_signal)
	AmpC=object_amplifier_state(list(str_state),position,phases[2],input_signal)
	AmpD=object_amplifier_state(list(str_state),position,phases[3],input_signal)
	AmpE=object_amplifier_state(list(str_state),position,phases[4],input_signal)
	list_of_amps=[AmpA,AmpB,AmpC,AmpD,AmpE]
	i=0
	while(AmpE.opcode!=99):
		if (list_of_amps[i]).opcode!=99:
			cycle_amp(list_of_amps[i])
		output_previous=(list_of_amps[i]).code_output
		i=i+1
		if i>4:i=0
		if (feedback!=0 or i!=0 ):
			(list_of_amps[i]).input_signal=output_previous
	return output_previous

class LearningCase(unittest.TestCase):
	def test_starting_out(self):
		self.assertEqual(test_amplifier_object("test_max_signal_139629729.txt",0,[9,8,7,6,5],1),"139629729")
		self.assertEqual(test_amplifier_object("test_max_signal_18216.txt",0,[9,7,8,5,6],1),"18216")
		self.assertEqual(run2_max_setting("test_max_signal_139629729.txt",1),139629729)
		self.assertEqual(run2_max_setting("test_max_signal_18216.txt",1),18216)
		self.assertEqual(run2_max_setting("test_max_signal_puzzle.txt",1),3745599)
		
def main():
	unittest.main()
	
if __name__ == "__main__":
	main()
