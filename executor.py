#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""This module is responsile for main execution of the application. It takes an input dict of lists and spawns the process for each group of lists.
Executes all processes using shared chache and prints their merged output on console.

"""
import multiprocessing
import xmlparser
import xmlfinder
import time
import memcache


def find_list(sublist,memc):
    '''This function fetctes recieves a list of words which are sent to Spotify search API for searching the XML.
    That XML object is then sent to xmlparser API which inturn sends back the racks which are matching with searched words.
    Parameters:
            sublist - list of words to be searched
            memc - memcache client instance
    Return:
            list of lists of word and corresponding href
    Exception:
            raising the genric exception thrown by xmlfinder

    '''
    trackhreflist = []
    for i in range(len(sublist)):
            key = sublist[i].replace(" ","")

            # finding if searched string is available in cache, otherwise search on Spotify search API
            href = memc.get(key)
            if not href:
                try:
                    xml = xmlfinder.fetch_xml(sublist[i])
                except Exception, e:
                   # raise any exception coming from xmlfinder 
                   raise
                href = xmlparser.parseTrackXML(xml,sublist[i])
                if href == None:
                    memc.set(key,'NOT_FOUND')
                else:
                    memc.set(key,href)
            trackhreflist.append([sublist[i],href])
    return trackhreflist
    
def matching_tracks(trackhreflist):
    '''This function returns the list of number of matched tracks for each list.
    Parameter:
            trackhreflist - a list of track and respective href value.
    Return:
            hrefcountdict - A list of dictioanries of successful search. All list have similar words

    '''
    hrefcount = 0
    hrefcountdict = {}
    maxcount = 0
    tracklist = []
    for i in range(len(trackhreflist)):
        words = trackhreflist[i][0]
        trackhref = trackhreflist[i][1]
        if not trackhref == None and not trackhref == 'NOT_FOUND':
            hrefcount = hrefcount + len(words.split())
        if maxcount < hrefcount:
            words = words+','
            tracklist.append(words)
            maxcount = hrefcount
    # populate the maximum count of tracklist with respective maximum count as key of the dictionary
    # If there are more than one tracks forming the maxcount, those are appended to previous match (TBD - this wil be fixed later, or hrefs can be displayed in result)
    hrefcountdict = {maxcount:tracklist}
    return hrefcountdict
  

def executeprocess(managerdict,i,tlist,memc):
    '''Executed for all processes spawned by "multiprocessing.Process" module this function finds the list of tracks for each set of lists using find_list() funtion.
    then calculating the matched tracks for each group of lists using matching_tracks() and finally populates the search string and corresponding found track into managerdic.
    Parameters:
                managerdict - dictionary from manager module shared among all processes.
                i = counter to manage the processe based indexing of data.
                tlist - a list of lists containg similar words.
                memc - memcache client instance
    Exception: 
             Exception - generic exception propogated from above
    '''
    hrefcountlist = []
    for ilist in tlist:
        trackhreflist = []
        try:
            trackhreflist.extend(find_list(ilist,memc))
        except Exception ,e:
            managerdict.update({'exception':unicode(e)})
            #exit the application in case of exception
            exit(1)
            
        hrefcountlist.append(matching_tracks(trackhreflist))
    maxkey = None
    lindex = None
    # find the index of list item (-a dictionary) where dictionary have the maximum key (the key is the maximum count populated in matching_tracks function).
    for i in range(len(hrefcountlist)):
        currentkey = max(hrefcountlist[i].keys())
        if maxkey < currentkey:
            maxkey = currentkey
            lindex = i
    if not maxkey == None and not lindex == None:
        #populate the track value with maximum number of counts into managerdict.
        managerdict.update({" ".join(ilist):" ".join((hrefcountlist[lindex][maxkey])[:])})
    else:
        managerdict[i] == None
        

def processrequest(inputdict):
    '''This function spawns one process for each list intem in stringlist, manages the lifecycle of all processes, collects output from all processes,
    merge as per the searched string, and finally outputs the searched result on console.
    Parameters:
                inputdict : a dictionary of lists to be searched.
    
    '''
    # Manager object for managing the shared resource - managerdict
    manager = multiprocessing.Manager()
    managerdict = manager.dict()

    # Instance of memcache client
    memc = memcache.Client(['127.0.0.1:11211'])

    # process list
    processes = [] 

    # create and start the n number of processes where n is the number of items in input dict.
    for i in range(len(inputdict)):      
            processes.append(multiprocessing.Process(target=executeprocess, args=(managerdict,i,inputdict[i],memc,)))
            processes[i].start()
            
    print "\nPlease wait we are processing your request...."
    # wait for all processes to finish the excecution
    [p.join() for p in processes]

    # sleeping the main thread for 1/5 seconds so that Multiprocessing module can populate and make the managerdict object ready with values for main process.
    # if we don't do this, main process can fail with keyerror while iterating the managerdict
    time.sleep(0.2)

    # if there is no exception, iterate managerdict to print the resulted tracks with corresponding serach string.
    if 'exception' in managerdict:
        print 'There is some exception: ',managerdict['exception']
    else:
        for key in inputdict:
            print "Search String: "," ".join(inputdict[key][0]),"\t Track: "," ".join((managerdict[" ".join(inputdict[key][0])]).split())[:-1]
    memc.flush_all()
