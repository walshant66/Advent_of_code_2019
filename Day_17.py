import time
import random
import numpy as np 
import unittest
import os
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import animation
import msvcrt
import graphviz
#from line_profiler import LineProfiler

class object_robot(object):
	def __init__(self,str1={},p1=0,s_in=1,s_out=-21,op=-1,rel_base1=0):
		fig1, ax1 = plt.subplots()
		self.fig=fig1
		self.ax=ax1
		cmap = colors.ListedColormap(['red','orange','yellow','green', 'blue'])
		bounds = [-0.1,0.1,1.1,2.1,3.1,4.1]
		norm = colors.BoundaryNorm(bounds, cmap.N)
		[min_x,min_y,max_x,max_y,k]=[0,0,48,50,0]
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
		self.find_any_green=1
		self.input_signal=s_in
		self.code_output=s_out
		self.opcode=op
		self.relative_base=rel_base1
		self.x=0
		self.y=0
		self.keyboard_trigger=0
		self.max_x=0
		self.max_y=0
		self.filled=0
		self.panels={}
		self.input_type=0
		self.keyboard_input=""
		self.data_y_update=[]
	def new_squares(self):
		[min_x,min_y,max_x,max_y,k]=[0,0,48,50,0]
		data_y=[]
		blank_line=0
		update_run=0
		for iy in range(min_y,self.max_y-2):
#		for iy in range(min_y,self.max_y+1):
			data_x=[]
#			for ix in range(min_x,self.max_x+1):
			for ix in range(min_x,self.max_x):
				try:
					value=int(self.panels[str([ix,iy])])
				except:
					value=3
					blank_line=iy
					print("Blank_line")
					print(blank_line)
				if self.x==ix and self.y==iy:
					value=4
				data_x=data_x+[value]
			data_y=data_y+[data_x]
		cmap = colors.ListedColormap(['red','orange','yellow','green', 'blue'])
		bounds = [-0.1,0.1,1.1,2.1,3.1,4.1]
		norm = colors.BoundaryNorm(bounds, cmap.N)
		self.data_y_update=data_y
		self.im.set_data(self.data_y_update)
		self.x=0
		self.y=0
#		print("blank_line")
#		print(blank_line)
		self.panels={}
		return self.im
	def plot_squares(self):
		plt.show(block=False)
		animation.FuncAnimation(self.fig,object_robot.new_squares(self),frames=50*150,interval=250)
		plt.pause(0.000003)
	def check_memory(self,position):
		try:
			tmp121=self.str_state[position]+"a"
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
		if int(self.code_output)==35:##
			self.panels[str([self.x,self.y])]=1
			self.x=self.x+1
		elif int(self.code_output)==46:#.
			self.panels[str([self.x,self.y])]=2
			self.x=self.x+1
		elif int(self.code_output)==10:#\n
			self.x=0
			self.y=self.y+1
		elif int(self.code_output) in [94,62,60,118,86]:#^><vV
			self.x_robot_start=self.x
			self.y_robot_start=self.y
			self.panels[str([self.x,self.y])]=0
			self.x=self.x+1
		self.max_x=max([self.max_x,self.x])
		self.max_y=max([self.max_y,self.y])
	def input_process(self):
		if len(self.keyboard_input)==0:
			if self.input_type==0:print('Main_function\n')
			elif self.input_type==1:print('Function_A\n')
			elif self.input_type==2:print('Function_B\n')
			elif self.input_type==3:print('Function_C\n')
			elif self.input_type==4:print('Monitor(Y/N)\n')
			self.input_type=self.input_type+1
			self.keyboard_input = input("Enter function: ")
			self.keyboard_input=self.keyboard_input+"\n"
			self.keyboard_trigger=1
		input_code=ord(self.keyboard_input[0])
		self.keyboard_input=self.keyboard_input[1:]
		self.input_signal=input_code
	def next_state(self):
		[mode_1,mode_2,mode_3,pos_1,pos_2,pos_3]=[0,0,0,-10,-11,-12]
		self.opcode=int((self.str_state[self.pos])[-2:])
		if not(self.opcode>0 and self.opcode<10) and self.opcode!=99:
			print("wrong opcode")
			print(self.opcode)
			halt_here121
		try:
			mode_1=int((self.str_state[self.pos])[-3])
			mode_2=int((self.str_state[self.pos])[-4])
			mode_3=int((self.str_state[self.pos])[-5])
		except:
			pass
		if self.opcode==3:
			object_robot.input_process(self)
		pos_1=object_robot.str_val(self,mode_1,1)
		if self.opcode in [1,2,5,6,7,8]:
			pos_2=object_robot.str_val(self,mode_2,2)
		if self.opcode in [1,2,7,8]:
			pos_3=object_robot.str_val(self,mode_3,3)
		object_robot.intcode_run(self,pos_1,pos_2,pos_3,int(self.pos))
		if self.opcode==4:
			object_robot.output_process(self)
			if self.keyboard_trigger==10:
				[full_path_result,str_analysed]=object_robot.full_path(self)
				print("full_path_result")
				print(full_path_result)
				print("str_analysed")
				print(str_analysed)
#			if self.x==0 and self.y==49:
			if self.x==0 and self.y==49:
				object_robot.plot_squares(self)
	def find_intersections(self):
		number_of_intersections=0
		alginment_parameter=0
		print("self.max_x")
		print(self.max_x)
		print("self.max_y")
		print(self.max_y)
		for x_tmp in range(0,self.max_x+1):
			for y_tmp in range(0,self.max_y+1):
				try:
					if (self.panels[str([x_tmp,y_tmp])]==1) and\
					(self.panels[str([x_tmp+1,y_tmp])]==1) and\
					(self.panels[str([x_tmp-1,y_tmp])]==1) and\
					(self.panels[str([x_tmp,y_tmp+1])]==1) and\
					(self.panels[str([x_tmp,y_tmp-1])]==1):
						number_of_intersections=number_of_intersections+1
						alginment_parameter=alginment_parameter+x_tmp*y_tmp
				except:
					pass
		return alginment_parameter
	def full_path(self):
		x_robot_old=self.x_robot_start
		y_robot_old=self.y_robot_start
		x_robot=x_robot_old
		y_robot=y_robot_old
		count_options=2
		full_path_result=""
		while count_options>0:
			try:
				[x_robot,y_robot,x_robot_old,y_robot_old,count_options]=object_robot.new_position(self,x_robot,y_robot,x_robot_old,y_robot_old)
				if x_robot-x_robot_old<0:
					print("L")
					full_path_result=full_path_result+"L"
				if x_robot-x_robot_old>0:
					print("R")
					full_path_result=full_path_result+"R"
				if y_robot-y_robot_old<0:
					print("U")
					full_path_result=full_path_result+"U"
				if y_robot-y_robot_old>0:
					print("D")
					full_path_result=full_path_result+"D"
			except:
				count_options=0
		count_steps=1
		str_analysed=""
		for i in range(0,len(full_path_result)-1):
			if full_path_result[i]==full_path_result[i+1]:
				count_steps=count_steps+1
			else:
				str_analysed=str_analysed+str(count_steps)
				count_steps=1
				if full_path_result[i:(i+2)] in ["LU","UR","RD","DL"]:
					str_analysed=str_analysed+"R"
				elif full_path_result[i:(i+2)] in ["UL","RU","DR","LD"]:
					str_analysed=str_analysed+"L"
		return [full_path_result,str_analysed]
	def new_position(self,x_robot,y_robot,x_robot_old,y_robot_old):
		count_options=0
		for ix in range (x_robot-1,x_robot+2):
			for iy in range (y_robot-1,y_robot+2):
				try:
					if int(self.panels[str([ix,iy])])==1  and  [ix,iy]!=[x_robot,y_robot]:##
						count_options=count_options+1
						if [ix,iy]!=[x_robot_old,y_robot_old]:
							x_robot_new=ix
							y_robot_new=iy
						if count_options>2:
							x_robot_new=x_robot+(x_robot-x_robot_old)
							y_robot_new=y_robot+(y_robot-y_robot_old)
				except:
					pass
		return [x_robot_new,y_robot_new,x_robot,y_robot,count_options]

def cycle_amp(AmpX,mode):
	AmpX.input_signal=1
	while AmpX.opcode!=99:
		AmpX.next_state()
	if mode=='1':
		return_value=AmpX.find_intersections()
	elif mode=='2':
		return_value=int(AmpX.code_output)
	return return_value

def test_arcade_object(filename_1,mode):
	str_state={}
	with open(filename_1) as f:
		for line2 in f:
			line=line2.rstrip()
			str_state_int = line.split(',')
	for i in range(0,len(str_state_int)):
		str_state[str(i)]=str_state_int[i]
	f.close()
	str_state['0']=mode
	Arcade_A=object_robot(dict(str_state),0,0)
	return_value=cycle_amp(Arcade_A,mode)
	print("return_value")
	print(return_value)
	plt.close()
	return return_value

class LearningCase(unittest.TestCase):
	def test_starting_out(self):
		self.assertEqual(test_arcade_object("Puzzle_input.txt",'1'),2508)
		#Keyboard inputs:
		#Main:A,B,A,B,A,C,B,C,A,C
		#A:L,4,6,L,6,6,R,6
		#B:R,4,6,L,4,L,4,L,6,6
		#C:L,4,6,R,4,6,R,6,L,4
		self.assertEqual(test_arcade_object("Puzzle_input.txt",'2'),799463)
		#position is [-15,-12]

def main():
	unittest.main()

if __name__ == "__main__":
	main()
