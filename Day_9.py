import time
import random
import numpy as np 
import unittest
import os


def str_val(str_ori,mode_1,position,relative_base):
	if mode_1==0:
		position_use=str_ori[position]
	elif mode_1==1:
		position_use=position
	elif mode_1==2:
		position_use=str(int(relative_base)+int(str_ori[position]))
	return position_use

def operation_run(str_ori,position_1,position_2,position_3,input_0,\
opcode,position,mode_2,code_output,relative_base):
#String manipulation,input/output,and relative_base changes:
	if opcode==1:
		str_ori[position_3]=str(int(str_ori[position_1])+\
		int(str_ori[position_2]))
	elif opcode==2:
		str_ori[position_3]=str(int(str_ori[position_1])*\
		int(str_ori[position_2]))
	elif opcode==3:
		str_ori[position_1]=str(input_0)
	elif opcode==4:
		code_output=str_ori[position_1]
		print("code_output")
		print(code_output)
	elif opcode==7:
		if int(str_ori[position_1])<int(str_ori[position_2]):
			str_ori[position_3]="1"
		else:
			str_ori[position_3]="0"
	elif opcode==8:
		if int(str_ori[position_1])==int(str_ori[position_2]):
			str_ori[position_3]="1"
		else:
			str_ori[position_3]="0"
	elif opcode==9:
		relative_base=relative_base+int(str_ori[position_1])

#Defining the next position:
	if opcode==1 or opcode==2 or opcode==7 or opcode==8:
		position=position+4
	elif opcode==3 or opcode==4 or opcode==9:
		position=position+2
	elif opcode==5:
		if int(str_ori[position_1])!=0:
			position=int(str_ori[position_2])
		else:
			position=position+3
	elif opcode==6:
		if int(str_ori[position_1])==0:
			position=int(str_ori[position_2])
		else:
			position=position+3
	return [str_ori,str(position),code_output,relative_base]

class object_sensor_state(object):
	def __init__(self,str1={},p1=0,s_in=-10,s_out=-20,op=-1,rel_base1=0):
		self.str_state=str1
		self.position=str(p1)
		self.input_signal=str(s_in)
		self.code_output=s_out
		self.opcode=op
		self.relative_base=rel_base1
	def next_state(self):
		[mode_1,mode_2,mode_3,input_1,input_2,input_3,\
		position_1,position_2,position_3]=[0,0,0,0,0,0,-10,-11,-12]
		input_0=self.input_signal
		self.opcode=int((self.str_state[self.position])[-2:])
		if not(self.opcode>0 and self.opcode<10) and self.opcode!=99:
			print("wrong opcode")
			halt_here123
		try:
			mode_1=int((self.str_state[self.position])[-3])
			mode_2=int((self.str_state[self.position])[-4])
			mode_3=int((self.str_state[self.position])[-5])
		except:
			pass
		if self.opcode!=99:
			position_1=str_val(self.str_state,mode_1,\
			str(int(self.position)+1),self.relative_base)
			if self.opcode==1 or self.opcode==2 or\
			(self.opcode>4 and self.opcode<9):
				position_2=str_val(self.str_state,mode_2,\
				str(int(self.position)+2),self.relative_base)
			if self.opcode==1 or self.opcode==2 or\
			self.opcode==7 or self.opcode==8:
				position_3=str_val(self.str_state,mode_3,\
				str(int(self.position)+3),self.relative_base)
			[self.str_state,self.position,self.code_output,\
			self.relative_base]=operation_run(self.str_state,position_1,\
			position_2,position_3,input_0,self.opcode,int(self.position),\
			mode_1,self.code_output,self.relative_base)

def cycle_amp(AmpX):
	x=0
	while AmpX.opcode!=99 and (AmpX.opcode!=4 or x==0):
		AmpX.next_state()
		x=1

def test_sensor_object(filename_1,input_signal):
	str_state={}
	with open(filename_1) as f:
		for line2 in f:
			line=line2.rstrip()
			str_state_int = line.split(',')
	for i in range(0,len(str_state_int)):
		str_state[str(i)]=str_state_int[i]
	f.close()
	position=0
	sensorA=object_sensor_state(dict(str_state),position,input_signal)
	while(sensorA.opcode!=99):
		cycle_amp(sensorA)
	return sensorA.code_output

class LearningCase(unittest.TestCase):
	def test_starting_out(self):
#		self.assertEqual(test_sensor_object("sensor_input_example_1.txt",0),\
#		"18216")
		self.assertEqual(test_sensor_object("sensor_input_example_2.txt",0),\
		"1219070632396864")
		self.assertEqual(test_sensor_object("sensor_input_example_3.txt",0),\
		"1125899906842624")
		self.assertEqual(test_sensor_object("sensor_puzzle_input.txt",1),\
		"3429606717")
		self.assertEqual(test_sensor_object("sensor_puzzle_input.txt",2),\
		"33679")
		
def main():
	unittest.main()
	
if __name__ == "__main__":
	main()
