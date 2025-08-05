import pandas as pd
from datetime import datetime
from io import StringIO
from typing import List
from icm.constants import InterfaceField, UserField, AssignmentField, AssignmentCompleteField, StatisticsField, AssignmentStatusTypes
from icm.data import TableNames
from icm.utils import log
from icm.access.models.assignment import ReassignmentModel, UpdateAssignmentModel, StatisticsModel
from icm.access.querys.query import Query
from icm.access.utils.adapter import AdapterAssignment


class AssignmentQuery(Query):
    """Class to manage assignment query."""

    def __init__(self, uri: str | None = None):
        super().__init__(uri=uri)

    def insert(self, data: StringIO) -> bool:
        """Insert assignment in database.
        
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
                table=TableNames.ASSIGNMENTS,
                sep=";",
                columns=(
                    AssignmentField.OLD_INTERFACE_ID.lower(),
                    AssignmentField.CURRENT_INTERFACE_ID.lower(),
                    AssignmentField.USERNAME.lower(),
                    AssignmentField.ASSIGN_BY.lower(),
                    AssignmentField.TYPE_STATUS.lower()
                )
            )
            self.database.get_connection().commit()
            self.database.close_connection()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment query error. Failed to insert assignment. {error}")
            return False
        else:
            return True
        
    def reassing(self, data: List[ReassignmentModel]) -> bool:
        """Reassing assignment in database.
        
        Parameters
        ----------
        data : List[ReassignmentModel]
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
            for assignment in data:
                cursor.execute(
                    f"""
                        UPDATE 
                            {TableNames.ASSIGNMENTS}
                        SET 
                            {AssignmentField.USERNAME} = %s,
                            {AssignmentField.ASSIGN_BY} = %s,
                            {AssignmentField.TYPE_STATUS} = %s,
                            {AssignmentField.CREATED_AT} = CURRENT_DATE,
                            {AssignmentField.UPDATED_AT} = NULL
                        WHERE 
                            {AssignmentField.OLD_INTERFACE_ID} = %s AND
                            {AssignmentField.CURRENT_INTERFACE_ID} = %s AND
                            {AssignmentField.USERNAME} = %s
                    """,
                    (
                        assignment.new_username,
                        assignment.assign_by.lower(),
                        AssignmentStatusTypes.PENDING,
                        assignment.old_interface_id,
                        assignment.current_interface_id,
                        assignment.old_username
                    )
                )
                self.database.get_connection().commit()
            self.database.close_connection()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment query error. Failed to insert assignment. {error}")
            return False
        else:
            return True
        
    def update_status(self, data: List[UpdateAssignmentModel]) -> bool:
        """Update assignments in database.
        
        Parameters
        ----------
        data : List[UpdateAssignmentModel]
            Data to update.

        Returns
        -------
        bool
            True if the data was updated successfully, False otherwise.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            for assignment in data:
                cursor.execute(
                    f"""
                        UPDATE 
                            {TableNames.ASSIGNMENTS}
                        SET 
                            {AssignmentField.TYPE_STATUS} = %s,
                            {AssignmentField.UPDATED_AT} = CURRENT_DATE
                        WHERE 
                            {AssignmentField.OLD_INTERFACE_ID} = %s AND
                            {AssignmentField.CURRENT_INTERFACE_ID} = %s AND
                            {AssignmentField.USERNAME} = %s
                    """,
                    (
                        assignment.type_status,
                        assignment.old_interface_id,
                        assignment.current_interface_id,
                        assignment.username
                    )
                )
                self.database.get_connection().commit()
            self.database.close_connection()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment query error. Failed to update assignment. {error}")
            return False
        else:
            return True
        
    def get_all_by_status(self, status: str) -> pd.DataFrame:
        """Get all assignments by status.
        
        Parameters
        ----------
        status : str
            Status to get assignments.

        Returns
        -------
        DataFrame
            DataFrame with all assignments.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        old.{InterfaceField.ID} as {AssignmentCompleteField.ID_OLD},
                        old.{InterfaceField.IP} as {AssignmentCompleteField.IP_OLD},
                        old.{InterfaceField.COMMUNITY} as {AssignmentCompleteField.COMMUNITY_OLD},
                        old.{InterfaceField.SYSNAME} as {AssignmentCompleteField.SYSNAME_OLD},
                        old.{InterfaceField.IFINDEX} as {AssignmentCompleteField.IFINDEX_OLD},
                        old.{InterfaceField.IFNAME} as {AssignmentCompleteField.IFNAME_OLD},
                        old.{InterfaceField.IFDESCR} as {AssignmentCompleteField.IFDESCR_OLD},
                        old.{InterfaceField.IFALIAS} as {AssignmentCompleteField.IFALIAS_OLD},
                        old.{InterfaceField.IFHIGHSPEED} as {AssignmentCompleteField.IFHIGHSPEED_OLD},
                        old.{InterfaceField.IFOPERSTATUS} as {AssignmentCompleteField.IFOPERSTATUS_OLD},
                        old.{InterfaceField.IFADMINSTATUS} as {AssignmentCompleteField.IFADMINSTATUS_OLD},
                        new.{InterfaceField.ID} as {AssignmentCompleteField.ID_NEW},
                        new.{InterfaceField.IP} as {AssignmentCompleteField.IP_NEW},
                        new.{InterfaceField.COMMUNITY} as {AssignmentCompleteField.COMMUNITY_NEW},
                        new.{InterfaceField.SYSNAME} as {AssignmentCompleteField.SYSNAME_NEW},
                        new.{InterfaceField.IFINDEX} as {AssignmentCompleteField.IFINDEX_NEW},
                        new.{InterfaceField.IFNAME} as {AssignmentCompleteField.IFNAME_NEW},
                        new.{InterfaceField.IFDESCR} as {AssignmentCompleteField.IFDESCR_NEW},
                        new.{InterfaceField.IFALIAS} as {AssignmentCompleteField.IFALIAS_NEW},
                        new.{InterfaceField.IFHIGHSPEED} as {AssignmentCompleteField.IFHIGHSPEED_NEW},
                        new.{InterfaceField.IFOPERSTATUS} as {AssignmentCompleteField.IFOPERSTATUS_NEW},
                        new.{InterfaceField.IFADMINSTATUS} as {AssignmentCompleteField.IFADMINSTATUS_NEW},
                        u.{UserField.USERNAME} as {AssignmentCompleteField.USERNAME},
                        u.{UserField.NAME} as {AssignmentCompleteField.NAME},
                        u.{UserField.LASTNAME} as {AssignmentCompleteField.LASTNAME},
                        a.{AssignmentField.ASSIGN_BY} as {AssignmentCompleteField.ASSIGN_BY},
                        a.{AssignmentField.TYPE_STATUS} as {AssignmentCompleteField.TYPE_STATUS},
                        a.{AssignmentField.CREATED_AT} as {AssignmentCompleteField.CREATED_AT},
                        a.{AssignmentField.UPDATED_AT} as {AssignmentCompleteField.UPDATED_AT}
                    FROM
                        {TableNames.ASSIGNMENTS} a
                    JOIN 
                        {TableNames.INTERFACES} old ON old.{InterfaceField.ID} = a.{AssignmentField.OLD_INTERFACE_ID}
                    JOIN 
                        {TableNames.INTERFACES} new ON new.{InterfaceField.ID} = a.{AssignmentField.CURRENT_INTERFACE_ID}
                    JOIN
                        {TableNames.USERS} u ON u.{UserField.USERNAME} = a.{AssignmentField.USERNAME}
                    WHERE
                        {AssignmentField.TYPE_STATUS} = %s
                """,
                (status,)
            )
            response = cursor.fetchall()
            self.database.close_connection()
            return AdapterAssignment.response(response)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment query error. Failed to get assignments by status. {error}")
            return pd.DataFrame()
        
    def assigned_by_status(self, username: str, status: str) -> pd.DataFrame:
        """Get all assignments of a user by status.
        
        Parameters
        ----------
        username : str
            Username to get assignments.
        status : str
            Status to get assignments.

        Returns
        -------
        pd.DataFrame
            DataFrame with all assignments.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        old.{InterfaceField.ID} as {AssignmentCompleteField.ID_OLD},
                        old.{InterfaceField.IP} as {AssignmentCompleteField.IP_OLD},
                        old.{InterfaceField.COMMUNITY} as {AssignmentCompleteField.COMMUNITY_OLD},
                        old.{InterfaceField.SYSNAME} as {AssignmentCompleteField.SYSNAME_OLD},
                        old.{InterfaceField.IFINDEX} as {AssignmentCompleteField.IFINDEX_OLD},
                        old.{InterfaceField.IFNAME} as {AssignmentCompleteField.IFNAME_OLD},
                        old.{InterfaceField.IFDESCR} as {AssignmentCompleteField.IFDESCR_OLD},
                        old.{InterfaceField.IFALIAS} as {AssignmentCompleteField.IFALIAS_OLD},
                        old.{InterfaceField.IFHIGHSPEED} as {AssignmentCompleteField.IFHIGHSPEED_OLD},
                        old.{InterfaceField.IFOPERSTATUS} as {AssignmentCompleteField.IFOPERSTATUS_OLD},
                        old.{InterfaceField.IFADMINSTATUS} as {AssignmentCompleteField.IFADMINSTATUS_OLD},
                        new.{InterfaceField.ID} as {AssignmentCompleteField.ID_NEW},
                        new.{InterfaceField.IP} as {AssignmentCompleteField.IP_NEW},
                        new.{InterfaceField.COMMUNITY} as {AssignmentCompleteField.COMMUNITY_NEW},
                        new.{InterfaceField.SYSNAME} as {AssignmentCompleteField.SYSNAME_NEW},
                        new.{InterfaceField.IFINDEX} as {AssignmentCompleteField.IFINDEX_NEW},
                        new.{InterfaceField.IFNAME} as {AssignmentCompleteField.IFNAME_NEW},
                        new.{InterfaceField.IFDESCR} as {AssignmentCompleteField.IFDESCR_NEW},
                        new.{InterfaceField.IFALIAS} as {AssignmentCompleteField.IFALIAS_NEW},
                        new.{InterfaceField.IFHIGHSPEED} as {AssignmentCompleteField.IFHIGHSPEED_NEW},
                        new.{InterfaceField.IFOPERSTATUS} as {AssignmentCompleteField.IFOPERSTATUS_NEW},
                        new.{InterfaceField.IFADMINSTATUS} as {AssignmentCompleteField.IFADMINSTATUS_NEW},
                        u.{UserField.USERNAME} as {AssignmentCompleteField.USERNAME},
                        u.{UserField.NAME} as {AssignmentCompleteField.NAME},
                        u.{UserField.LASTNAME} as {AssignmentCompleteField.LASTNAME},
                        a.{AssignmentField.ASSIGN_BY} as {AssignmentCompleteField.ASSIGN_BY},
                        a.{AssignmentField.TYPE_STATUS} as {AssignmentCompleteField.TYPE_STATUS},
                        a.{AssignmentField.CREATED_AT} as {AssignmentCompleteField.CREATED_AT},
                        a.{AssignmentField.UPDATED_AT} as {AssignmentCompleteField.UPDATED_AT}
                    FROM
                        {TableNames.ASSIGNMENTS} a
                    JOIN 
                        {TableNames.INTERFACES} old ON old.{InterfaceField.ID} = a.{AssignmentField.OLD_INTERFACE_ID}
                    JOIN 
                        {TableNames.INTERFACES} new ON new.{InterfaceField.ID} = a.{AssignmentField.CURRENT_INTERFACE_ID}
                    JOIN
                        {TableNames.USERS} u ON u.{UserField.USERNAME} = a.{AssignmentField.USERNAME}
                    WHERE
                        {AssignmentField.USERNAME} = %s AND
                        {AssignmentField.TYPE_STATUS} = %s
                """,
                (username, status)
            )
            response = cursor.fetchall()
            self.database.close_connection()
            return AdapterAssignment.response(response)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment query error. Failed to get assignments by username and status. {error}")
            return pd.DataFrame()
        
    def completed_by_month(self, username: str, date: int) -> pd.DataFrame:
        """Get all assignments completed of a user by filter month.
        
        Parameters
        ----------
        username : str
            Username to get assignments.
        date : int
            Month to get assignments (YYYY-MM).

        Returns
        -------
        pd.DataFrame
            DataFrame with all assignments.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        old.{InterfaceField.ID} as {AssignmentCompleteField.ID_OLD},
                        old.{InterfaceField.IP} as {AssignmentCompleteField.IP_OLD},
                        old.{InterfaceField.COMMUNITY} as {AssignmentCompleteField.COMMUNITY_OLD},
                        old.{InterfaceField.SYSNAME} as {AssignmentCompleteField.SYSNAME_OLD},
                        old.{InterfaceField.IFINDEX} as {AssignmentCompleteField.IFINDEX_OLD},
                        old.{InterfaceField.IFNAME} as {AssignmentCompleteField.IFNAME_OLD},
                        old.{InterfaceField.IFDESCR} as {AssignmentCompleteField.IFDESCR_OLD},
                        old.{InterfaceField.IFALIAS} as {AssignmentCompleteField.IFALIAS_OLD},
                        old.{InterfaceField.IFHIGHSPEED} as {AssignmentCompleteField.IFHIGHSPEED_OLD},
                        old.{InterfaceField.IFOPERSTATUS} as {AssignmentCompleteField.IFOPERSTATUS_OLD},
                        old.{InterfaceField.IFADMINSTATUS} as {AssignmentCompleteField.IFADMINSTATUS_OLD},
                        new.{InterfaceField.ID} as {AssignmentCompleteField.ID_NEW},
                        new.{InterfaceField.IP} as {AssignmentCompleteField.IP_NEW},
                        new.{InterfaceField.COMMUNITY} as {AssignmentCompleteField.COMMUNITY_NEW},
                        new.{InterfaceField.SYSNAME} as {AssignmentCompleteField.SYSNAME_NEW},
                        new.{InterfaceField.IFINDEX} as {AssignmentCompleteField.IFINDEX_NEW},
                        new.{InterfaceField.IFNAME} as {AssignmentCompleteField.IFNAME_NEW},
                        new.{InterfaceField.IFDESCR} as {AssignmentCompleteField.IFDESCR_NEW},
                        new.{InterfaceField.IFALIAS} as {AssignmentCompleteField.IFALIAS_NEW},
                        new.{InterfaceField.IFHIGHSPEED} as {AssignmentCompleteField.IFHIGHSPEED_NEW},
                        new.{InterfaceField.IFOPERSTATUS} as {AssignmentCompleteField.IFOPERSTATUS_NEW},
                        new.{InterfaceField.IFADMINSTATUS} as {AssignmentCompleteField.IFADMINSTATUS_NEW},
                        u.{UserField.USERNAME} as {AssignmentCompleteField.USERNAME},
                        u.{UserField.NAME} as {AssignmentCompleteField.NAME},
                        u.{UserField.LASTNAME} as {AssignmentCompleteField.LASTNAME},
                        a.{AssignmentField.ASSIGN_BY} as {AssignmentCompleteField.ASSIGN_BY},
                        a.{AssignmentField.TYPE_STATUS} as {AssignmentCompleteField.TYPE_STATUS},
                        a.{AssignmentField.CREATED_AT} as {AssignmentCompleteField.CREATED_AT},
                        a.{AssignmentField.UPDATED_AT} as {AssignmentCompleteField.UPDATED_AT}
                    FROM
                        {TableNames.ASSIGNMENTS} a
                    JOIN 
                        {TableNames.INTERFACES} old ON old.{InterfaceField.ID} = a.{AssignmentField.OLD_INTERFACE_ID}
                    JOIN 
                        {TableNames.INTERFACES} new ON new.{InterfaceField.ID} = a.{AssignmentField.CURRENT_INTERFACE_ID}
                    JOIN
                        {TableNames.USERS} u ON u.{UserField.USERNAME} = a.{AssignmentField.USERNAME}
                    WHERE
                        {AssignmentField.USERNAME} = %s AND
                        {AssignmentField.TYPE_STATUS} != '{AssignmentStatusTypes.PENDING}' AND
                        TO_CHAR(a.{AssignmentField.CREATED_AT}, 'YYYY-MM') = %s
                """,
                (username, date)
            )
            response = cursor.fetchall()
            self.database.close_connection()
            return AdapterAssignment.response(response)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment query error. Failed to get assignments by username and month. {error}")
            return pd.DataFrame()
        
    def date_available_to_consult_history(self) -> List[str]:
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    SELECT DISTINCT 
                        TO_CHAR({AssignmentField.CREATED_AT}, 'YYYY-MM') AS unique_date
                    FROM 
                        {TableNames.ASSIGNMENTS}
                    ORDER BY 
                        unique_date DESC;
                """
            )
            response = cursor.fetchall()
            self.database.close_connection()
            return response[0]
        except Exception as error:
            return pd.DataFrame()
        
    def get_statistics(self, usernames: List[str]) -> List[StatisticsModel]:
        """Get statistics of assignments by a list of usernames.
        
        Parameters
        ----------
        usernames : List[str]
            Usernames to get statistics.

        Returns
        -------
        List[StatisticsModel]
            Statistics of assignments by username.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            responses = []
            for username in usernames:
                cursor.execute(
                    f"""
                        SELECT
                            COUNT(
                                CASE WHEN {AssignmentField.TYPE_STATUS} = '{AssignmentStatusTypes.PENDING}' AND
                                {AssignmentField.CREATED_AT} = '{datetime.now().strftime("%Y-%m-%d")}' THEN 1 END
                            ) AS {StatisticsField.TOTAL_PENDING_TODAY},
                            COUNT(
                                CASE WHEN {AssignmentField.TYPE_STATUS} = '{AssignmentStatusTypes.INSPECTED}' AND
                                {AssignmentField.CREATED_AT} = '{datetime.now().strftime("%Y-%m-%d")}' THEN 1 END
                            ) AS {StatisticsField.TOTAL_INSPECTED_TODAY},
                            COUNT(
                                CASE WHEN {AssignmentField.TYPE_STATUS} = '{AssignmentStatusTypes.REDISCOVERED}' AND
                                {AssignmentField.CREATED_AT} = '{datetime.now().strftime("%Y-%m-%d")}' THEN 1 END
                            ) AS {StatisticsField.TOTAL_REDISCOVERED_TODAY},
                            COUNT(
                                CASE WHEN {AssignmentField.TYPE_STATUS} = '{AssignmentStatusTypes.PENDING}' AND
                                EXTRACT(MONTH FROM a.{AssignmentField.CREATED_AT}) = EXTRACT(MONTH FROM CURRENT_DATE) THEN 1 END
                            ) AS {StatisticsField.TOTAL_PENDING_MONTH},
                            COUNT(
                                CASE WHEN {AssignmentField.TYPE_STATUS} = '{AssignmentStatusTypes.INSPECTED}' AND
                                EXTRACT(MONTH FROM a.{AssignmentField.CREATED_AT}) = EXTRACT(MONTH FROM CURRENT_DATE) THEN 1 END
                            ) AS {StatisticsField.TOTAL_INSPECTED_MONTH},
                            COUNT(
                                CASE WHEN {AssignmentField.TYPE_STATUS} = '{AssignmentStatusTypes.REDISCOVERED}' AND
                                EXTRACT(MONTH FROM a.{AssignmentField.CREATED_AT}) = EXTRACT(MONTH FROM CURRENT_DATE) THEN 1 END
                            ) AS {StatisticsField.TOTAL_REDISCOVERED_MONTH},
                            u.{UserField.USERNAME} AS {StatisticsField.USERNAME},
                            u.{UserField.NAME} AS {StatisticsField.NAME},
                            u.{UserField.LASTNAME} AS {StatisticsField.LASTNAME}
                        FROM
                            {TableNames.ASSIGNMENTS} a
                        JOIN
                            {TableNames.USERS} u ON u.{UserField.USERNAME} = a.{AssignmentField.USERNAME}
                        WHERE
                            a.{AssignmentField.USERNAME} = %s
                        GROUP BY
                            u.{UserField.USERNAME},
                            u.{UserField.NAME},
                            u.{UserField.LASTNAME}
                    """,
                    (username,)
                )
                response = cursor.fetchone()
                responses.append(response)
            self.database.close_connection()
            return AdapterAssignment.response_statistics(responses)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment query error. Failed to get statistics. {error}")
            return []
