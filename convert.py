#!/usr/bin/python

import os

# just modify links and basedir

links_12 = [
    'Tease Apart Inheritance',
    'Convert Procedural Design to Objects',
    'Separate Domain from Presentation',
    'Extract Hierarchy'
]
basedir_12 = '{{site.baseurl}}/' + 'big-refactorings/'

links_11 = [
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
basedir_11 = '{{site.baseurl}}/' + 'dealing-with-generalization/'

links_10 = [
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
'Replace Exception with Test'
]
basedir_10 = '{{site.baseurl}}/' + 'making-method-calls-simpler/'

links_9 = [
'Decompose Conditional',
'Consolidate Conditional Expression',
'Consolidate Duplicate Conditional Fragments',
'Remove Control Flag',
'Replace Nested Conditional with Guard Clauses',
'Replace Conditional with Polymorphism',
'Introduce Null ObjectNull',
'Introduce Assertion'
]
basedir_9 = '{{site.baseurl}}/' + 'simplifying-conditional-expressions/'

links_8 = [
'Self Encapsulate Field',
'Replace Data Value with Object',
'Change Value to Reference',
'Change Reference to Value',
'Replace Array with Object',
'Duplicate Observed Data',
'Change Unidirectional Association to Bidirectional',
'Change Bidirectional Association to Unidirectional',
'Replace Magic Number with Symbolic Constant',
'Encapsulate Field',
'Encapsulate Collection',
'Replace Record with Data Class',
'Replace Type Code with Class',
'Replace Type Code with Subclasses',
#'Replace Type Code with State/Strategy',
'Replace Subclass with Fields'
]
basedir_8 = '{{site.baseurl}}/' + 'organizing-data/'

links = [
'Move Method',
'Move Field',
'Extract Class',
'Inline Class',
'Hide Delegate',
'Remove Middle Man',
'Introduce Foreign Method',
'Introduce Local Extension'
]
basedir = '{{site.baseurl}}/' + 'moving-features-between-objects/'


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
