import time
import random
import numpy as np 
import unittest
import os
import matplotlib.pyplot as plt
from matplotlib import colors
import msvcrt

def plot_squares(Arcade_A):
	[min_x,min_y,max_x,max_y,k]=[0,0,0,0,0]
	for x in Arcade_A.panels:
		k=k+1
		split_x_y=(((x.split('['))[1].split(']'))[0]).split(',')
		if min_x>int(split_x_y[0]):min_x=int(split_x_y[0])
		if max_x<int(split_x_y[0]):max_x=int(split_x_y[0])
		if min_y>int(split_x_y[1]):min_y=int(split_x_y[1])
		if max_y<int(split_x_y[1]):max_y=int(split_x_y[1])
	data_y=[]
	for iy in range(min_y,max_y+1):
		data_x=[]
		for ix in range(min_x,max_x+1):
			try:
				value=int(Arcade_A.panels[str([ix,iy])])
			except:
				value=0
			data_x=data_x+[value]
		data_y=data_y+[data_x]
	cmap = colors.ListedColormap(['red','orange','yellow','green', 'blue'])
	bounds = [-0.1,0.1,1.1,2.1,3.1,4.1]
	norm = colors.BoundaryNorm(bounds, cmap.N)
	Arcade_A.ax.imshow(data_y, cmap=cmap, norm=norm)
	plt.show(block=False)
	plt.pause(0.000003)

def str_val(str_ori,mode_1,position,relative_base):
	if mode_1==0:position_use=str_ori[position]
	elif mode_1==1:position_use=position
	elif mode_1==2:position_use=str(int(relative_base)+int(str_ori[position]))
	return position_use

def operation_run(str_ori,position_1,position_2,position_3,input_0,\
opcode,position,mode_2,code_output,relative_base):
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
	elif opcode==3:str_ori[position_1]=str(input_0)
	elif opcode==4:code_output=str_ori[position_1]
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
	if opcode==1 or opcode==2 or opcode==7 or opcode==8:position=position+4
	elif opcode==3 or opcode==4 or opcode==9:position=position+2
	elif opcode==5:
		if int(str_ori[position_1])!=0:position=int(str_ori[position_2])
		else:position=position+3
	elif opcode==6:
		if int(str_ori[position_1])==0:position=int(str_ori[position_2])
		else:position=position+3
	return [str_ori,str(position),code_output,relative_base]

class object_robot_state(object):
	def __init__(self,str1={},p1=0,s_in=-10,s_out=-20,op=-1,rel_base1=0):
		fig1, ax1 = plt.subplots()
		self.fig=fig1
		self.ax=ax1
		self.str_state=str1
		self.position=str(p1)
		self.input_signal=str(s_in)
		self.code_output=s_out
		self.opcode=op
		self.relative_base=rel_base1
		self.x=0
		self.y=0
		self.panels={}
		self.x_y_tile='x'
	def next_state(self,paddle_x,target):
		[mode_1,mode_2,mode_3,input_1,input_2,input_3,\
		position_1,position_2,position_3]=[0,0,0,0,0,0,-10,-11,-12]
		return_value=[]
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
			if self.opcode==3:
#				plot_squares(self)
				try:
					print('Score')
					print(str(self.panels['[-1, 0]']))
#					if self.panels['[-1, 0]']:
#						plot_squares(self)
				except:
					pass
				if paddle_x>target:self.input_signal=-1
				if paddle_x==target:self.input_signal=0
				if paddle_x<target:self.input_signal=1
				input_0=self.input_signal
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
				if self.x_y_tile=='x':
					self.x=int(self.code_output)
					self.x_y_tile='y'
				elif self.x_y_tile=='y':
					self.y=int(self.code_output)
					self.x_y_tile='tile'
				elif self.x_y_tile=='tile':
					self.panels[str([self.x,self.y])]=int(self.code_output)
					self.x_y_tile='x'

def cycle_amp(AmpX):
	paddle_x=20
	target=18
	while AmpX.opcode!=99:
		AmpX.next_state(paddle_x,target)
		try:
			a=list(AmpX.panels.keys())[list(AmpX.panels.values()).index(3)]
			paddle_x=int(((a.split('['))[1]).split(',')[0])
			b=list(AmpX.panels.keys())[list(AmpX.panels.values()).index(4)]
			ball_x=int(((b.split('['))[1]).split(',')[0])
			target=ball_x
		except:
			pass

def test_arcade_object(filename_1):
	str_state={}
	with open(filename_1) as f:
		for line2 in f:
			line=line2.rstrip()
			str_state_int = line.split(',')
	for i in range(0,len(str_state_int)):
		str_state[str(i)]=str_state_int[i]
	f.close()
	str_state['0']='2'
	Arcade_A=object_robot_state(dict(str_state),0,0)
	cycle_amp(Arcade_A)
	print('Final_Score')
	print(str(Arcade_A.panels['[-1, 0]']))

	plt.close()
	return str(Arcade_A.panels['[-1, 0]'])

class LearningCase(unittest.TestCase):
#	test_arcade_object("Puzzle_input.txt")
	def test_starting_out(self):
		self.assertEqual(test_arcade_object("Puzzle_input.txt"),\
		"16999")
#FINAL SCORE: 16999

def main():
	unittest.main()

if __name__ == "__main__":
	main()

