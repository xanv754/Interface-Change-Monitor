import pandas as pd
from io import StringIO
from typing import List
from database.constants.database import TableNames
from database.querys.query import Query
from database.utils.adapter import AdapterChange
from models.interface import InterfaceField
from models.user import UserField
from models.change import ChangeField, ChangeCompleteModel, ChangeCompleteField
from utils.log import log


class ChangeQuery(Query):
    """Class to manage change query."""

    def __init__(self, uri: str | None = None):
        super().__init__(uri=uri)

    def insert(self, data: StringIO) -> bool:
        """Insert change in database.
        
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
                table=TableNames.CHANGES,
                sep=";",
                columns=(
                    ChangeField.CURRENT_INTERFACE_ID.lower(),
                    ChangeField.OLD_INTERFACE_ID.lower(),
                    ChangeField.ASSIGNED.lower()
                )
            )
            self.database.get_connection().commit()
            self.database.close_connection()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Change query error. Failed to insert changes. {error}")
            return False
        else:
            return True
        
    def get_all(self) -> pd.DataFrame:
        """Get all changes.
        
        Returns
        -------
        pd.DataFrame
            DataFrame with all changes.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        old.{InterfaceField.ID} as {ChangeCompleteField.ID_OLD},
                        old.{InterfaceField.IP} as {ChangeCompleteField.IP_OLD},
                        old.{InterfaceField.COMMUNITY} as {ChangeCompleteField.COMMUNITY_OLD},
                        old.{InterfaceField.SYSNAME} as {ChangeCompleteField.SYSNAME_OLD},
                        old.{InterfaceField.IFINDEX} as {ChangeCompleteField.IFINDEX_OLD},
                        old.{InterfaceField.IFNAME} as {ChangeCompleteField.IFNAME_OLD},
                        old.{InterfaceField.IFDESCR} as {ChangeCompleteField.IFDESCR_OLD},
                        old.{InterfaceField.IFALIAS} as {ChangeCompleteField.IFALIAS_OLD},
                        old.{InterfaceField.IFHIGHSPEED} as {ChangeCompleteField.IFHIGHSPEED_OLD},
                        old.{InterfaceField.IFOPERSTATUS} as {ChangeCompleteField.IFOPERSTATUS_OLD},
                        old.{InterfaceField.IFADMINSTATUS} as {ChangeCompleteField.IFADMINSTATUS_OLD},
                        new.{InterfaceField.ID} as {ChangeCompleteField.ID_NEW},
                        new.{InterfaceField.IP} as {ChangeCompleteField.IP_NEW},
                        new.{InterfaceField.COMMUNITY} as {ChangeCompleteField.COMMUNITY_NEW},
                        new.{InterfaceField.SYSNAME} as {ChangeCompleteField.SYSNAME_NEW},
                        new.{InterfaceField.IFINDEX} as {ChangeCompleteField.IFINDEX_NEW},
                        new.{InterfaceField.IFNAME} as {ChangeCompleteField.IFNAME_NEW},
                        new.{InterfaceField.IFDESCR} as {ChangeCompleteField.IFDESCR_NEW},
                        new.{InterfaceField.IFALIAS} as {ChangeCompleteField.IFALIAS_NEW},
                        new.{InterfaceField.IFHIGHSPEED} as {ChangeCompleteField.IFHIGHSPEED_NEW},
                        new.{InterfaceField.IFOPERSTATUS} as {ChangeCompleteField.IFOPERSTATUS_NEW},
                        new.{InterfaceField.IFADMINSTATUS} as {ChangeCompleteField.IFADMINSTATUS_NEW},
                        u.{UserField.USERNAME} as {ChangeCompleteField.USERNAME},
                        u.{UserField.NAME} as {ChangeCompleteField.NAME},
                        u.{UserField.LASTNAME} as {ChangeCompleteField.LASTNAME}
                    FROM 
                        {TableNames.CHANGES} change
                    JOIN 
                        {TableNames.INTERFACES} old ON old.{InterfaceField.ID} = change.{ChangeField.OLD_INTERFACE_ID}
                    JOIN 
                        {TableNames.INTERFACES} new ON new.{InterfaceField.ID} = change.{ChangeField.CURRENT_INTERFACE_ID}
                    JOIN
                        {TableNames.USERS} u ON u.{UserField.USERNAME} = change.{ChangeField.ASSIGNED}
                """
            )
            response = cursor.fetchall()
            self.database.close_connection()
            return AdapterChange.response(response)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Change query error. Failed to get all changes. {error}")
            return pd.DataFrame()