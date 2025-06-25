import unittest
from io import StringIO
from database.querys.interface import InterfaceQuery
from models.interface import InterfaceField
from test import InterfaceDBTest


class Query(unittest.TestCase):
    test_database: InterfaceDBTest = InterfaceDBTest()

    def setUp(self) -> None:
        self.test_database.create_table()

    def tearDown(self) -> None:
        self.test_database.clean()

    def test_insert(self) -> None:
        """Test of insert interfaces."""
        first_interface = self.test_database.get_mock()
        data = ";".join(str(value) for value in first_interface.model_dump(exclude={"id"}).values())
        print(data)
        buffer = StringIO()
        buffer.write(data)
        buffer.seek(0)
        self.setUp()
        
        query = InterfaceQuery()
        status_operation = query.insert(data=buffer)

        self.tearDown()
        self.assertTrue(status_operation)

    def test_get_by_date_consult(self) -> None:
        """Test of get interfaces by date."""
        interface_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_interface=interface_mock)

        query = InterfaceQuery()
        response = query.get_by_date_consult(date=interface_mock.consulted_at)
        print(response)

        self.tearDown()
        self.assertFalse(response.empty)
        self.assertEqual(response[InterfaceField.IP][0], interface_mock.ip)
        self.assertEqual(response[InterfaceField.COMMUNITY][0], interface_mock.community)
        self.assertEqual(response[InterfaceField.SYSNAME][0], interface_mock.sysname)
        self.assertEqual(response[InterfaceField.IFINDEX][0], interface_mock.ifIndex)
        self.assertEqual(response[InterfaceField.CONSULTED_AT][0], interface_mock.consulted_at)






if __name__ == "__main__":
    unittest.main()