from enum import Enum

class EquipmentFieldsDatabase(Enum):
    id = "id"
    ip = "ip"
    community = "community"
    sysname = "sysname"
    createdAt = "createdAt"
    updatedAt = "updatedAt"

class InterfaceFieldsDatabase(Enum):
    id = "id" 
    ifIndex = "ifIndex" 
    idEquipment = "idEquipment" 
    dateConsult = "dateConsult"
    dateType = "dateType" 
    ifName = "ifName"
    ifDescr = "ifDescr"
    ifAlias = "ifAlias"
    ifSpeed = "ifSpeed" 
    ifHighSpeed = "ifHighSpeed" 
    ifPhysAddress = "ifPhysAddress"
    ifType = "ifType"
    ifOperStatus = "ifOperStatus" 
    ifAdminStatus = "ifAdminStatus" 
    ifPromiscuousMode = "ifPromiscuousMode"
    ifConnectorPresent = "ifConnectorPresent"
    ifLastCheck = "ifLastCheck"

class AssignmentFieldsDatabase(Enum):
    changeInterface = "changeInterface"
    oldInterface = "oldInterface"
    operator = "operator"
    dateAssignment = "dateAssignment"
    statusAssignment = "statusAssignment"
    assignedBy = "assignedBy"
    dateReview = "dateReview"

class OperatorFieldsDatabase(Enum):
    username = "username"
    name = "name"
    lastname = "lastname"
    password = "password"
    profile = "profile"
    statusAccount = "statusAccount"
    deleteOperator = "deleteOperator"