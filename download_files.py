'''
Author: 	E. Reichenberger
Date: 	11.24.2015 

Purpose: Given a tab-del file, extract accession number (for chromosome & plasmid) from file to download genbank records from Entrez. Files will be downloaded and renamed to reflect the accession number.

IMPORTANT!!!!! Times are listed for EST, if you are in another time zone, make the proper hour changes in this script 
'''

import os
import os.path
import sys
import re #regular expressions
from Bio import Entrez
import datetime
import time

arguments = sys.argv
Entrez.email = arguments[1] #email

accession = [] # GI/accession number (from fasta file)  needed when calling Entrez

##EXTRACT ACCESSION NUMBERS: Open file, look for accession number (tab-del file, index 10)
##########################################################################
with open('genomeReport_Ecoli.txt', 'r') as inputFile: inputFile.readline()
	for line in inputFile.readlines():
		line = line.replace('\n', '')
		accessions = line.split('\t')[10]
		accessions = accessions.replace('chromosome', '')
		Saccession = accessions.split(';')

		for s in Saccession:
			s = s.lstrip()
			acc = s.split(':')
			
			for a in acc:
				if '/' in a:
					a = a.split('/')[0]
				if a.startswith('plasmid') == False and a.startswith(' ') == False and len(a) > 3:
					accession.append(a)
#--------------------------------------------------------------------------

##PRINT ACCESSIONS TO FILE: Write all accession numbers to file. Comment out if need be
##########################################################################
with open('accessions.txt', 'w') as outputFile:
	for a in accession:
		outputFile.write(a + '\n')
#--------------------------------------------------------------------------

print('You have ' + str(len(accession)) + ' file(s) to download.')

###############################################################################
#---ACHTUNG--ACHTUNG--ACHTUNG--ACHTUNG--ACHTUNG--ACHTUNG--ACHTUNG--ACHTUNG----#
###############################################################################
# Call Entrez to download files
# If downloading more than 100 files...
# Run this script only between 9pm-5am Monday - Friday EST
# Send E-utilities requests to http://eutils.ncbi.nlm.nih.gov
# Make no more than 3 requests every 1 second.
# Use URL parameter email & tool for distributed software
# NCBI's Disclaimer and Copyright notice must be evident to users of your service. 
#
# Use this script at your own risk. 
# Neither the script author nor author's employers are responsible for consequences arising from improper usage 
###############################################################################

##CALL ENTREZ: Call Entrez to download genbank AND fasta (nucleotide) files using accession numbers.
###############################################################################
start_day = datetime.date.today().weekday() # 0 is Monday, 6 is Sunday
start_time = datetime.datetime.now().time()
print(str(start_day), str(start_time))
print('')

if ((start_day < 5 and start_time > datetime.time(hour=21)) or (start_day < 5 and start_time < datetime.time(hour=5)) or start_day > 5 or len(accession) <= 100 ):
	print('Calling Entrez...')
	for a in accession:
		print(a)
		if ( (datetime.date.today().weekday() < 5 and datetime.datetime.now().time() > datetime.time(hour=21)) or (datetime.date.today().weekday() < 5 and datetime.datetime.now().time() < datetime.time(hour=5)) or (datetime.date.today().weekday() == start_day + 1 and datetime.datetime.now().time() < datetime.time(hour=5)) or (datetime.date.today().weekday() > 5) or len(accession) <= 100 ):
			while True:
		print('Downloading ' + a)

		handle=Entrez.efetch(db='nucleotide', id=a, rettype='gb', retmode='text') 
		FILENAME =  'GenbankFiles_E_coli/' + a + '.gb'
		local_file=open(FILENAME,'w')
		local_file.write(handle.read())
		handle.close()
		local_file.close()

		handle=Entrez.efetch(db='nucleotide', id=a, rettype='fasta', retmode='text') 
		FILENAME =  'GenbankFiles_E_coli/' + a + '.fna'
		local_file=open(FILENAME,'w')
		local_file.write(handle.read())
		handle.close()
		local_file.close()
#--------------------------------------------------------------------------
