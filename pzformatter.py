#!/usr/bin/env python

import os

#setting the global variables
outputFile = 'latestpz.txt'
outline = []
header = '#             i  real          imag          real_error    imag_error'
skeleton = ['B053F10-13     0  0.000000E+00  0.000000E+00  +0.00000E+00  +0.00000E+00','B053F15-18     0  0.000000E+00  0.000000E+00  +0.00000E+00  +0.00000E+00']
zeros = ['#             Complex zeroes:', header]
poles = ['#             Complex poles:', header]
#count[0] == zeros, count[1] == poles
count = [0,0]
#mode = 0 == zeros, mode = 1 == poles
mode = 0
delete = False

def main():
	#main logic sequence
	contents = getClipboardContents()
	initializeFile()
	processContents(contents)
	writeFile()
	copyToClipboard()
	# deleteFile()

def getClipboardContents():
	#gets the contents of the clipboard and writes it to file, which it returns
	os.system('pbpaste > ' + outputFile)
	return readFile()

def readFile():
	#reads the file and returns its contents
	fob = open(outputFile,'r')
	contents = fob.read().split('\n')
	fob.close()
	return contents

def initializeFile():
	#rewrites the file to a blank state for future writing
	fob = open(outputFile,'w')
	fob.write('')
	fob.close()

def processContents(contents):
	#parses the contents and sets the outline of formatting
	for line in contents:
		#cycles through each line
		real = ''
		imag = ''
		realError = 0
		imagError = 0
		if   'zero' in line.lower():
			#sets the mode for zeroes
			global mode
			mode = 0
			outline.extend(zeros)
		elif 'pole' in line.lower():
			#sets the mode for poles
			mode = 1
			outline.extend(poles)
		elif '-' in line or '+' in line:
			#figures out which lines contain numbers
			real, imag = getValues(line)
			#copies a fake row to populate with values in the lines following this
			appendage = skeleton[mode]
			appendage = appendage[:14] + leftAlignedNo(str(count[mode])) + ' ' + real + '  ' + imag + '  ' + appendage[-26:]
			#writes the populated row to a global list
			outline.append(appendage)
			#increments the count of zeroes or poles accordingly for future reference
			count[mode] += 1
	#sets the Number of zeroes and poles line
	outline.insert(0, 'B053F09     Number of zeroes:                      ' + str(count[0]))
	outline.insert(1, 'B053F14     Number of poles:                       ' + str(count[1]))

def getValues(line):
	#reads the line given and parses it for values
	real, imag = separateValues(line)
	return value2SciNo(real), value2SciNo(imag)

def separateValues(line):
	#reads the line given, separates the values, and returns them
	real = '0'
	imag = '0'
	line = line.split()
	if line[2][-1] == 'i':
		#if the last character is 'i', remove the i (it's already known this value is imaginary)
		line[2] = line[2][:-1]
	if len(line) == 3:
		#if the line has 2 values and a plus or minus sign, append the sign to the second value
		real = line[0]
		imag = line[1] + line[2]
	return real, imag

def value2SciNo(value):
	#converts the string, int, or float value into scientific notation, returns it as a string
	value = "%06.5e" % float(value)
	if value[0] != '-':
		value = '+' + value
	return value.replace('e','E')

def leftAlignedNo(number):
	if len(number) == 1:
		number += ' '
	return number

def writeFile():
	#appends lines (in list form) to the file
	fob = open(outputFile, 'a')
	for line in outline:
		fob.write(line + '\n')
	fob.close()

def copyToClipboard():
	#copies the contents of the file to the clipboard
	os.system('cat ' + outputFile + '| pbcopy')
	print 'The formatted values have been copied to your clipboard'

def deleteFile():
	#deletes the file, this is optional
	if delete:
		os.system('rm ' + outputFile)
		

main()