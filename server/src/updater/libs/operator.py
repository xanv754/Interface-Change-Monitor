from database import OperatorController, AssignmentController

def get_all_operators():
    operators = OperatorController.read_all_operators()
    print(f'| |__Total operators: {len(operators)}')
    print(f'| |__Info about operators: ')
    for operator in operators:
        print(f'| | |--> Username: {operator["username"]}')
        print(f'| | |     Name: {operator["name"]}')
        print(f'| | |     Lastname: {operator["lastname"]}')
        print(f'| | |     Password: {operator["password"]}')
        print(f'| | |     Profile: {operator["profile"]}')
        print(f'| | |     Status Account: {operator["statusAccount"]}')
        print(f'| | |     Deleted Account?: {operator["deleteOperator"]}')
        assignments = AssignmentController.read_assignments_by_operator(operator["username"])
        print(f'| | |     Total assignments: {len(assignments)}')
        pendings = [operator for operator in assignments if operator["statusAssignment"] == "PENDING"]
        print(f'| | |     Total pending assignments: {len(pendings)}')
        finished = [operator for operator in assignments if operator["statusAssignment"] != "PENDING"]
        print(f'| | |     Total finished assignments: {len(finished)}')
        reviews = [operator for operator in assignments if operator["statusAssignment"] == "REVIEW"]
        print(f'| | |        Total reviews assignments: {len(reviews)}')
        rediscovered = [operator for operator in assignments if operator["statusAssignment"] == "REDISCOVER"]
        print(f'| | |        Total rediscovered assignments: {len(rediscovered)}')

def get_operators():
    operators = OperatorController.read_operators()
    print(f'| |__Total operators: {len(operators)}')
    print(f'| |__Info about operators: ')
    for operator in operators:
        print(f'| | |--> Username: {operator["username"]}')
        print(f'| | |     Name: {operator["name"]}')
        print(f'| | |     Lastname: {operator["lastname"]}')
        print(f'| | |     Password: {operator["password"]}')
        print(f'| | |     Profile: {operator["profile"]}')
        print(f'| | |     Status Account: {operator["statusAccount"]}')
        print(f'| | |     Deleted Account?: {operator["deleteOperator"]}')
        assignments = AssignmentController.read_assignments_by_operator(operator["username"])
        print(f'| | |     Total assignments: {len(assignments)}')
        pendings = [operator for operator in assignments if operator["statusAssignment"] == "PENDING"]
        print(f'| | |     Total pending assignments: {len(pendings)}')
        finished = [operator for operator in assignments if operator["statusAssignment"] != "PENDING"]
        print(f'| | |     Total finished assignments: {len(finished)}')
        reviews = [operator for operator in assignments if operator["statusAssignment"] == "REVIEW"]
        print(f'| | |        Total reviews assignments: {len(reviews)}')
        rediscovered = [operator for operator in assignments if operator["statusAssignment"] == "REDISCOVER"]
        print(f'| | |        Total rediscovered assignments: {len(rediscovered)}')

def get_operator(username: str):
    operator = OperatorController.read_operator(username)[0]
    print(f'|__Name: {operator["name"]}')
    print(f'|__Lastname: {operator["lastname"]}')
    print(f'|__Password: {operator["password"]}')
    print(f'|__Profile: {operator["profile"]}')
    print(f'|__Status Account: {operator["statusAccount"]}')
    print(f'|__Deleted Account?: {operator["deleteOperator"]}')
    assignments = AssignmentController.read_assignments_by_operator(operator["username"])
    print(f'|__Total assignments: {len(assignments)}')
    pendings = [operator for operator in assignments if operator["statusAssignment"] == "PENDING"]
    print(f'|__Total pending assignments: {len(pendings)}')
    finished = [operator for operator in assignments if operator["statusAssignment"] != "PENDING"]
    print(f'|__Total finished assignments: {len(finished)}')
    reviews = [operator for operator in assignments if operator["statusAssignment"] == "REVIEW"]
    print(f'|     Total reviews assignments: {len(reviews)}')
    rediscovered = [operator for operator in assignments if operator["statusAssignment"] == "REDISCOVER"]
    print(f'|     Total rediscovered assignments: {len(rediscovered)}')