import pandas as pd
from io import StringIO
from typing import List
from database.constants.database import TableNames
from database.querys.query import Query
from database.utils.adapter import AdapterChange
from models.user import UserField
from models.change import ChangeField, ChangeCompleteField
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
                    ChangeField.ID_OLD.lower(),
                    ChangeField.IP_OLD.lower(),
                    ChangeField.COMMUNITY_OLD.lower(),
                    ChangeField.SYSNAME_OLD.lower(),
                    ChangeField.IFINDEX_OLD.lower(),
                    ChangeField.IFNAME_OLD.lower(),
                    ChangeField.IFDESCR_OLD.lower(),
                    ChangeField.IFALIAS_OLD.lower(),
                    ChangeField.IFHIGHSPEED_OLD.lower(),
                    ChangeField.IFOPERSTATUS_OLD.lower(),
                    ChangeField.IFADMINSTATUS_OLD.lower(),
                    ChangeField.ID_NEW.lower(),
                    ChangeField.IP_NEW.lower(),
                    ChangeField.COMMUNITY_NEW.lower(),
                    ChangeField.SYSNAME_NEW.lower(),
                    ChangeField.IFINDEX_NEW.lower(),
                    ChangeField.IFNAME_NEW.lower(),
                    ChangeField.IFDESCR_NEW.lower(),
                    ChangeField.IFALIAS_NEW.lower(),
                    ChangeField.IFHIGHSPEED_NEW.lower(),
                    ChangeField.IFOPERSTATUS_NEW.lower(),
                    ChangeField.IFADMINSTATUS_NEW.lower(),
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
                        c.{ChangeField.ID_OLD},
                        c.{ChangeField.IP_OLD},
                        c.{ChangeField.COMMUNITY_OLD},
                        c.{ChangeField.SYSNAME_OLD},
                        c.{ChangeField.IFINDEX_OLD},
                        c.{ChangeField.IFNAME_OLD},
                        c.{ChangeField.IFDESCR_OLD},
                        c.{ChangeField.IFALIAS_OLD},
                        c.{ChangeField.IFHIGHSPEED_OLD},
                        c.{ChangeField.IFOPERSTATUS_OLD},
                        c.{ChangeField.IFADMINSTATUS_OLD},
                        c.{ChangeField.ID_NEW},
                        c.{ChangeField.IP_NEW},
                        c.{ChangeField.COMMUNITY_NEW},
                        c.{ChangeField.SYSNAME_NEW},
                        c.{ChangeField.IFINDEX_NEW},
                        c.{ChangeField.IFNAME_NEW},
                        c.{ChangeField.IFDESCR_NEW},
                        c.{ChangeField.IFALIAS_NEW},
                        c.{ChangeField.IFHIGHSPEED_NEW},
                        c.{ChangeField.IFOPERSTATUS_NEW},
                        c.{ChangeField.IFADMINSTATUS_NEW},
                        u.{UserField.USERNAME} as {ChangeCompleteField.USERNAME},
                        u.{UserField.NAME} as {ChangeCompleteField.NAME},
                        u.{UserField.LASTNAME} as {ChangeCompleteField.LASTNAME}
                    FROM 
                        {TableNames.CHANGES} c
                    JOIN
                        {TableNames.USERS} u ON u.{UserField.USERNAME} = c.{ChangeField.ASSIGNED}
                """
            )
            response = cursor.fetchall()
            self.database.close_connection()
            return AdapterChange.response(response)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Change query error. Failed to get all changes. {error}")
            return pd.DataFrame()