from typing import List
from database.entities.interface import InterfaceEntity
from database.constants.date import TypeDate
from database.utils.database import Database


class InterfaceModel:
    @staticmethod
    def get_interface_by_id(id: int) -> InterfaceEntity | None:
        """Obtain an interface by performing a database query.

        Parameters
        ----------
        id : int
            The id of the interface to be obtained.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM interface WHERE id = %s", (id,))
        res = cur.fetchone()
        database.close_connection()
        if res:
            data = dict(zip(InterfaceEntity.model_fields.keys(), res))
            interface = InterfaceEntity(**data)
            return interface
        else:
            return None

    @staticmethod
    def get_interfaces() -> List[InterfaceEntity]:
        """Obtain a list of all interfaces by performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM interface")
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []

    @staticmethod
    def get_interfaces_by_equipment(id_equipment: int) -> List[InterfaceEntity]:
        """Obtain a list of all interfaces filter by equipment performing a database query.

        Parameters
        ----------
        id_equipment : int
            The id of the equipment.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM interface WHERE idEquipment = %s", (id_equipment,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []

    @staticmethod
    def get_interfaces_by_index(
        id_equipment: int, if_index: int
    ) -> InterfaceEntity | None:
        """Obtain an interfaces filter by equipment and index performing a database query.

        Parameters
        ----------
        id_equipment : int
            The id of the equipment.
        if_index : int
            The index of the interface.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute(
            "SELECT * FROM interface WHERE idEquipment = %s AND ifIndex = %s",
            (id_equipment, if_index),
        )
        res = cur.fetchone()
        database.close_connection()
        if res:
            data = dict(zip(InterfaceEntity.model_fields.keys(), res))
            interface = InterfaceEntity(**data)
            return interface
        else:
            return None

    @staticmethod
    def get_interfaces_by_date_consult(date_consult: str) -> List[InterfaceEntity]:
        """Obtain a list of all interfaces filter by date consult performing a database query.

        Parameters
        ----------
        date_consult : str
            The date of the consult in format YYYY-MM-DD.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM interface WHERE dateConsult = %s", (date_consult,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []

    @staticmethod
    def get_interfaces_today() -> List[InterfaceEntity]:
        """Obtain a list of all interfaces filter by date type TODAY performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute(
            "SELECT * FROM interface WHERE dateType = %s", (TypeDate.TODAY.value,)
        )
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []

    @staticmethod
    def get_interfaces_yesterday() -> List[InterfaceEntity]:
        """Obtain a list of all interfaces filter by date type YESTERDAY performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute(
            "SELECT * FROM interface WHERE dateType = %s", (TypeDate.YESTERDAY.value,)
        )
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []

    @staticmethod
    def get_interfaces_old() -> List[InterfaceEntity]:
        """Obtain a list of all interfaces filter by date type OLD performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute(
            "SELECT * FROM interface WHERE dateType = %s", (TypeDate.OLD.value,)
        )
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []

    def insert_interface(data: dict) -> InterfaceEntity | None:
        """Create an interface by performing a database query.

        Parameters
        ----------
        data: dict
            Dict with the values of the interface to be created.
        """
        new_interface = InterfaceEntity(**data)
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            "INSERT INTO interface (ifIndex, idEquipment, dateConsult, dateType, ifName, ifDescr, ifAlias, ifSpeed, ifHighSpeed, ifPhysAddress, ifType, ifOperStatus, ifAdminStatus, ifPromiscuousMode, ifConnectorPresent, ifLastCheck) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                new_interface.ifIndex,
                new_interface.idEquipment,
                new_interface.dateConsult,
                new_interface.dateType.value,
                new_interface.ifName,
                new_interface.ifDescr,
                new_interface.ifAlias,
                new_interface.ifSpeed,
                new_interface.ifHighSpeed,
                new_interface.ifPhysAddress,
                new_interface.ifType,
                new_interface.ifOperStatus.value,
                new_interface.ifAdminStatus.value,
                new_interface.ifPromiscuousMode,
                new_interface.ifConnectorPresent,
                new_interface.ifLastCheck,
            ),
        )
        res = cur.statusmessage
        if res == "INSERT 0 1":
            conn.commit()
            database.close_connection()
            return InterfaceModel.get_interfaces_by_index(
                new_interface.idEquipment, new_interface.ifIndex
            )
        else:
            database.close_connection()
            return None

    def insert_interfaces(data: List[dict]) -> int:
        """Create a list of interfaces by performing a database query.

        Parameters
        ----------
        data: List[dict]
            List of dicts with the values of the interfaces to be created.
        """
        total_inserted = 0
        data = [InterfaceEntity(**interface) for interface in data]
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        for interface in data:
            cur.execute(
                "INSERT INTO interface (ifIndex, idEquipment, dateConsult, dateType, ifName, ifDescr, ifAlias, ifSpeed, ifHighSpeed, ifPhysAddress, ifType, ifOperStatus, ifAdminStatus, ifPromiscuousMode, ifConnectorPresent, ifLastCheck) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    interface.ifIndex,
                    interface.idEquipment,
                    interface.dateConsult,
                    interface.dateType.value,
                    interface.ifName,
                    interface.ifDescr,
                    interface.ifAlias,
                    interface.ifSpeed,
                    interface.ifHighSpeed,
                    interface.ifPhysAddress,
                    interface.ifType,
                    interface.ifOperStatus.value,
                    interface.ifAdminStatus.value,
                    interface.ifPromiscuousMode,
                    interface.ifConnectorPresent,
                    interface.ifLastCheck,
                ),
            )
            res = cur.statusmessage
            if res == "INSERT 0 1": total_inserted += 1
        conn.commit()
        database.close_connection()
        return total_inserted