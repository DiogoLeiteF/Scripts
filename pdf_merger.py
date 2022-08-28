import sys
import PyPDF2

# with open('dummy.pdf', 'rb') as file:
#     reader = PyPDF2.PdfFileReader(file)
#     page = reader.getPage(0)
#     page.rotateCounterClockwise(90)
    
#     writer = PyPDF2.PdfFileWriter()
#     writer.addPage(page)

#     with open ('tilt.pdf', 'wb') as new_file:
#         writer.write(new_file)


merger = PyPDF2.PdfMerger()
inputs = sys.argv[1:]
opened_inputs = []
for i in inputs:
    opened_inputs.append(open(i, 'rb'))
# input1 = open('dummy.pdf', 'rb')
# input2 = open('twopage.pdf', 'rb')

for pdf in opened_inputs:
    merger.append(pdf)

with open(f'merged_{inputs[0]}', 'wb') as merged_file:
    merger.write(merged_file)

merger.close()
