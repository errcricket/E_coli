'''
Author: 	E. Reichenberger
Date:		9.10.2014
Modified: 12.3.2015

Purpose: Concatenate sequence reads which are spread across multiple lines (e.g., not wrapped)

>G0DGX7Q01D7GVH rank=0000275 x=1608.0 y=667.0 length=174
TTGCTCTCCTTCGAGGGTGCATTAACGCAGACGACCTAGGATCACCGACTGTGTTGTGGT
ACAACTTGACGAGCAACACGTGGATCCTGCTGTATGTTGCACACTCACCTTGTTTAGGAG
AGTAGAATTTCAACATGTAGGGTTACCATGAATTCTTGGTGACTTGGACCGGTT
'''

import glob
import os
import sys
import gzip


#arguments = sys.argv
#f_name_in = arguments[1] #'NC_008253.fna' 
#f_name_out = arguments[2] 
dir_name = 'GenbankFiles_E_coli/'

####################################DEFINITIONS############################
def format_file(directory, fileIn):
	print(fileIn)
	singleLine = ''
	fileOut = directory + 'temp.fna'
	with open(fileOut, 'wt') as outputFile: #this approach opens file and closes it when finished. 
#	outputFile = open(fileOut, 'wt') 

		with open(fileIn, 'r') as inputFile: #this approach opens file and closes it when finished. 
			lines = inputFile.readlines()
			for index, line in enumerate(lines):
				line = line.replace('\n', '')
				lines[index] = lines[index].replace('\n', '')

				if lines[index].startswith('>'):
					lines[index] = '?' + lines[index] + '?' #adds ? to beginining of line and adds '>' to end of lines that starts with '>'
				singleLine = singleLine + lines[index]

		spliter = singleLine.split('?')

		for i in range(len(spliter)):
			if i != 0:
				outputFile.write(spliter[i] + '\n')

#	outputFile.close()
	os.rename(fileOut, fileIn)
#--------------------------------------------------------------------------

##GET FILE LISTING: Get a list of all fasta files within specified directory 
##########################################################################
fileList = []
for file in os.listdir(dir_name):
	if file.endswith('.fna'):
		fileList.append(file)
#--------------------------------------------------------------------------

##FORMAT FILES:
##########################################################################
for f in fileList:
	f = dir_name + f
	format_file(dir_name, f)
#--------------------------------------------------------------------------
