from pynput.mouse import Button,Controller
import time
import pyautogui
import random
import numpy as np 
#from scipy import signal

def run1(v1,v2):
	filename_1 = "program_inputs.txt"
	x=0
	with open(filename_1) as f:
		for line in f:
			print(type([1,2,3]))
			print(type(line))
			interestedin = line.split(',')
			a123=interestedin
#	for v1 in range(0, 20): 
#		for v2 in range(0, 20): 
#			interestedin[1]=12
#			interestedin[2]=2
#			interestedin=a123
			interestedin[1]=v1
			interestedin[2]=v2
#			print("v1")
#			print(v1)
#			print("v2")
#			print(v2)
#			print("Input array")
#			print(interestedin)
			a=str_process1(interestedin)
#			print("Output array")
#			print(a)
			print("First Number")
			print(a[0])
#			print("Vector")
#			print([v1,v2,a[0]])
			if a[0]==2894520:
				print("Output 2894520")
#				print("v1")
#				print(v1)
#				print("v2")
#				print(v2)
#				asfsdfsfsdfasdfsdfasfsdfsfsdfasdf
			if a[0]==19690720:
				print("Output 19690720")
				print("v1")
				print(v1)
				print("v2")
				print(v2)
				asfsdfsfsdfasdfsdfasfsdfsfsdfasdf


	
	

	
def str_process1(str1):
#	print("Checking")
#	print("str1[1]")
#	print(str1[1])
#	print("str1[2]")
#	print(str1[2])
	for i in range(0, len(str1)): 
		str1[i] = int(str1[i]) 
	s=0
	for i in range(0,len(str1),4):
#		print("Position")
#		print(i)
#		print("Operation")
#		print(str1[i])
		if str1[i]==99 and s==0:
			s=1
			break
		elif str1[i]==1 and s==0:
			try:
				str1[str1[i+3]]=str1[str1[i+1]]+str1[str1[i+2]]
			except:
				sfsfsdfsfsfsadf=1
		elif str1[i]==2 and s==0:
			try:
				str1[str1[i+3]]=str1[str1[i+1]]*str1[str1[i+2]]
			except:
				sfsfsdfsfsfsadf=1
	return str1





