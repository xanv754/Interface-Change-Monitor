from io import StringIO
from pandas import DataFrame
from icm.data import TableNames
from icm.utils import log
from icm.access.querys.query import Query
from icm.access.utils.adapter import AdapterInterface
from icm.constants.fields import InterfaceField


class InterfaceQuery(Query):
    """Class to manage interface query."""

    def __init__(self, uri: str | None = None):
        super().__init__(uri=uri)


    def insert(self, data: StringIO) -> bool:
        """Insert interfaces in database.
        
        Parameters
        ----------
        data : StringIO
            Data to insert.

        Returns
        -------
        bool
            True if the data was inserted successfully, False otherwise.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.copy_from(
                file=data, 
                table=TableNames.INTERFACES,
                sep=";",
                columns=(
                    InterfaceField.IP.lower(),
                    InterfaceField.COMMUNITY.lower(),
                    InterfaceField.SYSNAME.lower(),
                    InterfaceField.IFINDEX.lower(),
                    InterfaceField.IFNAME.lower(),
                    InterfaceField.IFDESCR.lower(),
                    InterfaceField.IFALIAS.lower(),
                    InterfaceField.IFHIGHSPEED.lower(),
                    InterfaceField.IFOPERSTATUS.lower(),
                    InterfaceField.IFADMINSTATUS.lower(),
                    InterfaceField.CONSULTED_AT.lower()
                )
            )
            self.database.get_connection().commit()
            self.database.close_connection()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Interface query error. Failed to insert interfaces. {error}")
            return False
        else:
            return True
        
    def delete_by_date_consult(self, date: str) -> bool:
        """Delete interfaces by date.
        
        Parameters
        ----------
        date : str
            Date to delete interfaces.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    DELETE FROM {TableNames.INTERFACES}
                    WHERE {InterfaceField.CONSULTED_AT} = %s
                """,
                (date,)
            )
            self.database.get_connection().commit()
            self.database.close_connection()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Interface query error. Failed to delete interfaces by date. {error}")
            return False
        else:
            return True
        
    def get_by_date_consult(self, date: str) -> DataFrame:
        """Get interfaces by date.
        
        Parameters
        ----------
        date : str
            Date to get interfaces.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        *
                    FROM
                        {TableNames.INTERFACES}
                    WHERE
                        {InterfaceField.CONSULTED_AT} = %s
                """,
                (date,)
            )
            response = cursor.fetchall()
            self.database.close_connection()
            return AdapterInterface.response(response)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Interface query error. Failed to get interfaces by date. {error}")
            return []