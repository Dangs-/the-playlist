#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''This is a utility module which takes a string as input and splits that into smaller groups of lists for better results in finding the poem in trackfinder application'''

import math

def splitter(first,inputlist,rlist):
    '''This function splites the words of a list with few combinations.
    Parameter:
                firstlist - a sublist from main list
                inputlist - a sublist from main input from user
                rlist - list of lists (same words rearranged in each list) which serves the main output.
    
    '''
    bufferd = list()
    bufferd = first + list([inputlist])
    returnlist = list()
    [returnlist.append(" ".join(el)) for el in bufferd]
    rlist.append(returnlist)

    # breaking the input list and calling the same method untill the size of input list reduces to 1
    if len(" ".join(inputlist[:]).split(" ")) > 1:
        for i in range(len(" ".join(inputlist[:]).split(" "))-1):
            tlist = list()
            if len(first) > 0:
                tlist.extend(first)
            tlist.append(((" ".join(inputlist[:])).split())[0:i+1])
            secondlist =  [" ".join((" ".join(inputlist[:]).split()[i+1:len(" ".join(inputlist[:]))])[:])]
            splitter(tlist,secondlist,rlist)

def break_string(inputstring):
    '''This function splits an input string into parts each part having sqrt(input string) elements.
    Then sends this list to spitter function for more combinations of the words.
    Parameter:
                inputstring - a input string from user
    Return:
                a dictionary of lists keyed each entry from 0 to n(number of parts in input string)

    '''
    inputdict = {}
    inputlist = inputstring.split()
    msgsqrt = int(math.sqrt(len(inputlist)))
    startindex,endindex,dictkey = 0,msgsqrt,0
    while endindex <= len(inputlist):
            rlist = list()
            splitter([],inputlist[startindex:endindex],rlist)            
            inputdict.update({dictkey:rlist})
            startindex = endindex
            endindex = endindex +  msgsqrt
            dictkey += 1

    if startindex < len(inputlist):
        rlist = []
        splitter([],inputlist[startindex-msgsqrt:],rlist)
        inputdict[dictkey-1] = rlist
    return inputdict
