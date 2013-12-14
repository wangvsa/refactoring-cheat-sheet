#!/usr/bin/python

headlist = [
'Rename Method',
'Add Parameter',
'Remove Parameter',
'Separate Query from Modifier',
'Parameterize Method',
'Replace Parameter with Explicit Methods',
'Preserve Whole Object',
'Replace Parameter with Method',
'Introduce Parameter Object',
'Remove Setting Method',
'Hide Method',
'Replace Constructor with Factory Method',
'Encapsulate Downcast',
'Replace Error Code with Exception',
'Replace Exception with Test',
]

basedir = 'making-method-calls-simpler'

for element in headlist:
    print(element)
    filename = basedir + '/' + element.replace(' ', '-') + '.html'
    f = open(filename, 'w')
    f.write("---\n")
    f.write('layout: making-method-calls-simpler\n')
    f.write('head_en: '+element)
    f.write("\n---")
    f.close()
