#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""This is the entry module of this application. This module collects the input form user, gets it splitted by stringsplitter module and then passes
the control to executor module for further processing which prints the list of searched tracks

"""

import stringsplitter
import executor
import time


def findtracks():
    """this method takes input from user and breaks that input in different parts using stringsplitter module and sends that list of dicts to executor module.
    
    """
    trackstr = raw_input('input your poem: ')
    trackstr = trackstr.strip()
    inputdict = stringsplitter.break_string(trackstr)
    executor.processrequest(inputdict)
    
if __name__ == '__main__':
     findtracks()
