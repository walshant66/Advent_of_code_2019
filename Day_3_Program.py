from pynput.mouse import Button,Controller
import time
import pyautogui
import random
import numpy as np 
#from scipy import signal

def run1():
	filename_1 = "wire_directions.txt"
	x=0
	with open(filename_1) as f:
		for line in f:
			print(type([1,2,3]))
			print(type(line))
			line1=line.rstrip()
			if x==1:
				wire2 = line1.split(',')
			if x==0:
				wire1 = line1.split(',')
				x=x+1

	total_list1=[[0,0]]
	present_position=[0,0]
	for i in range(0,len(wire1)-1,1):
		print('Remaining_1')
		print(len(wire1)-i)
		total_list1=next_coordinate_rec(present_position,wire1[i],total_list1)
#		print("total_list1_tmp")
#		print(total_list1[0])
		total_list1=total_list1[0]
		present_position=((total_list1[-1]))
		
#		print('i_present_position')
#		print(present_position)
#		print(i)
#	print('total_list1')
#	print(total_list1)
	
	total_list2=[[0,0]]
	present_position=[0,0]
	for i in range(0,len(wire2)-1,1):
		print('Remaining_2')
		print(len(wire2)-i)
		total_list2=next_coordinate_rec(present_position,wire2[i],total_list2)
#		print("total_list2_tmp")
#		print(total_list2[0])
		total_list2=total_list2[0]
		present_position=((total_list2[-1]))
		
#		print('i_present_position')
#		print(present_position)
#		print(i)
	for i in range(0,len(total_list1)):
#		print('Individual_points')
		total_list1[i]=str(total_list1[i])
#		print(total_list1[i])

	for i in range(0,len(total_list2)):
#		print('Individual_points')
		total_list2[i]=str(total_list2[i])
#		print(total_list2[i])
#	print('total_list1')
#	print(str(total_list1))
#	print('total_list2')
#	print(str(total_list2))
#	print('sorted(total_list2, key=lambda x: x[1])')
#	print(sorted(total_list2, key=lambda x: x[1]))
	sorted_total_list1=sorted(total_list1, key=lambda x: x[1])
	sorted_total_list2=sorted(total_list2, key=lambda x: x[1])

#	printIntersection(total_list1,total_list2,len(total_list1),len(total_list2))

	
#	nf = [x for x in total_list1 if x in total_list2]
#	print('nf = [x for x in total_list1 if x in total_list2]')
#	print(set(ListA).intersection(ListB))
#	nf=common_member(total_list1,total_list2)
	nf1=set(sorted_total_list1).intersection(sorted_total_list2)
	print('nf1')
	print(nf1)
	x_min=-1
	nf=list(nf1)
	print('nf')
	print(nf)
	
	for i in range(0,len(nf)):
#		print('nf[0]-split')
#		print(((nf[0]).split(',')))
		nf_arg1=int(((((nf[i]).split(','))[0]).split('['))[1])
		nf_arg2=int(((((nf[i]).split(','))[1]).split(']'))[0])
		print('nf_arg1')
		print(nf_arg1)
		print('nf_arg2')
		print(nf_arg2)
		s1=abs(nf_arg1)+abs(nf_arg2)
		if s1!=0: 
			if (s1<x_min or x_min==-1):
				x_min=s1

	s1=1			
	x_min_timing=-1
	for i in range(0,len(nf)):
#		print('nf[0]-split')
#		print(((nf[0]).split(',')))
#		nf_arg1=int(((((nf[i]).split(','))[0]).split('['))[1])
#		nf_arg2=int(((((nf[i]).split(','))[1]).split(']'))[0])
#		print('nf_arg1')
#		print(nf_arg1)
#		print('nf_arg2')
#		print(nf_arg2)
#		print("total_list1.index((nf[i]))")
#		print(total_list1.index((nf[i])))
#		print("total_list2.index((nf[i]))")
#		print(total_list2.index((nf[i])))
		
#		print('[i for i, x in enumerate(my_list1) if x == "whatever"')
#		print([i1 for i1, x in enumerate(total_list1) if x == nf[i]])
#		print('[i for i, x in enumerate(my_list2) if x == "whatever"')
#		print([i1 for i1, x in enumerate(total_list2) if x == nf[i]])

#		s1=int(total_list1.index((nf[i])))+int(total_list2.index((nf[i])))
		s1=int(count_position_with_loop(total_list1,nf[i]))+int(count_position_with_loop(total_list2,nf[i]))
		if s1!=0: 
			if (s1<x_min_timing or x_min_timing==-1):
				x_min_timing=s1


#Answer 7534

				
	print('Minimum Manhattan distance')
	print(x_min)
	print('Minimum timing distance')
	print(x_min_timing)
	print("nf[0]")
	print(nf[0])
#	print("total_list1[0:total_list1.index(nf[0])]")
#	print(count_position_with_loop(total_list1,nf[0]))
#	print(count_position_with_loop(total_list2,nf[0]))
#	print("total_list1[0::total_list1.index(nf[0])]")
#	print(total_list1[0:total_list1.index(nf[0])])
	
def count_position_with_loop(list1,position1):
	list=list1[0:(list1.index(position1)+1)]
#	print("fsfsdfsfs")
#	print(list)
	x=0
	count=0
	i=(([i1 for i1, x in enumerate(list) if x == list[0]])[-1])
	while x==0:
		if list[i]==position1:
			x=1
		else:
			i=i+1
			i=int(([i1 for i1, x in enumerate(list) if x == list[i]])[-1])
#			if len([i1 for i1, x in enumerate(list) if x == list[i-1]])>1:
#				print("duplicate")
#				print(list[i])
			count=count+1
	return count
		


# Python program to find intersection of 
# two sorted arrays 
# Function prints Intersection of arr1[] and arr2[] 
# m is the number of elements in arr1[] 
# n is the number of elements in arr2[] 
def printIntersection(arr1, arr2, m, n): 
	i,j = 0,0
	intersection_1=[]
	while i < m and j < n: 
		if arr1[i] < arr2[j]: 
			i += 1
		elif arr2[j] < arr1[i]: 
			j+= 1
		else: 
			print('Intersection')
			print((arr2[j]).split(','))	 
			j += 1
			i += 1
	return intersection_1
				

def next_coordinate(present_position,instruction):
	if instruction.find('D')==0:
		number = int((instruction.split('D'))[1])
		next_position=[present_position[0],present_position[1]-1]
		new_number=number-1
		new_instruction='D'+str(new_number)
	elif instruction.find('U')==0:
		number = int((instruction.split('U'))[1])
		next_position=[present_position[0],present_position[1]+1]
		new_number=number-1
		new_instruction='U'+str(new_number)
	elif instruction.find('L')==0:
		number = int((instruction.split('L'))[1])	
		next_position=[present_position[0]-1,present_position[1]]
		new_number=number-1
		new_instruction='L'+str(new_number)
	elif instruction.find('R')==0:
		number = int((instruction.split('R'))[1])
		next_position=[present_position[0]+1,present_position[1]]
		new_number=number-1
		new_instruction='R'+str(new_number)
	if new_number==0:
		new_instruction='X'
	return [next_position,new_instruction]

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	[new_position,new_instruction]=next_coordinate_rec(present_position,wire1[0])
	wire1[0]=new_instruction
	total_list.append(new_position)

	[total_list]=next_coordinate_rec(present_position,wire1[0])
	
	
def next_coordinate_rec(present_position,instruction,total_list):
	next_position=present_position
	if instruction.find('D')==0:
		number = int((instruction.split('D'))[1])
		new_number=number
		while new_number>0:
			next_position=[next_position[0],next_position[1]-1]
			new_number=new_number-1
			new_instruction='D'+str(new_number)
			total_list.append(next_position)
	elif instruction.find('U')==0:
		number = int((instruction.split('U'))[1])
		new_number=number
		while new_number>0:
			next_position=[next_position[0],next_position[1]+1]
			new_number=new_number-1
			new_instruction='U'+str(new_number)
			total_list.append(next_position)
	elif instruction.find('L')==0:
		number = int((instruction.split('L'))[1])	
		new_number=number
		while new_number>0:
			next_position=[next_position[0]-1,next_position[1]]
			new_number=new_number-1
			new_instruction='L'+str(new_number)
			total_list.append(next_position)
	elif instruction.find('R')==0:
		number = int((instruction.split('R'))[1])
		new_number=number
		while new_number>0:
			next_position=[next_position[0]+1,next_position[1]]
			new_number=new_number-1
			new_instruction='R'+str(new_number)
			total_list.append(next_position)
	if new_number==0:
		new_instruction='X'
	else:
		[total_list]=next_coordinate_rec(next_position,new_instruction,total_list)
	return [total_list]
