from pynput.mouse import Button,Controller
import time
import pyautogui
import random
import numpy as np 
import unittest
import os
	
def find_minimum_line(filename_1,width,height):
	with open(filename_1) as f:
		for line in f:
			str_state = list(line)
	f.close()
	count_zeros=width*height+1
	product_ones_zeros=-1
	for i in range(0,len(str_state),width*height):
		if (str_state[i:(i+width*height)]).count('0')<count_zeros:
			count_zeros=(str_state[i:(i+width*height)]).count('0')
			product_ones_zeros=((str_state[i:(i+width*height)]).count('1'))*((str_state[i:(i+width*height)]).count('2'))
	return product_ones_zeros


def find_message(filename_1,width,height):
	with open(filename_1) as f:
		for line in f:
			str_state = list(line)
	f.close()
	layer=[]
	count_zeros=width*height+1
	product_ones_zeros=-1
	for i in range(0,len(str_state),width*height):
		layer=(str_state[i:(i+width*height)])
		if i==0:
			layer_current=layer
		else:
			for k in range(0,width*height):
				if layer_current[k]=="2":
					layer_current[k]=layer[k]
	layer_print=layer_current
	for k in range(0,width*height):
		if layer_current[k]=="0":
			layer_print[k]=" "
	for k in range(0,width*height,width):
		print((str(layer_print[k:(k+width)])).replace(',', '').replace("'", '').replace("[", '').replace("]", ''))

class LearningCase(unittest.TestCase):
	def test_starting_out(self):
		self.assertEqual(find_minimum_line("image_file_example_input.txt",6,6),272)
		self.assertEqual(find_minimum_line("image_file_puzzle_input.txt",25,6),2064)
		find_message("image_file_puzzle_input.txt",25,6)
		
def main():
	unittest.main()
	
if __name__ == "__main__":
	main()
