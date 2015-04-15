""" RAID Validation.

This module validate the RAID configuration from the GCF. It uses the
RAID_CONTAINER node.

Author: Lorenzo Hernandez
Date: 04/14/2015

"""

import xml.etree.ElementTree as ET
from pprint import pprint

def main(GCF):
    """
    for controller in SUT.POXML.xpath("/GCF/DATACONTAINERS/CONTAINER/CONTROLLERS/CONTROLLER"):
        for node in controller.xpath("RAID_CONTAINERS/RAID_CONTAINER"):
            slots = node.attrib['sas_id'].split(',')
            try:
                lvl = int(node.attrib['level'])
            except Exception:
                raise Exception('Found Invalid Raid Level in GCF %s' % node.attrib['level'])
            if lvl in RaidRules:
                if len(set(slots)) < RaidRules[lvl][0] or len(set(slots)) > RaidRules[lvl][1]:
                    raise Exception('Found invalid Raid in GCF LVL:%d DRIVES:%s' % (lvl, str(set(slots))))
            drives = []
            for drive in controller.xpath("DRIVES/DRIVE"):
                driveChannelId = drive.xpath("ATTRIBUTE[@key='driveChannelId']/@value", smart_strings=False)[0]
                if driveChannelId in slots:
                    cap = drive.xpath("ATTRIBUTE[@key='capacity(MB)']/@value", smart_strings=False)[0]
                    try:
                        speed = drive.xpath("ATTRIBUTE[@key='spindle_speed(RPM)']/@value", smart_strings=False)[0]
                    except IndexError:
                        speed = 'N/A'
                    drives.append((cap, speed))

            # test slots
            if len(slots) != len(drives):
                raise Exception('Missing Slots in raid conteiners (%s)' % str(slots))

            # test size and speed
            for i in range(1, len(drives)):
                if drives[0][0] != drives[i][0]:
                    raise Exception("different HDD Size in raid container (Level %s - Slots %s)" % (node.attrib['level'], slots))
                elif drives[0][1] != drives[i][1]:
                    raise Exception("different HDD Speed in raid container (Level %s - Slots %s)" % (node.attrib['level'], slots))
    """

def exception(GCF):
    """
    Validate all the exceptions.
    input GCF string.
    output True/False bool.

    old code:
    for info in SUT.POPartList:
        for name, value in info.iteritems():
            if 'R0206' == value:
                return True
    """
    if 'R0206' in GCF:
        return True
    else:
        return False

def getControllers(GCF):
    """
    Parse the GCF in order to extract the controllers information.
    (Drives and RAIDDContainers)
    node: /GCF/DATACONTAINERS/CONTAINER/CONTROLLERS/

    input GCF string
    output controllers list
    """
    root = ET.fromstring(GCF)

    c,d,r = ('CONTROLLER','DRIVE','RAID_CONTAINER')
    controllers = [[x,y,z] for x in root.iter(c) for y in x.iter(d) for z in x.iter(r)]


    pprint(controllers)

    #controllers = []
    #for item in root.iter('CONTROLLER'):
        #controller = {
            #'info': item.attrib,
            #'drives': [],
            #'raids': []
        #}
        #for drive in item.iter('DRIVE'):
            #dr = {}
            #for att in drive.iter('ATTRIBUTE'):
                #e = att.attrib.values()
                #dr.update({e[0]:e[1]})
            #controller['drives'].append(dr)
        #for raid in item.iter('RAID_CONTAINER'):
            #for con in raid.iter('RAID_CONTAINER'):
                #controller['raids'].append(con.attrib)
        #controllers.append(controller)
    #pprint(controllers)

def validate(controllers):
    """
    Recursive function to validate every controller information.
    RAID, RAIDLevel, Capacity and Speed.

    input controllers [Tail] list
    output True/False bool
    """
    pass

def isValidRAIDLevel(RAIDLevel):
    """
    Evaluate the RAID level to int type, and check if exists in validRAIDLevels.

    input RAIDLevel string
    output True/False bool
    """
    #validRAIDLevels = [0,1,5,6,10,50,60]

def isValidRAID(raids):
    """
    Compare slots quantity vs rules min/max.

    input raids list
    output True/False bool
    """
    rules = {
        0: [1, 999],
        1: [2, 2],
        5: [3, 999],
        6: [4, 999],
        10: [4, 999],
        50: [6, 999],
        60: [8, 999]
    }
    print rules

def isSameCapacity(drives):
    """
    Check if all the HDDs in the controller have the same capacity.

    input drives list
    output True/False bool
    """

def isSameSpeed(drives):
    """
    Check if all the HDDs in the controller have the same speed.

    input drives list
    output True/False bool
    """


if __name__ == '__main__':
    gcf = None
    with open('gcf.xml', 'r') as file:
        gcf = file.read()

    getControllers(gcf)

