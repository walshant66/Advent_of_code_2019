from pynput.mouse import Button,Controller
import time
import pyautogui
import random
import numpy as np 
import unittest
	
def run2(filename_1):
	orbit_dict={}
	with open(filename_1) as f:
		for line in f:
			split_list1 = line.split(')')
			orbit_dict[(split_list1[1]).rstrip()]=split_list1[0]
	sum=0
#	print("orbit_dict")
#	print(orbit_dict)
	planet="YOU"
	you_array=[planet]
	while planet!="COM":
		planet=orbit_dict[planet]
		you_array=you_array+[planet]
	you_array=you_array[::-1]
#	print("you_array")
#	print(you_array)
	planet="SAN"
	san_array=[planet]
	while planet!="COM":
		planet=orbit_dict[planet]
		san_array=san_array+[planet]
	san_array=san_array[::-1]
#	print("san_array")
#	print(san_array)
	k1=0
	s1=0
	k2=0
	s2=0
	planet_1=""
	planet_2=""
	print(san_array[k2])
	while planet_1!="YOU" or planet_2!="SAN":
		planet_1=you_array[k1]
		planet_2=san_array[k2]
		if planet_1==planet_2:
			k1=k1+1
			k2=k2+1
		else:
			if planet_1!="YOU":
				k1=k1+1
				s1=s1+1
#				print("planet_1")
#				print(planet_1)
			if planet_2!="SAN":
				k2=k2+1
				s2=s2+1
#				print("planet_2")
#				print(planet_2)
	print("s1")
	print(s1)
	print("s2")
	print(s2)
	sum=s1+s2
	print("sum")
	print(sum)
	return sum



def run1(filename_1):
	orbit_dict={}
	with open(filename_1) as f:
		for line in f:
			split_list1 = line.split(')')
			orbit_dict[(split_list1[1]).rstrip()]=split_list1[0]
	sum=0
#	print("orbit_dict")
#	print(orbit_dict)
	for key in orbit_dict.keys():
#		print(key)
		a=0
		planet=key
		while planet!="COM":
			planet=orbit_dict[planet]
			a=a+1
#		print("key,a")
#		print(key,a)
		sum=sum+a
	print("sum")
	print(sum)		
#	print(orbit_dict)
	return sum


class LearningCase(unittest.TestCase):
	def test_starting_out(self):
		self.assertEqual(run1("Orbits_input_test_case.txt"),130681)
		self.assertEqual(run2("Orbits_input_test_case_example.txt"),4)
		self.assertEqual(run2("Orbits_input_test_case.txt"),313)


def main():
    unittest.main()

if __name__ == "__main__":
    main()

