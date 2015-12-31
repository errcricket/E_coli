import sys
import os
import os.path
from sqlalchemy import *
import Bio
import os
from Bio import GenBank
from Bio import SeqIO
from Bio import SeqFeature
from Bio.Seq import Seq

'''
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
'''
#--------------------------------------------------------------------------

##PROCESS GENBANK FILES: Open up genbank files to extract information used to populate database
##########################################################################
eColi_dic = {} #holds genes for each chromosome & plasmids separately (even if from the same strain)

genome_file = 'GenbankFiles_E_coli/AB011549.gb'
##########################GET GENBANK INFORMATION#################################
for record in SeqIO.parse(genome_file, 'genbank'):
	count = 1 #keeping track of CDS encounters

##########################GET CHROMOSOME TABLE DATA#################################
#	print(record)
	ID = record.id
	sequence = record.seq
	seqLength = len(sequence)
	GI = record.annotations['gi']
	featureCount = len(record.features)
	description = record.description
	organism = record.annotations['organism']
	date = record.annotations['date']
	keywords = record.annotations['keywords']
	accessions = ','.join(record.annotations['accessions'])
	taxonomy = record.annotations['taxonomy']
	sequence_version = record.annotations['sequence_version']
	reference = record.annotations['references']
	comment = record.annotations['comment']
	source = record.annotations['source']
	data_file_division = record.annotations['data_file_division']
	#print(comment)
	
	#print('id, accession, sequence_length, feature_count, description, date', 'organism')
	#print(ID, accession, seqLength, featureCount, description, date, organism)
	for r in record.annotations['references']:
		print(r.authors)
		print('gap')
	article = record.annotations['references'][0].title
	journal = record.annotations['references'][0].journal
	authors = record.annotations['references'][0].authors
	pubmedID = record.annotations['references'][0].pubmed_id
#	print(record.annotations.values())
#dict_values(['19-MAY-2007', 'Escherichia coli O157:H7 str. Sakai', '4589740', [''], 2, 'On Apr 20, 1999 this sequence version replaced gi:3336997.', ['AB011549'], 'Escherichia coli O157:H7 str. Sakai', 'BCT', [Reference(title='Complete nucleotide sequences of 93-kb and 3.3-kb plasmids of an enterohemorrhagic Escherichia coli O157:H7 derived from Sakai outbreak', ...), Reference(title='Direct Submission', ...)], ['Bacteria', 'Proteobacteria', 'Gammaproteobacteria', 'Enterobacteriales', 'Enterobacteriaceae', 'Escherichia']])

#	print(record.annotations.keys())
#dict_keys(['accessions', 'keywords', 'taxonomy', 'sequence_version', 'references', 'organism', 'date', 'gi', 'comment', 'source', 'data_file_division'])
#	print(record.annotations['gi'])


	#print(record)

'''
ID: AB011549.2
Name: AB011549
Description: Escherichia coli O157:H7 str. Sakai plasmid pO157 DNA, complete sequence.
Database cross-references: BioProject:PRJNA226
Number of features: 133
/taxonomy=['Bacteria', 'Proteobacteria', 'Gammaproteobacteria', 'Enterobacteriales', 'Enterobacteriaceae', 'Escherichia']
/organism=Escherichia coli O157:H7 str. Sakai
/date=19-MAY-2007
/comment=On Apr 20, 1999 this sequence version replaced gi:3336997.
/gi=4589740
/sequence_version=2
/data_file_division=BCT
/accessions=['AB011549']
/source=Escherichia coli O157:H7 str. Sakai
/keywords=['']
/references=[Reference(title='Complete nucleotide sequences of 93-kb and 3.3-kb plasmids of an enterohemorrhagic Escherichia coli O157:H7 derived from Sakai outbreak', ...), Reference(title='Direct Submission', ...)]
Seq('AGCCAGATTTTACCCGCCCATCCTAAAGAAGGGGATAGTCAACCACATCTGACC...CAA', IUPACAmbiguousDNA())
'''

'''
	for feature in record.features:
		if feature.type=='CDS':
			count+=1
			feats = 'CDS'
			locus_tag = feature.qualifiers.get('locus_tag')
			frame = feature.qualifiers.get('codon_start')
			product = feature.qualifiers.get('product')
			if type(product) == list:
				product = ' '.join(feature.qualifiers.get('product'))
			transl_table = int(''.join(feature.qualifiers.get('transl_table')))
			AA_sequence = Seq(''.join(feature.qualifiers.get('translation')))
			extracted_feature = feature.extract(sequence).translate(table=transl_table)
			identity = 0
			
			if extracted_feature == AA_sequence:
				identity = 100.00

			elif extracted_feature[-1] == '*':
				extracted_feature = extracted_feature[0:-1]
				if extracted_feature == AA_sequence:
					identity = 100.00
				elif 'M' + extracted_feature[1:] == AA_sequence:
					extracted_feature = 'M' + extracted_feature[1:-1]
					identity = round(100*len(extracted_feature)/float(len(AA_sequence)), 2)
				else: #THIS SHOULD GO TO ANOTHER PROGRAM (MAUVE??) TO GET IDENTITY
					identity = 'NA'
					fasta_entry = '>' + locus_tag + '\n' + feature.extract(sequence) + '\n'
					unpairedFile.write(fasta_entry)

			string = '\t'.join([str(ID), str(''.join(locus_tag)), str(product), str(identity), str(''.join(frame)), str(1)])
			outputFile.write(string + '\n')

	print(count)
'''
#--------------------------------------------------------------------------


'''
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
