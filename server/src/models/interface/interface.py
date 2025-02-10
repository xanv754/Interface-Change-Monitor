from typing import List
from constants import GTABLES, InterfaceFields
from utils import PostgresDatabase

class Interface:
    id: int
    ifIndex: int
    idEquipment: int
    dateConsult: str

    def __init__(
        self,
        id: int | None = None,
        ifIndex: int | None = None,
        idEquipment: int | None = None,
        dateConsult: str | None = None,
    ):
        self.id = id
        self.ifIndex = ifIndex
        self.idEquipment = idEquipment
        self.dateConsult = dateConsult

    def get_all_by_date(self) -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"SELECT * FROM {GTABLES.INTERFACE.value} WHERE {InterfaceFields.DATE_CONSULT.value} = %s",
                (self.dateConsult,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            interfaces: List[dict] = []
            for res in result:
                interfaces.append(
                    {
                        InterfaceFields.ID.value: res[0],
                        InterfaceFields.IFINDEX.value: res[1],
                        InterfaceFields.IDEQUIPMENT.value: res[2],
                        InterfaceFields.DATE_CONSULT.value: res[3].strftime("%Y-%m-%d"),
                        InterfaceFields.IFNAME.value: res[4],
                        InterfaceFields.IFDESCR.value: res[5],
                        InterfaceFields.IFALIAS.value: res[6],
                        InterfaceFields.IFSPEED.value: res[7],
                        InterfaceFields.IFHIGHSPEED.value: res[8],
                        InterfaceFields.IFPHYSADDRESS.value: res[9],
                        InterfaceFields.IFTYPE.value: res[10],
                        InterfaceFields.IFOPERSTATUS.value: res[11],
                        InterfaceFields.IFADMINSTATUS.value: res[12],
                        InterfaceFields.IFPROMISCUOUSMODE.value: res[13],
                        InterfaceFields.IFCONNECTORPRESENT.value: res[14],
                        InterfaceFields.IFLASTCHECK.value: res[15]
                    }
                )
            return interfaces
        except Exception as e:
            print(e)
            return []
        
    def get_by_device_date(self) -> dict | None:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"SELECT * FROM {GTABLES.INTERFACE.value} WHERE {InterfaceFields.IDEQUIPMENT.value} = %s AND {InterfaceFields.IFINDEX.value} = %s AND {InterfaceFields.DATE_CONSULT.value} = %s",
                (self.idEquipment, self.ifIndex, self.dateConsult),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            interface = {
                InterfaceFields.ID.value: result[0],
                InterfaceFields.IFINDEX.value: result[1],
                InterfaceFields.IDEQUIPMENT.value: result[2],
                InterfaceFields.DATE_CONSULT.value: result[3].strftime("%Y-%m-%d"),
                InterfaceFields.IFNAME.value: result[4],
                InterfaceFields.IFDESCR.value: result[5],
                InterfaceFields.IFALIAS.value: result[6],
                InterfaceFields.IFSPEED.value: result[7],
                InterfaceFields.IFHIGHSPEED.value: result[8],
                InterfaceFields.IFPHYSADDRESS.value: result[9],
                InterfaceFields.IFTYPE.value: result[10],
                InterfaceFields.IFOPERSTATUS.value: result[11],
                InterfaceFields.IFADMINSTATUS.value: result[12],
                InterfaceFields.IFPROMISCUOUSMODE.value: result[13],
                InterfaceFields.IFCONNECTORPRESENT.value: result[14],
                InterfaceFields.IFLASTCHECK.value: result[15]
            }
            return interface
        except Exception as e:
            print(e)
            return None

    def get_by_id(self) -> dict | None:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"SELECT * FROM {GTABLES.INTERFACE.value} WHERE {InterfaceFields.ID.value} = %s",
                (self.id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            interface = {
                InterfaceFields.ID.value: result[0],
                InterfaceFields.IFINDEX.value: result[1],
                InterfaceFields.IDEQUIPMENT.value: result[2],
                InterfaceFields.DATE_CONSULT.value: result[3].strftime("%Y-%m-%d"),
                InterfaceFields.IFNAME.value: result[4],
                InterfaceFields.IFDESCR.value: result[5],
                InterfaceFields.IFALIAS.value: result[6],
                InterfaceFields.IFSPEED.value: result[7],
                InterfaceFields.IFHIGHSPEED.value: result[8],
                InterfaceFields.IFPHYSADDRESS.value: result[9],
                InterfaceFields.IFTYPE.value: result[10],
                InterfaceFields.IFOPERSTATUS.value: result[11],
                InterfaceFields.IFADMINSTATUS.value: result[12],
                InterfaceFields.IFPROMISCUOUSMODE.value: result[13],
                InterfaceFields.IFCONNECTORPRESENT.value: result[14],
                InterfaceFields.IFLASTCHECK.value: result[15]
            }
            return interface
        except Exception as e:
            print(e)
            return None

    def delete(self) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"DELETE FROM {GTABLES.INTERFACE.value} WHERE {InterfaceFields.ID.value} = %s",
                (self.id,),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            print(e)
            return False
        else:
            if status and status == "DELETE 1":
                return True
            else:
                return False
