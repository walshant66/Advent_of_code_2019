from pynput.mouse import Button,Controller
import time
import pyautogui
import random
import numpy as np
import unittest
import math

def FFT_N_phases_repeats(input_signal,base_pattern,position,N,repeats):
	N=N+1
	position=position+1
	phases_old=[int(input_signal[-1])] * N
	phases_new=[int(input_signal[-1])] * N
	output_str=input_signal[-1]
	if position>0:
		for i_position1 in range(1,position+1):
			i_position=i_position1%len(input_signal)
			phases_new[0]=int(input_signal[-i_position-1])
			for i in range(1,N):
				phases_new[i]=(phases_old[i]+phases_new[i-1])%10
			phases_old=list(phases_new)
			output_str=str(phases_new[i]%10)+output_str
	return int(output_str[-position])

def FFT_N_phases_position_from_right(input_signal,base_pattern,position,N):
	N=N+1
	position=position+1
	phases_old=[int(input_signal[-1])] * N
	phases_new=[int(input_signal[-1])] * N
	output_str=input_signal[-1]
	if position>0:
		for i_position in range(1,position+1):
			phases_new[0]=int(input_signal[-i_position-1])
			for i in range(1,N):
				phases_new[i]=(phases_old[i]+phases_new[i-1])%10
			phases_old=list(phases_new)
			output_str=str(phases_new[i]%10)+output_str
	return int(output_str[-position])

def output_element(input_signal_int_list,base_pattern,element_1):
	sum=0
	for i in range(len(input_signal_int_list)):
			i_new=i%len(input_signal_int_list)
			sum=sum+input_signal_int_list[i_new]*\
			base_pattern[int((np.floor((i+1)/(element_1+1)))%4)]
	return abs(sum)%10

def FFT_single_phase(input_signal,base_pattern):
	input_signal_int_list=[]
	output_signal=""
	for i in range(len(input_signal)):
		input_signal_int_list=input_signal_int_list+[int(input_signal[i])]
	for element_1 in range(len(input_signal_int_list)):
		output_signal=output_signal+\
		str(output_element(input_signal_int_list,base_pattern,element_1))
	return output_signal

def FFT_multiple_phases_filename(filename_1,base_pattern,number_of_phases):
	with open(filename_1) as f:
		for line2 in f:
			input_signal=line2.rstrip()
#	print(input_signal)
	output_signal=input_signal
	max_length=len(input_signal)-1
	for i in range(number_of_phases):
		output_signal=FFT_single_phase(output_signal,base_pattern)
	return output_signal

def FFT_real_signal(filename_1,N):
	with open(filename_1) as f:
		for line2 in f:
			input_signal=line2.rstrip()
	str_test_1=input_signal
	offset=len(str_test_1)*10000-int(str_test_1[0:7])		
	str_out=""
	for i in range(8):
		a_out1=FFT_N_phases_repeats(str_test_1,[0,1,0,-1],offset-8+i,N,10000)
		str_out=str(a_out1)+str_out
	return str_out

class LearningCase(unittest.TestCase):
	def test_starting_out(self):
		N=100
		str_test=FFT_multiple_phases_filename("puzzle_input_16.txt",\
		[0,1,0,-1],N)
		print("str_test[0:8]")
		print(str_test[0:8])
		self.assertEqual(str_test[0:8],"44098263")
			
		N=100
		str_out1=FFT_real_signal("puzzle_input_16.txt",N)
		self.assertEqual(str_out1,"12482168")

def main():
	unittest.main()

if __name__ == "__main__":
    main()
