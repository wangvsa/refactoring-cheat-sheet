#!/usr/bin/python

import os

# just modify links and basedir

links_12 = [
    'Tease Apart Inheritance',
    'Convert Procedural Design to Objects',
    'Separate Domain from Presentation',
    'Extract Hierarchy'
]
basedir12 = '{{site.baseurl}}/' + 'big-refactorings/'

links = [
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
basedir = '{{site.baseurl}}/' + 'dealing-with-generalization/'

targetDirs = [
'bad-smells-in-code/',
'big-refactorings/',
'composing-methods/',
'making-method-calls-simpler/',
'dealing-with-generalization/',
'organizing-data/',
'simplifying-conditional-expressions/',
'moving-features-between-objects/'
]


def buildFile(fileStr):
    newFileStr = fileStr
    for key in links:
        newFileStr = newFileStr.replace(key, formLink(key))
    return newFileStr

def formLink(key):
    link = key.replace(' ', '-') + '.html'
    link = '<a href=\"' + basedir + link + '\">' + key + '</a>'
    return link


def fun(theDir):
    for f in os.listdir(theDir):
        if(f.endswith('.html')):
            print f
            i = 0
            head = list()
            result = list()
            file = open(theDir+f, 'r')
            line = file.readline()
            while line!='':
                if i<=4:
                    head.append(line)
                else:
                    result.append(line)
                i = i+1
                line = file.readline()

            newFileStr = buildFile(''.join(result))

            file = open(theDir+f, 'w')
            file.write('%s' % ''.join(head))
            file.close()

            file = open(theDir+f, 'a')
            file.write(newFileStr)
            file.close()

def myMain():
    for theDir in targetDirs:
        fun(theDir)

print '...start...'
myMain()
print '...end...'
