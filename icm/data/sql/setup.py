from icm.business.controllers.user import UserController
from icm.business.controllers.interface import InterfaceController
from icm.constants import RoleTypes, UserStatusTypes
from icm.business.models.user import UserModel
from icm.constants import InterfaceField
from icm.data import Database
from datetime import datetime, timedelta
import pandas as pd

if __name__ == "__main__":
    database = Database()
    print("Drop Database:", database.drop())
    database = Database()
    status = database.initialize()
    print("Initialize Database:", status)
    if not status:
        exit(1)

    # User Seed
    user_admin = UserModel(
        username="admin",
        password="admin",
        name="admin",
        lastname="admin",
        status=UserStatusTypes.ACTIVE,
        role=RoleTypes.ADMIN,
        created_at=None,
        updated_at=None,
    )
    user_a = UserModel(
        username="user_a",
        password="usertest",
        name="User A",
        lastname="Test",
        status=UserStatusTypes.ACTIVE,
        role=RoleTypes.USER,
        created_at=None,
        updated_at=None,
    )
    user_b = UserModel(
        username="user_b",
        password="usertest",
        name="User B",
        lastname="Test",
        status=UserStatusTypes.ACTIVE,
        role=RoleTypes.USER,
        created_at=None,
        updated_at=None,
    )

    print(f"User Admin: {user_admin.username} | {user_admin.password}")
    print(f"User Test: {user_a.username} | {user_a.password}")

    users = [user_admin, user_a, user_b]

    user_controller = UserController()
    for user in users:
        user_controller.new_user(user)

    # Interface Seed
    interfaces = {
        InterfaceField.IP: [
            "1.1.1.1",
            "2.2.2.2",
            "3.3.3.3",
            "1.1.1.1",
            "2.2.2.2",
            "3.3.3.3",
        ],
        InterfaceField.COMMUNITY: [
            "public1",
            "public2",
            "public3",
            "public1",
            "public2",
            "public3",
        ],
        InterfaceField.SYSNAME: [
            "equipo1",
            "equipo2",
            "equipo3",
            "equipo1",
            "equipo2",
            "equipo3",
        ],
        InterfaceField.IFINDEX: ["1", "2", "3", "1", "2", "3"],
        InterfaceField.IFNAME: ["eth1", "eth2", "eth3", "eth1", "eth2", "eth3"],
        InterfaceField.IFDESCR: [
            "ethernet1",
            "ethernet2",
            "ethernet3",
            "ethernet1 1",
            "ethernet2 2",
            "ethernet3 3",
        ],
        InterfaceField.IFALIAS: ["eth1", "eth2", "eth3", "eth1", "eth2", "eth3"],
        InterfaceField.IFHIGHSPEED: ["1000", "1000", "1000", "1000", "1000", "1000"],
        InterfaceField.IFOPERSTATUS: [
            "up(1)",
            "up(1)",
            "up(1)",
            "down(2)",
            "up(1)",
            "down(2)",
        ],
        InterfaceField.IFADMINSTATUS: [
            "up(1)",
            "up(1)",
            "up(1)",
            "up(1)",
            "up(1)",
            "up(1)",
        ],
        InterfaceField.CONSULTED_AT: [
            (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        ],
    }
    df_interfaces = pd.DataFrame(interfaces)

    interface_controller = InterfaceController()
    interface_controller.new_interfaces(df_interfaces)
