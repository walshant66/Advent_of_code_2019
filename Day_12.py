import time
import math
import random
import numpy as np 
import unittest
import os
import matplotlib.pyplot as plt
from matplotlib import colors
import re

def cyc_moons_once(Moon_list):
	#velocity
	for i1 in range(0,4):
		v_x=(Moon_list[i1]).vel_x
		v_y=(Moon_list[i1]).vel_y
		v_z=(Moon_list[i1]).vel_z
		for i2 in range(0,4):
			if i1!=i2:
				if (Moon_list[i1]).pos_x>(Moon_list[i2]).pos_x:
					v_x=v_x-1
				if (Moon_list[i1]).pos_x<(Moon_list[i2]).pos_x:
					v_x=v_x+1
				if (Moon_list[i1]).pos_y>(Moon_list[i2]).pos_y:
					v_y=v_y-1
				if (Moon_list[i1]).pos_y<(Moon_list[i2]).pos_y:
					v_y=v_y+1
				if (Moon_list[i1]).pos_z>(Moon_list[i2]).pos_z:
					v_z=v_z-1
				if (Moon_list[i1]).pos_z<(Moon_list[i2]).pos_z:
					v_z=v_z+1
		(Moon_list[i1]).vel_x=v_x
		(Moon_list[i1]).vel_y=v_y
		(Moon_list[i1]).vel_z=v_z
	for i1 in range(0,4):
		(Moon_list[i1]).pos_x=(Moon_list[i1]).pos_x+(Moon_list[i1]).vel_x
		(Moon_list[i1]).pos_y=(Moon_list[i1]).pos_y+(Moon_list[i1]).vel_y
		(Moon_list[i1]).pos_z=(Moon_list[i1]).pos_z+(Moon_list[i1]).vel_z
		(Moon_list[i1]).pot=abs((Moon_list[i1]).pos_x)+\
		abs((Moon_list[i1]).pos_y)+abs((Moon_list[i1]).pos_z)
		(Moon_list[i1]).kin=abs((Moon_list[i1]).vel_x)+\
		abs((Moon_list[i1]).vel_y)+abs((Moon_list[i1]).vel_z)
		(Moon_list[i1]).total=(Moon_list[i1]).pot*(Moon_list[i1]).kin

class object_moon_state(object):
	def __init__(self,posx=0,posy=0,posz=0,velx=0,vely=0,velz=0):
		self.pos_x=posx
		self.pos_y=posy
		self.pos_z=posz
		self.vel_x=velx
		self.vel_y=vely
		self.vel_z=velz
		self.pot=0
		self.kin=0
		self.total=0
		self.pos_x_initial=posx
		self.pos_y_initial=posy
		self.pos_z_initial=posz
		self.vel_x_initial=velx
		self.vel_y_initial=vely
		self.vel_z_initial=velz

def test_moon_object(filename_1,number_of_cycles):
	Moon_A=object_moon_state()
	Moon_B=object_moon_state()
	Moon_C=object_moon_state()
	Moon_D=object_moon_state()
	Moon_list=[Moon_A,Moon_B,Moon_C,Moon_D]
	i=0
	with open(filename_1) as f:
		for line2 in f:
			line=line2.rstrip()
			str_state_int = re.split(',|=|>|<',line)
			(Moon_list[i]).pos_x=int(str_state_int[2])
			(Moon_list[i]).pos_y=int(str_state_int[4])
			(Moon_list[i]).pos_z=int(str_state_int[6])
			i=i+1
	f.close()
	for i in range(0,number_of_cycles):
		cyc_moons_once(Moon_list)
	return Moon_A.total+Moon_B.total+Moon_C.total+Moon_D.total

def check_match(Moon_list,dimension):
	#velocity
	match_found=0
	all_match=0
	for i1 in range(0,4):
		if (Moon_list[i1]).vel_x_initial==(Moon_list[i1]).vel_x and \
		(Moon_list[i1]).pos_x_initial==(Moon_list[i1]).pos_x and \
		dimension=="X":
			match_found=match_found+1
		if (Moon_list[i1]).vel_y_initial==(Moon_list[i1]).vel_y and \
		(Moon_list[i1]).pos_y_initial==(Moon_list[i1]).pos_y and \
		dimension=="Y":
			match_found=match_found+1
		if (Moon_list[i1]).vel_z_initial==(Moon_list[i1]).vel_z and \
		(Moon_list[i1]).pos_z_initial==(Moon_list[i1]).pos_z and \
		dimension=="Z":
			match_found=match_found+1
	if match_found==4:all_match=1
	return all_match
	
def test_moon_object_find_match(filename_1,dimension):
	Moon_A=object_moon_state()
	Moon_B=object_moon_state()
	Moon_C=object_moon_state()
	Moon_D=object_moon_state()
	Moon_list=[Moon_A,Moon_B,Moon_C,Moon_D]
	i=0
	with open(filename_1) as f:
		for line2 in f:
			line=line2.rstrip()
			str_state_int = re.split(',|=|>|<',line)
			(Moon_list[i]).pos_x=int(str_state_int[2])
			(Moon_list[i]).pos_y=int(str_state_int[4])
			(Moon_list[i]).pos_z=int(str_state_int[6])
			(Moon_list[i]).pos_x_initial=int(str_state_int[2])
			(Moon_list[i]).pos_y_initial=int(str_state_int[4])
			(Moon_list[i]).pos_z_initial=int(str_state_int[6])
			i=i+1
	f.close()
#	number_of_cycles=3000
	cycle_count=0
#	for i in range(0,number_of_cycles):
	while 1<2:
		cyc_moons_once(Moon_list)
		cycle_count=cycle_count+1
		if check_match(Moon_list,dimension)==1:
			break
	return cycle_count

def lcm_tmp(a,b):
 return a*b//math.gcd(a,b)

def find_period_with_LCM_X_Y_Z(filename_1):
# Just need to find lowest common multiple of individual periods of
#X, Y, and Z co-ordinates to find the total period of the moon orbits
	Period_X=test_moon_object_find_match(filename_1,"X")
	Period_Y=test_moon_object_find_match(filename_1,"Y")
	Period_Z=test_moon_object_find_match(filename_1,"Z")
	Total_period=lcm_tmp(lcm_tmp(Period_X,Period_Y),Period_Z)
	return Total_period

class LearningCase(unittest.TestCase):
	def test_starting_out(self):
		self.assertEqual(test_moon_object("Example_input.txt",10),\
		179)
		self.assertEqual(test_moon_object("Example_input_2.txt",100),\
		1940)
		self.assertEqual(test_moon_object("Puzzle_input.txt",1000),\
		7077)
		self.assertEqual(find_period_with_LCM_X_Y_Z("Example_input.txt"),\
		2772)
		self.assertEqual(find_period_with_LCM_X_Y_Z("Example_input_2.txt"),\
		4686774924)
		self.assertEqual(find_period_with_LCM_X_Y_Z("Puzzle_input.txt"),\
		402951477454512)

def main():
	unittest.main()

if __name__ == "__main__":
	main()
