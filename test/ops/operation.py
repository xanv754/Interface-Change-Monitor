import unittest 
import pandas as pd
from models.interface import InterfaceField
from utils.operation import OperationData


DATA1 = pd.DataFrame({
    InterfaceField.ID: [1, 2, 3, 4, 5],
    InterfaceField.IP: ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5"],
    InterfaceField.COMMUNITY: ["public1", "public2", "public3", "public4", "public5"],
    InterfaceField.SYSNAME: ["sysname1", "sysname2", "sysname3", "sysname4", "sysname5"],
    InterfaceField.IFINDEX: [1, 2, 3, 4, 5],
    InterfaceField.IFNAME: ["ifName1", "ifName2", "ifName3", "ifName4", "ifName5"],
    InterfaceField.IFDESCR: ["ifDescr1", "ifDescr2", "ifDescr3", "ifDescr4", "ifDescr5"],
    InterfaceField.IFALIAS: ["ifAlias1", "ifAlias2", "ifAlias3", "ifAlias4", "ifAlias5"],
    InterfaceField.IFHIGHSPEED: [1000, 1000, 1000, 1000, 1000],
    InterfaceField.IFOPERSTATUS: ["up", "up", "up", "up", "up"],
    InterfaceField.IFADMINSTATUS: ["up", "up", "up", "up", "up"],
    InterfaceField.CONSULTED_AT: ["2022-01-01", "2022-01-01", "2022-01-01", "2022-01-01", "2022-01-01"]
})

DATA2 = pd.DataFrame({
    InterfaceField.ID: [6, 7, 8, 9, 10],
    InterfaceField.IP: ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5"],
    InterfaceField.COMMUNITY: ["public1", "public2", "public3", "public4", "public5"],
    InterfaceField.SYSNAME: ["sysname1", "sysname2", "sysname3", "sysname4", "sysname5"],
    InterfaceField.IFINDEX: [1, 2, 3, 4, 5],
    InterfaceField.IFNAME: ["ifName1.1", "ifName2", "ifName3", "ifName4", "ifName5"],
    InterfaceField.IFDESCR: ["ifDescr1.1", "ifDescr2.2", "ifDescr3", "ifDescr4", "ifDescr5"],
    InterfaceField.IFALIAS: ["ifAlias1", "ifAlias2", "ifAlias3", "ifAlias4", "ifAlias5"],
    InterfaceField.IFHIGHSPEED: [1000, 1000, 1000, 1000, 1000],
    InterfaceField.IFOPERSTATUS: ["up", "up", "up", "up", "up"],
    InterfaceField.IFADMINSTATUS: ["up", "up", "up", "up", "up"],
    InterfaceField.CONSULTED_AT: ["2022-01-02", "2022-01-02", "2022-01-02", "2022-01-02", "2022-01-02"]
})



class Test(unittest.TestCase):
    def test_compare(self) -> None:
        """Test of compare data frames."""
        data = OperationData.compare(old_data=DATA1, new_data=DATA2)

        print(data)

        self.assertFalse(data.empty)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[InterfaceField.IP][0], DATA1[InterfaceField.IP][0])
        self.assertEqual(data[InterfaceField.IP][1], DATA1[InterfaceField.IP][1])


if __name__ == "__main__":
    unittest.main()