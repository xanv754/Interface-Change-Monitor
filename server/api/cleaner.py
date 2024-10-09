from controllers.element import ElementController
from controllers.user import UserController
from utils.date import get_month_to_clean

month_to_clean = get_month_to_clean()

def cleanerElementsDatabase() -> bool:
    if month_to_clean:
        status = ElementController.delete_elements_by_month(month_to_clean)
        if status: return status
    return False

def cleanerAssignmentUser() -> bool:
    someWrong = False
    month_to_clean = get_month_to_clean('11-02-2024')
    if month_to_clean:
        users = UserController.read_users()
        for user in users:
            new_assigned = []
            for assign in user.assigned:
                if assign.assignment.reviewMonth != month_to_clean:
                    new_assigned.append(assign)
            status = UserController.clean_assigned(user.username, new_assigned)
            if not status: someWrong = True
        return not someWrong
    return False
            
def cleanerUserDisabled():
    return UserController.clean_users_disabled()

if __name__ == "__main__":
    print("Cleaner database ...")
    clean_db = cleanerElementsDatabase()
    clean_users = cleanerUserDisabled()
    clean_assignment = cleanerAssignmentUser()
    if clean_db and clean_assignment and clean_users: print("Cleaned database.")
    elif not clean_db: print("Failed to clean elements")
    elif not clean_assignment: print("Failed to clean assignments")
    elif not clean_users: print("Failed to clean users")



