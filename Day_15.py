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


def new_direction_rotation(direction,rotation):
	direction_dict={"up":0,"left":90,"down":180,"right":270}
	new_angle=(direction_dict[direction]+rotation)%360
	for key in direction_dict.keys():
		if direction_dict[key]==new_angle:
			return_value=key
	return return_value





class object_robot(object):
	def __init__(self,str1={},p1=0,s_in=1,s_out=-21,op=-1,rel_base1=0):
		fig1, ax1 = plt.subplots()
		self.fig=fig1
		self.ax=ax1
		cmap = colors.ListedColormap(['red','orange','yellow','green', 'blue'])
		bounds = [-0.1,0.1,1.1,2.1,3.1,4.1]
		norm = colors.BoundaryNorm(bounds, cmap.N)
		[min_x,min_y,max_x,max_y,k]=[-19,-21,21,19,0]
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
		self.filled=0
		self.check_green=0
		self.x_previous=100
		self.y_previous=1000
		self.count_search=0
		self.panels={}
		self.direction='down'
		self.list_all=[]
		self.green=0
		self.direction_previous="Whatever"
	def new_squares(self):
		[min_x,min_y,max_x,max_y,k]=[-19,-21,21,19,0]
		data_y=[]
		for iy in range(min_y,max_y+1):
			data_x=[]
			for ix in range(min_x,max_x+1):
				try:
					value=int(self.panels[str([ix,iy])])
				except:
					value=3
				if self.x==ix and self.y==iy:
					value=4
				data_x=data_x+[value]
			data_y=data_y+[data_x]
	#		self.im.set_data(data_y)
		cmap = colors.ListedColormap(['red','orange','yellow','green', 'blue'])
		bounds = [-0.1,0.1,1.1,2.1,3.1,4.1]
		norm = colors.BoundaryNorm(bounds, cmap.N)
#		self.im = self.ax.imshow(data_y, cmap=cmap, norm=norm)
		self.im.set_data(data_y)
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
		if int(self.code_output)==2:
			print("found")
			print([self.x,self.y])

		if int(self.code_output)!=0:
			if self.input_signal==1:
				self.y=self.y-1
				self.direction="up"
			if self.input_signal==2:
				self.y=self.y+1
				self.direction="down"
			if self.input_signal==3:
				self.x=self.x+1
				self.direction="right"
			if self.input_signal==4:
				self.x=self.x-1
				self.direction="left"
			self.x_previous=self.x
			self.y_previous=self.y
			self.panels[str([self.x,self.y])]=int(self.code_output)
		else:
			if self.input_signal==1:
				self.panels[str([self.x,self.y-1])]=int(self.code_output)
			if self.input_signal==2:
				self.panels[str([self.x,self.y+1])]=int(self.code_output)
			if self.input_signal==3:
				self.panels[str([self.x+1,self.y])]=int(self.code_output)
			if self.input_signal==4:
				self.panels[str([self.x-1,self.y])]=int(self.code_output)
	def new_location(self,input1):
		if input1==1:
			tmp_y=self.y-1
			tmp_x=self.x
		if input1==2:
			tmp_y=self.y+1
			tmp_x=self.x
		if input1==3:
			tmp_x=self.x+1
			tmp_y=self.y
		if input1==4:
			tmp_x=self.x-1
			tmp_y=self.y
		return [tmp_x,tmp_y]
	def input_process(self):
		[tmp_x,tmp_y]=object_robot.new_location(self,self.input_signal)
		#Assume up:
		try:a_forward=int(self.panels[str([self.x,self.y-1])])
		except:a_forward=3
		try:a_back=int(self.panels[str([self.x,self.y+1])])
		except:a_back=3
		try:a_right=int(self.panels[str([self.x+1,self.y])])
		except:a_right=3
		try:a_left=int(self.panels[str([self.x-1,self.y])])
		except:a_left=3
		
		if self.direction=="up":
			neighbour_points=[a_back,a_left,a_forward,a_right]
		elif self.direction=="left":
			neighbour_points=[a_right,a_back,a_left,a_forward]
		elif self.direction=="down":
			neighbour_points=[a_forward,a_right,a_back,a_left]
		elif self.direction=="right":
			neighbour_points=[a_left,a_forward,a_right,a_back]

		if self.green==1:
			self.direction=self.direction_previous
			self.green=0
		else:
			self.direction=new_direction_rotation(self.direction,object_robot.rotation_used(self,neighbour_points))
		if self.direction=="up":
			self.input_signal=1
		elif self.direction=="left":
			self.input_signal=4
		elif self.direction=="down":
			self.input_signal=2
		elif self.direction=="right":
			self.input_signal=3
	def rotation_used(self,neighbour_points):
		a_back=neighbour_points[0]
		a_left=neighbour_points[1]
		a_forward=neighbour_points[2]
		a_right=neighbour_points[3]
		self.green=0
		self.direction_previous=self.direction
		#up
		rotation=0
	#	time.sleep(0.1)
		if a_left!=0 and a_forward==0:
			#Left
			rotation=90
		elif a_left==0 and a_forward==0:
			#right
			rotation=270
		elif a_right==0 and a_forward==0:
			#left
			rotation=90
		if a_left==0 and a_forward==0 and a_back==0:
			#right
			rotation=270
		if a_left!=0 and a_forward!=0 and a_back==1 and a_right==0:
			#left
			rotation=90
		if a_left==1 and a_forward==1 and a_back==1 and a_right==1:
			#left
			rotation=90
	#GREEN:
		if a_left==3:
			rotation=90
			self.green=1
		elif a_forward==3:
			rotation=0
		elif a_right==3:
			rotation=270
		elif a_back==3:
			rotation=180
		return rotation

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
			self.count_search=self.count_search+1
		if self.code_output!=0:
			self.list_all=self.list_all+[str([self.x,self.y])]
			print("self.count_search")
			print(self.count_search)
		if self.count_search>100:
			self.count_search=0
			self.find_any_green=object_robot.find_central_green(self)
			if self.find_any_green==0:
			#if object_robot.find_any_orange_list(self,2)==1:
				count_yellow=0
				while object_robot.find_any_orange_list(self,1)==1:
					time.sleep(1)
					find_any_orange=object_robot.push_through_oxygen(self)
					count_yellow=count_yellow+1
				print("count_yellow")
				print(count_yellow)
#					count_yellow=390
	def push_through_oxygen(self):
		[min_x,min_y,max_x,max_y]=[-19,-21,21,19]
		find_any_orange=0
		for iy in range(min_y,max_y+1):
			for ix in range(min_x,max_x+1):
				try:
					if self.panels[str([ix,iy])]==2:
						for ax in range(-1,2):
							for ay in range(-1,2):
								if self.panels[str([ix+ax,iy+ay])]==1 and (abs(ax)+abs(ay))<2:
									self.panels[str([ix+ax,iy+ay])]=8
				except:
					pass
		for iy in range(min_y,max_y+1):
			for ix in range(min_x,max_x+1):
				try:
					if self.panels[str([ix,iy])]==8:
						self.panels[str([ix,iy])]=2
				except:
					pass
		object_robot.plot_squares(self)
		return find_any_orange
	def find_any_orange_list(self,colour):
		[min_x,min_y,max_x,max_y]=[-19,-21,21,19]
		find_any_orange=0
		for iy in range(min_y,max_y+1):
			for ix in range(min_x,max_x+1):
				try:
					if self.panels[str([ix,iy])]==colour:
						find_any_orange=1
				except:
					pass
		return find_any_orange
	def find_central_green(self):
		object_robot.plot_squares(self)
		[min_x,min_y,max_x,max_y]=[-19,-21,21,19]
		self.find_any_green=0
		for iy in range(min_y,max_y+1):
			for ix in range(min_x,max_x+1):
				if ix==min_x or ix==max_x or iy==min_y or iy==max_y:
					self.panels[str([ix,iy])]=0
				try:
					value=int(self.panels[str([ix,iy])])
				except:
					self.find_any_green=1
					object_robot.change_central_green(self,ix,iy)
#					print("HERE_2")
#					time.sleep(1)
		return self.find_any_green
	def change_central_green(self,ix,iy):
		try:
			if int(self.panels[str([ix+1,iy])])==0 and \
			int(self.panels[str([ix-1,iy])])==0 and \
			int(self.panels[str([ix,iy+1])])==0 and \
			int(self.panels[str([ix,iy-1])])==0:
				self.panels[str([ix,iy])]=0
				print("HERE_1")
				time.sleep(1)
		except:
			pass

def minimize_list(list_all):
	i=0
	k=0
#	print("Start_of_list")
	while i<len(list_all):
		i=last_element_index(list_all,i)
#		print(list_all[i])
		k=k+1
		i=i+1
#	print("First Element")
#	print(list_all[0])
#	print("Last Element")
#	print(list_all[-2])	
	return k-1
	
def last_element_index(list1,index):
	return ([i for i, e in enumerate(list1) if e == list1[index]])[-1]
			
def cycle_amp(AmpX):
	AmpX.input_signal=1
	while AmpX.opcode!=99 and AmpX.find_any_green!=0:
		AmpX.next_state()
#		if int(AmpX.code_output)==2:
#			break

def test_arcade_object(filename_1):
	str_state={}
	with open(filename_1) as f:
		for line2 in f:
			line=line2.rstrip()
			str_state_int = line.split(',')
	for i in range(0,len(str_state_int)):
		str_state[str(i)]=str_state_int[i]
	f.close()
	Arcade_A=object_robot(dict(str_state),0,0)
	cycle_amp(Arcade_A)
	plt.close()
	number_of_steps=minimize_list(Arcade_A.list_all)
	return number_of_steps

class LearningCase(unittest.TestCase):
	def test_starting_out(self):
		self.assertEqual(test_arcade_object("Puzzle_input.txt"),79)
		#position is [-15,-12]

		
		
def do_stuff(numbers):
    print(numbers)

		
		
		
def main():
#	numbers = 2
#	profile = LineProfiler(do_stuff(numbers))
#	profile.print_stats()
	unittest.main()

if __name__ == "__main__":
	main()
