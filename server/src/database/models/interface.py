from typing import List
from database.entities.interface import InterfaceEntity
from database.constants.date import TypeDate
from database.utils.database import Database
from database.constants.tables import NameTablesDatabase
from database.constants.fields import InterfaceFieldsDatabase


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
        cur.execute(f"SELECT * FROM {NameTablesDatabase.interface.value} WHERE {InterfaceFieldsDatabase.id.value} = %s", (id,))
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
        cur.execute(f"SELECT * FROM {NameTablesDatabase.interface.value}")
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
        cur.execute(f"SELECT * FROM {NameTablesDatabase.interface.value} WHERE {InterfaceFieldsDatabase.idEquipment.value} = %s", (id_equipment,))
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
            f"SELECT * FROM {NameTablesDatabase.interface.value} WHERE {InterfaceFieldsDatabase.idEquipment.value} = %s AND {InterfaceFieldsDatabase.ifIndex.value} = %s",
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
        cur.execute(f"SELECT * FROM {NameTablesDatabase.interface.value} WHERE {InterfaceFieldsDatabase.dateConsult.value} = %s", (date_consult,))
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
            f"SELECT * FROM {NameTablesDatabase.interface.value} WHERE {InterfaceFieldsDatabase.dateType.value} = %s", (TypeDate.TODAY.value,)
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
            f"SELECT * FROM {NameTablesDatabase.interface.value} WHERE {InterfaceFieldsDatabase.dateType.value} = %s", (TypeDate.YESTERDAY.value,)
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
            f"SELECT * FROM {NameTablesDatabase.interface.value} WHERE {InterfaceFieldsDatabase.dateType.value} = %s", (TypeDate.OLD.value,)
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
            f"INSERT INTO {NameTablesDatabase.interface.value} ({InterfaceFieldsDatabase.ifIndex.value}, {InterfaceFieldsDatabase.idEquipment.value}, {InterfaceFieldsDatabase.dateConsult.value}, {InterfaceFieldsDatabase.dateType.value}, {InterfaceFieldsDatabase.ifName.value}, {InterfaceFieldsDatabase.ifDescr.value}, {InterfaceFieldsDatabase.ifAlias.value}, {InterfaceFieldsDatabase.ifSpeed.value}, {InterfaceFieldsDatabase.ifHighSpeed.value}, {InterfaceFieldsDatabase.ifPhysAddress}, {InterfaceFieldsDatabase.ifType.value}, {InterfaceFieldsDatabase.ifOperStatus.value}, {InterfaceFieldsDatabase.ifAdminStatus.value}, {InterfaceFieldsDatabase.ifPromiscuousMode.value}, {InterfaceFieldsDatabase.ifConnectorPresent.value}, {InterfaceFieldsDatabase.ifLastCheck.value}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
                f"INSERT INTO {NameTablesDatabase.interface.value} ({InterfaceFieldsDatabase.ifIndex.value}, {InterfaceFieldsDatabase.idEquipment.value}, {InterfaceFieldsDatabase.dateConsult.value}, {InterfaceFieldsDatabase.dateType.value}, {InterfaceFieldsDatabase.ifName.value}, {InterfaceFieldsDatabase.ifDescr.value}, {InterfaceFieldsDatabase.ifAlias.value}, {InterfaceFieldsDatabase.ifSpeed.value}, {InterfaceFieldsDatabase.ifHighSpeed.value}, {InterfaceFieldsDatabase.ifPhysAddress}, {InterfaceFieldsDatabase.ifType.value}, {InterfaceFieldsDatabase.ifOperStatus.value}, {InterfaceFieldsDatabase.ifAdminStatus.value}, {InterfaceFieldsDatabase.ifPromiscuousMode.value}, {InterfaceFieldsDatabase.ifConnectorPresent.value}, {InterfaceFieldsDatabase.ifLastCheck.value}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
            if res == "INSERT 0 1":
                total_inserted += 1
        conn.commit()
        database.close_connection()
        return total_inserted

    @staticmethod
    def delete_interface(id_equipment: int, if_index: int) -> bool:
        """Delete an interface by performing a database query.

        Parameters
        ----------
        id_equipment : int
            The id of the equipment.
        if_index : int
            The index of the interface.
        """
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            f"DELETE FROM {NameTablesDatabase.interface.value} WHERE {InterfaceFieldsDatabase.idEquipment.value} = %s AND {InterfaceFieldsDatabase.ifIndex.value} = %s",
            (id_equipment, if_index),
        )
        res = cur.statusmessage
        if res == "DELETE 1":
            conn.commit()
            database.close_connection()
            return True
        else:
            database.close_connection()
            return False

    @staticmethod
    def delete_interfaces(data: List[tuple]) -> int:
        """Delete a list of interfaces by performing a database query.

        Parameters
        ----------
        data: List[dict]
            List of dicts with the values of the interfaces to be deleted.
        """
        total_deleted = 0
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        for interface in data:
            cur.execute(
                f"DELETE FROM {NameTablesDatabase.interface.value} WHERE {InterfaceFieldsDatabase.idEquipment.value} = %s AND {InterfaceFieldsDatabase.ifIndex.value} = %s",
                (interface[0], interface[1]),
            )
            res = cur.statusmessage
            if res == "DELETE 1":
                total_deleted += 1
        conn.commit()
        database.close_connection()
        return total_deleted

    def delete_interfaces_by_date(data: List[int]) -> int:
        """Delete a list of interfaces by performing a database query.

        Parameters
        ----------
        data: List[dict]
            List of ids of the interfaces to be deleted.
        """
        total_deleted = 0
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        for id in data:
            cur.execute(f"DELETE FROM {NameTablesDatabase.interface.value} WHERE {InterfaceFieldsDatabase.id.value} = %s", (id,))
            res = cur.statusmessage
            if res == "DELETE 1":
                total_deleted += 1
        conn.commit()
        database.close_connection()
        return total_deleted

    def delete_interfaces_by_date_consult(date_consult: str) -> int:
        """Delete a list of interfaces by performing a database query.

        Parameters
        ----------
        date_consult : str
            The date of the consult in format YYYY-MM-DD.
        """
        status = False
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(f"DELETE FROM {NameTablesDatabase.interface.value} WHERE {InterfaceFieldsDatabase.dateConsult.value} = %s", (date_consult,))
        res = cur.statusmessage
        if "DELETE" in res:
            status = True
        conn.commit()
        database.close_connection()
        return status

    def update_interface(data: dict) -> InterfaceEntity | None:
        """Update an interface by performing a database query.

        Parameters
        ----------
        data: dict
            Dict with the values of the interface to be updated.
        """
        new_interface = InterfaceEntity(**data)
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            f"UPDATE {NameTablesDatabase.interface.value} SET {InterfaceFieldsDatabase.dateConsult.value} = %s, {InterfaceFieldsDatabase.dateType.value} = %s, {InterfaceFieldsDatabase.ifName.value} = %s, {InterfaceFieldsDatabase.ifDescr.value} = %s, {InterfaceFieldsDatabase.ifAlias.value} = %s, {InterfaceFieldsDatabase.ifSpeed.value} = %s, {InterfaceFieldsDatabase.ifHighSpeed.value} = %s, {InterfaceFieldsDatabase.ifPhysAddress.value} = %s, {InterfaceFieldsDatabase.ifType.value} = %s, {InterfaceFieldsDatabase.ifOperStatus.value} = %s, {InterfaceFieldsDatabase.ifAdminStatus.value} = %s, {InterfaceFieldsDatabase.ifPromiscuousMode.value} = %s, {InterfaceFieldsDatabase.ifConnectorPresent.value} = %s, {InterfaceFieldsDatabase.ifLastCheck.value} = %s WHERE {InterfaceFieldsDatabase.ifIndex.value} = %s AND {InterfaceFieldsDatabase.idEquipment.value} = %s",
            (
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
                new_interface.ifIndex,
                new_interface.idEquipment,
            ),
        )
        conn.commit()
        database.close_connection()
        return InterfaceModel.get_interfaces_by_index(
            new_interface.idEquipment, new_interface.ifIndex
        )
    
    def update_interfaces(data: List[dict]) -> int:
        """Update a list of interfaces by performing a database query.

        Parameters
        ----------
        data: List[dict]
            List of dicts with the values of the interfaces to be updated.
        """
        total_updated = 0
        data = [InterfaceEntity(**interface) for interface in data]
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        for interface in data:
            cur.execute(
                f"UPDATE {NameTablesDatabase.interface.value} SET {InterfaceFieldsDatabase.dateConsult.value} = %s, {InterfaceFieldsDatabase.dateType.value} = %s, {InterfaceFieldsDatabase.ifName.value} = %s, {InterfaceFieldsDatabase.ifDescr.value} = %s, {InterfaceFieldsDatabase.ifAlias.value} = %s, {InterfaceFieldsDatabase.ifSpeed.value} = %s, {InterfaceFieldsDatabase.ifHighSpeed.value} = %s, {InterfaceFieldsDatabase.ifPhysAddress.value} = %s, {InterfaceFieldsDatabase.ifType.value} = %s, {InterfaceFieldsDatabase.ifOperStatus.value} = %s, {InterfaceFieldsDatabase.ifAdminStatus.value} = %s, {InterfaceFieldsDatabase.ifPromiscuousMode.value} = %s, {InterfaceFieldsDatabase.ifConnectorPresent.value} = %s, {InterfaceFieldsDatabase.ifLastCheck.value} = %s WHERE {InterfaceFieldsDatabase.ifIndex.value} = %s AND {InterfaceFieldsDatabase.idEquipment.value} = %s",
                (
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
                    interface.ifIndex,
                    interface.idEquipment,
                ),
            )
            res = cur.statusmessage
            if res == "UPDATE 1":
                total_updated += 1
        conn.commit()
        database.close_connection()
        return total_updated
