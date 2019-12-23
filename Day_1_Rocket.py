from pynput.mouse import Button,Controller
import time
import pyautogui
import random
#from scipy import signal

def run1():
	filename_1 = "fuel_inputs.txt"
	x=0
	with open(filename_1) as f:
		for line in f:
			line_str=line.rstrip()
			if isinstance(float(line_str), float):
				y=float(line_str)
				b=(fuel_1(y))
				x=x+b
	print(x)
	
	
	

	
def fuel_1(mass):
	import math
#	print("mass")
#	print(mass)
	a = math.floor(mass/3)
	b=a-2
	if b>6:
		b=b+fuel_1(b)
	return b
	
	
	
	
	
