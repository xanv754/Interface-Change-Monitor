from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

IP = "192.168.1.1"

COMMUNITY = "public"
COMMUNITY_TWO = "private"

SYSNAME = "Router1"
SYSNAME_TWO = "Router2"

IFINDEX = 206

DATE_CONSULT = "2024-01-01"
DATE_CONSULT_TWO = "2024-01-05"
DATE_ALTERNATIVE = "2024-02-02"

USERNAME = "unittest"
USERNAME_TWO = "unittest_two"
USERNAME_ALTERNATIVE = "DefaultUnittest"

PASSWORD = "secret123456"
PASSWORD_HASH = pwd_context.hash(PASSWORD)
PASSWORD_TWO = "secret12345678"
PASSWORD_TWO_HASH = pwd_context.hash(PASSWORD_TWO)