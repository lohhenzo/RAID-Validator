import os,urllib, urllib2
import raid

path = '/home/lorenzo/projects/assets/GCF_52/'

def testMultiple():
    gcfList = {}

    for filename in os.listdir(path):
        gcf = {filename: None}
        with open(path + filename, 'r') as file:
            gcf[filename] = file.read()
        gcfList.update(gcf)

    print len(gcfList)

    for gcf in gcfList.items():
        print gcf[0][:-4], raid.main(gcf[1])

def testOne(filename):
    gcf = None
    with open(path + filename + '.xml', 'r') as file:
        gcf = file.read()

    print raid.main(gcf)

def testWS(filename):
    gcf = None
    with open(path + filename + '.xml', 'r') as file:
        gcf = file.read()

    parameters = { 'po': gcf }
    arguments = urllib.urlencode(parameters)
    response = urllib2.urlopen('http://localhost:8890/', arguments)
    print response.read()

#testMultiple()
#testOne('20674984470_1')
#testOne('20675014450_1')
#testOne('20673569920_1')
testWS('20673569920_1')
