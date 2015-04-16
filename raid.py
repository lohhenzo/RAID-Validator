""" RAID Validation.
This module validate the RAID configuration from the GCF. It uses the
RAID_CONTAINER node.

Author: Lorenzo Hernandez
Date: 04/14/2015
"""

import xml.etree.ElementTree as ET

def main(GCF):
    controllers = getControllers(GCF)
    return validate(controllers)

def exception(GCF):
    """ Validate all the exceptions.
    """
    if 'R0206' in GCF:
        return True
    else:
        return False

def getControllers(GCF):
    """ Parse the GCF in order to extract the controllers information.
    (Drives and RAIDDContainers). Return a controllers list.
    node: /GCF/DATACONTAINERS/CONTAINER/CONTROLLERS/
    """
    root = ET.fromstring(GCF)
    controllers = []
    for item in root.iter('CONTROLLER'):
        controller = {
            'info': item.attrib,
            'drives': [],
            'raids': []
        }
        for drive in item.iter('DRIVE'):
            dr = {}
            for att in drive.iter('ATTRIBUTE'):
                e = att.attrib.values()
                dr.update({e[0]:e[1]})
            controller['drives'].append(dr)
        for raid in item.iter('RAID_CONTAINERS'):
            for con in raid.iter('RAID_CONTAINER'):
                controller['raids'].append(con.attrib)
        controllers.append(controller)

    return controllers

def validate(controllers):
    """ Recursive function to validate every controller information.
    RAID, RAIDLevel, Capacity and Speed. Return True if OK, else
    return an error message.
    """
    if len(controllers) <= 0:
        return True
    else:
        drives = controllers[0]['drives']
        raids  = controllers[0]['raids']

        RAIDLevel = isValidRAIDLevel(raids)
        if RAIDLevel == True: pass
        else: return RAIDLevel

        RAID = isValidRAID(raids)
        if RAID == True: pass
        else: return RAID

        capacity=isSameCapacityAndSpeed(drives,raids)
        if capacity == True: return validate(controllers[1:])
        else: return capacity

def isValidRAIDLevel(raids):
    """ Evaluate the RAID level to int type, and check if
    exists in valid RAID Levels. Return True if OK, else return
    an error message.
    """
    validRAIDLevels = [0,1,5,6,10,50,60]
    if len(raids) <= 0:
        return True
    else:
        if int(raids[0]['level']) in validRAIDLevels:
            return isValidRAIDLevel(raids[1:])
        else:
            return 'Invalid RAID level %s' % raids[0]['level']

def isValidRAID(raids):
    """ Compare slots quantity vs rules min/max.
    Return True if OK, else return an error message.
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
    if len(raids) <= 0:
        return True
    else:
        slots = len(set(raids[0]['sas_id'].split(',')))
        level = int(raids[0]['level'])
        rule  = rules[level]
        if slots < rule[0] or slots > rule[1]:
            msg = (slots,rule[0],rule[1])
            return 'Invalid RAID, %s slots, min %s - max %s' % msg
        else:
            return isValidRAID(raids[1:])

def isSameCapacityAndSpeed(drives,raids):
    """ Check if all the HDDs in the RAID container have the
    same capacity and speed. Return True if so, if not
    return an error message.
    """
    if len(raids) <= 0:
        return True
    else:
        slots = raids[0]['sas_id'].split(',')
        drivesOnRAID = filter(lambda x: x['driveChannelId'] in slots, drives)
        sameCapacity = getSameCapacity(drivesOnRAID)
        sameSpeed    = getSameSpeed(drivesOnRAID)

        if len(drivesOnRAID) != len(sameCapacity):
            return 'Drives with diff capacity in RAID Ctrl. %s '%str(drivesOnRAID)
        elif len(drivesOnRAID) != len(sameSpeed):
            return 'Drives with diff speed in RAID Ctrl. %s '%str(drivesOnRAID)
        else:
            return isSameCapacityAndSpeed(drives,raids[1:])

def getSameCapacity(drives):
    """ Return a drives list of same capacity
    """
    capacity = drives[0]['capacity(MB)'] # get capacity frm first drive
    return filter(lambda x:x['capacity(MB)']==capacity,drives)

def getSameSpeed(drives):
    """ Return a drives list of same capacity if attribute
    'spindle_speed' exists in each drive information.

    Return an empty list if 'spindle_speed' exists only in
    some drives, otherwise, return the drives list without
    the attribute.
    """
    try:
        speed = drives[0]['spindle_speed(RPM)']# get speed from first drive
        return filter(lambda x:x['spindle_speed(RPM)']== speed,drives)
    except KeyError:
        if len(set(map(len,drives))) > 1:
            return []
        else:
            return drives


if __name__ == '__main__':
    gcf = None
    with open('gcf.xml', 'r') as file:
        gcf = file.read()

    getControllers(gcf)

