import time
import math
import random
import numpy as np 
import unittest
import os
import re

def rotate(l, n):
    return l[n:] + l[:n]		

def full_list_target(asteroid_list):
	[max_asteroid_count,best_location]=best_asteroid_position(asteroid_list)
	full_list=[]
	while len(asteroid_list)>1:
		full_list=full_list+\
		sort_points_by_angles(asteroid_list,best_location)
		asteroid_list=[x for x in asteroid_list if x not in full_list]
	return full_list

def sort_points_by_angles(asteroid_list,best_location):
	[list_angles,list_visible_points,start_point]=\
	list_of_current_angles(asteroid_list,best_location)
	index_list=sorted(range(len(list_angles)), \
	key=lambda k: list_angles[k], reverse = True)
	sorted_points=[list_visible_points[i] for i in index_list]
	k=0
	for i in range(0,len(sorted_points)):
		if sorted_points[i]==start_point:
			k=i
	sorted_points=rotate(sorted_points,k)
	return sorted_points


def list_of_current_angles(asteroid_list,best_location):
	list_angles=[]
	list_visible_points=[]
	start_point=[]
	best_angle=-200
	vertical_found=0
	for x in asteroid_list:
		if(x!=best_location):
			if can_a_see_b(best_location,x,asteroid_list)==1:
				#Rotating axis to make angle manipulation
#				angle=math.atan2(-(x[1]-best_location[1]),\
#				x[0]-best_location[0])
				angle=math.atan2(x[0]-best_location[0],\
				(x[1]-best_location[1]))
				list_angles=list_angles+[angle]
				list_visible_points=list_visible_points+[x]
				if angle>best_angle and vertical_found==0:
					best_angle=angle
					start_point=x
	return [list_angles,list_visible_points,start_point]

def best_asteroid_position(asteroid_list):
	max_asteroid_count=-1
	best_location=[]
	for x in asteroid_list:
		tmp1=number_of_visible_asteroids(x,asteroid_list)
		if tmp1>max_asteroid_count:
			best_location=x
			max_asteroid_count=tmp1
	print("best_location\t"+str(best_location))
	print("max_asteroid_count\t"+str(max_asteroid_count))
	return [max_asteroid_count,best_location]


def number_of_visible_asteroids(a,asteroid_list):
	count1=0
	for x in asteroid_list:
		if(x!=a):
			count1=count1+can_a_see_b(a,x,asteroid_list)
	return count1

def can_a_see_b(a,b,asteroid_list):
	visible1=1
	diff_x=abs(b[0]-a[0])
	diff_y=abs(b[1]-a[1])
	gcd_diff=math.gcd(diff_x,diff_y)
	increment_x=int(round(diff_x/gcd_diff*(np.sign(b[0]-a[0]))))
	increment_y=int(round(diff_y/gcd_diff*(np.sign(b[1]-a[1]))))

	for i in range(1,gcd_diff):
		ix=a[0]+i*increment_x
		iy=a[1]+i*increment_y
		if [ix,iy] in asteroid_list and [ix,iy]!=a and  [ix,iy]!=b:
			visible1=0
	return visible1

def asteroid_tuples_from_file(filename_1):
	asteroid_list=[]
	k=0
	with open(filename_1) as f:
		for line2 in f:
			for i in range(0,len(line2)):
				if line2[i]=='#':
					asteroid_list=asteroid_list+[[i,k]]
			k=k+1
	return asteroid_list


class LearningCase(unittest.TestCase):
	def test_starting_out(self):
		list1=asteroid_tuples_from_file("Test_input_3_4.txt")
		print(can_a_see_b([3,4],[1,0],list1),0)
		print("number_of_visible_asteroids1\t"+\
		str(number_of_visible_asteroids([3,4],list1)))
		self.assertEqual((best_asteroid_position(list1))[0],8)
		list2=asteroid_tuples_from_file("Test_input_5_8.txt")
		self.assertEqual((best_asteroid_position(list2))[0],33)
		list3=asteroid_tuples_from_file("Test_input_1_2.txt")
		self.assertEqual((best_asteroid_position(list3))[0],35)
		list4=asteroid_tuples_from_file("Test_input_6_3.txt")
		self.assertEqual((best_asteroid_position(list4))[0],41)
		list5=asteroid_tuples_from_file("Test_input_11_13.txt")
		self.assertEqual((best_asteroid_position(list5))[0],210)
		list6=asteroid_tuples_from_file("puzzle_input.txt")
		self.assertEqual((best_asteroid_position(list6))[0],286)
		full_list5=full_list_target(list5)
		self.assertEqual([full_list5[i] for i in\
		[0,1,2,9,19,49,99,198,199,200,298]],\
		[[11,12],[12,1],[12,2],[12,8],[16,0],[16,9],\
		[10,16],[9,6],[8,2],[10,9],[11,1]])
		full_list6=full_list_target(list6)
		print("full_list6[199]")
		print(full_list6[199])
		self.assertEqual([(full_list6[199])[0]*100+(full_list6[199])[1]]\
		,[504])
		
def main():
	unittest.main()
	
if __name__ == "__main__":
	main()
