from pynput.mouse import Button,Controller
import time
import pyautogui
import random
import numpy as np
import unittest
import math

def required_converation(fuel_name,fuel_quant,fuel_convert,Cost):
	fuel_quantity=int(fuel_quant[fuel_name])
	#List of conversions required
	fuel_convert_required=(fuel_convert[str(fuel_quantity)+' '+fuel_name])\
	.split(',')
	multiplier_1=math.ceil(int(Cost[fuel_name])/fuel_quantity)
	#Removing fuel_name first from Cost dictionary
	Cost[fuel_name]=int(Cost[fuel_name])-fuel_quantity*multiplier_1
	#Putting in required fuels back into the cose dictionary
	for fuel_single in fuel_convert_required:
		fuel_parts=(fuel_single.strip()).split(' ')
		fuel_quant_1=int((fuel_parts[0]))*multiplier_1
		fuel_type_1=(fuel_parts[1])
		try:
			Cost[fuel_type_1]=Cost[fuel_type_1]+fuel_quant_1
		except:
			Cost[fuel_type_1]=fuel_quant_1
	return Cost

def next_key(Cost):
	new_key="Complete"
	for key in Cost.keys():
		#Next key needs to be something that is positive which is a value
		#that is not needed or is not zero.
		if key!="ORE" and int(Cost[key])>0:
			new_key=key
			break
	return new_key

def run1(filename_1,starting_fuel):
	fuel_convert={}
	fuel_quant={}
	Cost={}
	#Creating dictionaries of chemical conversions
	with open(filename_1) as f:
		for line in f:
			split_convert = line.split('=>')
			fuel_convert[(split_convert[1]).rstrip().strip()]=split_convert[0]
			split_space = line.split(' ')
			fuel_quant[(split_space[-1]).rstrip()]=split_space[-2]
	#Cost dictionary contains the fuel budget, postive numbers is what is
	#needed and negative is what is left over.
	Cost["FUEL"]=starting_fuel
	fuel_name="FUEL"
	#Converting keys until only key left is ORE
	while(str(Cost.keys())!="dict_keys(['ORE'])"):
		Cost=required_converation(fuel_name,fuel_quant,fuel_convert,Cost)
		fuel_name=next_key(Cost)
		if fuel_name=="Complete":
			break
	return int(Cost["ORE"])

def binary_search_fuel(filename_1):
	max_fuel=1
	#Finding fuel points above and below 10**12 ORE
	while run1(filename_1,max_fuel)<=10**12:
		max_fuel=2*max_fuel
	fuel_size_above=max_fuel
	fuel_size_below=max_fuel/2
	fuel_size_now=round((fuel_size_above+fuel_size_below)/2)
	ORE_now=run1(filename_1,fuel_size_now)
	ORE_now_Plus_1=run1(filename_1,fuel_size_now+1)
	#Doing binary search to tighten points until ORE is just below 10**12
	while not(ORE_now<=10**12) or not(ORE_now_Plus_1>10**12):
		ORE_now=run1(filename_1,fuel_size_now)
		ORE_now_Plus_1=run1(filename_1,fuel_size_now+1)
		fuel_size_now_output=fuel_size_now
		if ORE_now>10**12:
			#Down
			fuel_size_above=min([fuel_size_above,fuel_size_now])
			fuel_size_now=round((fuel_size_above+fuel_size_below)/2)
		else:
			#Up
			fuel_size_below=max([fuel_size_below,fuel_size_now])
			fuel_size_now=round((fuel_size_above+fuel_size_below)/2)
	return fuel_size_now_output

class LearningCase(unittest.TestCase):
	def test_starting_out(self):
		self.assertEqual(run1("Fuel_example_1.txt",1),31)
		self.assertEqual(run1("Fuel_example_2.txt",1),165)
		self.assertEqual(run1("Fuel_example_3.txt",1),13312)
		self.assertEqual(run1("Fuel_example_4.txt",1),180697)
		self.assertEqual(run1("Fuel_example_5.txt",1),2210736)
		self.assertEqual(run1("Puzzle_input.txt",1),483766)
		self.assertEqual(binary_search_fuel("Fuel_example_3.txt"),82892753)
		self.assertEqual(binary_search_fuel("Fuel_example_4.txt"),5586022)
		self.assertEqual(binary_search_fuel("Fuel_example_5.txt"),460664)
		self.assertEqual(binary_search_fuel("Puzzle_input.txt"),3061522)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

