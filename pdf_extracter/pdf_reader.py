'''
Library: pip install PyPDF2
File: https://www.acko.com/policy/document/PjWqmVQOndwfZk6bIy4Yog.pdf?latest=true
'''
import PyPDF2
pdfFileObj = open('acko.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pageObj = pdfReader.getPage(0)
page1 = pageObj.extractText()
print(page1)
