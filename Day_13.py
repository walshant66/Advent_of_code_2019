import time
import random
import numpy as np 
import unittest
import os
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import animation
import msvcrt

class object_robot(object):
	def __init__(self,str1={},p1=0,s_in=-10,s_out=-20,op=-1,rel_base1=0):
		fig1, ax1 = plt.subplots()
		self.fig=fig1
		self.ax=ax1
		cmap=colors.ListedColormap(['red','orange','yellow','green', 'blue'])
		bounds = [-0.1,0.1,1.1,2.1,3.1,4.1]
		norm = colors.BoundaryNorm(bounds, cmap.N)
		[min_x,min_y,max_x,max_y,k]=[-1,0,39,24,0]
		data_y=[]
		for iy in range(min_y,max_y+1):
			data_x=[]
			for ix in range(min_x,max_x+1):
				try:
					value=int(self.panels[str([ix,iy])])
				except:
					value=3
				data_x=data_x+[value]
			data_y=data_y+[data_x]
		self.im = self.ax.imshow(data_y, cmap=cmap, norm=norm)
		self.str_state=str1
		self.pos=str(p1)
		self.input_signal=str(s_in)
		self.code_output=s_out
		self.opcode=op
		self.relative_base=rel_base1
		self.x=0
		self.y=0
		self.panels={}
		self.x_y_tile='x'
	def new_squares(self):
		[min_x,min_y,max_x,max_y,k]=[-1,0,39,24,0]
		data_y=[]
		for iy in range(min_y,max_y+1):
			data_x=[]
			for ix in range(min_x,max_x+1):
				try:
					value=int(self.panels[str([ix,iy])])
				except:
					value=0
				data_x=data_x+[value]
			data_y=data_y+[data_x]
	#		self.im.set_data(data_y)
		cmap=colors.ListedColormap(['red','orange','yellow','green', 'blue'])
		bounds = [-0.1,0.1,1.1,2.1,3.1,4.1]
		norm = colors.BoundaryNorm(bounds, cmap.N)
#		self.im = self.ax.imshow(data_y, cmap=cmap, norm=norm)
		self.im.set_data(data_y)
		return self.im
	def plot_squares(self):
		plt.show(block=False)
		animation.FuncAnimation(self.fig,object_robot.new_squares(self),\
		frames=50*150,interval=250)
		plt.pause(0.000003)
	def check_memory(self,position):
		try:
			tmp123=self.str_state[position]+"a"
		except:
			self.str_state[position]="0"
	def str_val(self,mode_1,shift):
		position=str(int(self.pos)+shift)
		if mode_1==0:position_use=self.str_state[position]
		elif mode_1==1:position_use=position
		elif mode_1==2:position_use=str(int(self.relative_base)+\
		int(self.str_state[position]))
		return position_use
	def intcode_run(self,pos_1,pos_2,pos_3,pos):
		object_robot.check_memory(self,pos_1)
		object_robot.check_memory(self,pos_2)
		object_robot.check_memory(self,pos_3)
		if self.opcode==1:
			self.str_state[pos_3]=str(int(self.str_state[pos_1])+\
			int(self.str_state[pos_2]))
		elif self.opcode==2:
			self.str_state[pos_3]=str(int(self.str_state[pos_1])*\
			int(self.str_state[pos_2]))
		elif self.opcode==3:self.str_state[pos_1]=str(self.input_signal)
		elif self.opcode==4:self.code_output=self.str_state[pos_1]
	#		print("self.code_output")
	#		print(self.code_output)
		elif self.opcode==7:
			if int(self.str_state[pos_1])<int(self.str_state[pos_2]):
				self.str_state[pos_3]="1"
			else:
				self.str_state[pos_3]="0"
		elif self.opcode==8:
			if int(self.str_state[pos_1])==int(self.str_state[pos_2]):
				self.str_state[pos_3]="1"
			else:
				self.str_state[pos_3]="0"
		elif self.opcode==9:
			self.relative_base=self.relative_base+int(self.str_state[pos_1])

	#Defining the next position:
		if self.opcode in [1,2,7,8]:pos=pos+4
		elif self.opcode in [3,4,9]:pos=pos+2
		elif self.opcode==5:
			if int(self.str_state[pos_1])!=0:pos=int(self.str_state[pos_2])
			else:pos=pos+3
		elif self.opcode==6:
			if int(self.str_state[pos_1])==0:pos=int(self.str_state[pos_2])
			else:pos=pos+3
		self.pos=str(pos)
	def output_process(self):
		if self.x_y_tile=='x':
			self.x=int(self.code_output)
			self.x_y_tile='y'
		elif self.x_y_tile=='y':
			self.y=int(self.code_output)
			self.x_y_tile='tile'
		elif self.x_y_tile=='tile':
			self.panels[str([self.x,self.y])]=int(self.code_output)
			self.x_y_tile='x'
	def input_process(self,paddle_x,target):
		object_robot.plot_squares(self)
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
		return paddle_x
	def next_state(self,paddle_x,target):
		[mode_1,mode_2,mode_3,pos_1,pos_2,pos_3]=[0,0,0,-10,-11,-12]
		self.opcode=int((self.str_state[self.pos])[-2:])
		if not(self.opcode>0 and self.opcode<10) and self.opcode!=99:
			print("wrong opcode")
			halt_here123
		try:
			mode_1=int((self.str_state[self.pos])[-3])
			mode_2=int((self.str_state[self.pos])[-4])
			mode_3=int((self.str_state[self.pos])[-5])
		except:
			pass
		if self.opcode!=99:
			if self.opcode==3:
				paddle_x=object_robot.input_process(self,paddle_x,target)
			pos_1=object_robot.str_val(self,mode_1,1)
			if self.opcode in [1,2,5,6,7,8]:
				pos_2=object_robot.str_val(self,mode_2,2)
			if self.opcode in [1,2,7,8]:
				pos_3=object_robot.str_val(self,mode_3,3)
			object_robot.intcode_run(self,pos_1,pos_2,pos_3,int(self.pos))
			if self.opcode==4:object_robot.output_process(self)
 
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
	Arcade_A=object_robot(dict(str_state),0,0)
	cycle_amp(Arcade_A)
	print('Final_Score')
	print(str(Arcade_A.panels['[-1, 0]']))
	plt.close()
	return str(Arcade_A.panels['[-1, 0]'])

class LearningCase(unittest.TestCase):
	def test_starting_out(self):
		self.assertEqual(test_arcade_object("Puzzle_input.txt"),"16999")

def main():
	unittest.main()

if __name__ == "__main__":
	main()
