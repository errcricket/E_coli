import os
from sqlalchemy import *
import os.path
import Bio
import os
import sys
from Bio import GenBank
from Bio import SeqIO
from Bio import SeqFeature
from Bio.GenBank import Record
from Bio.GenBank.Record import Record
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna, generic_protein
from Bio.SeqFeature import Reference, SeqFeature, FeatureLocation
from Bio.Alphabet import IUPAC


##CREATE DATABASE: Check if db exists; if present, delete and then create it (testing phase)
##########################################################################
if os.path.isfile('DB_Ecoli/tutorial.db') == True:
	os.remove('DB_Ecoli/tutorial.db')
db = create_engine('sqlite:///DB_Ecoli/tutorial.db')

db.echo = False  # Try changing this to True and see what happens
metadata = MetaData(db)

#Create table for chromosomes------------------------------------------------
chromosome = Table('chromosome', metadata,
    Column('chromosome_id', Integer, primary_key=True),
    Column('species', String(40)),
    Column('strain', String(40)),
    Column('serotype', String(40)),
    Column('accession', String(20)),
    Column('locus_tag', String(40)),
    Column('journal', String(40)),
    Column('pub_title', String(40)),
    Column('authors', String(40)),
    Column('seq_method', String(40)),
    Column('collection_date', Date()),
    Column('isolation_source', String(40)),
    Column('source_country', String(40)),
    Column('annotation_method', String(40)),
    Column('gene_count', Integer),
    Column('plasmid_count', Integer),
    Column('GC_content', Integer),
)
Chromosome.create()
#--------------------------------------------------------------------------

##PROCESS GENBANK FILES: Open up genbank files to extract information used to populate database
##########################################################################
eColi_dic = {} #holds genes for each chromosome & plasmids separately (even if from the same strain)

fName = 'GenbankFile_E_coli/Z48231.gb'
with open(fName, 'w') as inputFile:
	record = SeqIO.parse(fName, 'genbank').next()

	featureCount = 0
	for f in record.features:
		if f.type == 'CDS':
			CDS = record.features[featureCount]
			string = file_name + '\t' + strain + '\t' + dna_type 

			for q in qualies:
				if q in CDS.qualifiers:
					string = string + '\t' + str(CDS.qualifiers[q]).replace('\'', '')
					qualies[q] = CDS.qualifiers[q]
				else: # not q in CDS.qualifiers:
					string = string + '\tNA' 

			string = strip_it(string)
			outputFile.write(string+'\n')
				
		featureCount+=1

'''
#How do I check if the entry already exists before I add it?
i = Chromosome.insert()
i.execute(name='Mary', age=30, password='secret')
i.execute({'name': 'John', 'age': 42},
          {'name': 'Susan', 'age': 57},
          {'name': 'Carl', 'age': 33})

s = Chromosome.select()
rs = s.execute()

row = rs.fetchone()
print('Id:', row[0])
print('Name:', row['name'])
print('Age:', row.age)
print('Password:', row[Chromosome.c.password])

for row in rs:
    print(row.name, 'is', row.age, 'years old')

'''
