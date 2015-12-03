# E_coli Database Project
---------------------------

###The following scripts are used to create a database of E_coli strains.
---------------------------------------------------------------------------------------------

#####Step 1. python download_files.py emailAddress
######Given a tab-del file, extract accession number (for chromosome & plasmid) from file to download genbank records from Entrez. Files will be downloaded and renamed to reflect the accession number.
######**Input**: genomeReport_Ecoli.txt
######**Output**: Downloaded Genebank/Fasta files (renamed after accession number)

#####Step 2. fasta_formatter_Ecoli.py 
###### Concatenate sequence reads which are spread across multiple lines (e.g., not wrapped). This script has been adapted to search a specified directory for fasta (*.fna) files. 
######**Input**: Directory name (directory contains fasta files)
######**Output**: Formatted fasta files saved to temp.txt, then renamed to replace original fasta file.


######**References**: 
http://pythoncentral.io/introductory-tutorial-python-sqlalchemy/
http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html
http://www.blog.pythonlibrary.org/2010/02/03/another-step-by-step-sqlalchemy-tutorial-part-1-of-2/
