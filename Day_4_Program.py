from pynput.mouse import Button,Controller
import time
import pyautogui
import random
import numpy as np 
from collections import deque
#from scipy import signal

def exact_match_2(i_str,position):
	match_1=0
	if i_str[position]==i_str[position+1] and i_str.count(i_str[position])==2:
		match_1=1
#		print("Possible_password")
#		print(i_str)
	return match_1

def run1():
	N_min=359282
#	N_min=100000
	N_max=820401
	tmp_str=str(N_min)
#	print("tmp_str")
#	print(tmp_str[0])
	k=0
	for i in range(N_min,N_max+1):
		i_str=str(i)
		if i_str[0]<=i_str[1] and i_str[1]<=i_str[2] and i_str[2]<=i_str[3] and i_str[3]<=i_str[4] and i_str[4]<=i_str[5]:
#			if i_str[0]==i_str[1] or i_str[1]==i_str[2] or i_str[2]==i_str[3] or i_str[3]==i_str[4] or i_str[4]==i_str[5]:
			match_1=0
			for i2 in range(0,5):
				if exact_match_2(i_str,i2)==1 and match_1==0:
					match_1=1
			if match_1==1:
				k=k+1
				if i==112233 or i==123444 or i==111122:
					print("test_cases")
					print(i)
	print('Number of passwords')
	print(k)
'''	filename_1 = "wire_directions.txt"
	x=0
	a_in=[[0,1],[1,0]]
	a2=a_in+[[2,2]]
	print('a_in')
	print(a_in)
	print('a2')
	print(a2)
	a_out1=a_in
	N=2
	print("factorial_complete(N)")
	print(factorial_complete(N))
	print("len(factorial_complete(N))")
	print(len(factorial_complete(N)))
'''
	
	
	
	
	
	
	
def factorial_complete(N):
	a_out1=[[0,1],[1,0]]
	for i in range(2,N):
		a_out1=factorial_run(a_out1,[i])
	return a_out1

def rotate(l, n):
    return l[n:] + l[:n]		
	
def factorial_run(a_in,new_addition):
	for i in range(0,len(a_in)):
		for j in range(0,(len(a_in[i])+1)):
			if j==0 and i==0:
				a_out=[rotate(rotate(a_in[i],j)+new_addition,-j)]
			else:
				a_out=a_out+[(rotate(rotate(a_in[i],j)+new_addition,-j))]
	return a_out
