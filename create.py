#!/usr/bin/python

headlist = [
'Self Encapsulate Field',
'Replace Data Value with Object',
'Change Value to Reference',
'Change Reference to Value',
'Replace Array with Object',
'Duplicate Observed Data',
'Change Unidirectional Association to Bidirectional',
'Encapsulate Collection',
'Replace Record with Data Class',
'Replace Type Code with Class',
'Replace Type Code with Subclasses',
'Replace Type Code with State/Strategy',
'Replace Subclass with Fields'
]
for element in headlist:
    print(element)
    filename = element.replace('/',' or ').replace(' ', '-') + '.html'
    f = open(filename, 'w')
    f.write("---\n")
    f.write('layout: organizing-data\n')
    f.write('head_en: '+element)
    f.write("\n---")
    f.close()
