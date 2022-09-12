#*-----------------------------------------------------------------*#
#| Bit Algorithm (N-up Duplex pages)                               |#
#| ----------------------------------------------------------------|#
#| 1. Get PDF file and total no. of pages (n)                      |#
#| 2. Add blank pages such that total pages becomes multiple of 8  |#
#|     2.1 blank_page = (nearest ceil multiple of 8) - n           |#
#| 3. Split pages into odd set and even set                        |#
#| 4. Swap every 2 neighbouring pages with each other in even set  |#
#| 5. Append 4 pages from odd and even sets till n                 |#
#|                                                    - Mid Hunter |#
#*-----------------------------------------------------------------*#

import ntpath
from PyPDF2 import PdfFileReader, PdfFileWriter
from os import remove
from math import ceil

print("""
  __  __ _     _   _    _             _
 |  \/  (_)   | | | |  | |           | |
 | \  / |_  __| | | |__| |_   _ _ __ | |_ ___ _ __
 | |\/| | |/ _` | |  __  | | | | '_ \| __/ _ \ '__|
 | |  | | | (_| | | |  | | |_| | | | | ||  __/ |
 |_|  |_|_|\__,_| |_|  |_|\__,_|_| |_|\__\___|_|
            Duplex N-up page (imposition) algorithm
""")

# 1. Get PDF file and total no. of pages (n)
pdf_document = input(("Drop file here : "))
if (pdf_document[0] == "\""):
	# Remove quotes from the ends of path
	pdf_document = pdf_document[1:-1]
pdf = PdfFileReader(pdf_document)
n = pdf.getNumPages()

# 2. Add blank pages such that total pages becomes multiple of 8
temp_file = "X_"+ntpath.basename(pdf_document)
pageWidth = pdf.getPage(0).mediaBox[2] - pdf.getPage(0).mediaBox[0]
pageHeight = pdf.getPage(0).mediaBox[3] - pdf.getPage(0).mediaBox[1]

# Developing a function to round to a multiple
def round_to_multiple(number, multiple):
    return multiple * ceil(number / multiple)

whitepage = round_to_multiple(n, 8) - n
temp_writer = PdfFileWriter(pdf_document)

for i in range(n):
	temp_writer.addPage(pdf.getPage(i))
for i in range(whitepage):
	temp_writer.addBlankPage(pageWidth,pageHeight)
	# temp_writer.addBlankPage(219,297) #A4 size dimensions

temp_writer.write(open(temp_file, "wb"))
# updating values
pdf = PdfFileReader(temp_file)
n = pdf.getNumPages()

# 3. Split pages into odd set and even set
odd_file = "69odd69"
even_file = "69even69"
odd_set = PdfFileWriter()
even_set = PdfFileWriter()

for page in range(n):
	current_page = pdf.getPage(page)
	if page % 2 == 0:
		odd_set.addPage(current_page)
	else:
		even_set.addPage(current_page)

with open(odd_file, "wb") as out:
	odd_set.write(out)
	print("created", odd_file)

with open(even_file, "wb") as out:
	even_set.write(out)
	print("created", even_file)

# 4. Swap every 2 neighbouring pages with each other in even set
temp_reader = PdfFileReader(even_file)
temp_writer = PdfFileWriter()
even_set_size = temp_reader.getNumPages()

for i in range(even_set_size):
	if i % 2 == 0:
		current_page = temp_reader.getPage(i)
		next_page = temp_reader.getPage(i+1)
		temp_writer.addPage(next_page)
	else:
		temp_writer.addPage(current_page)

temp_writer.write(open(even_file, "wb"))
print("corrected", even_file)

# 5. Append 4 pages from odd and even sets till n
file1 = PdfFileReader(odd_file)
file2 = PdfFileReader(even_file)
temp_reader = PdfFileReader(temp_file)
temp_writer = PdfFileWriter()
file1_page = 0
file2_page = 0

for i in range(n//8):
	for i in range(4):
		current_page = file1.getPage(file1_page)
		temp_writer.addPage(current_page)
		file1_page += 1
	for i in range(4):
		current_page = file2.getPage(file2_page)
		temp_writer.addPage(current_page)
		file2_page += 1

temp_writer.write(open(temp_file, "wb"))
print("finalized", temp_file)

# Cleaning up
remove(odd_file)
remove(even_file)
