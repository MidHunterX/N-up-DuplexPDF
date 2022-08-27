#*----------------------------------------------------------------*#
#| Bit Algorithm (N-up Duplex pages)                              |#
#| ---------------------------------------------------------------|#
#| 1. Get PDF file and total no. of pages (n)                     |#
#| 2. Add blank pages such that total pages becomes multiple of 8 |#
#|     2.1 No. of pages to add = n % 8                            |#
#| 3. Split pages into odd set and even set                       |#
#| 4. Swap every 2 neighbouring pages with each other in even set |#
#| 5. Append 4 pages from odd and even sets till n                |#
#|                                                   - Mid Hunter |#
#*----------------------------------------------------------------*#

from PyPDF2 import PdfFileReader, PdfFileWriter


# 1. Get PDF file and total no. of pages (n)
pdf_document = input(("Enter file name : "))
pdf = PdfFileReader(pdf_document)
n = pdf.getNumPages()


# 2. Add blank pages such that total pages becomes multiple of 8
temp_file = "temp.pdf"
whitepage = n % 8
temp_writer = PdfFileWriter(pdf_document)

for i in range(n):
	temp_writer.addPage(pdf.getPage(i))
for i in range(whitepage):
	temp_writer.addBlankPage(219,297) #A4 size dimensions

temp_writer.write(open(temp_file, "wb"))
# updating values
pdf = PdfFileReader(temp_file)
n = pdf.getNumPages()


# 3. Split pages into odd set and even set
odd_file = "odd.pdf"
even_file = "even.pdf"
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
