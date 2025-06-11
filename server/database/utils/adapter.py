import pandas as pd
from typing import List
from models.interface import InterfaceField
from models.user import UserModel
from models.change import ChangeField, ChangeCompleteField
from models.assignment import AssignmentCompleteField, StatisticsModel
from utils.log import log


class AdapterInterface:
    """Class to manage interface adapter."""

    @staticmethod
    def response(response_db: List[tuple]) -> pd.DataFrame:
        """Adapt response from database to model.
        
        Parameters
        ----------
        response_db : List[tuple]
            Response from database.

        Returns
        -------
        pd.DataFrame
            Response adapted.
        """
        header = [
            InterfaceField.IP,
            InterfaceField.COMMUNITY,
            InterfaceField.SYSNAME,
            InterfaceField.IFINDEX,
            InterfaceField.IFNAME,
            InterfaceField.IFDESCR,
            InterfaceField.IFALIAS,
            InterfaceField.IFHIGHSPEED,
            InterfaceField.IFOPERSTATUS,
            InterfaceField.IFADMINSTATUS,
            InterfaceField.CONSULTED_AT
        ]
        try:
            if not response_db: return pd.DataFrame(columns=header)            
            columns = list(zip(*response_db))
            response = pd.DataFrame({
                InterfaceField.ID: columns[0],
                InterfaceField.IP: columns[1],
                InterfaceField.COMMUNITY: columns[2],
                InterfaceField.SYSNAME: columns[3],
                InterfaceField.IFINDEX: columns[4],
                InterfaceField.IFNAME: columns[5],
                InterfaceField.IFDESCR: columns[6],
                InterfaceField.IFALIAS: columns[7],
                InterfaceField.IFHIGHSPEED: columns[8],
                InterfaceField.IFOPERSTATUS: columns[9],
                InterfaceField.IFADMINSTATUS: columns[10],
                InterfaceField.CONSULTED_AT: columns[11]
            })
            response[InterfaceField.ID] = response[InterfaceField.ID].astype(str)
            response[InterfaceField.IP] = response[InterfaceField.IP].astype(str)
            response[InterfaceField.CONSULTED_AT] = response[InterfaceField.CONSULTED_AT].astype(str)
            return response
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Interface adapter error. Failed to adapt response. {error}")
            return pd.DataFrame(columns=header)


class AdapterUser:
    """Class to manage user adapter."""

    @staticmethod
    def response(response_db: List[tuple]) -> List[UserModel]:
        """Adapt response from database to model.
        
        Parameters
        ----------
        response_db : List[tuple]
            Response from database.

        Returns
        -------
        UserModel
            Response adapted.
        """
        try:
            response = []
            for row in response_db:
                if row:
                    response.append(
                        UserModel(
                            username=row[0],
                            password=row[1],
                            name=row[2],
                            lastname=row[3],
                            status=row[4],
                            role=row[5],
                            created_at=row[6].strftime("%Y-%m-%d") if row[6] else None,
                            updated_at=row[7].strftime("%Y-%m-%d") if row[7] else None
                        )
                    )
            return response
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User adapter error. Failed to adapt response. {error}")
            return []
        

class AdapterChange:
    """Class to manage change adapter."""

    @staticmethod
    def response(response_db: List[tuple]) -> pd.DataFrame:
        """Adapt response from database to model.
        
        Parameters
        ----------
        response_db : List[tuple]
            Response from database.

        Returns
        -------
        pd.DataFrame
            Response adapted.
        """
        header = [
            ChangeField.ID_OLD, ChangeField.IP_OLD, ChangeField.COMMUNITY_OLD, ChangeField.SYSNAME_OLD,
            ChangeField.IFINDEX_OLD, ChangeField.IFNAME_OLD, ChangeField.IFDESCR_OLD, ChangeField.IFALIAS_OLD,
            ChangeField.IFHIGHSPEED_OLD, ChangeField.IFOPERSTATUS_OLD, ChangeField.IFADMINSTATUS_OLD,
            ChangeField.ID_NEW, ChangeField.IP_NEW, ChangeField.COMMUNITY_NEW, ChangeField.SYSNAME_NEW,
            ChangeField.IFINDEX_NEW, ChangeField.IFNAME_NEW, ChangeField.IFDESCR_NEW, ChangeField.IFALIAS_NEW,
            ChangeField.IFHIGHSPEED_NEW, ChangeField.IFOPERSTATUS_NEW, ChangeField.IFADMINSTATUS_NEW,
            ChangeCompleteField.USERNAME, ChangeCompleteField.NAME, ChangeCompleteField.LASTNAME
        ]
        try:
            if not response_db: return pd.DataFrame(columns=header)            
            columns = list(zip(*response_db))
            response = pd.DataFrame({
                ChangeField.ID_OLD: columns[0],
                ChangeField.IP_OLD: columns[1],
                ChangeField.COMMUNITY_OLD: columns[2],
                ChangeField.SYSNAME_OLD: columns[3],
                ChangeField.IFINDEX_OLD: columns[4],
                ChangeField.IFNAME_OLD: columns[5],
                ChangeField.IFDESCR_OLD: columns[6],
                ChangeField.IFALIAS_OLD: columns[7],
                ChangeField.IFHIGHSPEED_OLD: columns[8],
                ChangeField.IFOPERSTATUS_OLD: columns[9],
                ChangeField.IFADMINSTATUS_OLD: columns[10],
                ChangeField.ID_NEW: columns[11],
                ChangeField.IP_NEW: columns[12],
                ChangeField.COMMUNITY_NEW: columns[13],
                ChangeField.SYSNAME_NEW: columns[14],
                ChangeField.IFINDEX_NEW: columns[15],
                ChangeField.IFNAME_NEW: columns[16],
                ChangeField.IFDESCR_NEW: columns[17],
                ChangeField.IFALIAS_NEW: columns[18],
                ChangeField.IFHIGHSPEED_NEW: columns[19],
                ChangeField.IFOPERSTATUS_NEW: columns[20],
                ChangeField.IFADMINSTATUS_NEW: columns[21],
                ChangeCompleteField.USERNAME: columns[22] if columns[22] else None,
                ChangeCompleteField.NAME: columns[23] if columns[23] else None,
                ChangeCompleteField.LASTNAME: columns[24] if columns[24] else None
            })
            return response
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Change adapter error. Failed to adapt response. {error}")
            return pd.DataFrame(columns=header)
        

class AdapterAssignment:
    """Class to manage assignment adapter."""

    @staticmethod
    def response(response_db: List[tuple]) -> pd.DataFrame:
        """Adapt response from database to model.
        
        Parameters
        ----------
        response_db : List[tuple]
            Response from database.

        Returns
        -------
        pd.DataFrame
            Response adapted.
        """
        header = [
            AssignmentCompleteField.ID_OLD, AssignmentCompleteField.IP_OLD, AssignmentCompleteField.COMMUNITY_OLD, AssignmentCompleteField.SYSNAME_OLD,
            AssignmentCompleteField.IFINDEX_OLD, AssignmentCompleteField.IFNAME_OLD, AssignmentCompleteField.IFDESCR_OLD, AssignmentCompleteField.IFALIAS_OLD,
            AssignmentCompleteField.IFHIGHSPEED_OLD, AssignmentCompleteField.IFOPERSTATUS_OLD, AssignmentCompleteField.IFADMINSTATUS_OLD,
            AssignmentCompleteField.ID_NEW, AssignmentCompleteField.IP_NEW, AssignmentCompleteField.COMMUNITY_NEW, AssignmentCompleteField.SYSNAME_NEW,
            AssignmentCompleteField.IFINDEX_NEW, AssignmentCompleteField.IFNAME_NEW, AssignmentCompleteField.IFDESCR_NEW, AssignmentCompleteField.IFALIAS_NEW,
            AssignmentCompleteField.IFHIGHSPEED_NEW, AssignmentCompleteField.IFOPERSTATUS_NEW, AssignmentCompleteField.IFADMINSTATUS_NEW,
            AssignmentCompleteField.USERNAME, AssignmentCompleteField.NAME, AssignmentCompleteField.LASTNAME, AssignmentCompleteField.ASSIGN_BY,
            AssignmentCompleteField.TYPE_STATUS, AssignmentCompleteField.CREATED_AT, AssignmentCompleteField.UPDATED_AT
        ]
        try:
            if not response_db: return pd.DataFrame(columns=header)            
            columns = list(zip(*response_db))
            response = pd.DataFrame({
                AssignmentCompleteField.ID_OLD: columns[0],
                AssignmentCompleteField.IP_OLD: columns[1],
                AssignmentCompleteField.COMMUNITY_OLD: columns[2],
                AssignmentCompleteField.SYSNAME_OLD: columns[3],
                AssignmentCompleteField.IFINDEX_OLD: columns[4],
                AssignmentCompleteField.IFNAME_OLD: columns[5],
                AssignmentCompleteField.IFDESCR_OLD: columns[6],
                AssignmentCompleteField.IFALIAS_OLD: columns[7],
                AssignmentCompleteField.IFHIGHSPEED_OLD: columns[8],
                AssignmentCompleteField.IFOPERSTATUS_OLD: columns[9],
                AssignmentCompleteField.IFADMINSTATUS_OLD: columns[10],
                AssignmentCompleteField.ID_NEW: columns[11],
                AssignmentCompleteField.IP_NEW: columns[12],
                AssignmentCompleteField.COMMUNITY_NEW: columns[13],
                AssignmentCompleteField.SYSNAME_NEW: columns[14],
                AssignmentCompleteField.IFINDEX_NEW: columns[15],
                AssignmentCompleteField.IFNAME_NEW: columns[16],
                AssignmentCompleteField.IFDESCR_NEW: columns[17],
                AssignmentCompleteField.IFALIAS_NEW: columns[18],
                AssignmentCompleteField.IFHIGHSPEED_NEW: columns[19],
                AssignmentCompleteField.IFOPERSTATUS_NEW: columns[20],
                AssignmentCompleteField.IFADMINSTATUS_NEW: columns[21],
                AssignmentCompleteField.USERNAME: columns[22],
                AssignmentCompleteField.NAME: columns[23],
                AssignmentCompleteField.LASTNAME: columns[24],
                AssignmentCompleteField.ASSIGN_BY: columns[25],
                AssignmentCompleteField.TYPE_STATUS: columns[26],
                AssignmentCompleteField.CREATED_AT: columns[27],
                AssignmentCompleteField.UPDATED_AT: columns[28]
            })
            response[AssignmentCompleteField.ID_OLD] = response[AssignmentCompleteField.ID_OLD].astype(str)
            response[AssignmentCompleteField.IP_OLD] = response[AssignmentCompleteField.IP_OLD].astype(str)
            response[AssignmentCompleteField.ID_NEW] = response[AssignmentCompleteField.ID_NEW].astype(str)
            response[AssignmentCompleteField.IP_NEW] = response[AssignmentCompleteField.IP_NEW].astype(str)
            response[AssignmentCompleteField.CREATED_AT] = response[AssignmentCompleteField.CREATED_AT].astype(str)
            response[AssignmentCompleteField.UPDATED_AT] = response[AssignmentCompleteField.UPDATED_AT].astype(str)
            return response
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment adapter error. Failed to adapt response. {error}")
            return pd.DataFrame(columns=header)
        
    def response_statistics(response_db: List[tuple]) -> List[StatisticsModel]:
        """Adapt response from database to model.
        
        Parameters
        ----------
        response_db : List[tuple]
            Response from database.

        Returns
        -------
        List[StatisticsModel]
            Response adapted.
        """
        try:
            response: List[StatisticsModel] = []
            for row in response_db:
                if row:
                    response.append(
                        StatisticsModel(
                            total_pending_today=row[0],
                            total_inspected_today=row[1],
                            total_rediscovered_today=row[2],
                            total_pending_month=row[3],
                            total_inspected_month=row[4],
                            total_rediscovered_month=row[5],
                            username=row[6],
                            name=row[7],
                            lastname=row[8]
                        )
                    )
            return response
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment adapter error. Failed to adapt response. {error}")
            return []