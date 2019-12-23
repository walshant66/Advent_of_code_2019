from pynput.mouse import Button,Controller
import time
import pyautogui
import random
import numpy as np 
import unittest
	
def run1(filename_1,input_0):
	x=0
	with open(filename_1) as f:
		for line in f:
			interestedin = line.split(',')
			a=str_process1(interestedin,input_0)
	return a

def str_process1(str_ori,input_0):
	i=0
	code_output=[]
	while i< (len(str_ori)):
		opcode=int(((str_ori[i]).rstrip())[-2:])
		if (opcode>0 and opcode<9) or opcode==99:
			dsfdsfsdafsdfsdf=1
		else:
			print("wrong opcode")
			break
		if opcode==99:
			break
		mode_1=0
		mode_2=0
		mode_3=1
		print("(str_ori[i])")
		print((str_ori[i]))
		if len(str_ori[i])==5:
			asfsdafsdfsfdsfsadfsadfdsafsd
			mode_3=1
			mode_2=int((str_ori[i])[1])
			mode_1=int((str_ori[i])[2])
		if len(str_ori[i])==4:
			mode_3=1
			mode_2=int((str_ori[i])[0])
			mode_1=int((str_ori[i])[1])
		if len(str_ori[i])==3:
			mode_3=1
			mode_2=0
			mode_1=int((str_ori[i])[0])
		input_1=0
		input_2=0
		input_3=0
		if opcode==1 or opcode==2 or (opcode>4 and opcode<9):
			input_1=str_val(str_ori,mode_1,i+1)
			input_2=str_val(str_ori,mode_2,i+2)
			if opcode==7 or opcode==8:
				input_3=str_val(str_ori,mode_3,i+3)
		print("str_ori")
		print(str_ori)
		print("position")
		print(i)
		print("opcode")
		print(opcode)
		[str_ori,i,code_output]=operation_run(str_ori,input_1,input_2,input_3,input_0,opcode,i,mode_1,code_output)
	return code_output

def str_val(str_ori,mode_1,position):
	if mode_1==0:
		val_1=int(str_ori[int(str_ori[position])])
	else:
		val_1=int(str_ori[position])
	return val_1

def operation_run(str_ori,input_1,input_2,input_3,input_0,opcode,position,mode_2,code_output):
	if opcode==1:
		new_location=int(str_ori[position+3])
		str_ori[new_location]=str(input_1+input_2)
		position=position+4
	elif opcode==2:
		new_location=int(str_ori[position+3])
		str_ori[new_location]=str(input_1*input_2)
		position=position+4
	elif opcode==3:
		new_location=int(str_ori[position+1])
		str_ori[new_location]=str(input_0)
		position=position+2
	elif opcode==4:
		if mode_2==0:
			code_output=str_ori[int(str_ori[position+1])]
			print("Code_output")
			print(str_ori[int(str_ori[position+1])])
		if mode_2==1:
			code_output=(str_ori[position+1])
			print("Code_output")
			print(str_ori[position+1])
		position=position+2
	elif opcode==5:
		if input_1!=0:
			position=input_2
		else:
			position=position+3
	elif opcode==6:
		if input_1==0:
			position=input_2
		else:
			position=position+3
	elif opcode==7:
		if input_1<input_2:
			str_ori[input_3]="1"
		else:
			str_ori[input_3]="0"
		position=position+4
	elif opcode==8:
		if input_1==input_2:
			print("input_3_1")
			print(input_3)
			print("str_ori[input_3]")
			print(str_ori[input_3])
			str_ori[input_3]="1"
		else:
			print("input_3_2")
			print(input_3)
			str_ori[input_3]="0"
		position=position+4
	return [str_ori,position,code_output]

class LearningCase(unittest.TestCase):
	def test_starting_out(self):
#		self.assertEqual(run1("program_inputs_8.txt",8), "1")
		self.assertEqual(run1("program_inputs_3.txt",5), "9168267")
#		self.assertEqual(run1("program_inputs.txt",7), "6745903")
		self.assertEqual(run1("program_inputs_2.txt",1), "999")
		self.assertEqual(run1("program_inputs_2.txt",1), "999")
		self.assertEqual(run1("program_inputs_2.txt",2), "999")
		self.assertEqual(run1("program_inputs_2.txt",3), "999")
		self.assertEqual(run1("program_inputs_2.txt",4), "999")
		self.assertEqual(run1("program_inputs_2.txt",5), "999")
		self.assertEqual(run1("program_inputs_2.txt",6), "999")
		self.assertEqual(run1("program_inputs_2.txt",7), "999")
		self.assertEqual(run1("program_inputs_2.txt",8), "1000")
		self.assertEqual(run1("program_inputs_2.txt",9), "1001")
		self.assertEqual(run1("program_inputs_2.txt",10), "1001")
		self.assertEqual(run1("program_inputs_2.txt",11), "1001")
		self.assertEqual(run1("program_inputs_2.txt",12), "1001")
		self.assertEqual(run1("program_inputs_2.txt",22), "1001")
		self.assertEqual(run1("program_inputs_2.txt",25), "1001")
		self.assertEqual(run1("program_inputs_2.txt",109), "1001")
		self.assertEqual(run1("program_inputs_2.txt",119), "1001")
		self.assertEqual(run1("program_inputs_4.txt",10), "1")
		self.assertEqual(run1("program_inputs_4.txt",0), "0")
		self.assertEqual(run1("program_inputs_equal_8_first.txt",8), "1")
		self.assertEqual(run1("program_inputs_equal_8_first.txt",7), "0")
		self.assertEqual(run1("program_inputs_less_than_8_first.txt",8), "0")
		self.assertEqual(run1("program_inputs_less_than_8_first.txt",7), "1")
		self.assertEqual(run1("program_inputs_equal_8_second.txt",8), "1")
		self.assertEqual(run1("program_inputs_equal_8_second.txt",7), "0")
		self.assertEqual(run1("program_inputs_less_than_8_second.txt",8), "0")
		self.assertEqual(run1("program_inputs_less_than_8_second.txt",7), "1")


def main():
    unittest.main()

if __name__ == "__main__":
    main()

