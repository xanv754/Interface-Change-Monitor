from typing import List
from database.entities.interface import InterfaceEntity, InterfaceField
from database.constants.tables import TableDatabase
from database.constants.types.interface import Date
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
        cur.execute(f"SELECT * FROM {TableDatabase.interface.value} WHERE {InterfaceField.id.value} = %s", (id,))
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
        cur.execute(f"SELECT * FROM {TableDatabase.interface.value}")
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
        cur.execute(f"SELECT * FROM {TableDatabase.interface.value} WHERE {InterfaceField.idEquipment.value} = %s", (id_equipment,))
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
            f"SELECT * FROM {TableDatabase.interface.value} WHERE {InterfaceField.idEquipment.value} = %s AND {InterfaceField.ifIndex.value} = %s",
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
        cur.execute(f"SELECT * FROM {TableDatabase.interface.value} WHERE {InterfaceField.dateConsult.value} = %s", (date_consult,))
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
            f"SELECT * FROM {TableDatabase.interface.value} WHERE {InterfaceField.dateType.value} = %s", (Date.TODAY.value,)
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
            f"SELECT * FROM {TableDatabase.interface.value} WHERE {InterfaceField.dateType.value} = %s", (Date.YESTERDAY.value,)
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
            f"SELECT * FROM {TableDatabase.interface.value} WHERE {InterfaceField.dateType.value} = %s", (Date.OLD.value,)
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
            f"INSERT INTO {TableDatabase.interface.value} ({InterfaceField.ifIndex.value}, {InterfaceField.idEquipment.value}, {InterfaceField.dateConsult.value}, {InterfaceField.dateType.value}, {InterfaceField.ifName.value}, {InterfaceField.ifDescr.value}, {InterfaceField.ifAlias.value}, {InterfaceField.ifSpeed.value}, {InterfaceField.ifHighSpeed.value}, {InterfaceField.ifPhysAddress}, {InterfaceField.ifType.value}, {InterfaceField.ifOperStatus.value}, {InterfaceField.ifAdminStatus.value}, {InterfaceField.ifPromiscuousMode.value}, {InterfaceField.ifConnectorPresent.value}, {InterfaceField.ifLastCheck.value}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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

    # def insert_interfaces(data: List[dict]) -> int:
    #     """Create a list of interfaces by performing a database query.

    #     Parameters
    #     ----------
    #     data: List[dict]
    #         List of dicts with the values of the interfaces to be created.
    #     """
    #     total_inserted = 0
    #     data = [InterfaceEntity(**interface) for interface in data]
    #     database = Database()
    #     conn = database.get_connection()
    #     cur = database.get_cursor()
    #     for interface in data:
    #         cur.execute(
    #             f"INSERT INTO {NameTablesDatabase.interface.value} ({InterfaceField.ifIndex.value}, {InterfaceField.idEquipment.value}, {InterfaceField.dateConsult.value}, {InterfaceField.dateType.value}, {InterfaceField.ifName.value}, {InterfaceField.ifDescr.value}, {InterfaceField.ifAlias.value}, {InterfaceField.ifSpeed.value}, {InterfaceField.ifHighSpeed.value}, {InterfaceField.ifPhysAddress}, {InterfaceField.ifType.value}, {InterfaceField.ifOperStatus.value}, {InterfaceField.ifAdminStatus.value}, {InterfaceField.ifPromiscuousMode.value}, {InterfaceField.ifConnectorPresent.value}, {InterfaceField.ifLastCheck.value}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    #             (
    #                 interface.ifIndex,
    #                 interface.idEquipment,
    #                 interface.dateConsult,
    #                 interface.dateType.value,
    #                 interface.ifName,
    #                 interface.ifDescr,
    #                 interface.ifAlias,
    #                 interface.ifSpeed,
    #                 interface.ifHighSpeed,
    #                 interface.ifPhysAddress,
    #                 interface.ifType,
    #                 interface.ifOperStatus.value,
    #                 interface.ifAdminStatus.value,
    #                 interface.ifPromiscuousMode,
    #                 interface.ifConnectorPresent,
    #                 interface.ifLastCheck,
    #             ),
    #         )
    #         res = cur.statusmessage
    #         if res == "INSERT 0 1":
    #             total_inserted += 1
    #     conn.commit()
    #     database.close_connection()
    #     return total_inserted

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
            f"DELETE FROM {TableDatabase.interface.value} WHERE {InterfaceField.idEquipment.value} = %s AND {InterfaceField.ifIndex.value} = %s",
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
    def delete_interfaces_by_equipment(data: List[tuple]) -> int:
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
                f"DELETE FROM {TableDatabase.interface.value} WHERE {InterfaceField.idEquipment.value} = %s AND {InterfaceField.ifIndex.value} = %s",
                (interface[0], interface[1]),
            )
            res = cur.statusmessage
            if res == "DELETE 1":
                total_deleted += 1
        conn.commit()
        database.close_connection()
        return total_deleted

    def delete_interfaces_by_id(data: List[int]) -> int:
        """Delete all interfaces by performing a database query.

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
            cur.execute(f"DELETE FROM {TableDatabase.interface.value} WHERE {InterfaceField.id.value} = %s", (id,))
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
        cur.execute(f"DELETE FROM {TableDatabase.interface.value} WHERE {InterfaceField.dateConsult.value} = %s", (date_consult,))
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
        id: int
            The id of the interface to be updated.
        data: dict
            Dict with the values of the interface to be updated.
        """
        new_interface = InterfaceEntity(**data)
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            f"UPDATE {TableDatabase.interface.value} SET {InterfaceField.dateConsult.value} = %s, {InterfaceField.dateType.value} = %s, {InterfaceField.ifName.value} = %s, {InterfaceField.ifDescr.value} = %s, {InterfaceField.ifAlias.value} = %s, {InterfaceField.ifSpeed.value} = %s, {InterfaceField.ifHighSpeed.value} = %s, {InterfaceField.ifPhysAddress.value} = %s, {InterfaceField.ifType.value} = %s, {InterfaceField.ifOperStatus.value} = %s, {InterfaceField.ifAdminStatus.value} = %s, {InterfaceField.ifPromiscuousMode.value} = %s, {InterfaceField.ifConnectorPresent.value} = %s, {InterfaceField.ifLastCheck.value} = %s WHERE {InterfaceField.id.value} = %s",
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
                id,
            ),
        )
        conn.commit()
        database.close_connection()
        return InterfaceModel.get_interfaces_by_index(
            new_interface.idEquipment, new_interface.ifIndex
        )
    
    # def update_interfaces(data: List[dict]) -> int:
    #     """Update a list of interfaces by performing a database query.

    #     Parameters
    #     ----------
    #     data: List[dict]
    #         List of dicts with the values of the interfaces to be updated.
    #     """
    #     total_updated = 0
    #     data = [InterfaceEntity(**interface) for interface in data]
    #     database = Database()
    #     conn = database.get_connection()
    #     cur = database.get_cursor()
    #     for interface in data:
    #         cur.execute(
    #             f"UPDATE {NameTablesDatabase.interface.value} SET {InterfaceField.dateConsult.value} = %s, {InterfaceField.dateType.value} = %s, {InterfaceField.ifName.value} = %s, {InterfaceField.ifDescr.value} = %s, {InterfaceField.ifAlias.value} = %s, {InterfaceField.ifSpeed.value} = %s, {InterfaceField.ifHighSpeed.value} = %s, {InterfaceField.ifPhysAddress.value} = %s, {InterfaceField.ifType.value} = %s, {InterfaceField.ifOperStatus.value} = %s, {InterfaceField.ifAdminStatus.value} = %s, {InterfaceField.ifPromiscuousMode.value} = %s, {InterfaceField.ifConnectorPresent.value} = %s, {InterfaceField.ifLastCheck.value} = %s WHERE {InterfaceField.ifIndex.value} = %s AND {InterfaceField.idEquipment.value} = %s",
    #             (
    #                 interface.dateConsult,
    #                 interface.dateType.value,
    #                 interface.ifName,
    #                 interface.ifDescr,
    #                 interface.ifAlias,
    #                 interface.ifSpeed,
    #                 interface.ifHighSpeed,
    #                 interface.ifPhysAddress,
    #                 interface.ifType,
    #                 interface.ifOperStatus.value,
    #                 interface.ifAdminStatus.value,
    #                 interface.ifPromiscuousMode,
    #                 interface.ifConnectorPresent,
    #                 interface.ifLastCheck,
    #                 interface.ifIndex,
    #                 interface.idEquipment,
    #             ),
    #         )
    #         res = cur.statusmessage
    #         if res == "UPDATE 1":
    #             total_updated += 1
    #     conn.commit()
    #     database.close_connection()
    #     return total_updated

    def update_type_date_to_yesterday() -> bool:
        """Update the type of the date of TODAY to YESTERDAY."""
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            f"UPDATE {TableDatabase.interface.value} SET {InterfaceField.dateType.value} = %s WHERE {InterfaceField.dateType.value} = %s",
            (Date.YESTERDAY.value, Date.TODAY.value),
        )
        res = cur.statusmessage
        if res == "UPDATE 1":
            conn.commit()
            database.close_connection()
            return True
        else:
            database.close_connection()
            return False
        
    def update_type_date_to_old() -> bool:
        """Update the type of the date of YESTERDAY to OLD."""
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            f"UPDATE {TableDatabase.interface.value} SET {InterfaceField.dateType.value} = %s WHERE {InterfaceField.dateType.value} = %s",
            (Date.OLD.value, Date.YESTERDAY.value),
        )
        res = cur.statusmessage
        if res == "UPDATE 1":
            conn.commit()
            database.close_connection()
            return True
        else:
            database.close_connection()
            return False