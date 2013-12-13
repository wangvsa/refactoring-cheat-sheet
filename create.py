#!/usr/bin/python

headlist = [
'Decompose Conditional',
'Consolidate Conditional Expression',
'Consolidate Duplicate Conditional Fragments',
'Remove Control Flag',
'Replace Nested Conditional with Guard Clauses',
'Replace Conditional with Polymorphism',
'Introduce Null Object',
'Introduce Assertion'
]

basedir = 'simplifying-conditional-expressions'

for element in headlist:
    print(element)
    filename = basedir + '/' + element.replace(' ', '-') + '.html'
    f = open(filename, 'w')
    f.write("---\n")
    f.write('layout: simplifying-conditional-expressions\n')
    f.write('head_en: '+element)
    f.write("\n---")
    f.close()
