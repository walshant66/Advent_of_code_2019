import time
import random
import numpy as np 
import unittest
import os
import matplotlib.pyplot as plt
from matplotlib import colors

def plot_squares(data):
	# create discrete colormap
	cmap = colors.ListedColormap(['red', 'blue'])
	bounds = [0,0.5,0.7]
	norm = colors.BoundaryNorm(bounds, cmap.N)

#	print("data")
#	print(data)

	fig, ax = plt.subplots()
	ax.imshow(data, cmap=cmap, norm=norm)

	# draw gridlines
	ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0)

	plt.show()

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
#Any new memory locations need values of 0:
	try:
		tmp123=str_ori[position_1]+"asdf"
	except:
		str_ori[position_1]="0"
	try:
		tmp123=str_ori[position_2]+"asdf"
	except:
		str_ori[position_2]="0"
	try:
		tmp123=str_ori[position_3]+"asdf"
	except:
		str_ori[position_3]="0"
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
#		print("code_output")
#		print(code_output)
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

class object_robot_state(object):
	def __init__(self,str1={},p1=0,s_in=-10,s_out=-20,op=-1,rel_base1=0):
		self.str_state=str1
		self.position=str(p1)
		self.input_signal=str(s_in)
		self.code_output=s_out
		self.opcode=op
		self.relative_base=rel_base1
		self.x=0
		self.y=0
		self.panels={}
		self.direction=90
		self.colour_or_direction='colour'
		self.start_panel='black'
	def increment_robot_position(self):
		if self.direction==0:
			self.x=self.x-1
		elif self.direction==180:
			self.x=self.x+1
		elif self.direction==90:
			self.y=self.y-1
		elif self.direction==270:
			self.y=self.y+1
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
			if self.opcode==4:
				if self.colour_or_direction=='colour':
					self.panels[str([self.x,self.y])]=self.code_output
					self.colour_or_direction='direction'
				elif self.colour_or_direction=='direction':
					self.direction=(self.direction+(2*int(self.code_output)-1)*90+360)%360
					object_robot_state.increment_robot_position(self)
					self.colour_or_direction='colour'
					try:
						self.input_signal=int(self.panels[str([self.x,self.y])])
					except:
						if self.start_panel=='black':
							self.input_signal=0
						elif self.start_panel=='white':
							self.input_signal=1

def cycle_amp(AmpX):
	x=0
	while AmpX.opcode!=99 and (AmpX.opcode!=4 or x==0):
		AmpX.next_state()
		x=1

def test_robot_object(filename_1,input_signal,start_panel):
	str_state={}
	
	with open(filename_1) as f:
		for line2 in f:
			line=line2.rstrip()
			str_state_int = line.split(',')
	for i in range(0,len(str_state_int)):
		str_state[str(i)]=str_state_int[i]
	f.close()
	position=0
	Robot_A=object_robot_state(dict(str_state),position,input_signal)
	Robot_A.start_panel=start_panel
	while(Robot_A.opcode!=99):
		cycle_amp(Robot_A)
	list_white=[]
	[min_x,min_y,max_x,max_y]=[0,0,0,0]
	k=0
	for x in Robot_A.panels:
		k=k+1
		if Robot_A.panels[x]=='1':
			split_x_y=(((x.split('['))[1].split(']'))[0]).split(',')
			list_white=list_white+[[int(split_x_y[0]),int(split_x_y[1])]]
			if min_x>int(split_x_y[0]):min_x=int(split_x_y[0])
			if max_x<int(split_x_y[0]):max_x=int(split_x_y[0])
			if min_y>int(split_x_y[1]):min_y=int(split_x_y[1])
			if max_y<int(split_x_y[1]):max_y=int(split_x_y[1])
	data_y=[]
	for iy in range(min_y,max_y+1):
		data_x=[]
		for ix in range(min_x,max_x+1):
			try:
				value=int(Robot_A.panels[str([ix,iy])])
			except:
				if start_panel=='black':
					value=0
				if start_panel=='white':
					value=1
			data_x=data_x+[value]
		data_y=data_y+[data_x]
	plot_squares(data_y)
	return k

class LearningCase(unittest.TestCase):
	def test_starting_out(self):
		self.assertEqual(test_robot_object("Panel_puzzle_input.txt",0,'black'),\
		2255)
		self.assertEqual(test_robot_object("Panel_puzzle_input.txt",1,'white'),\
		249)
		#Output code: BCKFPCRA
		
def main():
	unittest.main()

if __name__ == "__main__":
	main()
