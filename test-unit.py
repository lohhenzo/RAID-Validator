import os
import raid

path = '/home/lorenzo/projects/RAIDValidation/GCF_52/'

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

testMultiple()
#testOne('20674984470_1')
#testOne('20675014450_1')
#testOne('20673569920_1')
