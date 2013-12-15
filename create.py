#!/usr/bin/python

headlist = [
'Pull Up Field',
'Pull Up Method',
'Pull Up Constructor Body',
'Push Down Method',
'Push Down Field',
'Extract Subclass',
'Extract Superclass',
'Extract Interface',
'Collapse Hierarchy',
'Form Template Method',
'Replace Inheritance with Delegation',
'Replace Delegation with Inheritance'
]

basedir = 'dealing-with-generalization'

for element in headlist:
    print(element)
    filename = basedir + '/' + element.replace(' ', '-') + '.html'
    f = open(filename, 'w')
    f.write("---\n")
    f.write('layout: ' + basedir + '\n')
    f.write('head_en: ' + element)
    f.write("\n---")
    f.close()
