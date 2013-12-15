#!/usr/bin/python

headlist = [
'Tease Apart Inheritance',
'Convert Procedural Design to Objects',
'Separate Domain from Presentation',
'Extract Hierarchy',
]

basedir = 'big-refactorings'

for element in headlist:
    print(element)
    filename = basedir + '/' + element.replace(' ', '-') + '.html'
    f = open(filename, 'w')
    f.write("---\n")
    f.write('layout: ' + basedir + '\n')
    f.write('head_en: ' + element)
    f.write("\n---")
    f.close()
