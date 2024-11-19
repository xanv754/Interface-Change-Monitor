import json
from os import getcwd, listdir
from updater.constant import keywords, default, path
from updater.models.SNMP import SNMPModel
from updater.utils.date import get_date

async def get_equipments_by_file(filepath: str) -> list:
    """Read a file and return a list of JSON of SNMPModel.
    
    Parameters
    ----------
    filepath : str
        The path to the file to read.
    """
    snmp: list = []
    equipments: list = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
    equipment: list = []
    for line in lines:
        line = line.strip()
        if not keywords.DATE in line: equipment.append(line)
        elif keywords.DATE in line and len(equipment) <= 0: equipment.append(line)
        elif keywords.DATE in line and len(equipment) > 0:
            equipments.append(equipment)
            equipment = []
            equipment.append(line)
    equipments.append(equipment)
    for equipment in equipments:
        index = 0
        date: str = ''
        ip: str = ''
        community: str = ''
        sysname: str = ''
        for line in equipment:
            if keywords.DATE in line: date = line.split('=')[1]
            elif keywords.IP in line: ip = line.split('=')[1]
            elif keywords.COMMUNITY in line: community = line.split('=')[1]
            elif keywords.SYSNAME in line: sysname = line.split(default.SYSNAME)[1].strip()
            elif keywords.IFINDEX in line: 
                ifIndex = line.split(default.IFINDEX)[1].strip()
                ifName = default.DEFAULT
                ifAlias = default.DEFAULT
                ifDescr = default.DEFAULT
                ifSpeed = default.DEFAULT
                ifHighSpeed = default.DEFAULT
                ifPhysAddress = default.DEFAULT
                ifType = default.DEFAULT
                ifOperStatus = default.DEFAULT
                ifAdminStatus = default.DEFAULT
                ifLastChange = default.DEFAULT
                ifPromiscuousMode = default.DEFAULT
                ifConnectorPresent = default.DEFAULT
                for line in equipments[index]:
                    if keywords.IFNAME in line and ifIndex in line: ifName = line.split(default.IFNAME)[1].strip()
                    elif keywords.IFALIAS in line and ifIndex in line: ifAlias = line.split(default.IFALIAS)[1].strip()
                    elif keywords.IFDESCR in line and ifIndex in line: ifDescr = line.split(default.IFDESCR)[1].strip()
                    elif keywords.IFSPEED in line and ifIndex in line: ifSpeed = line.split(default.IFSPEED)[1].strip()
                    elif keywords.IFHIGHSPEED in line and ifIndex in line: ifHighSpeed = line.split(default.IFHIGHSPEED)[1].strip()
                    elif keywords.IFPHYSADDRESS in line and ifIndex in line: ifPhysAddress = line.split(default.IFPHYSADDRESS)[1].strip()
                    elif keywords.IFTYPE in line and ifIndex in line: ifType = line.split(default.IFTYPE)[1].strip()
                    elif keywords.IFOPERSTATUS in line and ifIndex in line: ifOperStatus = line.split(default.IFOPERSTATUS)[1].strip()
                    elif keywords.IFADMINSTATUS in line and ifIndex in line: ifAdminStatus = line.split(default.IFADMINSTATUS)[1].strip()
                    elif keywords.IFLASTCHANGE in line and ifIndex in line: ifLastChange = line.split(default.IFLASTCHANGE)[1].strip()
                    elif keywords.IFPROMISCUOUSMODE in line and ifIndex in line: ifPromiscuousMode = line.split(default.IFPROMISCUOUSMODE)[1].strip()
                    elif keywords.IFCONNECTORPRESENT in line and ifIndex in line: ifConnectorPresent = line.split(default.IFCONNECTORPRESENT)[1].strip()
                new_equipment = SNMPModel(
                                    date=date, 
                                    ip=ip, 
                                    community=community, 
                                    sysname=sysname, 
                                    ifIndex=ifIndex, 
                                    ifName=ifName, 
                                    ifAlias=ifAlias, 
                                    ifDescr=ifDescr, 
                                    ifSpeed=ifSpeed, 
                                    ifHighSpeed=ifHighSpeed, 
                                    ifPhysAddress=ifPhysAddress, 
                                    ifType=ifType, 
                                    ifOperStatus=ifOperStatus, 
                                    ifAdminStatus=ifAdminStatus, 
                                    ifLastChange=ifLastChange, 
                                    ifPromiscuousMode=ifPromiscuousMode, 
                                    ifConnectorPresent=ifConnectorPresent
                )
                snmp.append(new_equipment.model_dump())
            else: break
        index += 1
    return snmp

async def read_file(filepath: str) -> None:
    """Read a file and save it in a JSON file.
    
    Parameters
    ----------
    filepath : str
        The path to the file to read.
    """
    pwd = getcwd().split(path.HOME_PROJECT)[0]
    save = pwd + path.SAVE_DATA + 'data.json'
    equipments = await get_equipments_by_file(filepath)
    with open(save, "w") as file:
        json.dump(equipments, file, indent=4)

async def read_files(date: str | None = None) -> None:
    """Read all files in the directory for default of the data and save them in a JSON file.
    
    Parameters
    ----------
    date : str, optional
        The date of the file to read. If not provided, the current date will be used.
    """
    if not date: date = get_date()
    pwd = getcwd().split(path.HOME_PROJECT)[0]
    dir = pwd + path.DIR_DATA
    save = pwd + path.SAVE_DATA
    files = listdir(dir)
    for file in files:
        if path.SNMP_DATA in file and date in file:
            part = file.split('part_')[1]
            equipments = await get_equipments_by_file(dir + '/' + file)
            with open(save + f'data_{part}.json', "w") as file:
                json.dump(equipments, file, indent=4)